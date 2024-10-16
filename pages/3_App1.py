# pages/3_App1.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import StringIO

def descargar_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Codificar en base64
    href = f'<a href="data:file/csv;base64,{b64}" download="datos_procesados.csv">Descargar CSV Procesado</a>'
    return href

st.title("Análisis de Datos CSV")  # Título de la página

# Verificar si hay un DataFrame cargado en el estado de la sesión
if 'uploaded_df' in st.session_state:
    df = st.session_state['uploaded_df']
    st.success("Datos cargados desde la página principal.")
else:
    # Ruta al archivo CSV estático 
    ruta_csv = '../static/Base_datos.csv'  # Ajustada para acceder desde 'pages' a 'static'

    try:
        df = pd.read_csv(ruta_csv)
        st.warning("No se ha cargado ningún archivo desde la página principal. Se están utilizando datos estáticos.")
    except FileNotFoundError:
        st.error(f"No se encontró el archivo CSV en la ruta: {ruta_csv}")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("El archivo CSV está vacío.")
        st.stop()
    except pd.errors.ParserError:
        st.error("Error al parsear el archivo CSV. Revisa el formato del archivo.")
        st.stop()
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
        st.stop()

st.sidebar.header("Opciones de Análisis y Descarga")
opcion = st.sidebar.selectbox("Selecciona una opción:", 
                              ["Análisis Básico", 
                               "Filtrado y Descarga"])

if opcion == "Análisis Básico":
    st.write("### Primeras 5 filas del dataset:")
    st.dataframe(df.head())

    st.write("### Información general del DataFrame:")
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("### Estadísticas descriptivas de las columnas numéricas:")
    st.dataframe(df.describe())

    # Valores únicos en la columna "País"
    if 'País' in df.columns:
        st.write("### Valores únicos en la columna 'País':")
        valores_unicos_pais = df['País'].unique()
        st.write(valores_unicos_pais)
    else:
        st.warning("La columna 'País' no existe en el DataFrame.")

    # Conteo de ocurrencias en la columna "Género"
    if 'Género' in df.columns:
        st.write("### Cantidad de ocurrencias por 'Género':")
        conteo_genero = df['Género'].value_counts()
        st.bar_chart(conteo_genero)
    else:
        st.warning("La columna 'Género' no existe en el DataFrame.")

    st.write("### Visualización de Datos:")
    grafico_tipo = st.selectbox("Selecciona el tipo de gráfico:", ["Dispersión", "Histograma", "Box Plot", "Mapa de Calor"])

    if grafico_tipo == "Dispersión":
        x_axis = st.selectbox("Selecciona la columna para el eje X:", df.columns, key='scatter_x')
        y_axis = st.selectbox("Selecciona la columna para el eje Y:", df.columns, key='scatter_y')
        st.line_chart(df[[x_axis, y_axis]])

    elif grafico_tipo == "Histograma":
        columna = st.selectbox("Selecciona la columna para el histograma:", df.columns, key='hist_col')
        st.hist_chart(df[columna])

    elif grafico_tipo == "Box Plot":
        columna = st.selectbox("Selecciona la columna para el Box Plot:", df.columns, key='box_col')
        fig, ax = plt.subplots()
        sns.boxplot(y=df[columna], ax=ax)
        st.pyplot(fig)

    elif grafico_tipo == "Mapa de Calor":
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

elif opcion == "Filtrado y Descarga":
    st.write("### Filtrar datos:")
    
    # Filtros independientes
    # Filtrar por "País"
    if 'País' in df.columns:
        st.subheader("Filtrar por País")
        pais_filtrar = st.selectbox("Selecciona el País:", ["Todos"] + df['País'].unique().tolist(), key='pais_filter')
        if pais_filtrar != "Todos":
            df = df[df['País'] == pais_filtrar]

    # Filtrar por "Género"
    if 'Género' in df.columns:
        st.subheader("Filtrar por Género")
        genero_filtrar = st.selectbox("Selecciona el Género:", ["Todos"] + df['Género'].unique().tolist(), key='genero_filter')
        if genero_filtrar != "Todos":
            df = df[df['Género'] == genero_filtrar]

    # Filtrar por otra columna (ejemplo genérico)
    otras_columnas = [col for col in df.columns if col not in ['País', 'Género']]
    columna_filtrar = st.selectbox("Selecciona la columna para filtrar:", otras_columnas, key='otra_columna')
    valor_filtrar = st.text_input(f"Ingresa el valor para filtrar en '{columna_filtrar}':")

    if valor_filtrar and columna_filtrar in df.columns:
        df = df[df[columna_filtrar].astype(str).str.contains(valor_filtrar, case=False, na=False)]

    # Mostrar datos filtrados
    st.write("#### Datos filtrados:")
    st.dataframe(df)

    # Descargar CSV filtrado
    st.markdown(descargar_csv(df), unsafe_allow_html=True)
