import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import (
    st_autorefresh
)

from bot import analyze

st.set_page_config(
    page_title="Crypto AI Bot",
    layout="wide"
)

st_autorefresh(
    interval=300000,
    key="refresh"
)

st.title(
    "🚀 Crypto AI Dashboard"
)

results = analyze()

df = pd.DataFrame(results)

st.subheader(
    "📊 Análisis General"
)

st.dataframe(df)

best = df.iloc[0]

st.subheader(
    "📌 Señal del Día"
)

st.write(best)

fig1 = px.bar(
    df,
    x="symbol",
    y="probability",
    title="Probabilidad"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)