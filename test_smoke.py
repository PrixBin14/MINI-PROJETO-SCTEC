from pathlib import Path

from Miniprojeto_Priscila_Analise_de_Dados_T1 import (
    carregar_csv,
    normalizar_colunas,
    parse_datas,
    resumo_basico,
    dados_exemplo,
)


def test_pipeline_with_example():
    # força uso dos dados de exemplo chamando um arquivo inexistente
    df = carregar_csv(Path('arquivo_inexistente_para_teste.csv'))
    assert df is not None
    df = normalizar_colunas(df)
    df = parse_datas(df, coluna='data')
    resumo = resumo_basico(df)
    assert 'coluna' in resumo.columns


if __name__ == '__main__':
    test_pipeline_with_example()
    print('Smoke test Ok!')
