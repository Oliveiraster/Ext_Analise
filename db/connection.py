import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_connection():

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="data",
            user="postgres",
            password="",
            port=5432
        )
        conn.set_client_encoding('UTF8')
        logging.info("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        raise