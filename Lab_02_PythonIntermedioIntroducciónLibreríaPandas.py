Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> # ==================================================
... # IMPORTAR LIBRERÍAS
... # ==================================================
...  
... import pandas as pd
... import numpy as np
...  
... # ==================================================
... # CARGA DE DATOS
... # ==================================================
...  
... ventas = pd.read_csv('/workspace/ventas.csv')
... inventarios = pd.read_csv('/workspace/inventarios.csv')
... satisfaccion = pd.read_csv('/workspace/satisfaccion.csv')
...  
... # Eliminar filas nulas
... ventas = ventas.dropna()
... inventarios = inventarios.dropna()
... satisfaccion = satisfaccion.dropna()
...  
... print("Ventas")
... print(ventas.head())
...  
... print("\nInventarios")
... print(inventarios.head())
...  
... print("\nSatisfacción")
... print(satisfaccion.head())
...  
... # ==================================================
... # EXPLORACIÓN DE DATOS (PANDAS)
... # ==================================================
...  
... # Crear columna de ingresos totales
... ventas["Total_Ventas"] = (
... ventas["Cantidad_Vendida"] *
... ventas["Precio_Unitario"]
... )
...  
... # 1. Ventas totales por producto
... ventas_producto = ventas.groupby(
... "Producto"
... )["Cantidad_Vendida"].sum()
...  
... print("\nVENTAS POR PRODUCTO")
... print(ventas_producto)
...  
... # 2. Ventas totales por tienda
... ventas_tienda = ventas.groupby(
... "ID_Tienda"
... )["Cantidad_Vendida"].sum()
...  
... print("\nVENTAS POR TIENDA")
... print(ventas_tienda)
...  
... # 3. Ingresos totales por tienda
... ingresos_tienda = ventas.groupby(
... "ID_Tienda"
... )["Total_Ventas"].sum()
...  
... print("\nINGRESOS POR TIENDA")
... print(ingresos_tienda)
...  
... # 4. Resumen estadístico
print("\nRESUMEN ESTADÍSTICO")
print(ventas.describe())
 
# Mediana
print("\nMEDIANA DE CANTIDAD VENDIDA")
print(ventas["Cantidad_Vendida"].median())
 
# 5. GroupBy por tienda
ventas_groupby = ventas.groupby(
"ID_Tienda"
).agg({
"Cantidad_Vendida": "sum",
"Total_Ventas": "sum"
})
 
print("\nGROUPBY TIENDA")
print(ventas_groupby)
 
# ==================================================
# ANÁLISIS DE INVENTARIOS
# ==================================================
 
# Ventas por tienda y producto
ventas_tp = ventas.groupby(
["ID_Tienda", "Producto"]
)["Cantidad_Vendida"].sum().reset_index()
 
# Unir inventarios con ventas
inventarios_rotacion = pd.merge(
inventarios,
ventas_tp,
on=["ID_Tienda", "Producto"],
how="left"
)
 
inventarios_rotacion["Cantidad_Vendida"] = (
inventarios_rotacion["Cantidad_Vendida"].fillna(0)
)
 
# Rotación de inventario
inventarios_rotacion["Rotacion"] = (
inventarios_rotacion["Cantidad_Vendida"] /
inventarios_rotacion["Stock_Disponible"]
)
 
print("\nROTACIÓN INVENTARIOS")
print(inventarios_rotacion)
 
# Rotación por tienda
rotacion_tienda = inventarios_rotacion.groupby(
"ID_Tienda"
).agg({
"Cantidad_Vendida": "sum",
"Stock_Disponible": "sum"
})
 
rotacion_tienda["Rotacion"] = (
rotacion_tienda["Cantidad_Vendida"] /
rotacion_tienda["Stock_Disponible"]
)
 
print("\nROTACIÓN POR TIENDA")
print(rotacion_tienda)
 
# Tiendas críticas (<10%)
tiendas_criticas = rotacion_tienda[
rotacion_tienda["Rotacion"] < 0.10
]
 
print("\nTIENDAS CON INVENTARIO CRÍTICO")
print(tiendas_criticas)
 
# ==================================================
# SATISFACCIÓN DEL CLIENTE
# ==================================================
 
# Unir ventas e información de satisfacción
analisis = pd.merge(
ingresos_tienda.reset_index(),
satisfaccion,
on="ID_Tienda"
)
 
print("\nSATISFACCIÓN Y VENTAS")
print(analisis)
 
# Filtrar satisfacción menor de 60%
baja_satisfaccion = analisis[
analisis["Satisfacción_Promedio"] < 60
]
 
print("\nTIENDAS CON SATISFACCIÓN < 60%")
print(baja_satisfaccion)
 
print("\nRECOMENDACIONES")
 
for tienda in baja_satisfaccion["ID_Tienda"]:
print(f"""
Tienda {tienda}
- Mejorar atención al cliente
- Revisar disponibilidad de productos
- Analizar reclamaciones recibidas
- Aplicar promociones y fidelización
""")
 
# ==================================================
# OPERACIONES CON NUMPY
# ==================================================
 
# Convertir a array numpy
array_ventas = ventas["Total_Ventas"].to_numpy()
 
# Mediana
mediana = np.median(array_ventas)
 
# Desviación estándar
desviacion = np.std(array_ventas)
 
print("\nMEDIANA DE LAS VENTAS")
print(mediana)
 
print("\nDESVIACIÓN ESTÁNDAR")
print(desviacion)
 
# ==================================================
# PROYECCIONES FUTURAS
# ==================================================
 
np.random.seed(42)
 
proyecciones = np.random.normal(
loc=np.mean(array_ventas),
scale=np.std(array_ventas),
size=12
)
 
print("\nPROYECCIONES FUTURAS")
print(proyecciones)
 
print("\nMEDIA PROYECTADA")
print(np.mean(proyecciones))
 
print("\nMEDIANA PROYECTADA")
print(np.median(proyecciones))
 
print("\nDESVIACIÓN PROYECTADA")
