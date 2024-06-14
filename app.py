import streamlit as st
import pandas as pd
from utils import create_dataframe_sankey, create_dataframe_sankey2
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from itertools import chain
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')
COLORS_LINKS = dict(enumerate(["#D9D9ED", "#FFE9C5", "#CBECEF", "#CBECEF", "#CBECEF"]))
COLORS_NODES = dict(enumerate(["#2F399B", "#F7B261", "#0FB7B3", "#81D3CD", "#81D3CD", "#81D3CD"]))

st.title("Test-alt")

tab1, tab2, tab3, tab4 = st.tabs(["Alt-budget", 
                      "Diff 2019 - 2024",
                      "Flujo de gasto",
                      "Diff 2019-2024 (ordenada)"])


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


    
# with tab3:
#     data = pd.read_csv('dataset_192425.csv')

#     df2 = data.copy()
#     df2['PGN'] = 'PGN'
#     st.write("Seleccione el nivel de profundidad a analizar (solo funcionamiento): ")
#     col1, col2, col3, col4 = st.columns(4)
#     col5, col6, col7 = st.columns(3)
    
#     with col1:
#         pgn = st.checkbox(" PGN")
#         cuenta = st.checkbox(" Cuenta")
        
#     with col2:
#         sector = st.checkbox(" Sector")
#         subcuenta = st.checkbox(" Subcuenta")
        
#     with col3:
#         entidad = st.checkbox(" Entidad")
#         objeto = st.checkbox(" Objeto")
        
#     with col4:
#         tipo_gasto = st.checkbox(" Tipo de gasto")
#         ordinal = st.checkbox(" Ordinal") 
        
         
#     dic_cols = {'PGN': pgn, 
#                 'Sector': sector,
#                 'Entidad': entidad,
#                 'Tipo de gasto': tipo_gasto,
#                 'Cuenta': cuenta,
#                 'Subcuenta': subcuenta,
#                 'Objeto/proyecto': objeto, 
#                 'Subproyecto': ordinal}
#     if (dic_cols['PGN'] and dic_cols['Sector']) or (dic_cols['PGN'] and dic_cols['Entidad']) or (dic_cols['Entidad'] and dic_cols['Sector']):
#         st.error("Demasiada información para mostrar. Evite combinaciones entre sector, pgn y entidad.")
#         st.stop()
    
#     cols_to_include = pd.Series(dic_cols)
#     cols_to_include = cols_to_include[cols_to_include == True].index
#     if len(cols_to_include) > 5:
#         st.warning("El número de columnas no puede ser mayor a 5.")
#         st.stop()
#     if len(cols_to_include) >= 2: 
#         cols = st.columns(len(cols_to_include))
#         filters = {}
#         df3 = df2[df2['Tipo de gasto'] == 'Funcionamiento'].copy()
#         dfs1 = []
#         nodes1 = []
#         pos1 = []
#         for idx, col in enumerate(cols):
#             with col:
#                 vals = st.multiselect(f" Seleccione para la columna: {cols_to_include[idx]}",
#                                 df3[cols_to_include[idx]].unique())
                
#                 filters[cols_to_include[idx]] = vals
#                 for value in df3[cols_to_include[idx]].unique():
#                     nodes1.append(value)
#                     pos1.append(idx)
#                 df3 = df3[df3[cols_to_include[idx]].isin(vals)]
#                 if idx != len(cols_to_include) - 1:
#                     try:
#                         dfs1.append((df3
#                             .pivot_table(index = [cols_to_include[idx], 
#                                     cols_to_include[idx + 1]],
#                                     values='Apropiación en precios constantes (2025)',
#                                     aggfunc='sum',
#                                     columns='Año'
#                                     )
#                             .reset_index()
#                             .assign(diff=lambda x: (x[2024] - x[2019]) / 1_000_000_000)
#                             .query("diff > 0")
#                             .rename(columns={cols_to_include[idx]:'source',
#                                             cols_to_include[idx + 1]: 'target',
#                                             'diff':'value'})
#                             ).assign(color=COLORS_LINKS[idx]))
#                     except:
#                         st.warning("Hacen falta selecciones.")
#                         st.stop()
                

        

#         prov = dfs1[-1]
#         dfs1[-1] = prov[prov['target'].isin(vals)]
#         pr1 = pd.concat(dfs1, ignore_index=True)

#         l1 = list(pr1['source'].unique())
#         l2 = list(pr1['target'].unique())
#         lt = list(set(l1 + l2))
        

