import requests
import csv
from datetime import datetime

# Configuración
ORG_NAME = 'UPT-FAING-EPIS'  # Nombre de la organización
TOKEN = 'TU_TOKEN_AQUI'       # Pega aquí tu token de GitHub

# Headers para autenticación
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Función para obtener repositorios
def get_repositories(org):
    url = f'https://api.github.com/orgs/{org}/repos'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Función para obtener commits de un repositorio
def get_commits_count(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/commits'
    response = requests.get(url, headers=headers, params={'per_page': 1})
    if 'Link' in response.headers:
        # Buscar en el Link header la última página
        links = response.headers['Link'].split(',')
        for link in links:
            if 'rel="last"' in link:
                last_page_url = link.split(';')[0].strip('<> ')
                last_page = int(last_page_url.split('page=')[-1])
                return last_page
    return len(response.json())

# Función para obtener número de archivos
def get_files_count(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/contents'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        return len(files)
    return 0

# Función para obtener fechas de commits
def get_commit_dates(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/commits'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    commits = response.json()
    dates = [commit['commit']['committer']['date'] for commit in commits]
    return dates

# Función principal
def scrape_organization_data(org_name):
    repos = get_repositories(org_name)
    data = []

    for repo in repos:
        full_name = repo['full_name']
        print(f'Procesando repositorio: {full_name}')
        
        commits_count = get_commits_count(full_name)
        files_count = get_files_count(full_name)
        commit_dates = get_commit_dates(full_name)

        if commit_dates:
            most_recent_commit = max(commit_dates)
            commit_day_counts = {}
            for date_str in commit_dates:
                day = date_str.split('T')[0]
                commit_day_counts[day] = commit_day_counts.get(day, 0) + 1
            most_active_day = max(commit_day_counts, key=commit_day_counts.get)
        else:
            most_recent_commit = 'N/A'
            most_active_day = 'N/A'

        data.append({
            'Repositorio': repo['name'],
            'Commits Totales': commits_count,
            'Fecha Último Commit': most_recent_commit,
            'Día Más Activo': most_active_day,
            'Cantidad de Archivos': files_count
        })

    # Guardar en CSV
    with open('repositorios_upt.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Repositorio', 'Commits Totales', 'Fecha Último Commit', 'Día Más Activo', 'Cantidad de Archivos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo_data in data:
            writer.writerow(repo_data)

    print('CSV generado: repositorios_upt.csv')

# Ejecutar
if __name__ == "__main__":
    scrape_organization_data(ORG_NAME)
