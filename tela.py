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