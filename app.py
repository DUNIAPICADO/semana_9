# -*- coding: utf-8 -*-
import streamlit as st
st.title('Hola, Streamlit!')
import plotly.express as px 
import pandas as pd
import sqlite3
import numpy as np
import os

st.title("Título")
st.header("Título 2")
st.write("Hola, este es un párrafo de prueba")
st.markdown('''
### Ejemplo Markdown 
Este texto es un ejemplo de markdown. 
:rocket:
''')
df = px.data.tips()
# st.dataframe(df) 
datos = df.rename(columns={
    'total_bill' : 'cuenta_total',
    'tip' : 'propina',
    'sex' : 'genero',
    'smoker' : 'fumador', 
    'day' : 'dia',
    'time' : 'hora',
    'size' : 'tamano_mesa'
    
})
# st.dataframe(datos)
st.sidebar.header('Título sidebar')
rango_cuenta = st.sidebar.slider(
    'Rango de cuenta',
    min_value=float(datos['cuenta_total'].min()),
    max_value=float(datos['cuenta_total'].max()),
    value=(float(datos['cuenta_total'].min()), float(datos['cuenta_total'].max()))
)
personas = st.sidebar.slider(
    '# Personas en la mesa',
    min_value=int(datos['tamano_mesa'].min()),
    max_value=int(datos['tamano_mesa'].max()),
    value=(int(datos['tamano_mesa'].min()), int(datos['tamano_mesa'].max()))
)
hora_seleccionada = st.sidebar.radio(
    'Hora del día', 
    options=['Todos', 'Lunch', 'Dinner']
)
mask = (
    (datos['cuenta_total'] >= rango_cuenta[0]) &
    (datos['cuenta_total'] <= rango_cuenta[1]) &
    (datos['tamano_mesa'] >= personas[0]) &
    (datos['tamano_mesa'] <= personas[1])
)
if hora_seleccionada != 'Todos':
    mask = mask & (datos['hora'] == hora_seleccionada)\
        
datos_filtrados = datos[mask]
st.subheader('Métricas de interés')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
    label = 'Total de registros',
    value = len(datos_filtrados),
    delta = f"{len(datos_filtrados) - len(datos)} vs total"   
    )
with col2: 
    st.metric(
        label= 'Promedio de propinas',
        value=f"${datos_filtrados['propina'].mean():.2f}"
    )
    
with col3: 
    st.metric(
        label= 'Promedio de cuentas',
        value=f"${datos_filtrados['cuenta_total'].mean():.2f}"
    )
st.subheader('Datos filtrados')
st.dataframe(datos_filtrados)
st.subheader('Relación Cuenta/Propina')
fig = px.scatter(
    datos_filtrados,
    x='cuenta_total',
    y='propina', 
    color = 'hora',
    size = 'tamano_mesa',
    hover_data=['dia', 'fumador']
)
st.plotly_chart(fig)

import streamlit as st
import plotly.express as px 
import pandas as pd 

