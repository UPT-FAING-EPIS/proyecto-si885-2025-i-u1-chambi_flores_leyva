from github import Github
import pandas as pd
import os

# -----------------------
# CONFIGURACIÓN
# -----------------------


GITHUB_TOKEN = ''

# Organización que quieres analizar
ORG_NAME = 'UPT-FAING-EPIS'

# Carpeta de salida
OUTPUT_FOLDER = 'data'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------
# INICIO DE SESIÓN
# -----------------------

g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG_NAME)
repos = org.get_repos()

# -----------------------
# EXTRAER DATOS
# -----------------------

repos_info = []
commits_info = []

for repo in repos:
    print(f'Analizando repositorio: {repo.name}')
    
    # Datos generales del repositorio
    repo_data = {
        'name': repo.name,
        'full_name': repo.full_name,
        'description': repo.description,
        'default_branch': repo.default_branch,
        'language': repo.language,
        'created_at': repo.created_at,
        'updated_at': repo.updated_at,
        'pushed_at': repo.pushed_at,
        'forks_count': repo.forks_count,
        'stargazers_count': repo.stargazers_count,
        'watchers_count': repo.watchers_count,
        'open_issues_count': repo.open_issues_count,
        'branches_count': repo.get_branches().totalCount,
        'pull_requests_open': repo.get_pulls(state='open').totalCount,
        'pull_requests_closed': repo.get_pulls(state='closed').totalCount,
    }
    repos_info.append(repo_data)

    # Datos de commits
    try:
        commits = repo.get_commits()
        for commit in commits:
            commit_data = {
                'repo_name': repo.name,
                'commit_sha': commit.sha,
                'author': commit.author.login if commit.author else None,
                'date': commit.commit.author.date,
                'message': commit.commit.message
            }
            commits_info.append(commit_data)
    except Exception as e:
        print(f"Error en commits del repo {repo.name}: {e}")

# -----------------------
# GUARDAR CSV
# -----------------------

df_repos = pd.DataFrame(repos_info)
df_repos.to_csv(os.path.join(OUTPUT_FOLDER, 'repos_data.csv'), index=False)

df_commits = pd.DataFrame(commits_info)
df_commits.to_csv(os.path.join(OUTPUT_FOLDER, 'commits_data.csv'), index=False)

print("✅ Extracción completada. Archivos guardados en la carpeta 'data'.")

# -----------------------
# MÉTRICAS BÁSICAS
# -----------------------

metrics = {
    'total_repositorios': len(repos_info),
    'total_commits': len(commits_info),
    'promedio_commits_por_repo': len(commits_info) / len(repos_info) if repos_info else 0
}

df_metrics = pd.DataFrame([metrics])
df_metrics.to_csv(os.path.join(OUTPUT_FOLDER, 'metrics_summary.csv'), index=False)

print("✅ Métricas básicas generadas.")
