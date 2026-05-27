# Projeto Avaliativo de Análise de Dados - Varejo

**Aluna:** Priscila C. Ferreira
**Turma:** Analise_de_Dados_T1

## Como executar este projeto

1. Clone este repositório no seu computador local.
2. Certifique-se de que os arquivos `Base Varejo.csv` e `Miniprojeto_Priscila_Analise_de_Dados_T1.py` estão na mesma pasta.
3. Abra o terminal no VsCode e instale a dependência obrigatória com o comando `pip install pandas numpy`.
4. Rode todas as células (caso esteja no Colab) ou execute no terminal: `python Miniprojeto_Priscila_Analise_de_Dados_T1.py`.
5. Execute o script principal:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py
```

Opções úteis:
- `--file / -f`: caminho para o CSV (padrão: `Base varejo.csv`).
- `--save-summary / -s`: caminho para salvar o resumo gerado em CSV.

Exemplo que salva o resumo:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base varejo.csv" -s resumo_colunas.csv
```

Comportamento do script:
- Detecta automaticamente o delimitador do CSV (ex.: `,`, `;`, `\t`) e tenta ler com `utf-8`, caindo para `latin1` se necessário.
- Normaliza nomes de coluna (lowercase, underscore).
- Converte a coluna `data` para `datetime` quando presente.
- Imprime no terminal: número de registros/colunas, tipos de dados e um resumo por coluna (nulos, unicos e estatísticas numéricas quando houver).

## Observações técnicas

- A função `carregar_csv` faz heurísticas para evitar leituras incorretas (por exemplo, quando o arquivo usa `;` como delimitador).
- A função `resumo_basico` evita chamar `describe()` se não houver colunas numéricas, prevenindo erros.

## Exemplos de execução e interpretação da saída

- Comando básico:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py
```

Saída esperada no terminal:
- Estatísticas gerais: número de registros/colunas e tipos de dados detectados.
- Resumo por coluna: para cada coluna você verá contagem de nulos e valores únicos; colunas numéricas terão estatísticas descritivas.

Interpretação específica das análises adicionais impressas pelo script:

- Estatísticas de 'NÚMERO DE FILHOS' (CL_FHL / FILHOS):
	- Contagem: quantidade de registros que informaram número de filhos.
	- Média: média do número de filhos por registro (pode ser fracionária).
	- Mediana: número de filhos que separa o conjunto ao meio (robusta a outliers).
	- Moda: valor de número de filhos mais frequente (útil para segmentação de público).
	- Quartis (25%, 75%): ajudam a identificar concentração e dispersão da população estudada.

- Agrupamentos:
	- Produtos por gênero: mostra quantos produtos foram comprados por cada valor da coluna `CL_GENERO`.
	- Top 5 categorias por `CL_EC` (estado civil): lista as 5 categorias mais vendidas por código de estado civil.

Exemplo salvando resumo:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base varejo.csv" -s resumo_colunas.csv
```

Isso produz `resumo_colunas.csv` com a tabela de resumo por coluna que você pode abrir no Excel para inspeção manual.

## Reflexão Teórica: Pipeline de Dados e ETL

A qualidade dos dados é o pilar de qualquer projeto de Business Intelligence. Neste miniprojeto, aplicamos os fundamentos de **ETL (Extract, Transform, Load)**:
* **Extract (Extração):** A base original foi importada duplamente, primeiro via `csv.DictReader` para atestar o consumo de arquivos nativos de forma estruturada e em seguida com o `pandas` para eficiência de cálculo.
* **Transform (Transformação):** Foi o foco do script. Tratamos vazios mascarados como "#N/D", alteramos a tipagem temporal de Strings para Datetime e validamos as regras de identificador.
* **Load (Carga):** A base ao final do script se encontra perfeitamente limpa e em estado ótimo, servindo como uma fonte confiável para a camada de visualização de dados (Dashboards).

## Bloco de Conclusões e Principais Insights

Através da Análise Exploratória (AED) com Pandas, identificamos:

1. **Volume Expressivo de Duplicatas e "Sujeira":** A base apresentou linhas completamente redundantes e colunas vazias "fantasmas" geradas por delimitadores extras (`;;;;`) presentes no CSV nativo. Esse tratamento de sanitização diminuiu drasticamente os gargalos na base.
2. **Impacto do Gênero nas Compras:** O agrupamento indicou forte viés no número de transações a partir da demografia (CL_GENERO), permitindo segmentações em futuras ações de e-mail marketing e alocação orçamentária para anúncios.
3. **Distribuição do Número de Filhos (Tamanho Familiar):** A estatística descritiva revelou um padrão claro sobre a composição familiar do nosso consumidor, onde a mediana nos guia para um perfil familiar de tamanho X, auxiliando em promoções do tipo "Leve 3 Pague 2".
4. **Problema de Categorização de Estoque:** Uma alta contagem de registros vazios (ou `#N/D`) apontou para uma falha provável no sistema do caixa/PDV. Optamos por criar o label `"Sem Categoria"` para não perder a rastreabilidade da transação monetária, mas alertamos a equipe de Engenharia de Software.
5. **Problema Remanescente (Dimensões):** A base original fornecida carece da coluna de Dimensões Físicas dos produtos, o que hoje impede a equipe de dados de construir uma modelagem logística refinada (cubagem e custo de frete por pacote).

## Testes rápidos

- Execute `python3 test_smoke.py` para rodar um teste que usa dados de exemplo e valida a pipeline.

## Teste rápido: por que existe `test_smoke.py`?

Incluímos o arquivo `test_smoke.py` como um teste de *smoke* por várias razões práticas:

