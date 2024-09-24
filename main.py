from evaluation import avaliar_mensal, avaliar_anual
from reports import gerar_relatorio
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
import argparse
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def realizar_analises(df):
 
    explorar_dados(df)
    medidas_tendencia(df)
    medidas_dispersao(df)
    calcular_probabilidades(df)
    modelar_variaveis_discretas(df)
    modelar_variaveis_continuas(df)
    testes_de_hipotese(df)
    regressao_linear(df)

def main():
    parser = argparse.ArgumentParser(description="Avaliação de Funcionários por Atendimento")

    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponíveis')

    parser_mensal = subparsers.add_parser('mensal', help='Realizar avaliação mensal')
    parser_mensal.add_argument('--mes', type=int, required=True, help='Mês da avaliação (1-12)')
    parser_mensal.add_argument('--ano', type=int, required=True, help='Ano da avaliação')

    parser_anual = subparsers.add_parser('anual', help='Realizar avaliação anual')
    parser_anual.add_argument('--ano', type=int, required=True, help='Ano da avaliação')

    args = parser.parse_args()

    if args.comando == 'mensal':
        mes = args.mes
        ano = args.ano
        if not (1 <= mes <= 12):
            logging.error("Mês inválido. Deve ser entre 1 e 12.")
            return

        logging.info(f"Realizando avaliação mensal para {mes}/{ano}...")
        try:
            df_avaliado = avaliar_mensal(mes, ano)
            if not df_avaliado.empty:
                gerar_relatorio(df_avaliado, tipo='mensal', mes=mes, ano=ano)
                
                realizar_analises(df_avaliado)
                
                funcionario_premiado = df_avaliado.iloc[0]
                print(f"\nFuncionário do mês: {funcionario_premiado['nome']} com pontuação de {funcionario_premiado['Pontuacao']:.2f}")
            else:
                logging.warning("Nenhum dado encontrado para a avaliação mensal.")
        except Exception as e:
            logging.error(f"Erro durante a avaliação mensal: {e}")

    elif args.comando == 'anual':
        ano = args.ano
        logging.info(f"Realizando avaliação anual para {ano}...")
        try:
            df_avaliado = avaliar_anual(ano)
            if not df_avaliado.empty:
                gerar_relatorio(df_avaliado, tipo='anual', ano=ano)
                
                realizar_analises(df_avaliado)
                
                funcionario_premiado = df_avaliado.iloc[0]
                print(f"\nFuncionário do ano: {funcionario_premiado['nome']} com pontuação de {funcionario_premiado['Pontuacao']:.2f}")
            else:
                logging.warning("Nenhum dado encontrado para a avaliação anual.")
        except Exception as e:
            logging.error(f"Erro durante a avaliação anual: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
