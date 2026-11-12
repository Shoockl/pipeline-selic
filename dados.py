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












# ---------- IPCA ----------
url_ipca = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final_hoje}'

df_ipca = pd.read_json(url_ipca)
df_ipca = df_ipca.rename(columns={"valor": "taxa_ipca"})
df_ipca["data"] = pd.to_datetime(df_ipca["data"], dayfirst=True).dt.date


def criar_ipca(engine):
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ipca (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                data DATE NOT NULL,
                taxa_ipca DOUBLE PRECISION NOT NULL
            )
        """))
        conn.execute(text("TRUNCATE TABLE ipca"))


criar_ipca(engine)

df_ipca.to_sql("ipca", engine, if_exists="append", index=False)

print(pd.read_sql_query("SELECT * FROM ipca ORDER BY data DESC LIMIT 5", engine))