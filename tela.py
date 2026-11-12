import os  
import pandas as pd
import streamlit as st
from dotenv import load_dotenv 
from sqlalchemy import create_engine

load_dotenv()  

engine = create_engine(os.environ["DATABASE_URL"])  
df = pd.read_sql("SELECT data, taxa_selic FROM selic ORDER BY data", engine)

st.title("Selic ao longo do tempo")
st.metric("Taxa mais recente (% a.a.)", f"{df['taxa_selic'].iloc[-1]:.2f}")
st.line_chart(df, x="data", y="taxa_selic")