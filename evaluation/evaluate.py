import pandas as pd
from db import get_connection
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(mes=None, ano=None):
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        
        query = """
            SELECT 
                f.id, 
                f.nome, 
                d.atendimentos,  -- Nome da coluna corrigido
                d.satisfacao, 
                d.tempo_medio_atendimento, 
                d.horario_pico, 
                d.resolucao_primeiro_contato, 
                d.atrasos, 
                EXTRACT(MONTH FROM d.data) AS mes,
                EXTRACT(YEAR FROM d.data) AS ano
            FROM funcionarios f
            JOIN dados_diarios d ON f.id = d.funcionario_id
        """

        params = []
        conditions = []

        if mes:
            conditions.append("EXTRACT(MONTH FROM d.data) = %s")
            params.append(mes)
        if ano:
            conditions.append("EXTRACT(YEAR FROM d.data) = %s")
            params.append(ano)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        logging.info(f"Executando query: {query} com parâmetros {params}")
        df = pd.read_sql_query(query, conn, params=params)
        cursor.close()
        conn.close()

        logging.info(f"Dados recuperados: {len(df)} registros encontrados.")
        return df
    except Exception as e:
        logging.error(f"Erro ao buscar dados: {e}")
        raise

def avaliar_funcionarios(df):
   
    if df.empty:
        logging.warning("Nenhum dado para avaliação.")
        return df

    df['Pontuacao'] = (
        (df['satisfacao'] * 0.4) +
        (df['resolucao_primeiro_contato'].astype(int) * 0.3) +
        (df['atendimentos'] * 0.2) +
        (df['horario_pico'].astype(int) * 0.1)
    )

    df_ordenado = df.sort_values(by='Pontuacao', ascending=False).reset_index(drop=True)

    logging.info("Avaliação dos funcionários realizada com sucesso.")
    return df_ordenado

def avaliar_mensal(mes, ano):
    
    logging.info(f"Iniciando avaliação mensal para {mes}/{ano}.")
    df = fetch_data(mes=mes, ano=ano)
    df_avaliado = avaliar_funcionarios(df)
    return df_avaliado

def avaliar_anual(ano):
    
    logging.info(f"Iniciando avaliação anual para {ano}.")
    df = fetch_data(ano=ano)

    if df.empty:
        logging.warning("Nenhum dado para avaliação anual.")
        return df

    df_agregado = df.groupby(['id', 'nome']).agg({
        'atendimentos': 'sum',
        'satisfacao': 'mean',
        'tempo_medio_atendimento': 'mean',
        'horario_pico': 'mean',  
        'resolucao_primeiro_contato': 'mean',
        'atrasos': 'sum'
    }).reset_index()

    df_agregado['horario_pico'] = df_agregado['horario_pico'].apply(lambda x: True if x >= 0.5 else False)

    df_agregado['Pontuacao'] = (
        (df_agregado['satisfacao'] * 0.4) +
        (df_agregado['resolucao_primeiro_contato'].astype(int) * 0.3) +
        (df_agregado['atendimentos'] * 0.2) +
        (df_agregado['horario_pico'].astype(int) * 0.1)
    )

    df_ordenado = df_agregado.sort_values(by='Pontuacao', ascending=False).reset_index(drop=True)

    logging.info("Avaliação anual dos funcionários realizada com sucesso.")
    return df_ordenado
