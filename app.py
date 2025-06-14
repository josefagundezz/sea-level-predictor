# app.py (Simulador del Nivel del Mar)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Predicción del Nivel del Mar",
    page_icon="🌊",
    layout="wide"
)

# --- Funciones de Cálculo (con caché para eficiencia) ---
@st.cache_data
def load_and_process_data():
    """Carga los datos y calcula las dos líneas de regresión."""
    # Cargar datos
    url = 'https://raw.githubusercontent.com/freeCodeCamp/boilerplate-sea-level-predictor/master/epa-sea-level.csv'
    df = pd.read_csv(url)

    # Modelo 1: Regresión sobre todos los datos
    res_full = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Modelo 2: Regresión sobre datos recientes (desde el año 2000)
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    return df, res_full, res_recent

# Cargamos los datos y los modelos
df_sea, model_full, model_recent = load_and_process_data()


# --- Título e Introducción ---
st.title("Simulador de Aumento del Nivel del Mar 🌊")
st.markdown("""
Esta herramienta visualiza los datos históricos del aumento del nivel del mar desde 1880 y proyecta las tendencias a futuro.
Se muestran dos modelos de predicción:
1.  **Tendencia a Largo Plazo:** Basada en todos los datos desde 1880.
2.  **Tendencia Acelerada:** Basada en los datos más recientes (desde el año 2000), que reflejan un ritmo de aumento más rápido.
""")


# --- Gráfico Principal ---
st.subheader("Visualización Histórica y Proyecciones")

# Creamos los rangos de años para las líneas de predicción
years_full_extended = pd.Series(range(1880, 2101))
line_full = model_full.intercept + model_full.slope * years_full_extended

years_recent_extended = pd.Series(range(2000, 2101))
line_recent = model_recent.intercept + model_recent.slope * years_recent_extended

# Creamos la figura
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(df_sea['Year'], df_sea['CSIRO Adjusted Sea Level'], label='Datos Históricos', alpha=0.7)
ax.plot(years_full_extended, line_full, 'r', label='Predicción (Tendencia 1880-2014)', linestyle='--')
ax.plot(years_recent_extended, line_recent, 'orange', label='Predicción (Tendencia Acelerada 2000-2014)', linewidth=3)
ax.set_title('Aumento del Nivel del Mar: Comparación de Tendencias', fontsize=18)
ax.set_xlabel('Año', fontsize=14)
ax.set_ylabel('Nivel del Mar Ajustado (en pulgadas)', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True)

st.pyplot(fig)


# --- Simulador Interactivo ---
st.subheader("Viaja al Futuro: Simulador Interactivo")

# Slider para que el usuario elija un año
future_year = st.slider(
    'Selecciona un año futuro para ver la predicción:',
    min_value=date.today().year,
    max_value=2100,
    value=2050,
    step=1
)

# Calculamos las predicciones para el año seleccionado
prediction_full = model_full.intercept + model_full.slope * future_year
prediction_recent = model_recent.intercept + model_recent.slope * future_year
difference = prediction_recent - prediction_full

# Mostramos los resultados en columnas con st.metric
st.write(f"#### Predicciones para el año {future_year}:")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Predicción (Tendencia Histórica)",
        value=f"{prediction_full:.2f} pulgadas"
    )

with col2:
    st.metric(
        label="Predicción (Tendencia Acelerada Reciente)",
        value=f"{prediction_recent:.2f} pulgadas",
        delta=f"{difference:.2f} pulgadas más alto",
        delta_color="inverse" # Rojo para indicar que es un aumento
    )

st.warning(f"**Análisis:** Basado en la tendencia de las últimas décadas, el nivel del mar en **{future_year}** podría ser **{difference:.2f} pulgadas más alto** de lo que predeciría el modelo a largo plazo. Esto subraya la urgencia del problema climático.")