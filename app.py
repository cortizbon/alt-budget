import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

st.title("Presupesto alternativo")


df = pd.read_csv('datos_desag_2024_cuentas.csv')

df = df[df['Tipo de gasto'] == 'Funcionamiento']
sectors = list(df['Sector'].unique())
piv = df.groupby(['Sector'])['Aporte nacional'].sum().sort_values(ascending=False)
st.dataframe(piv)


dict = {}

for idx, sector in enumerate(sectors):
    dict[sector] = st.slider(sector, 
                    min_value=0,
                    max_value=int(piv[sector]), 
                    key=idx,
                    value=int(piv[sector]))
    
val = sum(dict.values())

st.dataframe(pd.Series(dict).to_frame())




