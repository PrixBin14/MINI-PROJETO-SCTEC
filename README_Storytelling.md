# A Jornada dos Dados: Desvendando o Caos no Varejo

**Estudante:** Priscila C. Ferreira 
**Turma:** Analise_de_Dados_T1  

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

### 2.1 Dados duplicados

Analisando o arquivo foram identificados produtos que possuem o mesmo nome, mas códigos (`PR_ID`) diferentes.
Processei os dados do seu arquivo CSV, para identificar produtos "duplicados":

* **Resumo da Análise Total de produtos nessa situação:** Encontrei 4 nomes de produtos que estão duplicados com IDs diferentes.
* **Total de códigos envolvidos:** Esses 4 nomes se dividem em 8 códigos distintos.

* **Quais são esses produtos e seus códigos:** 
Categoria (`PR_CAT`).  Nome do Produto (`PR_NOME`).	Códigos Encontrados (`PR_ID`)
ALIMENTOS				MACARRAO						11 e 12
ALIMENTOS				BISCOITO						141 e 142
ALIMENTOS				REQUEIJAO						207 e 208
LIMPEZA					SABÃO EM PÓ						112 e 220

* **Por que isso costuma acontecer no varejo:** 
Esse cenário geralmente ocorre por três motivos: 
* Variação de Tamanho/Peso: O produto tem o mesmo nome, mas um código é para a versão de 500g e o outro para a de 1kg (muito comum em Macarrão e Sabão em Pó).
* Marcas Diferentes: O sistema cadastrou apenas o nome genérico ("Biscoito"), mas separou os códigos para marcas ou sabores diferentes.
* Erro de Cadastro: Duplicidade real no banco de dados onde o mesmo item recebeu dois códigos por falha operacional.

* **Inconsistência Detectada: Linhas Duplicadas**
O único — e principal — problema identificado na base foi um volume massivo de linhas idênticas duplicadas.
Total de linhas afetadas: Existem 96.553 linhas repetidas na base.
* **O problema:** Dentro do mesmo cupom (`CO_ID`), o exato mesmo produto (`PR_ID`) aparece listado mais de uma vez em linhas totalmente separadas e idênticas, em vez de estar consolidado em uma coluna de "Quantidade".

* **Exemplo real extraído da sua base:**
No cupom 1000, o cliente comprou o produto 4 (ALIMENTOS - ABACAXI). Em vez de o sistema registrar que ele levou 2 unidades, o arquivo gerou duas linhas idênticas para a mesma compra:

Linha 3:  01/02/2019;1000;534;M;4;1;C;4;ALIMENTOS;ABACAXI
Linha 40: 01/02/2019;1000;534;M;4;1;C;4;ALIMENTOS;ABACAXI

O mesmo acontece no mesmo cupom para os itens Azeite, Banana, Refrigerante Limão e Bife de Coxão Mole.

Por esse motivo apliquei o comando de *remoção de duplicadas* antes de prosseguir com as análises.
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

## Por que existe `df_limpo` e o teste de integridade

No meio do projeto houve um momento decisivo — rodando o script pela primeira vez com a base bruta, percebemos que pequenas mudanças no pipeline (um replace aqui, uma normalização ali) podiam alterar muito o resultado final. Foi nesse ponto que nasceu o `df_limpo` e o teste de verificação rápida.

Imagine o seguinte: você está a poucos minutos de enviar um relatório executivo. Em vez de reprocessar tudo manualmente, basta gerar o `df_limpo` (o DataFrame final após leitura, parsing e limpeza) e rodar a verificação rápida. Em segundos você tem:

* Quantidade de nulos por coluna (sinais de problemas de ingestão);
* Quantidade de duplicatas (ajuda a confirmar a contagem real de vendas);
* Tipos de dado detectados (garante que as colunas temporais e numéricas estão corretas).

* O arquivo original Base Varejo.csv possui *830.000* linhas (incluindo o cabeçalho).

- Após realizar o processo de limpeza e remover as linhas duplicadas, o novo arquivo gerado (df_limpo.csv) ficou com *733.447* linhas.

Essa rotina não é mágica — é um contrato de confiança: `df_limpo` representa o estado do dado pronto para análise, e a verificação rápida é um pequeno roteiro de checagem que reduz o risco de regressões e acelera revisões por pares.

**Quando usar:**
* Durante desenvolvimento: execute antes de abrir um PR para garantir que suas alterações não quebraram a transformação final.
* Em revisão: o avaliador consegue reproduzir o estado final da transformação com um conjunto mínimo de comandos.
* Em produção experimental: como smoke test em pipelines CI para captar mudanças inesperadas na entrada de dados.

**Exemplo rápido (CLI):**

```bash
python3 Miniprojeto_Priscila_Analise_de_Dados_T1.py -f "Base Varejo.csv"
```

Exemplo rápido (programático):

```python
from Miniprojeto_Priscila_Analise_de_Dados_T1 import carregar_csv, normalizar_colunas, parse_datas, process_dataframe, validar_limpeza
from pathlib import Path

df = carregar_csv(Path('Base Varejo.csv'))
df = normalizar_colunas(df)
df = parse_datas(df, coluna='data')
df_limpo = process_dataframe(df)
validar_limpeza(df_limpo)
```

THE END ! 