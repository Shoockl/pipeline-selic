# Pipeline Selic: API do Banco Central → PostgreSQL → Dashboard

Pipeline de dados que coleta a taxa Selic da API pública do Banco Central, valida e carrega em um banco PostgreSQL, e exibe a série histórica em um dashboard interativo.

## Problema

Dados econômicos públicos ficam em APIs, mas para analisar a evolução ao longo do tempo é preciso coletar, armazenar de forma organizada e visualizar. Este projeto automatiza esse ciclo.

## Arquitetura

```
API do Banco Central (SGS, série 1178)
        ↓
  pipeline.py  (extrai, trata os tipos, carrega)
        ↓
    PostgreSQL  (tabela selic)
        ↓
  dashboard.py (Streamlit lê do banco e exibe)
```

## Tecnologias

Python, pandas, SQLAlchemy, PostgreSQL, Streamlit.