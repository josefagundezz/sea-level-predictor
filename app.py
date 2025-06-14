# app.py (Versión 2.0 - Bilingüe)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import date

# --- 1. DICCIONARIO DE TEXTOS (ESPAÑOL E INGLÉS) ---
TEXTS = {
    'es': {
        'page_title': "Predicción del Nivel del Mar", 'page_icon': "🌊",
        'title': "Simulador de Aumento del Nivel del Mar 🌊",
        'description': """
            Esta herramienta visualiza datos históricos del aumento del nivel del mar y proyecta las tendencias a futuro.
            Se muestran dos modelos:
            1.  **Tendencia a Largo Plazo:** Basada en datos desde 1880.
            2.  **Tendencia Acelerada:** Basada en datos más recientes (desde el año 2000), que reflejan un ritmo de aumento más rápido.
            """,
        'subheader_viz': "Visualización Histórica y Proyecciones",
        'plot_title': "Aumento del Nivel del Mar: Comparación de Tendencias",
        'plot_xlabel': "Año", 'plot_ylabel': "Nivel del Mar Ajustado (en pulgadas)",
        'legend_hist': "Datos Históricos", 'legend_full': "Predicción (Tendencia 1880-2014)",
        'legend_recent': "Predicción (Tendencia Acelerada 2000-2014)",
        'subheader_sim': "Viaja al Futuro: Simulador Interactivo",
        'slider_label': "Selecciona un año futuro para ver la predicción:",
        'prediction_header': "Predicciones para el año",
        'metric1_label': "Predicción (Tendencia Histórica)",
        'metric2_label': "Predicción (Tendencia Acelerada)",
        'unit_inches': "pulgadas",
        'metric_delta_text': "más alto",
        'analysis_warning': "**Análisis:** Basado en la tendencia de las últimas décadas, el nivel del mar en"
    },
    'en': {
        'page_title': "Sea Level Predictor", 'page_icon': "🌊",
        'title': "Sea Level Rise Simulator 🌊",
        'description': """
            This tool visualizes historical sea level rise data and projects future trends.
            Two prediction models are shown:
            1.  **Long-Term Trend:** Based on all data since 1880.
            2.  **Accelerated Trend:** Based on more recent data (since the year 2000), reflecting a faster rate of increase.
            """,
        'subheader_viz': "Historical Visualization and Projections",
        'plot_title': "Sea Level Rise: Comparing Trends",
        'plot_xlabel': "Year", 'plot_ylabel': "CSIRO Adjusted Sea Level (inches)",
        'legend_hist': "Historical Data", 'legend_full': "Prediction (1880-2014 Trend)",
        'legend_recent': "Prediction (Accelerated 2000-2014 Trend)",
        'subheader_sim': "Travel to the Future: Interactive Simulator",
        'slider_label': "Select a future year to see the prediction:",
        'prediction_header': "Predictions for the year",
        'metric1_label': "Prediction (Historical Trend)",
        'metric2_label': "Prediction (Accelerated Trend)",
        'unit_inches': "inches",
        'metric_delta_text': "higher",
        'analysis_warning': "**Analysis:** Based on the trend of recent decades, the sea level in"
    }
}

# --- LÓGICA DE LA APP ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
def toggle_language():
    st.session_state.lang = 'es' if st.session_state.lang == 'en' else 'en'

# La llamada a st.set_page_config() debe ocurrir antes de que se use st.session_state para obtener los textos
st.set_page_config(
    page_title=TEXTS[st.session_state.get('lang', 'en')]['page_title'],
    page_icon=TEXTS[st.session_state.get('lang', 'en')]['page_icon'],
    layout="wide"
)
texts = TEXTS[st.session_state.lang]

@st.cache_data
def load_and_process_data():
    url = 'https://raw.githubusercontent.com/freeCodeCamp/boilerplate-sea-level-predictor/master/epa-sea-level.csv'
    df = pd.read_csv(url)
    res_full = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    return df, res_full, res_recent

df_sea, model_full, model_recent = load_and_process_data()

# --- INTERFAZ ---
st.button('Español / English', on_click=toggle_language)
st.title(texts['title'])
st.markdown(texts['description'])

st.subheader(texts['subheader_viz'])
years_full_extended = pd.Series(range(1880, 2101))
line_full = model_full.intercept + model_full.slope * years_full_extended
years_recent_extended = pd.Series(range(2000, 2101))
line_recent = model_recent.intercept + model_recent.slope * years_recent_extended

fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(df_sea['Year'], df_sea['CSIRO Adjusted Sea Level'], label=texts['legend_hist'], alpha=0.7)
ax.plot(years_full_extended, line_full, 'r', label=texts['legend_full'], linestyle='--')
ax.plot(years_recent_extended, line_recent, 'orange', label=texts['legend_recent'], linewidth=3)
ax.set_title(texts['plot_title'], fontsize=18)
ax.set_xlabel(texts['plot_xlabel'], fontsize=14)
ax.set_ylabel(texts['plot_ylabel'], fontsize=14)
ax.legend(fontsize=12)
ax.grid(True)
st.pyplot(fig)

st.subheader(texts['subheader_sim'])
future_year = st.slider(
    texts['slider_label'],
    min_value=date.today().year, max_value=2100, value=2050, step=1
)
prediction_full = model_full.intercept + model_full.slope * future_year
prediction_recent = model_recent.intercept + model_recent.slope * future_year
difference = prediction_recent - prediction_full

st.write(f"#### {texts['prediction_header']} {future_year}:")
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label=texts['metric1_label'],
        value=f"{prediction_full:.2f} {texts['unit_inches']}"
    )
with col2:
    st.metric(
        label=texts['metric2_label'],
        value=f"{prediction_recent:.2f} {texts['unit_inches']}",
        delta=f"{difference:.2f} {texts['unit_inches']} {texts['metric_delta_text']}",
        delta_color="inverse"
    )
st.warning(f"{texts['analysis_warning']} **{future_year}** podría ser **{difference:.2f} {texts['unit_inches']} más alto** de lo que predeciría el modelo a largo plazo.")