# Mini-Projeto: Análise Exploratória de Dados (Varejo)

## Instruções de Execução
Para executar este projeto na sua máquina:
1. Clone este repositório.
2. Certifique-se de ter o Python instalado, além da biblioteca pandas (`pip install pandas`).
3. Abra o terminal ou o VsCode e execute o comando: `python Miniprojeto_Priscila_Analise_de_Dados_T1.py`.
4. O script gerará um relatório completo no terminal.

## Reflexão Teórica: ETL e Qualidade de Dados
O processo de ETL (Extract, Transform, Load) é fundamental na área de dados. Neste projeto, a **Extração** ocorreu na leitura da base bruta; a **Transformação** envolveu a limpeza de nulos, remoção de duplicatas, adequação de tipos (como datas) e regras de negócio; e a **Carga** (simulada) seria a entrega do dataset limpo para consumo. A qualidade de dados garante que as decisões de negócio não sejam tomadas com base em informações irreais ou corrompidas.

## Insights Obtidos da Análise
* **Padronização de Categorias:** A ausência de categorias em muitos produtos mostrou a necessidade de classificar itens como "Sem Categoria" para não perder os dados financeiros atrelados a essas vendas.
* **Sazonalidade:** Após a conversão correta das datas para `datetime`, foi possível agrupar os dados e notar padrões temporais de compra (dias com maior volume de vendas).
* **Perfil de Clientes (Filhos):** A análise estatística da coluna de filhos demonstrou a média e a dispersão do tamanho familiar dos clientes, ajudando a direcionar campanhas de marketing futuras.
* **Volume por Gênero e Categoria:** O cruzamento (agrupamento) entre Gênero e Categorias revelou quais nichos de produtos são mais fortes para cada público.
* **Problemas Remanescentes:** Apesar da limpeza, a base original não possui padronização estrita nas dimensões físicas, o que exigiu imputação de valores padrão (0) que podem não refletir o volume real para logística.