import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

st.title("Vista de la Base de Datos")

# Verificar si hay un DataFrame cargado en el estado de la sesión
if 'uploaded_df' in st.session_state:
    df = st.session_state['uploaded_df']
    st.success("Datos cargados desde la página principal.")
else:
    ruta_csv = '../static/Base_datos.csv'

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

# Mostrar columnas del DataFrame
st.write("### Columnas en el DataFrame:")
st.write(df.columns.tolist())

st.sidebar.header("Opciones de Visualización")
opcion = st.sidebar.selectbox("Selecciona una opción:", 
                              ["Vista Completa", 
                               "Primeras 5 Filas", 
                               "Información General", 
                               "Estadísticas Descriptivas", 
                               "Valores Únicos en 'País'", 
                               "Conteo de 'Género'", 
                               "Visualización de Datos"])

if opcion == "Vista Completa":
    st.write("### Datos de la Base de Datos:")
    st.dataframe(df)

elif opcion == "Primeras 5 Filas":
    st.write("### Primeras 5 Filas del DataFrame:")
    st.dataframe(df.head())

elif opcion == "Información General":
    st.write("### Información General del DataFrame:")
    buffer = StringIO()
    df.info(buf=buffer)
    info_text = buffer.getvalue()
    st.text(info_text)

elif opcion == "Estadísticas Descriptivas":
    st.write("### Estadísticas Descriptivas de Columnas Numéricas:")
    st.dataframe(df.describe())

elif opcion == "Valores Únicos en 'País'":
    if 'País' in df.columns:
        st.write("### Valores Únicos en la Columna 'País':")
        pais_unicos = df['País'].unique()
        st.write(pais_unicos)
    else:
        st.error("La columna 'País' no existe en el DataFrame.")

elif opcion == "Conteo de 'Género'":
    if 'Género' in df.columns:
        st.write("### Conteo de Ocurrencias en la Columna 'Género':")
        genero_counts = df['Género'].value_counts()
        st.write(genero_counts)
    else:
        st.error("La columna 'Género' no existe en el DataFrame.")

elif opcion == "Visualización de Datos":
    st.write("### Visualización de Datos:")
    grafico_tipo = st.selectbox("Selecciona el tipo de gráfico:", 
                                ["Dispersión", "Histograma", "Box Plot", "Mapa de Calor"])

    # Verificar columnas numéricas
    num_columns = df.select_dtypes(include=['number']).columns

    if grafico_tipo == "Dispersión":
        if len(num_columns) < 2:
            st.error("No hay suficientes columnas numéricas para realizar un gráfico de dispersión.")
        else:
            x_axis = st.selectbox("Selecciona la columna para el eje X:", num_columns, key='scatter_x_bd')
            y_axis = st.selectbox("Selecciona la columna para el eje Y:", num_columns, key='scatter_y_bd')
            st.line_chart(df[[x_axis, y_axis]])

    elif grafico_tipo == "Histograma":
        if len(num_columns) == 0:
            st.error("No hay columnas numéricas para mostrar un histograma.")
        else:
            columna = st.selectbox("Selecciona la columna para el histograma:", num_columns, key='hist_col_bd')
            st.hist_chart(df[columna])

    elif grafico_tipo == "Box Plot":
        if len(num_columns) == 0:
            st.error("No hay columnas numéricas para mostrar un Box Plot.")
        else:
            columna = st.selectbox("Selecciona la columna para el Box Plot:", num_columns, key='box_col_bd')
            fig, ax = plt.subplots()
            sns.boxplot(y=df[columna], ax=ax)
            st.pyplot(fig)

    elif grafico_tipo == "Mapa de Calor":
        if df.corr().empty:
            st.error("No se puede generar un mapa de calor debido a la falta de datos numéricos.")
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
