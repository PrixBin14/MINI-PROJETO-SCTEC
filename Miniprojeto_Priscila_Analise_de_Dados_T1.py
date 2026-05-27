from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, List

import pandas as pd
import csv
import numpy as np


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

    # 1) detectar delimitador assumindo utf-8 (rápido)
    delim = detectar_delimiter(caminho, enc='utf-8')

    # 2) validação mínima com csv.DictReader (leitura nativa) - até 5 linhas
    for enc in ('utf-8', 'latin1'):
        try:
            with caminho.open('r', encoding=enc, errors='replace') as fh:
                reader = csv.DictReader(fh, delimiter=delim)
                sample = [row for _, row in zip(range(5), reader)]
            print(f"Validação: csv.DictReader ({enc}) leu {len(sample)} linhas de exemplo com delimitador '{delim}'")
            break
        except Exception:
            print(f"Aviso: validação com csv.DictReader ({enc}) falhou; tentando próximo encoding...")

    # 3) tentar leitura com pandas usando a combinação detectada
    try:
        df = pd.read_csv(caminho, encoding='utf-8', sep=delim, low_memory=False)
        print(f"Sucesso: arquivo '{caminho}' carregado com encoding utf-8 e delimitador '{delim}'")
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(caminho, encoding='latin1', sep=delim, low_memory=False)
            print(f"Aviso: utf-8 falhou, carregado '{caminho}' com latin1 e delimitador '{delim}'")
            return df
        except Exception as e:
            print(f"Erro ao ler com latin1: {e}")
    except Exception as e:
        print(f"Leitura com pandas (utf-8) falhou: {e}")

    # 4) última tentativa: engine python com sep=None (mais permissivo)
    try:
        df = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8', low_memory=False)
        print(f"Aviso: leitura alternativa sucedeu para '{caminho}' (engine=python, sep=None)")
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
    """Aplica limpeza e análises adicionais """
    df = df.copy()

    # 1) remover colunas totalmente vazias
    df = df.dropna(axis=1, how='all')

    # 2) substituir marcadores de erro '#N/D' por NaN
    df = df.replace('#N/D', np.nan)

    # 3) remover duplicatas exatas
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        print(f"- Duplicatas removidas: {dup_count}")

    # 4) trabalhar com cópia em UPPER para localizar colunas independentemente do casing
    df_upper = df.copy()
    df_upper.columns = df_upper.columns.str.strip().str.upper()

    # 5) preencher PR_CAT quando existir, tratando nulos e vazios como 'Sem Categoria'
    if 'PR_CAT' in df_upper.columns:
        def preencher_categoria(valor):
            try:
                s = str(valor).strip()
            except Exception:
                return 'Sem Categoria'
            return 'Sem Categoria' if (s == '' or s.lower() == 'nan') else valor

        df_upper['PR_CAT'] = df_upper['PR_CAT'].apply(preencher_categoria)
        print("- Categorias nulas/preenchidas vazias definidas como 'Sem Categoria'.")

    # 6) tratamento de dimensões
    if 'DIMENSOES' not in df_upper.columns:
        print("- Justificativa (Dimensões Físicas): coluna ausente; imputação seria '0x0x0' se existisse.")
    else:
        df_upper['DIMENSOES'] = df_upper['DIMENSOES'].fillna('Desconhecida')

    # 7) conversão de DATA
    if 'DATA' in df_upper.columns:
        df_upper['DATA'] = pd.to_datetime(df_upper['DATA'], format='%d/%m/%Y', errors='coerce')
        print("- Coluna DATA convertida para tipo datetime.")

    # 8) regra identificador de compra (CO_ID)
    if 'CO_ID' in df_upper.columns:
        df_upper['PREFIXO_COMPRA'] = 'CO'
        df_upper['NUM_COMPRA_FORMATADO'] = df_upper['PREFIXO_COMPRA'] + '-' + df_upper['CO_ID'].astype(str)
        print("- Regra de identificador de compra validada e separada (Ex: CO-1000).")

    # 9) Estatísticas descritivas para filhos (CL_FHL / filhos)
    print("\n--- Estatísticas Descritivas: NÚMERO DE FILHOS (CL_FHL) ---")
    filhos_col = None
    for candidate in ['CL_FHL', 'FILHOS', 'cl_fhl', 'filhos']:
        if candidate in df_upper.columns:
            filhos_col = df_upper[candidate]
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

    # 10) agrupamentos úteis
    print("\n--- PADRÕES DE AGRUPAMENTO ---")
    if 'CL_GENERO' in df_upper.columns and 'PR_ID' in df_upper.columns:
        grupo1 = df_upper.groupby('CL_GENERO')['PR_ID'].count().reset_index(name='Total_Produtos_Comprados')
        print("\nAgrupamento 1: Produtos Comprados por Gênero")
        print(grupo1.to_string(index=False))

    if 'CL_EC' in df_upper.columns and 'PR_CAT' in df_upper.columns and 'PR_ID' in df_upper.columns:
        grupo2 = df_upper.groupby(['CL_EC', 'PR_CAT'])['PR_ID'].count().reset_index(name='Vendas')
        grupo2 = grupo2.sort_values(by='Vendas', ascending=False).head(5)
        print("\nAgrupamento 2: Top 5 Categorias de Produtos por Código de Estado Civil (CL_EC)")
        print(grupo2.to_string(index=False))

    # 11) mapear colunas criadas de volta para df
    mapping_add = {}
    if 'PREFIXO_COMPRA' in df_upper.columns:
        mapping_add['prefixo_compra'] = df_upper['PREFIXO_COMPRA']
    if 'NUM_COMPRA_FORMATADO' in df_upper.columns:
        mapping_add['num_compra_formatado'] = df_upper['NUM_COMPRA_FORMATADO']
    if 'DATA' in df_upper.columns:
        mapping_add['data'] = df_upper['DATA']

    for k, series in mapping_add.items():
        df[k] = series.values

    return df


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='Análise exploratória inicial do dataset de varejo')
    parser.add_argument('--file', '-f', type=Path, default=Path('Base varejo.csv'), help='Caminho para o arquivo CSV')
    parser.add_argument('--save-summary', '-s', type=Path, help='Caminho para salvar o resumo (CSV)')
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

    print("\nProcessamento concluído com sucesso! Verifique o README para os insights e documentação.")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())