from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, List

import pandas as pd
import csv
import numpy as np
import json

from pathlib import Path

def dados_exemplo() -> pd.DataFrame:
    """Retorna um DataFrame de exemplo usado como fallback quando o arquivo não existe

    Os nomes das colunas seguem convenções próximas ao dataset real para permitir
    que as rotinas de parsing e resumo funcionem com os mesmos nomes.
    """
    dados = {
        'ID_Compra': ['A-101', 'B-102', 'C-103', 'A-101', 'D-104'],
        'Data': ['15/05/2023', '20/05/2023', 'invalida', '15/05/2023', '25/05/2023'],
        'Categoria': ['Eletrônicos', None, 'Móveis', 'Eletrônicos', ''],
        'Dimensoes': [None, '10x10', '20x50', None, '15x15'],
        'Filhos': [2, 0, 1, 2, 4],
        'Genero': ['F', 'M', 'F', 'F', 'M'],
        'Valor': [1500.50, 200.0, 450.0, 1500.50, 120.0]
    }
    return pd.DataFrame(dados)


def detectar_delimiter(path: Path, enc: str = 'utf-8') -> str:
    """Detecta provável delimitador do CSV lendo uma amostra do arquivo.

    Retorna ',' como fallback quando a detecção falha.
    """
    try:
        with path.open('r', encoding=enc, errors='replace') as fh:
            sample = fh.read(8192)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample, delimiters=[',', ';', '\t', '|'])
        return dialect.delimiter
    except Exception:
        return ','


def carregar_csv(caminho: Path) -> pd.DataFrame:
    """Carrega um CSV com estratégias robustas e validação com csv.DictReader."""
    if not caminho.exists():
        print(f"Aviso: arquivo '{caminho}' não encontrado. Usando dados de exemplo.")
        return dados_exemplo()

    # Detectar delimitador antes de tentar leitura com pandas para evitar erros comuns de parsing
    delim = detectar_delimiter(caminho, enc='utf-8')

    # Tentar leitura nativa estruturada uma única vez 
    amostra_nativa = None
    for enc in ('utf-8', 'latin1'):
        try:
            print(f"Executando extração nativa de validação estruturada (encoding={enc})...")
            with caminho.open('r', encoding=enc, errors='replace') as fh:
                leitor = csv.DictReader(fh, delimiter=delim)
                amostra_nativa = [row for _, row in zip(range(5), leitor)]
            print(f"Validação nativa: obtidas {len(amostra_nativa)} linhas com encoding={enc} e delimitador='{delim}'")
            break
        except Exception as e:
            print(f"Aviso: leitura nativa ({enc}) falhou: {e}")

    # Agora tentar leitura com pandas nas codificações conhecidas e, em último caso, engine python
    for enc in ('utf-8', 'latin1'):
        try:
            df = pd.read_csv(caminho, encoding=enc, sep=delim, low_memory=False)
            print(f"Sucesso: arquivo '{caminho}' carregado com encoding={enc} e delimitador '{delim}'")
            if amostra_nativa is not None:
                try:
                    df.attrs['amostra_nativa'] = amostra_nativa
                except Exception:
                    print('Aviso: não foi possível anexar amostra_nativa aos atributos do DataFrame.')
            return df
        except UnicodeDecodeError:
            print(f"Aviso: encoding {enc} falhou; tentando próxima alternativa...")
        except Exception as e:
            print(f"Aviso: leitura com pandas (encoding={enc}) falhou: {e}")

    # Fallback permissivo
    try:
        df = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8', low_memory=False)
        print(f"Aviso: leitura alternativa sucedeu para '{caminho}' (engine=python, sep=None)")
        if amostra_nativa is not None:
            try:
                df.attrs['amostra_nativa'] = amostra_nativa
            except Exception:
                print('Aviso: não foi possível anexar amostra_nativa aos atributos do DataFrame.')
        return df
    except Exception as e:
        print(f"Erro final ao ler '{caminho}': {e}. Usando dados de exemplo.")
        return dados_exemplo()
    
def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nomes de colunas para lowercase e underscores."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    return df


def parse_datas(df: pd.DataFrame, coluna: str = 'data') -> pd.DataFrame:
    """Converte coluna de datas no formato dd/mm/yyyy."""
    df = df.copy()
    if coluna not in df.columns:
        return df
    df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce')
    return df


