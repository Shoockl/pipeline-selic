import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])

df = pd.read_sql("SELECT data, taxa_selic FROM selic ORDER BY data", engine)
df["data"] = pd.to_datetime(df["data"]) 

PERIODOS = {  
    "1 ano": pd.DateOffset(years=1),
    "5 anos": pd.DateOffset(years=5),
    "10 anos": pd.DateOffset(years=10),
}

st.title("Selic ao longo do tempo")

escolha = st.radio("Período", list(PERIODOS), index=2, horizontal=True)  
corte = df["data"].max() - PERIODOS[escolha]  
df_filtrado = df[df["data"] >= corte]  

st.metric("Taxa mais recente (% a.a.)", f"{df['taxa_selic'].iloc[-1]:.2f}")
st.line_chart(df_filtrado, x="data", y="taxa_selic")  

df_ipca = pd.read_sql("SELECT data, taxa_ipca FROM ipca ORDER BY data", engine)

st.subheader("IPCA acumulado em 12 meses")
st.line_chart(df_ipca, x="data", y="taxa_ipca")


df_ipca = pd.read_sql("SELECT data, taxa_ipca FROM ipca ORDER BY data", engine)
df_ipca["data"] = pd.to_datetime(df_ipca["data"])

df["mes"] = df["data"].dt.to_period("M")
df_ipca["mes"] = df_ipca["data"].dt.to_period("M")

selic_mensal = df.groupby("mes")["taxa_selic"].last()
ipca_mensal = df_ipca.set_index("mes")["taxa_ipca"]

juntos = pd.concat([selic_mensal, ipca_mensal], axis=1).dropna()
juntos.index = juntos.index.to_timestamp()
juntos = juntos[juntos.index >= corte]  

juntos = juntos.rename(columns={
    "taxa_selic": "Selic (% a.a.)",
    "taxa_ipca": "IPCA 12 meses (%)",
})

st.subheader("Selic × IPCA")
st.line_chart(juntos)