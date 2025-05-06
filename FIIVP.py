import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de FIIs por P/VP", layout="wide")
st.title("Análise de FIIs com base no P/VP")

fiis_usuario = [
    'HGRU11', 'BTLG11', 'ALZR11', 'HGLG11', 'BRCO11', 'XPLG11', 'KNRI11', 'MALL11',
    'VISC11', 'MXRF11', 'VGIA11', 'BCRI11', 'VILG11', 'HCCI11', 'XPIN11', 'HGR11', 'VINO11'
]

@st.cache_data(show_spinner=True)
def carregar_dados_funds_explorer():
    url = 'https://www.fundsexplorer.com.br/ranking'
    try:
        df = pd.read_html(url, decimal=',', thousands='.')[0]
        df.columns = df.columns.droplevel(0) if isinstance(df.columns, pd.MultiIndex) else df.columns
        df = df.rename(columns={'Códigodo fundo': 'FII'})
        df['P/VP'] = pd.to_numeric(df['P/VP'], errors='coerce')
        df['Dividend Yield'] = pd.to_numeric(df['Dividend Yield'], errors='coerce')
        df['Preço Atual'] = pd.to_numeric(df['Preço Atual'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados_funds_explorer()

if not df.empty:
    df_carteira = df[df['FII'].isin(fiis_usuario)].copy()
    df_carteira = df_carteira[['FII', 'Setor', 'Preço Atual', 'Dividend Yield', 'P/VP']]
    df_carteira = df_carteira.sort_values(by='P/VP')

    st.subheader("FIIs da Carteira")
    st.dataframe(df_carteira, use_container_width=True)

    st.subheader("FIIs com P/VP abaixo de 1")
    limite_pvp = st.slider("Limite máximo de P/VP:", min_value=0.5, max_value=1.5, value=1.0, step=0.05)
    filtrados = df_carteira[df_carteira['P/VP'] < limite_pvp]
    st.dataframe(filtrados, use_container_width=True)

    st.markdown("**Observação:** P/VP abaixo de 1 pode indicar desconto, mas analise também qualidade da gestão, vacância, contratos e liquidez.")
else:
    st.error("Não foi possível carregar os dados.")