#         nodes1 = (pd.DataFrame({'names': nodes1,
#                               'pos': pos1})
#                               .query("names in @lt")
#                               .reset_index(drop=True)
#                               .reset_index()
#                               .rename(columns={'index':'id'}))
        
#         dic_lts = dict(nodes1[[ 'names', 'id']].values)

#         nodes1['x_pos'] = (nodes1['pos'] - nodes1['pos'].min()) / (nodes1['pos'].max() - nodes1['pos'].min()) + 0.02
#         nodes1['x_pos'] = [0.96 if v >=1 else v for v in nodes1['x_pos']]
#         nodes1['color'] = nodes1['pos'].map(COLORS_NODES)
        
       
#         pr1['source'] = pr1['source'].map(dic_lts)
#         pr1['target'] = pr1['target'].map(dic_lts)

        
        
#         fig = go.Figure(data=[go.Sankey(
#         arrangement='snap',
#         node = dict(
#             pad = 15,
#             thickness = 20,
#             line = dict(color = "#2635bf", width = 0.5),
#             label = nodes1['names'],
#             color = nodes1['color'],
#             x = nodes1['x_pos'].values ,
#             y = nodes1['x_pos'].values / 2.4
#         ),
#         link = dict(
#             source = pr1['source'], 
#             target = pr1['target'],
#             value = pr1['value'],
#             color = pr1['color'],
#             hovertemplate='Volumen del gasto de %{source.label}<br />'+
#         'hacia %{target.label}:<br /> <b>%{value:.2f}<extra></extra>'
#         ))])

#         fig.update_layout(title_text="Flujo de gasto - Cifras en miles de millones de pesos", 
#                           font_size=10, 
#                           width=1000, 
#                           height=600)
#         st.plotly_chart(fig)    
    
    
# with tab3:
#     df2 = pd.read_csv('dataset_192425.csv')
#     year = st.selectbox("Seleccione el año", df2['Año'].unique())
#     df2 = df2[df2['Año'].isin([year])]
#     df2['PGN'] = 'PGN'
#     st.write("Seleccione el nivel de profundidad a analizar: ")
#     col1, col2, col3, col4 = st.columns(4)
#     col5, col6, col7 = st.columns(3)
    
#     with col1:
#         pgn = st.checkbox("PGN")
#         cuenta = st.checkbox("Cuenta")
        
#     with col2:
#         sector = st.checkbox("Sector")
#         subcuenta = st.checkbox("Subcuenta")
        
#     with col3:
#         entidad = st.checkbox("Entidad")
#         objeto = st.checkbox("Objeto")
        
#     with col4:
#         tipo_gasto = st.checkbox("Tipo de gasto")
#         ordinal = st.checkbox("Ordinal") 
        
         
#     dic_cols = {'PGN': pgn, 
#                 'Sector': sector,
#                 'Entidad': entidad,
#                 'Tipo de gasto': tipo_gasto,
#                 'Cuenta': cuenta,
#                 'Subcuenta': subcuenta,
#                 'Objeto/proyecto': objeto, 
#                 'Subproyecto': ordinal}
#     if (dic_cols['PGN'] and dic_cols['Sector']) or (dic_cols['PGN'] and dic_cols['Entidad']) or (dic_cols['Entidad'] and dic_cols['Sector']):
#         st.error("Demasiada información para mostrar. Evite combinaciones entre sector, pgn y entidad.")
#         st.stop()
#     if not dic_cols['Tipo de gasto']:
#         st.error("Debe seleccionar Tipo de gasto")
#         st.stop()
#     cols_to_include = pd.Series(dic_cols)
#     cols_to_include = cols_to_include[cols_to_include == True].index
#     if len(cols_to_include) > 6:
#         st.warning("El número de columnas no puede ser mayor a 6.")
#         st.stop()
#     if len(cols_to_include) >= 2: 
#         cols = st.columns(len(cols_to_include))
#         filters = {}
#         df3 = df2.copy()
#         dfs = []
#         nodes = []
#         pos = []
#         for idx, col in enumerate(cols):
#             with col:
#                 vals = st.multiselect(f"Seleccione para la columna: {cols_to_include[idx]}",
#                                 df3[cols_to_include[idx]].unique())
                
