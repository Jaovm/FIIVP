import streamlit as st
import pandas as pd
import requests

# Lista de FIIs da carteira
fiis = [
    'HGRU11', 'BTLG11', 'ALZR11', 'HGLG11', 'BRCO11', 'XPLG11', 'KNRI11', 'MALL11', 'VISC11',
    'MXRF11', 'VGIA11', 'BCRI11', 'VILG11', 'LVBI11', 'XPIN11', 'HGR11', 'VINO11'
]

st.set_page_config(page_title="Análise de FIIs por P/VP", layout="wide")
st.title("Análise de FIIs com base no P/VP")

st.markdown("FIIs com **P/VP abaixo de 1** são considerados, em tese, descontados em relação ao valor patrimonial.")

@st.cache_data
def carregar_dados_fiis(fiis):
    base_url = "https://www.fundsexplorer.com.br/wp-json/funds/v1/funds/"
    dados = []
    for fii in fiis:
        try:
            response = requests.get(f"{base_url}{fii}")
            if response.status_code == 200:
                data = response.json()
                dados.append({
                    'FII': fii,
                    'Setor': data.get('segment', 'N/A'),
                    'P/VP': float(data.get('p_vp', 0)),
                    'Preço Atual': float(data.get('price', 0)),
                    'Valor Patrimonial': float(data.get('equity_value', 0)),
                    'Dividend Yield (%)': float(data.get('dividend_yield', 0)) * 100,
                })
        except Exception as e:
            st.warning(f"Erro ao carregar dados de {fii}: {e}")
    return pd.DataFrame(dados)

df = carregar_dados_fiis(fiis)

if df.empty:
    st.error("Não foi possível carregar os dados dos FIIs.")
else:
    st.subheader("Todos os FIIs da carteira:")
    st.dataframe(df.sort_values(by='P/VP'))

    st.subheader("FIIs com P/VP abaixo de 1 (potencial desconto):")
    pvp_limite = st.slider("Filtro de P/VP máximo:", min_value=0.5, max_value=1.5, value=1.0, step=0.05)
    fiis_baratos = df[df['P/VP'] < pvp_limite].sort_values(by='P/VP')
    st.dataframe(fiis_baratos)

    st.markdown("**Disclaimer:** P/VP baixo pode indicar desconto, mas deve ser analisado com outros fundamentos (vacância, localização, qualidade da gestão etc.).")
