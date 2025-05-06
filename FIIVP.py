import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Análise de FIIs por P/VP", layout="wide")
st.title("Análise de FIIs com base no P/VP")

fiis = [
    'HGRU11', 'BTLG11', 'ALZR11', 'HGLG11', 'BRCO11', 'XPLG11', 'KNRI11', 'MALL11', 'VISC11',
    'MXRF11', 'VGIA11', 'BCRI11', 'VILG11', 'LVBI11', 'XPIN11', 'HGR11', 'VINO11'
]

@st.cache_data(show_spinner=True)
def carregar_dados_status_invest(fiis):
    dados = []
    for fii in fiis:
        try:
            url = f'https://statusinvest.com.br/fundos-imobiliarios/{fii.lower()}'
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')

            def extrair_valor(label):
                try:
                    div = soup.find('h3', string=label)
                    if div:
                        return float(div.find_next('strong').text.strip().replace('R$', '').replace('%', '').replace(',', '.'))
                except:
                    return None

            preco = extrair_valor("Cotação")
            pvp = extrair_valor("P/VP")
            dy = extrair_valor("Dividend yield")

            dados.append({
                'FII': fii,
                'Preço Atual (R$)': preco,
                'P/VP': pvp,
                'Dividend Yield (%)': dy,
            })

            time.sleep(1.5)
        except Exception as e:
            st.warning(f"Erro ao buscar dados de {fii}: {e}")
    return pd.DataFrame(dados)

df = carregar_dados_status_invest(fiis)

if df.empty:
    st.error("Não foi possível carregar os dados dos FIIs.")
else:
    st.subheader("Todos os FIIs da carteira:")
    st.dataframe(df.sort_values(by='P/VP', ascending=True))

    st.subheader("FIIs com P/VP abaixo de 1 (potencial desconto):")
    pvp_limite = st.slider("Filtro de P/VP máximo:", min_value=0.5, max_value=1.5, value=1.0, step=0.05)
    fiis_baratos = df[df['P/VP'] < pvp_limite].sort_values(by='P/VP')
    st.dataframe(fiis_baratos)

    st.markdown("**Disclaimer:** P/VP baixo pode indicar desconto, mas deve ser analisado com outros fundamentos.")
