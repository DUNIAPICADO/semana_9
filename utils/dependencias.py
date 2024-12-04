import streamlit as st 
import plotly.express as px 
import pandas as pd
import sqlite3
import numpy as np
import os

def mapear_datos(nombre_bd, formato): 
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_bd}{formato}')
    return db_path

def cargar_datos(ruta_archivo):
    conn = sqlite3.connect(ruta_archivo)
    
    dataframes = {}
    
    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn)
    
    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)
    
    conn.close()   
    
    return dataframes

#Obtener la ruta del archivo SQLite
ruta = mapear_datos("Northwind_small", ".sqlite")  
# Cargar datos utilizando la ruta directamente
data = cargar_datos(ruta) 
# Ya no es necesario acceder a rutas[0]

# Acceder a las tablas específicas
ordenes = data["Order"]
cliente = data["Customer"]
categoria = data["Category"]
detalles_ordenes = data["Orderdetail"]
producto = data["Product"]
empleado = data["Employee"]
region = data["Region"]
provedor = data["Supplier"]
territorio = data["Territory"]


import pandas as pd

# Unir Order con Customer
ordenes_clientes = pd.merge(ordenes, cliente, on="CustomerID")

# Unir con Employee para obtener datos de los empleados que gestionaron las órdenes
ordenes_clientes_empleados = pd.merge(ordenes_clientes, empleado, on="EmployeeID")

# Unir con OrderDetail para obtener los detalles de las órdenes
ordenes_detalles = pd.merge(ordenes_clientes_empleados, detalles_ordenes, on="OrderID")

# Unir con Product para obtener los productos involucrados
ordenes_productos = pd.merge(ordenes_detalles, producto, on="ProductID")

# Unir con Category para clasificar los productos por categoría
ordenes_categorias = pd.merge(ordenes_productos, categoria, on="CategoryID")

# Unir con Supplier para obtener información del proveedor
ordenes_proveedores = pd.merge(ordenes_categorias, provedor, on="SupplierID")

# Mostrar las primeras filas del DataFrame final
print(ordenes_proveedores.head())