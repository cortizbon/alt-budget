import streamlit as st
import pandas as pd
from utils import create_dataframe_sankey
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(layout='wide')


st.title("Test-alt")

tab1, tab2 = st.tabs(["Alt-budget", "Flujo de gasto: 2024 - 2025"])


with tab1:
    st.header("Presupesto alternativo")
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
    st.dataframe(piv)
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
                                                        value=int(piv[2019][sector][entidad][cuenta]))

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

with tab2:
    df2 = pd.read_csv('dataset_192425.csv')
    df2 = df2[df2['Año'].isin([2024, 2025])]
    st.write("Seleccione el nivel de profundidad a analizar (si selecciona cuenta, otros tres niveles se despliegan): ")
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7 = st.columns(3)
    
    with col1:
        sector = st.checkbox("Sector")
        subcuenta = st.checkbox("Subcuenta")
    with col2:
        entidad = st.checkbox("Entidad")
        objeto = st.checkbox("Objeto")
    with col3:
        tipo_gasto = st.checkbox("Tipo de gasto")
        ordinal = st.checkbox("Ordinal")
    with col4: 
        cuenta = st.checkbox("Cuenta")
         
    dic_cols = {'Sector': sector,
                'Entidad': entidad,
                'Tipo de gasto': tipo_gasto,
                'Cuenta': cuenta,
                'Subcuenta': subcuenta,
                'Objeto/proyecto': objeto, 
                'Subproyecto': ordinal}
    
    cols_to_include = pd.Series(dic_cols)
    cols_to_include = cols_to_include[cols_to_include == True].index
    if len(cols_to_include) > 4:
        st.warning("El número de columnas no puede ser mayor a 4.")
        st.stop()
    if len(cols_to_include) >= 2: 
        cols = st.columns(len(cols_to_include))
        filters = {}
        for idx, col in enumerate(cols):
            with col:
                filters[cols_to_include[idx]] = st.multiselect(f"Seleccione para la columna: {cols_to_include[idx]}",
                            df2[cols_to_include[idx]].unique())
                

        rev_info, conc = create_dataframe_sankey(df2, 
                                    "Apropiación en precios constantes (2025)",
                                    *cols_to_include)
        
        fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "#2635bf", width = 0.5),
        label = list(rev_info.keys()),
        color = "#2635bf"
        ),
        link = dict(
        source = conc['source'], 
        target = conc['target'],
        value = conc['value']
        ))])

        fig.update_layout(title_text="Flujo de gasto", font_size=10, width=1000, height=600)
        st.plotly_chart(fig)
        

        
    

    


    
    



