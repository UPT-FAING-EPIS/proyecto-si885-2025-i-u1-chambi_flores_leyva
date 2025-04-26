import streamlit as st
import pandas as pd

# --- Login ---
def login():
    st.sidebar.title("Inicio de Sesión")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("Ingresar"):
        if username == "admin" and password == "admin":
            st.session_state["logged_in"] = True
        else:
            st.error("Credenciales inválidas")

# --- Dashboard Plantilla ---
def dashboard():
    st.title("📊 Dashboard de Monitoreo de Repositorios Académicos")

    # --- Cargar CSVs ---
    commits_data = pd.read_csv("commits_data.csv")
    repos_data = pd.read_csv("repos_data.csv")

    # --- Sección de Filtros ---
    st.sidebar.header("Filtros")

    # Repositorios únicos para selección
    repos_list = repos_data['name'].dropna().unique()  # 'name' de repos_data
    selected_repo = st.sidebar.selectbox("Selecciona un repositorio", repos_list)

    # Años únicos basados en commits (suponiendo que hay una columna 'commit_date')
    if 'commit_date' in commits_data.columns:
        commits_data['commit_date'] = pd.to_datetime(commits_data['commit_date'])
        years = commits_data['commit_date'].dt.year.unique()
        selected_year = st.sidebar.selectbox("Selecciona un año", sorted(years))
    else:
        selected_year = None

    # --- Filtros aplicados ---
    if selected_year:
        filtered_commits = commits_data[
            (commits_data['repo_name'] == selected_repo) &  # 'repos_name' de commits_data
            (commits_data['commit_date'].dt.year == selected_year)
        ]
    else:
        filtered_commits = commits_data[commits_data['repo_name'] == selected_repo]  # 'repos_name' de commits_data

    filtered_repo_info = repos_data[repos_data['name'] == selected_repo]  # 'name' de repos_data

    # --- Métricas principales ---
    st.subheader(f"Resumen del Repositorio: {selected_repo}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Commits", len(filtered_commits))
    col2.metric("Issues Abiertos", int(filtered_repo_info['open_issues'].values[0]) if 'open_issues' in filtered_repo_info else 0)
    col3.metric("Pull Requests", int(filtered_repo_info['pull_requests'].values[0]) if 'pull_requests' in filtered_repo_info else 0)

    # --- Tablas de datos ---
    st.subheader("Detalles de Commits")
    st.dataframe(filtered_commits)

    st.subheader("Información del Repositorio")
    st.dataframe(filtered_repo_info)

    # --- Espacios reservados para gráficos futuros ---
    st.subheader("Actividad de Commits (Gráficos pronto)")
    st.info("Aquí se graficará la actividad mensual de commits.")

    st.subheader("Lenguajes de Programación Detectados (Gráficos pronto)")
    st.info("Aquí se mostrará la distribución de lenguajes.")

    st.subheader("Documentación Detectada")
    st.info("Aquí se mostrará si hay README.md o informes .docx / .md.")

# --- Main ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login()
    else:
        dashboard()

if __name__ == "__main__":
    main()
