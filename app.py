import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

st.title("Presupesto alternativo")


df = pd.read_csv('desag_1924.csv')

df = df[df['Tipo de gasto'] == 'Funcionamiento']
sectors = list(df['Sector'].unique())
entities = list(df['Entidad'].unique())
cuentas = list(df['Cuenta'].unique())
piv = df.pivot_table(index=['Sector', 'Entidad', 'Cuenta'],
                     values='TOTAL',
                     aggfunc='sum',
                     columns='Año').fillna(0)
#piv = df.groupby(['Sector', 'Entidad', 'Cuenta'])['TOTAL'].sum().sort_values(ascending=False)
st.dataframe(piv)

col1, col2, col3 = st.columns(3)

list_lines = []
contador = 0
for col in [col1, col2, col3]:
        for idx, sector in enumerate(sectors):
            st.header(sector)
            entities = list(df[df['Sector'] == sector]['Entidad'].unique())
            for idx2, entidad in enumerate(entities):
                st.write(entidad)
                cuentas = list(df[df['Entidad'] == entidad]['Cuenta'].unique())
                with st.expander(entidad):
                    for idx3, cuenta in enumerate(cuentas):
                            
                        #try:
                        if int(piv[2019][sector][entidad][cuenta]) <= int(piv[2024][sector][entidad][cuenta]):
                            valor = st.slider(f"{sector[:1]}-{entidad[:1]}-{cuenta}", 
                                                    min_value=0,
                                                    max_value=int(piv[2024][sector][entidad][cuenta]), 
                                                    key=contador,
                                                    value=int(piv[2024][sector][entidad][cuenta]))
                        else:
                            valor = st.slider(f"{sector[:1]}-{entidad[:1]}-{cuenta}", 
                                                    min_value=int(piv[2019][sector][entidad][cuenta]),
                                                    max_value=int(piv[2024][sector][entidad][cuenta]), 
                                                    key=contador,
                                                    value=int(piv[2024][sector][entidad][cuenta]))

                        #except:
                        #    valor = st.slider(f"{sector[:1]}-{entidad[:1]}-{cuenta}", min_value=0)
                        line = pd.Series({'sector':sector,
                                            'entidad': entidad,
                                            'cuenta': cuenta,
                                            'valor': valor}).to_frame().T
                        list_lines.append(line)
                        contador += 1

            
alt_budget = pd.concat(list_lines)
val = sum(alt_budget['valor'])

st.metric("Gasto en funcionamiento", val)

st.dataframe(alt_budget)




