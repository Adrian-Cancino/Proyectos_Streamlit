import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Resultados gobernador 2021')
st.write('Este dashboard tiene información sobre las casillas del INE durante'
         'las elecciones del 2021')

data_casillas_2021 = pd.read_csv('./data/casillas_limpio.csv')
votos_gob = pd.read_csv('./data/votos_gob_2021.csv')
data_casillas_2021[['Sección', 'Padrón Electoral', 'Listado Nominal', 'postal_code']] = data_casillas_2021[['Sección', 'Padrón Electoral', 'Listado Nominal', 'postal_code']].astype('object')

# FILTRADO POR DISTRITO FEDERAL
col1, col2, col3 = st.columns(3)
distritos_federales = ['Todos'] + list(data_casillas_2021['Distrito Federal'].unique())
with col1:
    distrito_federal_casilla = st.selectbox('Distrito Federal', distritos_federales)

if distrito_federal_casilla == 'Todos':
    data_filtrado_federal = data_casillas_2021
else:
    data_filtrado_federal = data_casillas_2021[data_casillas_2021['Distrito Federal'] == distrito_federal_casilla]

#FILTRADO POR DISTRITO LOCAL
distritos_locales = ['Todos'] + list(data_filtrado_federal['Distrito Local'].unique())
with col2:
    distrito_local_casilla = st.selectbox('Distrito Local', distritos_locales)

if distrito_local_casilla == 'Todos':
    data_filtrado_local = data_filtrado_federal
else:
    data_filtrado_local = data_filtrado_federal[data_filtrado_federal['Distrito Local'] == distrito_local_casilla]

# FILTRADO MUNICIPIOS
municipios = ['Todos'] + list(data_filtrado_local['Municipio'].unique())
with col3:
    municipio_casilla = st.selectbox('Municipio', municipios)

if municipio_casilla == 'Todos':
    data_filtrado_municipio = data_filtrado_local
else:
    data_filtrado_municipio = data_filtrado_local[data_filtrado_local['Municipio'] == municipio_casilla]

#st.write(data_filtrado_municipio.head())
total_padron_nominal = data_filtrado_municipio['Padrón Electoral'].astype(int).sum()
total_lista_nominal = data_filtrado_municipio['Listado Nominal'].astype(int).sum()
col1, col2 = st.columns(2)
#st.write(data_filtrado_municipio.head(1)) 
# Mostrar las métricas en cada columna
with col1:
    st.metric(label="Padrón Electoral", value=total_padron_nominal)

with col2:
    st.metric(label="Lista Nominal", value=total_lista_nominal)

# DISTRITO LOCAL - DISTRITO
distrito = data_filtrado_municipio['Distrito Local_'].unique()
#print(distrito)
distrito_votos = votos_gob[votos_gob['DISTRITO'].isin(distrito)]
todos_votos = distrito_votos['TOTAL'].sum()
votos_morena = distrito_votos['MORENA'].sum()
porcentaje = round((votos_morena * 100) / todos_votos, 2)
suma_partidos = distrito_votos[['PAN', 'PRI', 'PRD', 'PVEM', 'MORENA']].sum()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Votos Morena", value=votos_morena)
with col2:
    st.metric(label="Porcentaje", value=f"{porcentaje}%")
with col3:
    st.metric(label="Votos Totales", value=todos_votos)

fig = px.bar(
    x=suma_partidos.index,
    y=suma_partidos.values,
    labels={'x': 'Partido', 'y': 'Suma'},
    title='Suma de valores por partido'
)

st.plotly_chart(fig)