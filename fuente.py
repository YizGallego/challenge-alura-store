import pandas as pd
import requests
from io import StringIO
import urllib3
import matplotlib.pyplot as plt
import seaborn as sns

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL base
base_url = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/main/base-de-datos-challenge1-latam/"
urls = [f"{base_url}tienda_{i}.csv" for i in range(1, 5)]

# Descargar respuestas
responses = [requests.get(url, verify=False) for url in urls]

# Leer solo las respuestas válidas
dataframes = []

# Cargar tienda 1 desde archivo local
try:
    tienda1 = pd.read_csv("data/tienda_1.csv", encoding="utf-8", on_bad_lines='skip')
    dataframes.append(tienda1)
    print("✅ Tienda 1 cargada localmente.")
except Exception as e:
    print("❌ No se pudo cargar tienda 1 local:", e)

# Cargar tiendas 2 a 4 desde GitHub
for i, r in enumerate(responses[1:]):
    if r.status_code == 200:
        df = pd.read_csv(StringIO(r.text), encoding='utf-8', on_bad_lines='skip')
        dataframes.append(df)
    else:
        print(f"No se pudo cargar tienda_{i+2}.csv")


print("\n📊 ANÁLISIS POR TIENDA")

for i, df in enumerate(dataframes):
    print(f"\n===== 📍 Tienda {i+1} =====")

    # Ingreso total
    ingreso_total = df['Precio'].sum()
    print(f"💰 Ingreso total: ${ingreso_total:,.2f}")

    # Ventas por categoría
    print("\n📦 Ventas por categoría:")
    print(df['Categoría del Producto'].value_counts())

    # Valoración promedio
    calificacion_promedio = df['Calificación'].mean()
    print(f"\n⭐ Calificación promedio: {calificacion_promedio:.2f}")

    # Productos más y menos vendidos
    productos = df['Producto'].value_counts()
    print("\n🔥 Producto más vendido:", productos.idxmax(), "-", productos.max(), "ventas")
    print("❄️ Producto menos vendido:", productos.idxmin(), "-", productos.min(), "ventas")

    # Promedio de costo de envío
    costo_envio_promedio = df['Costo de envío'].mean()
    print(f"\n🚚 Costo promedio de envío: ${costo_envio_promedio:.2f}")


    ingresos = [df['Precio'].sum() for df in dataframes]

plt.bar([f"Tienda {i+1}" for i in range(len(dataframes))], ingresos)
plt.title(" Ingreso Total por Tienda")
plt.xlabel("Tienda")
plt.ylabel("Ingresos ($)")
plt.tight_layout()
plt.show()

# 📊 Gráficos de ventas por categoría por tienda
for i, df in enumerate(dataframes):
    categoria_counts = df['Categoría del Producto'].value_counts()

    plt.figure(figsize=(8, 4))
    categoria_counts.plot(kind='bar')
    plt.title(f"Ventas por Categoría - Tienda {i+1}")
    plt.xlabel("Categoría")
    plt.ylabel("Cantidad vendida")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # ⭐ Gráfico de calificación promedio por categoría por tienda
for i, df in enumerate(dataframes):
    promedio_categoria = df.groupby("Categoría del Producto")["Calificación"].mean()

    plt.figure(figsize=(8, 4))
    promedio_categoria.plot(kind='bar', color='orange')
    plt.title(f" Calificación Promedio por Categoría - Tienda {i+1}")
    plt.xlabel("Categoría")
    plt.ylabel("Calificación Promedio")
    plt.ylim(0, 5)  # Calificaciones entre 0 y 5
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 🗺️ Gráfico de ventas por ciudad (Lugar de Compra)
for i, df in enumerate(dataframes):
    lugares = df["Lugar de Compra"].value_counts().sort_values(ascending=False)

    plt.figure(figsize=(8, 4))
    lugares.plot(kind='bar', color='green')
    plt.title(f"Ventas por Ciudad - Tienda {i+1}")
    plt.xlabel("Lugar")
    plt.ylabel("Cantidad de Ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    
plt.savefig(f"images/categorias_tienda_{i+1}.png")

# ✅ 1. Combinar todas las tiendas en un solo DataFrame
df_total = pd.concat(dataframes, ignore_index=True)

# ✅ 2. Agrupar por lat/lon para contar cantidad de compras
ubicaciones = df_total.groupby(['lat', 'lon']).size().reset_index(name='ventas')

# ✅ 3. Crear gráfico de dispersión geográfico
plt.figure(figsize=(10, 6))
sns.scatterplot(data=ubicaciones, x='lon', y='lat', size='ventas', hue='ventas', palette='viridis', legend=False)

plt.title("🗺️ Mapa de Ventas por Ubicación")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.tight_layout()
plt.show()

