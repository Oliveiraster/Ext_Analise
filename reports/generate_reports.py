import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def gerar_relatorio(df, tipo='mensal', mes=None, ano=None):

    if df.empty:
        logging.warning("Nenhum dado para gerar o relatório.")
        return

    if tipo == 'mensal':
        nome_relatorio = f"relatorio_mensal_{mes}_{ano}.csv"
        titulo = f"Avaliação Mensal - {mes}/{ano}"
    elif tipo == 'anual':
        nome_relatorio = f"relatorio_anual_{ano}.csv"
        titulo = f"Avaliação Anual - {ano}"
    else:
        logging.error("Tipo de relatório inválido. Use 'mensal' ou 'anual'.")
        return

    df_relatorio = df[['nome', 'atendimentos', 'satisfacao', 'resolucao_primeiro_contato', 'Pontuacao']]

    try:
        df_relatorio.to_csv(nome_relatorio, index=False)
        logging.info(f"Relatório salvo como '{nome_relatorio}'.")
    except Exception as e:
        logging.error(f"Erro ao salvar o relatório: {e}")
        return

    print(f"\n{titulo}:")
    print(df_relatorio.to_string(index=False))