#                 filters[cols_to_include[idx]] = vals
#                 for value in df3[cols_to_include[idx]].unique():
#                     nodes.append(value)
#                     pos.append(idx)
#                 df3 = df3[df3[cols_to_include[idx]].isin(vals)]
#                 if idx != len(cols_to_include) - 1:
#                     dfs.append((df3
#                         .groupby([cols_to_include[idx], 
#                                 cols_to_include[idx + 1]])['Apropiación en precios constantes (2025)']
#                         .sum()
#                         .reset_index()
#                         .rename(columns={cols_to_include[idx]:'source',
#                                          cols_to_include[idx + 1]: 'target',
#                                          'Apropiación en precios constantes (2025)':'value'})
#                         ).assign(value= lambda x: x['value'] / 1_000_000_000).assign(color=COLORS_LINKS[idx]))
                
    
        

#         prov = dfs[-1]
#         dfs[-1] = prov[prov['target'].isin(vals)]
#         pr = pd.concat(dfs, ignore_index=True)

#         l1 = list(pr['source'].unique())
#         l2 = list(pr['target'].unique())
#         lt = list(set(l1 + l2))

#         nodes = (pd.DataFrame({'names': nodes,
#                               'pos': pos})
#                               .query("names in @lt")
#                               .reset_index(drop=True)
#                               .reset_index()
#                               .rename(columns={'index':'id'}))
#         dic_lts = dict(nodes[[ 'names', 'id']].values)


#         nodes['x_pos'] = (nodes['pos'] - nodes['pos'].min()) / (nodes['pos'].max() - nodes['pos'].min()) + 0.02
#         nodes['x_pos'] = [0.96 if v >=1 else v for v in nodes['x_pos']]
#         nodes['color'] = nodes['pos'].map(COLORS_NODES)
       
#         pr['source'] = pr['source'].map(dic_lts)
#         pr['target'] = pr['target'].map(dic_lts)

        
#         fig = go.Figure(data=[go.Sankey(
#         arrangement='snap',
#         node = dict(
#             pad = 15,
#             thickness = 20,
#             line = dict(color = "#2635bf", width = 0.5),
#             label = nodes['names'],
#             color = nodes['color'],
#             x = nodes['x_pos'].values ,
#             y = nodes['x_pos'].values / 2.4
#         ),
#         link = dict(
#             source = pr['source'], 
#             target = pr['target'],
#             value = pr['value'],
#             color = pr['color'],
#             hovertemplate='Volumen del gasto de %{source.label}<br />'+
#         'hacia %{target.label}:<br /> <b>%{value:.2f}<extra></extra>'
#         ))])

#         fig.update_layout(title_text="Flujo de gasto - cifras en miles de millones de pesos", 
#                           font_size=10, 
#                           width=1000, 
#                           height=600)
#         st.plotly_chart(fig)

# with tab4:
#     st.header("Diff 2019 - 2014 (ordenado)")
#     st.divider()
#     sel = st.selectbox("Seleccione un nivel de desagregación",
#                  ["Entidad","Cuenta", 'Subcuenta', 'Objeto', 'Ordinal'])
#     dic_deep = {'Entidad':['Entidad'],
#                 'Cuenta': ['Entidad','Cuenta'],
#                 'Subcuenta': ['Entidad','Cuenta', 'Subcuenta'],
#                 'Objeto': ['Entidad','Cuenta', 'Subcuenta', 'Objeto'],
#                 'Ordinal': ['Entidad','Cuenta', 'Subcuenta', 'Objeto', 'Ordinal']}
#     df = pd.read_csv("data192425_hom.csv")
#     col1, col2 = st.columns(2)
#     with col1:
#         y1 = st.selectbox("Seleccione un año a comparar: ", [2019, 2024])
#     with col2:
#         y2 = st.selectbox("Seleccione contra qué año comparar: ", [2024, 2025])


#     df_func = df[df['Año'].isin([y1, y2])]
#     piv = (df_func.pivot_table(index=dic_deep[sel],
#                     columns=['Año'],
#                     values='TOTAL_const',
#                     aggfunc='sum')
#                     .div(1_000_000)
#                     .round(0)
#                     .assign(diff=lambda x: x[y2] - x[y1])
#                     .sort_values(by='diff', ascending=False)
#                     .reset_index())
#     st.subheader(f"Diferencia entre {y2} y {y1} - Cifras en millones de pesos")
#     st.dataframe(piv)


