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