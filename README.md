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

## Como rodar

1. Clone o repositório e instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Crie um banco PostgreSQL e um arquivo `.env` na raiz do projeto:
   ```
   DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco
   ```
3. Rode o pipeline para popular o banco:
   ```
   python dados.py
   ```
4. Abra o dashboard:
   ```
   streamlit run tela.py