# inicio.py

import streamlit as st
import pandas as pd
from PIL import Image

# Configura la página
st.set_page_config(page_title="Proyecto Futurista", page_icon="🌌", layout="centered")

# Estilos en CSS para fondo e imagen
st.markdown("""
    <style>
    .futuristic-background {
        background: url('https://firebasestorage.googleapis.com/v0/b/imagenes-e192b.appspot.com/o/graficos.jpg?alt=media&token=4b691a73-9189-472d-b143-41a60440df7d') no-repeat center center fixed;
        background-size: cover;
        padding: 50px;  /* Reducido para mejor adaptabilidad */
        border-radius: 15px;
        color: white;
    }
    .title {
        font-family: 'Courier New', monospace;
        color: #00FFEF;
        text-shadow: 0px 0px 10px #00FFEF;
        text-align: center;
    }
    .description {
        font-family: 'Arial', sans-serif;
        color: #FFFFFF;
        text-align: center;
        margin-top: 20px;
    }
    .upload-section {
        text-align: center;
        margin-top: 30px;
    }
    .button-container {
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Contenedor principal con fondo futurista
with st.container():
    st.markdown('<div class="futuristic-background">', unsafe_allow_html=True)
    
    # Título con estilo moderno
    st.markdown('<h1 class="title">Bienvenido al Analizador de Datos</h1>', unsafe_allow_html=True)

    # Descripción del proyecto
    st.markdown("""
    <div class="description">
    ### Exploración y análisis de datos CSV con un toque futurista.
    - Sube un archivo CSV para comenzar a analizar.
    - Visualiza gráficos avanzados y personaliza tu análisis.
    </div>
    """, unsafe_allow_html=True)

    # Sección de carga de archivos
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Sube tu archivo CSV aquí", type=["csv"], accept_multiple_files=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón para navegar a la página de visualización si se carga un archivo
    if uploaded_file is not None:
        try:
            # Detectar el delimitador automáticamente
            import csv
            sample = uploaded_file.read(1024).decode('utf-8')
            dialect = csv.Sniffer().sniff(sample)
            uploaded_file.seek(0)  # Reiniciar el puntero del archivo

            # Leer el archivo CSV con el delimitador detectado
            df = pd.read_csv(uploaded_file, delimiter=dialect.delimiter)
            st.success("Archivo CSV cargado exitosamente!")
            
            # Guardar el DataFrame en el estado de la sesión para usarlo en otras páginas
            st.session_state['uploaded_df'] = df

            # Botón para ir a la página de visualización
            st.markdown('<div class="button-container">', unsafe_allow_html=True)
            if st.button("🔍 Ir a la Vista de Datos"):
                # Informar al usuario que debe seleccionar la página desde la barra lateral
                st.info("Por favor, selecciona '1_proyecto_integrador' en la barra lateral para ver los datos.")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Ocurrió un error al leer el archivo CSV: {e}")

    # Cierra el contenedor futurista
    st.markdown('</div>', unsafe_allow_html=True)
