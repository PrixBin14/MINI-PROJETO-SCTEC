Projeto Avaliativo de Análise de Dados - Varejo

**Aluna:** Priscila C. Ferreira  
**Turma:** Analise_de_Dados_T1

Este projeto consiste em uma pipeline automatizada de **ETL (Extração, Transformação e Carga)** e Análise Exploratória de Dados (AED) para uma base de dados de varejo, utilizando Python e Pandas.

---

## Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e as dependências obrigatórias configuradas. No terminal, execute:

```bash
pip install pandas numpy
```

### 2. Execução Padrão
Garanta que o arquivo `Base Varejo.csv` e o script `Miniprojeto_Priscila_Analise_de_Dados_T1.py` estejam na mesma pasta. Rode o comando:

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py
```

### 3. Opções de Linha de Comando (CLI)
O script aceita argumentos para personalizar a execução:

- `--file / -f`: Caminho personalizado para o CSV (Padrão: Base varejo.csv).

- `--save-summary / -s`: Salva o resumo estatístico das colunas em formato CSV.

- `--audit-report / -a`: Gera um relatório de auditoria completo em CSV.

#### Exemplo completo com salvamento de relatórios

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -s resumo_colunas.csv -a relatorio_auditoria.csv
```

## Comportamento do Script e Pipeline de ETL

O projeto foi desenhado sob o conceito de Import Seguro, permitindo que suas funções sejam importadas por outros scripts sem executar a pipeline automaticamente. Quando executado diretamente, o comportamento segue estas etapas:

### Extract (Extração)
Detecta automaticamente o delimitador do CSV (`,`, `;`, `\t`, `|`). Faz uma validação estruturada inicial usando `csv.DictReader` e, em seguida, carrega os dados com `pandas`, alternando entre `utf-8` e `latin1` para evitar erros de encoding. Se o arquivo não existir, ele carrega um DataFrame de exemplo como fallback.

### Transform (Transformação)
Aplica as regras de saneamento, padronização e conversão de tipos (detalhes na seção abaixo).

### Load (Carga/Saída)
Exibe no terminal os insights gerados, roda um validador de integridade (`validar_limpeza`) e exporta os relatórios solicitados via CLI.

---

## Dados Tratados e Regras de Negócio

Durante a fase de Transformação, o script resolve problemas crônicos de qualidade de dados da base bruta:

- **Padronização de Colunas:** Todos os nomes de colunas são convertidos para letras minúsculas e espaços são substituídos por underscores (_).

- **Remoção de Redundâncias:** Linhas duplicadas exatas são eliminadas e colunas completamente vazias (geradas por delimitadores extras como `;;;;`) são descartadas.

- **Tratamento de Máscaras de Erro:** Textos como `#N/D` são convertidos para nulos reais (`NaN`).

- **Categorias Ausentes (PR_CAT):** Valores vazios ou nulos são preenchidos com o texto "Sem Categoria", evitando a perda de rastreabilidade da transação monetária.

- **Dimensões Físicas (DIMENSOES):** Caso a coluna não exista, o script injeta dados simulados para demonstrar a esteira logística. Valores nulos são preenchidos com `0x0x0`.

- **Tratamento Temporal (DATA):** Converte strings de data no formato `dd/mm/yyyy` para o tipo nativo `datetime`.

- **Identificador de Compra (CO_ID):** Valida e cria chaves formatadas no padrão `CO-XXXX`.

---

## Conclusões, Insights e Análises Geradas

O script calcula e exibe no terminal métricas valiosas para o negócio:

- **Estatísticas Descritivas (Número de Filhos - CL_FHL):** Calcula Contagem, Média, Mediana, Moda, Desvio Padrão, Mínimo, Máximo e Quartis (25% e 75%). Essa distribuição ajuda a mapear o tamanho familiar do consumidor para criar campanhas direcionadas (ex: "Leve 3, Pague 2").

- **Padrões de Agrupamento:**

	- Produtos por Gênero (CL_GENERO): Revela o volume de transações por demografia, útil para estratégias de marketing digital.

	- Top 5 Categorias por Estado Civil (CL_EC): Identifica quais categorias performam melhor de acordo com o estado civil do cliente.

- **Alerta de Engenharia:** A alta taxa de valores vazios em categorias apontou uma provável falha de integração nos sistemas de PDV (Frente de Caixa), e a ausência de dados reais de dimensões físicas limita o cálculo de frete e cubagem.

---

##  Ferramentas de Validação e Auditoria

### Teste de Fumaça (test_smoke.py)
Para garantir a estabilidade do código, foi incluído um script de teste rápido. Ele executa a pipeline inteira utilizando apenas os dados internos de exemplo, sem precisar do arquivo CSV real. Ideal para fluxos de Integração Contínua (CI/CD).

```bash
python3 test_smoke.py
```

Saída esperada: `Smoke test Ok!`

### Arquivos de Auditoria
Ao utilizar a flag `-a`, o projeto gera dois arquivos na pasta local:

- `relatorio_auditoria.csv`: Contém métricas por coluna (`num_nulos`, `num_unicos` e uma `amostra_1` do dado real) além de um dump em JSON das primeiras linhas para histórico de linhagem de dados (Data Lineage).

- `relatorio_auditoria.csv.meta.csv`: Um arquivo complementar que armazena metadados rápidos do processo (total de registros processados e quantidade de duplicatas removidas).