with tab2:
    data = pd.read_csv('data192425_hom.csv')

    def rename_ord(row):
        entidad = row['Entidad']
        cuenta = row['Cuenta']
        subcuenta = row['Subcuenta']
        objeto = row['Objeto']
        ordinal = row['Ordinal']
        l_objetos = ['PRESTACIONES SOCIALES RELACIONADAS CON EL EMPLEO', 
                    'PRESTACIONES SOCIALES ASUMIDAS POR EL GOBIERNO',
                    'PRESTACIONES DE ASISTENCIA SOCIAL']
        l_ordinal = ['ASEGURAMIENTO, RECLAMACIONES Y SERVICIOS INTEGRALES EN SALUD, (LEY 100 DE 1993 y DECRETO 780 DE 2016)',
                    'APOYO A PROGRAMAS DE DESARROLLO DE LA SALUD LEY 100 DE 1993']
        if entidad == 'Ministerio de hacienda y crédito público' and ordinal == 'OTRAS TRANSFERENCIAS - DISTRIBUCIÓN PREVIO CONCEPTO DGPPN':
            return 'FEPC'
        elif objeto in l_objetos:
            return "PRESTACIONES SOCIALES"
        elif objeto == 'SISTEMA GENERAL DE PARTICIPACIONES':
            return 'SISTEMA GENERAL DE PARTICIPACIONES'
        elif ordinal in l_ordinal:
            return 'Salud'
        else:
            return 'Otros (objeto)'

    def rename_cuenta(row):
        cuenta = row['Cuenta']

        if cuenta == 'TRANSFERENCIAS CORRIENTES':
            return 'TRANSFERENCIAS CORRIENTES'
        elif cuenta == 'GASTOS DE PERSONAL':
            return 'GASTOS DE PERSONAL'
        else:
            return 'Otros (cuenta)' 
    data['Cuenta_alt'] = data.apply(rename_cuenta, axis=1)
    data['Ord_alt'] = data.apply(rename_ord, axis=1)

    piv = (data
    .pivot_table(index=['Cuenta_alt', 'Ord_alt'],
                    columns='Año',
                    values='TOTAL_const',
                    aggfunc='sum')
                    .assign(diff_19_24=lambda x: x[2024] - x[2019],
                            diff_19_25=lambda x: x[2025] - x[2019],
                            diff_24_25=lambda x: x[2025] - x[2024])
                        .sort_values(by='diff_19_24', ascending=False).reset_index())

    piv = piv[['Cuenta_alt', 'Ord_alt', 'diff_19_24']]
    cop = piv.copy()
    st.dataframe(piv)

    labels = piv['Cuenta_alt'].unique().tolist() + piv['Ord_alt'].unique().tolist()
    dic_labels = dict(enumerate(labels))
    rev_labels = {}

    for key, value in dic_labels.items():
        rev_labels[value] = key


    piv['source'] = piv['Cuenta_alt'].map(rev_labels)
    piv['target'] = piv['Ord_alt'].map(rev_labels)
    piv['values'] = (piv['diff_19_24'] / 1_000_000_000).round(2)

    piv = piv.drop(columns=['Cuenta_alt', 'Ord_alt', 'diff_19_24'])

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = list(rev_labels.keys()),
        color = ["#2F399B"] * 3 +  ["#F7B261"] * 7
        ),
        link = dict(
        source = piv['source'], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = piv['target'],
        value = piv['values'],
        color = "#D9D9ED"
    ))])

    fig.update_layout(title_text="Flujo de gasto - diff (2019 - 2024) - Cifras en miles de millones de pesos", font_size=10)

    pie_chart = cop.groupby('Cuenta_alt')['diff_19_24'].sum() / 1_000_000_000
    pie_chart = pie_chart.reset_index() 
    fig2 = px.pie(pie_chart, 
                  values='diff_19_24', 
                  names='Cuenta_alt', 
                  color_discrete_sequence=["#2F399B", "#F7B261", "#0FB7B3"],
                  title="Proporción del cambio en el gasto de funcionamiento (cifras en miles de millones de pesos)")
    
    tabla = (data.pivot_table(index='Cuenta',
                 columns='Año',
                 values='TOTAL_const',
                 aggfunc='sum')
                 .assign(diff_19_24=lambda x: x[2024] - x[2019])
                 .drop(columns=[2019, 2024, 2025]).sort_values(by='diff_19_24') / 1_000_000_000).round(2)

    tabla = tabla.reset_index()

    colors = ["#2F399B"  if val >= 0 else "#F7B261" for val in tabla['diff_19_24']]

    # Create the horizontal bar chart
    fig3 = go.Figure(go.Bar(
        x=tabla['diff_19_24'],
        y=tabla['Cuenta'],
        orientation='h',
        marker=dict(color=colors)
    ))

    # Update layout for better appearance
    fig3.update_layout(
        title='Horizontal Bar Chart',
        xaxis=dict(title='diff_19_24'),
        yaxis=dict(title='Cuenta')
    )

    # Show the plot
    fig.show()
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig)     

        
    

    


    
    



