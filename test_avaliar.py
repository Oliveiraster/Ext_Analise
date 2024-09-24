from evaluation import avaliar_mensal, avaliar_anual
from analysis import (
    explorar_dados,
    medidas_tendencia,
    medidas_dispersao,
    calcular_probabilidades,
    modelar_variaveis_discretas,
    modelar_variaveis_continuas,
    testes_de_hipotese,
    regressao_linear
)
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_avaliar_mensal():
    mes = 9
    ano = 2024
    try:
        df = avaliar_mensal(mes, ano)
        if df.empty:
            print("Nenhum dado encontrado para a avaliação mensal.")
        else:
            print("Avaliação Mensal:")
            print(df)
            
            explorar_dados(df)
            medidas_tendencia(df)
            medidas_dispersao(df)
            calcular_probabilidades(df)
            modelar_variaveis_discretas(df)
            modelar_variaveis_continuas(df)
            testes_de_hipotese(df)
            regressao_linear(df)
    except Exception as e:
        print(f"Erro durante a avaliação mensal: {e}")


def test_avaliar_anual():
    ano = 2024
    try:
        df = avaliar_anual(ano)
        if df.empty:
            print("Nenhum dado encontrado para a avaliação anual.")
        else:
            print("Avaliação Anual:")
            print(df)

            explorar_dados(df)
            medidas_tendencia(df)
            medidas_dispersao(df)
            calcular_probabilidades(df)
            modelar_variaveis_discretas(df)
            modelar_variaveis_continuas(df)
            testes_de_hipotese(df)
            regressao_linear(df)
    except Exception as e:
        print(f"Erro durante a avaliação anual: {e}")


if __name__ == "__main__":
    print("Testando avaliação mensal:")
    test_avaliar_mensal()
    print("\nTestando avaliação anual:")
    test_avaliar_anual()