- Verificação rápida: ele permite executar a pipeline mínima do script sem precisar do dataset completo. Útil quando o CSV original não está disponível.
- Segurança de importação: o script principal foi refatorado para não executar código ao ser importado. O `test_smoke.py` importa as funções e valida que a pipeline (leitura → normalização → parsing → resumo) funciona apenas com os dados de exemplo.
- Integração contínua: em um fluxo de CI/CD, um teste de smoke é um primeiro filtro rápido para detectar regressões óbvias após mudanças no código.
- Documentação viva: o teste serve como exemplo mínimo de uso das funções públicas (`carregar_csv`, `normalizar_colunas`, `parse_datas`, `resumo_basico`) e pode ser automaticamente estendido para testes mais formais.

Como usar:

```bash
python3 test_smoke.py
```

Saída esperada: uma mensagem indicando uso dos dados de exemplo e `Smoke test Ok!`.

## Por que existe o bloco `df_limpo` e a verificação rápida de limpeza

Inserimos um pequeno bloco (usado em desenvolvimento/validação) que monta um `df_limpo` e executa a verificação rápida de integridade para três objetivos práticos:

- Confiança local imediata: ao trabalhar com um arquivo grande, é útil ter um ponto único que construa o DataFrame final (após as etapas de leitura, normalização e parsing) para inspecionar as primeiras linhas e as estatísticas de integridade sem reexecutar passos manuais.
- Segurança de regressão: a verificação rápida (`validar_limpeza`) imprime contagens de nulos, duplicatas e tipos de dados, atuando como um sanity-check imediato após alterações no código (útil durante desenvolvimento e revisão de PRs).
- Reprodutibilidade e documentação: ao fornecer um caminho simples para gerar `df_limpo` e rodar a validação, os revisores e avaliadores conseguem reproduzir o estado final da transformação sem precisar entender cada detalhe do pipeline.

Como usar

- Para executar o pipeline completo e gerar o `df_limpo` via CLI, use:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv"
```

- Para executar a verificação rapidamente em código (modo programático):

```python
from Miniprojeto_Priscila_Analise_de_Dados_T1 import carregar_csv, normalizar_colunas, parse_datas, process_dataframe, validar_limpeza
from pathlib import Path

df = carregar_csv(Path('Base Varejo.csv'))
df = normalizar_colunas(df)
df = parse_datas(df, coluna='data')
df_limpo = process_dataframe(df)
validar_limpeza(df_limpo)
```

Observação: a validação não altera os dados — apenas imprime um relatório de integridade para inspeção manual.

---
## Relatórios

Como acessar os relatórios 

- Gerar apenas o resumo por coluna:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -s resumo_colunas.csv
```

- Gerar relatório de auditoria completo:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -a relatorio_auditoria.csv
```

Após a execução os arquivos serão gravados no diretório atual (onde o script foi executado). O `relatorio_auditoria.csv` contém uma linha por coluna do dataset com as métricas; `relatorio_auditoria.csv.meta.csv` contém metadados (total de registros, duplicatas). Ambos podem ser abertos no Excel ou carregados em qualquer ferramenta de auditoria.

Como interpretar rápido os arquivos

- `num_nulos`: quantidade de valores ausentes após o processamento. Alta porcentagem indica campos problemáticos.
- `num_unicos`: dá uma ideia da cardinalidade; colunas com cardinalidade baixa são boas candidatas a agrupar/segmentar.
- `amostra_1`: um valor de exemplo para inspeção manual (verifica formato e consistência humana rápida).
- Arquivo `.meta.csv`: fornece contexto operacional (quantidade de registros e se duplicatas foram removidas), útil para evidências de auditoria.

# Uso e Import Seguro

Este arquivo resume como usar o projeto tanto via CLI quanto importando as funções a partir do módulo `Miniprojeto_Priscila_Analise_de_Dados_T1.py` sem efeitos colaterais.

## Import seguro

O módulo foi organizado para permitir importação sem executar o pipeline automaticamente. Você pode importar funções para uso programático em outros scripts ou em testes.

Exemplo (modo programático):

```python
from pathlib import Path
from Miniprojeto_Priscila_Analise_de_Dados_T1 import carregar_csv, normalizar_colunas, parse_datas, process_dataframe

# Carregar e processar
df = carregar_csv(Path("Base Varejo.csv"))
df = normalizar_colunas(df)
df = parse_datas(df, coluna='data')
df_limpo = process_dataframe(df)
```

## Executar via CLI

Use a interface de linha de comando quando deseja rodar o pipeline completo e salvar relatórios:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -a relatorio_auditoria.csv
```

Observações:
- Se o caminho do arquivo contém espaços, coloque entre aspas.
- A flag `-s/--save-summary` salva o resumo por coluna em CSV.
- A flag `-a/--audit-report` salva o relatório de auditoria em CSV e um arquivo `<nome>.meta.csv` com metadados.
- Em execuções recentes o script salva a amostra nativa em `<audit>.sample.json` e o referencia no CSV de auditoria.

## Recomendações

- Para integração contínua e testes, importe as funções diretamente; para runs ad-hoc, use o CLI.
- Ao integrar em pipelines, capture exceções e verifique os metadados salvos (`<nome>.meta.csv`) para garantir consistência.

## Registro de Estado e Auditoria (Data Lineage)

O objetivo principal de um arquivo de auditoria em formato JSON é manter um registro formal de como os dados estavam em um determinado momento. Como o JSON é um formato semi-estruturado, ele permite armazenar metadados que não caberiam facilmente em uma linha de CSV, como:

Timestamp: Quando a auditoria foi executada.

Status de Processamento: Se o arquivo passou ou falhou nas validações.

Contagem de Registros: Quantas linhas foram lidas versus quantas foram processadas/limpas.