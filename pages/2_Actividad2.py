
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Actividad 2 - Análisis Avanzado")  # Título de la página

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

# Mostrar los primeros datos para verificar la carga
st.write("### Datos Cargados:")
st.write(df.head())

# Mostrar los tipos de datos
st.write("### Tipos de Datos del DataFrame:")
st.write(df.dtypes)

# Intentar convertir columnas a numéricas si es posible
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='ignore')

# Seleccionar solo columnas numéricas
df_numeric = df.select_dtypes(include=['number'])

if df_numeric.empty:
    st.error("No hay columnas numéricas en el DataFrame para calcular la correlación.")
else:
    # Aplicar los requerimientos solicitados
    # 1. Selecciona las filas con índices 5 a 10
    filas_seleccionadas = df.iloc[5:11]  # 11 es exclusivo
    st.write("### Filas Seleccionadas (Índices 5 a 10):")
    st.dataframe(filas_seleccionadas)

    # 2. Selecciona las columnas 'Producto' y 'Precio'
    if 'Producto' in df.columns and 'Precio' in df.columns:
        df_productos_precios = filas_seleccionadas[['Producto', 'Precio']]
        st.write("### Filas Seleccionadas con 'Producto' y 'Precio':")
        st.dataframe(df_productos_precios)
    else:
        st.error("Las columnas 'Producto' o 'Precio' no existen en el DataFrame.")

    # 3. Filtra las filas donde el 'Precio' es mayor que 100
    df_filtrado_precio = df_productos_precios[df_productos_precios['Precio'] > 100]
    st.write("### Filas con 'Precio' Mayor que 100:")
    st.dataframe(df_filtrado_precio)

    # 4. Crea una nueva columna llamada 'Descuento' con un 10% del 'Precio'
    df_filtrado_precio['Descuento'] = df_filtrado_precio['Precio'] * 0.1
    st.write("### Filas con 'Descuento' Añadido:")
    st.dataframe(df_filtrado_precio)

    # 5. Elimina la columna 'Descuento' del DataFrame
    df_filtrado_precio.drop(columns=['Descuento'], inplace=True)
    st.write("### Filas Después de Eliminar la Columna 'Descuento':")
    st.dataframe(df_filtrado_precio)

    st.sidebar.header("Opciones de Análisis Avanzado")
    opcion = st.sidebar.selectbox("Selecciona una opción:", 
                                  ["Correlación", 
                                   "Distribución de Datos", 
                                   "Análisis de Componentes Principales (PCA)", 
                                   "Regresión Lineal"])

    if opcion == "Correlación":
        st.write("### Matriz de Correlación")
        corr = df_numeric.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    elif opcion == "Distribución de Datos":
        st.write("### Distribución de Datos por Columna")
        columna = st.selectbox("Selecciona la columna para visualizar su distribución:", df_numeric.columns, key='dist_col')
        fig, ax = plt.subplots()
        sns.histplot(df_numeric[columna].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    elif opcion == "Análisis de Componentes Principales (PCA)":
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        st.write("### Análisis de Componentes Principales (PCA)")

        # Preprocesamiento
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_numeric)

        # PCA
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(scaled_data)
        pca_df = pd.DataFrame(data=principal_components, columns=['Componente 1', 'Componente 2'])

        # Visualización
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='Componente 1', y='Componente 2', data=pca_df, ax=ax)
        ax.set_title('Análisis de Componentes Principales (PCA)')
        st.pyplot(fig)

    elif opcion == "Regresión Lineal":
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error, r2_score

        st.write("### Regresión Lineal")

        # Selección de variables
        columnas = df_numeric.columns.tolist()
        if len(columnas) < 2:
            st.error("Se requieren al menos dos columnas numéricas para realizar una regresión lineal.")
        else:
            variable_dependiente = st.selectbox("Selecciona la variable dependiente (Y):", columnas, key='reg_y')
            variables_independientes = st.multiselect("Selecciona las variables independientes (X):", [col for col in columnas if col != variable_dependiente], key='reg_x')

            if variables_independientes:
                X = df_numeric[variables_independientes].dropna()
                Y = df_numeric[variable_dependiente].dropna()

                # Alinear los índices
                X, Y = X.align(Y, join='inner', axis=0)

                # Dividir en entrenamiento y prueba
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

                # Modelo
                model = LinearRegression()
                model.fit(X_train, Y_train)
                Y_pred = model.predict(X_test)

                # Resultados
                st.write("#### Coeficientes de la Regresión:")
                coef_df = pd.DataFrame({
                    'Variable': variables_independientes,
                    'Coeficiente': model.coef_
                })
                st.dataframe(coef_df)

                st.write("#### Métricas del Modelo:")
                st.write(f"**Error Cuadrático Medio (MSE):** {mean_squared_error(Y_test, Y_pred):.2f}")
                st.write(f"**Coeficiente de Determinación (R²):** {r2_score(Y_test, Y_pred):.2f}")

                # Visualización de Predicciones
                fig, ax = plt.subplots()
                ax.scatter(Y_test, Y_pred)
                ax.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2)
                ax.set_xlabel('Valores Reales')
                ax.set_ylabel('Valores Predichos')
                ax.set_title('Valores Reales vs. Predichos')
                st.pyplot(fig)
            else:
                st.warning("Selecciona al menos una variable independiente para realizar la regresión.")
