import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

st.title("Presupesto alternativo")

st.divider()


df = pd.read_csv('desag_1924.csv')

df = df[df['Tipo de gasto'] == 'Funcionamiento']
sectors = list(df['Sector'].unique())
entities = list(df['Entidad'].unique())
cuentas = list(df['Cuenta'].unique())
piv = df.pivot_table(index=['Sector', 'Entidad', 'Cuenta'],
                     values='apropiaciones_constantes_2025',
                     aggfunc='sum',
                     columns='Año').fillna(0)
#piv = df.groupby(['Sector', 'Entidad', 'Cuenta'])['TOTAL'].sum().sort_values(ascending=False)
col1, col2, col3 = st.columns(3)

list_lines = []
contador = 0

for idx, sector in enumerate(sectors):
    st.header(sector)
    entities = list(df[df['Sector'] == sector]['Entidad'].unique())
    for idx2, entidad in enumerate(entities):
        cuentas = list(df[df['Entidad'] == entidad]['Cuenta'].unique())
        with st.expander(entidad):
            for idx3, cuenta in enumerate(cuentas):
                            
                        #try:
                if int(piv[2019][sector][entidad][cuenta]) + int(piv[2024][sector][entidad][cuenta]) == 0:
                    valor = st.slider(f"{sector[:1]}-{entidad[:1]}-{cuenta}", 
                                                    min_value=0,
                                                    max_value=100, 
                                                    key=contador,
                                                    value=0)
                        
                elif int(piv[2019][sector][entidad][cuenta]) >= int(piv[2024][sector][entidad][cuenta]):
                    valor = st.slider(f"{sector[:1]}-{entidad[:1]}-{cuenta}", 
                                                    min_value=int(piv[2024][sector][entidad][cuenta]),
                                                    max_value=int(piv[2024][sector][entidad][cuenta]) + 100, 
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

            
alt_budget = pd.concat(list_lines, ignore_index=True)
val = round(alt_budget['valor'].sum() / 1_000_000_000_000, 2)

ents_2024 = list(df[df['Año'] == 2024]['Entidad'].unique())
st.metric("Gasto en funcionamiento", val)

alt_budget = alt_budget[alt_budget['entidad'].isin(ents_2024)]
st.dataframe(alt_budget)




