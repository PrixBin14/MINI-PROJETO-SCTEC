import csv
import pandas as pd
from datetime import datetime

print("Iniciando o processamento do Mini-Projeto!\n")
caminho_arquivo = 'Base varejo.csv'
dados_brutos_dict = []
try:
    with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
        leitor_csv = csv.DictReader(file)
        for linha in leitor_csv:
            dados_brutos_dict.append(linha)
    print("Sucesso: Dados extraídos estruturalmente do arquivo CSV.\n")
except FileNotFoundError:
    print("Aviso: Arquivo Varejo.csv não encontrado. Verifique o caminho e tente novamente.\n")

try:
    df = pd.read_csv(caminho_arquivo)
    print("\n--- Informações Básicas do Dataset ---")
    print(f"Número de registros: {df.shape[0]}")
    print(f"Número de colunas: {df.shape[1]}")
    print("\nTipos de Dados Iniciais:")
    print(df.dtypes)
except FileNotFoundError:
    print("Aviso: Arquivo Varejo.csv não encontrado. Verifique o caminho e tente novamente.\n")
    
    print("\nGerando dados de exemplo para demonstração do script...")
    dados_exemplo = {
        'ID_Compra': ['A-101', 'B-102', 'C-103', 'A-101', 'D-104'],
        'Data': ['15/05/2023', '20/05/2023', 'invalida', '15/05/2023', '25/05/2023'],
        'Categoria': ['Eletrônicos', None, 'Móveis', 'Eletrônicos', ''],
        'Dimensoes': [None, '10x10', '20x50', None, '15x15'],
        'Filhos': [2, 0, 1, 2, 4],
        'Genero': ['F', 'M', 'F', 'F', 'M'],
        'Valor': [1500.50, 200.0, 450.0, 1500.50, 120.0]
    }
    df = pd.DataFrame(dados_exemplo)