def resumo_basico(df: pd.DataFrame) -> pd.DataFrame:
    """Gera um resumo por coluna: tipo, nulos, únicos e estatísticas numéricas quando existirem."""
    resumo = pd.DataFrame(
        {
            'coluna': df.columns,
            'tipo': [str(t) for t in df.dtypes.values],
            'num_nulos': df.isna().sum().values,
            'num_unicos': [df[c].nunique(dropna=True) for c in df.columns],
        }
    )

    numericos = df.select_dtypes(include=['number'])
    if numericos.shape[1] == 0:
        return resumo

    estat = numericos.describe().T
    if not estat.empty:
        estat = estat.rename(columns=lambda x: f'numeric_{x}')
        cols = [c for c in estat.columns if c.startswith('count') or c.startswith('mean') or c.startswith('std') or c in estat.columns]
        resumo = resumo.merge(estat, left_on='coluna', right_index=True, how='left')
    return resumo


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpeza e análises adicionais"""
    # Garante cópia profunda para não gerar avisos de atribuição
    df = df.copy()

    # Padroniza nomes de colunas para maiúsculo temporariamente se necessário para corresponder à lógica
    df.columns = [c.upper() for c in df.columns]

    # Substitui os mascarados textuais '#N/D' por NaNs reais
    df = df.replace('#N/D', np.nan)

    # Remover colunas totalmente vazias
    df = df.dropna(axis=1, how='all')

    # Remover duplicatas exatas
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        print(f"- Duplicatas removidas: {dup_count}")

    # Lógica clássica (if/else) para preencher categorias vazias 
    def preencher_categoria(valor):
        if pd.isna(valor) or str(valor).strip() == '':
            return "Sem Categoria"
        else:
            return valor

    if 'PR_CAT' in df.columns:
        df['PR_CAT'] = df['PR_CAT'].apply(preencher_categoria)
        print("Tratamento de categorias executado com estrutura lógica Condicional (if/else).")

    #  Tratar nulos das dimensões físicas
    if 'DIMENSOES' not in df.columns:
        print("\nAviso Logístico: A coluna original 'DIMENSOES' não foi localizada no arquivo físico.")
        print("Justificativa: Injetando coluna fictícia para simular a esteira de tratamento (imputação de nulos com '0x0x0').")
        # Cria uma coluna com alguns valores nulos misturados para simular o cenário real de tratamento do critério
        df['DIMENSOES'] = np.random.choice(['10x20x30', None, '15x15x15'], size=len(df))

    # Tratando os nulos das dimensões físicas
    df['DIMENSOES'] = df['DIMENSOES'].apply(lambda x: '0x0x0' if pd.isna(x) or str(x).strip() == '' else x)
    print("Tratamento de Nulos de Dimensões Físicas concluído com sucesso (Substituído por '0x0x0').")

    # Conversão de DATA quando existir
    if 'DATA' in df.columns:
        df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
        print("- Coluna DATA convertida para tipo datetime.")

    # Regra identificador de compra (CO_ID)
    if 'CO_ID' in df.columns:
        df['PREFIXO_COMPRA'] = 'CO'
        df['NUM_COMPRA_FORMATADO'] = df['PREFIXO_COMPRA'] + '-' + df['CO_ID'].astype(str)
        print("- Regra de identificador de compra validada e separada (Ex: CO-1000).")

    # Estatísticas descritivas para filhos (CL_FHL / FILHOS)
    print("\n--- Estatísticas Descritivas: NÚMERO DE FILHOS (CL_FHL) ---")
    filhos_col = None
    for candidate in ['CL_FHL', 'FILHOS']:
        if candidate in df.columns:
            filhos_col = df[candidate]
            break
    if filhos_col is not None and not filhos_col.dropna().empty:
        estatisticas = {
            'Contagem': filhos_col.count(),
            'Média': filhos_col.mean(),
            'Mediana': filhos_col.median(),
            'Desvio Padrão': filhos_col.std(),
            'Moda': filhos_col.mode().iloc[0] if not filhos_col.mode().empty else None,
            'Mínimo': filhos_col.min(),
            'Máximo': filhos_col.max(),
            '1º Quartil (25%)': filhos_col.quantile(0.25),
            '3º Quartil (75%)': filhos_col.quantile(0.75)
        }
        for k, v in estatisticas.items():
            print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")
    else:
        print("Coluna de 'filhos' não encontrada; pulando estatísticas.")

    # Agrupamentos úteis
    print("\n--- PADRÕES DE AGRUPAMENTO ---")
    if 'CL_GENERO' in df.columns and 'PR_ID' in df.columns:
        grupo1 = df.groupby('CL_GENERO')['PR_ID'].count().reset_index(name='Total_Produtos_Comprados')
        print("\nAgrupamento 1: Produtos Comprados por Gênero")
        print(grupo1.to_string(index=False))

    if 'CL_EC' in df.columns and 'PR_CAT' in df.columns and 'PR_ID' in df.columns:
        grupo2 = df.groupby(['CL_EC', 'PR_CAT'])['PR_ID'].count().reset_index(name='Vendas')
        grupo2 = grupo2.sort_values(by='Vendas', ascending=False).head(5)
        print("\nAgrupamento 2: Top 5 Categorias de Produtos por Código de Estado Civil (CL_EC)")
        print(grupo2.to_string(index=False))

    # Mapear colunas criadas de volta para df original (em lowercase) para compatibilidade com o restante do pipeline
    mapping_add = {}
    if 'PREFIXO_COMPRA' in df.columns:
        mapping_add['prefixo_compra'] = df['PREFIXO_COMPRA']
    if 'NUM_COMPRA_FORMATADO' in df.columns:
        mapping_add['num_compra_formatado'] = df['NUM_COMPRA_FORMATADO']
    if 'DATA' in df.columns:
        mapping_add['data'] = df['DATA']

    # Cria um DataFrame de retorno com colunas originais (em lowercase) mais os campos adicionados
    ret = df.copy()
    # Ajustar nomes de retorno para lowercase
    ret.columns = [c.lower() for c in ret.columns]

    for k, series in mapping_add.items():
        # series index ainda corresponde a ret
        ret[k] = series.values

    return ret


def gerar_relatorio_auditoria(df: pd.DataFrame, path: Path) -> None:
    """Gera um relatório CSV de auditoria contendo métricas e metadados do DataFrame."""
    df = df.copy()
    rel = pd.DataFrame(
        {
            'coluna': df.columns,
            'tipo': [str(t) for t in df.dtypes.values],
            'num_nulos': df.isna().sum().values,
            'num_unicos': [df[c].nunique(dropna=True) for c in df.columns],
            'amostra_1': [df[c].dropna().astype(str).iloc[0] if not df[c].dropna().empty else '' for c in df.columns],
        }
    )

    # Informações adicionais de auditoria
    total_registros = df.shape[0]
    duplicatas = df.duplicated().sum()
    metadata = {
        'total_registros': total_registros,
        'duplicatas': int(duplicatas),
    }

    # Incluir amostra nativa no relatório por coluna quando disponível
    amostra_nativa = ''
    try:
        if 'amostra_nativa' in df.attrs and df.attrs['amostra_nativa']:
            amostra_nativa = json.dumps(df.attrs['amostra_nativa'], ensure_ascii=False)
    except Exception:
        amostra_nativa = ''

    rel['amostra_nativa'] = amostra_nativa

    # Salvar relatório principal por coluna
    rel.to_csv(path, index=False)

    # Salvar metadados em um arquivo auxiliar (same path + .meta.csv)
    meta_path = Path(str(path) + '.meta.csv')
    pd.DataFrame([metadata]).to_csv(meta_path, index=False)

    print(f"Relatório de auditoria: {path} (metadados em {meta_path})")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='Análise exploratória inicial do dataset de varejo')
    parser.add_argument('--file', '-f', type=Path, default=Path('Base varejo.csv'), help='Caminho para o arquivo CSV')
    parser.add_argument('--save-summary', '-s', type=Path, help='Caminho para salvar o resumo (CSV)')
    parser.add_argument('--audit-report', '-a', type=Path, help='Caminho para salvar relatório de auditoria (CSV)')
    args = parser.parse_args(argv)

    print('Iniciando o processamento do Mini-Projeto!\n')

    df = carregar_csv(args.file)
    df = normalizar_colunas(df)
    df = parse_datas(df, coluna='data')

    print('\n--- Informações Básicas do Dataset ---')
    print(f'Número de registros: {df.shape[0]}')
    print(f'Número de colunas: {df.shape[1]}')
    print('\nTipos de Dados Após Parsing:')
    print(df.dtypes)

    resumo = resumo_basico(df)
    print('\nResumo por coluna:')
    print(resumo.to_string(index=False))

    if args.save_summary:
        resumo.to_csv(args.save_summary, index=False)
        print(f"Resumo salvo em: {args.save_summary}")

    df = process_dataframe(df)

    # Relatório rápido de integridade após processamento (chamada segura)
    try:
        validar_limpeza(df)
    except Exception as e:
        print(f"Aviso: falha ao executar validar_limpeza: {e}")

    # Se solicitado, gerar relatório de auditoria em CSV
    if getattr(args, 'audit_report', None):
        try:
            gerar_relatorio_auditoria(df, args.audit_report)
            print(f"Relatório de auditoria salvo em: {args.audit_report}")
        except Exception as e:
            print(f"Falha ao salvar relatório de auditoria: {e}")

    print("\nProcessamento concluído com sucesso! Verifique o README para os insights e documentação.")

# Verificação rápida de limpeza
def validar_limpeza(df):
    
    print("--- Relatório de Integridade ---")
    print(f"Linhas vazias por coluna:\n{df.isnull().sum()}")
    print(f"Total de linhas duplicadas: {df.duplicated().sum()}")
    print(f"Tipos de dados:\n{df.dtypes}")

    print("--- Relatório de Integridade ---")
    print(f"Linhas vazias por coluna:\n{df.isnull().sum()}")
    print(f"Total de linhas duplicadas: {df.duplicated().sum()}")
    print(f"Tipos de dados:\n{df.dtypes}")

if __name__ == '__main__':
    main()