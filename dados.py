import os  
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv  
from sqlalchemy import create_engine, text

load_dotenv()  

data_final_hoje = datetime.today().strftime('%d/%m/%Y')
data_inicial = '01/01/2018'

url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final_hoje}'

df = pd.read_json(url)
df = df.rename(columns={"data": "data", "valor": "taxa_selic"})
df["data"] = pd.to_datetime(df["data"], dayfirst=True).dt.date

engine = create_engine(os.environ["DATABASE_URL"])  


def criar(engine):
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS selic (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                data DATE NOT NULL,
                taxa_selic DOUBLE PRECISION NOT NULL
            )
        """))
        conn.execute(text("TRUNCATE TABLE selic"))


criar(engine)


df.to_sql(
    "selic",
    engine,
    if_exists="append",
    index=False
)

df_consulta = pd.read_sql_query("""
    SELECT *
    FROM selic
    ORDER BY data DESC
    LIMIT 20
""", engine)

print(df_consulta)

engine.dispose()