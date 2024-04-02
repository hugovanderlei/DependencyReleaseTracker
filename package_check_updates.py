import json
import requests
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

console = Console()
github_token = os.getenv('GITHUB_TOKEN')

def find_package_resolved(base_path='.'):
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.endswith('.xcworkspace'):
                resolved_path = os.path.join(root, dir_name, 'xcshareddata', 'swiftpm', 'Package.resolved')
                if os.path.exists(resolved_path):
                    return resolved_path
    return None

def read_package_resolved(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    packages = []
    for package in data['pins']:
        package_name = package['identity']
        current_version = package['state']['version']
        repo_url = package['location']
        packages.append((package_name, current_version, repo_url))
    
    return packages

def get_latest_release_info(package_name, repo_url, headers):
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    path_parts = repo_url.split('/')
    owner_repo = "/".join(path_parts[-2:])
    api_url = f"https://api.github.com/repos/{owner_repo}/releases/latest"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        release_data = response.json()
        return {
            'tag_name': release_data.get('tag_name'),
            'body': release_data.get('body', 'No release notes found.'),
            'url': f"https://github.com/{owner_repo}/releases"
        }
    except requests.RequestException as e:
        return {'tag_name': None, 'body': str(e), 'url': f"https://github.com/{owner_repo}/releases"}

def check_new_versions(packages, all_versions):
    new_versions = {}
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(), TimeRemainingColumn()) as progress:
        task = progress.add_task("[cyan]Checking versions...", total=len(packages))
        for package_name, current_version, repo_url in packages:
            release_data = get_latest_release_info(package_name, repo_url, headers)
            latest_version_raw = release_data.get('tag_name', current_version)
            latest_version = latest_version_raw.lstrip('v') if latest_version_raw else current_version.lstrip('v')
            current_version = current_version.lstrip('v')
            
            if all_versions or latest_version != current_version:
                new_versions[package_name] = {
                    'version': latest_version,
                    'notes': release_data.get('body'),
                    'url': release_data.get('url')
                }
            progress.update(task, advance=1)

    return new_versions

def main(all_versions):
    file_path = find_package_resolved()
    if not file_path:
        console.print("Package.resolved file not found in any .xcworkspace directory.", style="bold red")
        return

    packages = read_package_resolved(file_path)
    versions_info = check_new_versions(packages, all_versions)
    
    console.print("Relevant versions and their release notes:", style="bold")
    for name, info in versions_info.items():
        version = info['version']
        notes = info['notes']
        url = info['url']
        console.print(f"\n\n{name} ({version})\n\n", style="bold")
        md_text = f"Release notes:\n{notes}\n\n[{url}]({url})\n\n---"
        md = Markdown(md_text)
        console.print(md)

if __name__ == '__main__':
    import sys
    all_versions = '--all' in sys.argv[1:]
    main(all_versions)
