# A Jornada dos Dados: Desvendando o Caos no Varejo

**Estudante:** Priscila | **Turma:** Analise_de_Dados_T1  
**Tecnologias:** Python, Pandas, SQL Foundations, Git & VsCode

---

## O Cenário: O Desafio da Base Oculta

Imagine-se assumindo o papel de Analista de Dados em uma grande corporação de varejo. À sua mesa chega uma missão crítica: a diretoria precisa lançar uma nova campanha de marketing segmentada e otimizar a cadeia logística. O motor para essa tomada de decisão existe, mas está trancado em um arquivo bruto chamado `Base Varejo.csv`. 

Ao abrir o arquivo pela primeira vez, o cenário era caótico: delimitadores desajustados sabotando a leitura, registros duplicados inflando os números reais de faturamento, datas registradas como meros textos impossíveis de ordenar cronologicamente, e o pior: lacunas ocultas sob a sigla `#N/D`. 

Este projeto documenta a minha jornada técnica para resgatar, limpar e transformar esse deserto de dados brutos em um oásis de insights estratégicos e acionáveis.

---

## O Resgate Técnico (Passo a Passo do Pipeline)

Para que nenhuma informação fosse corrompida, montei uma estrutura de Sprints e tratamento de dados dividida em etapas rigorosas de engenharia:

### 1. A Extração e Reconhecimento do Terreno

O primeiro desafio foi a leitura precisa do arquivo. Para garantir a conformidade nativa, utilizei estruturas como `csv.DictReader` combinadas com o `csv.Sniffer` para que o script mapeasse autonomamente se o delimitador era vírgula ou ponto-e-vírgula. Com o terreno preparado, o Pandas assumiu o controle revelando o tamanho real do desafio (linhas, colunas e tipos primitivos de dados).

### 2. A Purificação da Base (Tratamento de Anomalias)

* **Eliminação de Ruídos:** Linhas idênticas e redundantes foram removidas para evitar distorções estatísticas.
* **Máscaras Reveladas:** Valores inválidos como `#N/D` foram convertidos em NaNs reais para tratamento adequado.
* **Lógica de Categorização:** Utilizando condicionais lógicas estruturadas, produtos sem classificação foram rotulados como `"Sem Categoria"`, impedindo a perda de histórico financeiro dessas transações.
* **A Linha do Tempo Ajustada:** Strings confusas de datas foram convertidas para objetos `datetime`, permitindo análises de tendências temporais.
* **Regra de Negócio Implementada:** O ID interno de compras foi decodificado e padronizado sob o prefixo corporativo `CO-` para indexação futura.

---

### Descobertas e Insights de Negócio (O Clímax da Análise)

Após estabilizar a base, os dados finalmente começaram a contar suas histórias através de agrupamentos e estatísticas descritivas:

* **O Perfil Familiar do Consumidor (`CL_FHL`):** A análise estatística descritiva completa revelou a distribuição exata do número de filhos dos clientes. Parâmetros como a *Média* e a *Mediana* traçam com precisão a estrutura familiar predominante do público-alvo, permitindo que a equipe de marketing crie campanhas personalizadas (ex: promoções de Dia das Crianças ou pacotes familiares).
* **Força Demográfica (`CL_GENERO`):** O cruzamento e agrupamento revelaram qual gênero lidera o volume total de transações e a quantidade de produtos movimentados, direcionando o orçamento de tráfego pago para o público de maior conversão.
* **Preferências por Estado Civil (`CL_EC`):** Mapeamos as Top 5 categorias de produtos mais consumidas cruzadas com o estado civil dos compradores. Descobrimos padrões comportamentais distintos que alteram as prioridades de estoque da loja.

---

## Problemas Remanescentes e Próximos Passos

Nenhuma jornada de dados termina na primeira limpeza. Identifiquei gargalos que devem ser tratados em Sprints futuras:
1. **Falha Originária no PDV:** O alto volume de produtos categorizados originalmente como `#N/D` sinaliza um problema estrutural no cadastro de produtos ou nos caixas físicos. A engenharia de software foi alertada.
2. **Ausência das Dimensões Físicas:** A falta de dados sobre altura, largura e peso dos itens impede que o time de logística calcule a cubagem exata de frete, limitando nossa automação logística atual.

---

## Como Executar e Validar o Projeto

O projeto foi totalmente projetado para ser reprodutível no **VsCode** ou **Google Colab**.

### Pré-requisitos

Instale as bibliotecas necessárias rodando no terminal:
```bash
pip install -r requirements.txt 
```  

## Relatórios gerados

1. Por que geramos relatórios?

- Auditoria e Transparência: para que um time externo (auditores, compliance) possa verificar o histórico e as decisões de limpeza sem reprocessar a base.
- Rastreabilidade: documentar pre/post transformações facilita replicação e investigação de regressões.
- Entregáveis de Negócio: resumos rápidos permitem que as áreas (Marketing, Logística) consumam insights sem aguardar dashboards completos.
- Reprodutibilidade: salvar resumos e relatórios permite reproduzir resultados, comparar versões e documentar quais transformações foram aplicadas.
- Entrega de Valor Rápida: um CSV de resumo e um relatório de auditoria dão às áreas de negócio (Marketing, Logística, BI) entregáveis imediatamente utilizáveis.

2. Quais relatórios o script pode gerar?

- Resumo por coluna (CSV): use a flag `--save-summary / -s` para exportar a tabela gerada por `resumo_basico()`.
- Relatório de auditoria (CSV + .meta.csv): use `--audit-report / -a` para gerar um CSV com métricas por coluna (tipo, nulos, únicos, exemplo) e um arquivo auxiliar de metadados (`<nome>.meta.csv`) com informações como total de registros e duplicatas detectadas.

3. Quais relatórios e como gerá-los?

- Resumo por coluna (CSV): `--save-summary / -s`
	- Exemplo: `python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -s resumo_colunas.csv`
- Relatório de auditoria (CSV + meta): `--audit-report / -a`
	- Exemplo: `python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv" -a relatorio_auditoria.csv`

4. O que contém o relatório de auditoria?

- Por coluna: nome, tipo, número de nulos, número de valores únicos e um exemplo de valor (`amostra_1`).
- Arquivo meta (`<nome>.meta.csv`) com metadados do processamento: total de registros e duplicatas removidas.

5. Por que isso importa:

> Imagine que um auditor precise confirmar se o número de vendas divulgado pela equipe de BI não foi inflado por duplicatas ou erros de leitura. Com os relatórios gerados, o auditor pode checar rapidamente as contagens e as transformações aplicadas, sem reexecutar todo o pipeline — evitando reprovações e acelerando a validação.