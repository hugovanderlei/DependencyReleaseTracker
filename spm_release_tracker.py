import argparse
import json
import requests
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
import sys
from version import __version__

github_token = os.getenv('GITHUB_TOKEN')
console = Console()


def main():
    try:
        parser = argparse.ArgumentParser(
            description='Check for package updates in Swift Package Manager projects.',
            epilog='Execute the command in the root directory of your project where the .xcworkspace directory is located.'
        )        
        parser.add_argument('--all', action='store_true', help='Show release notes for all versions, regardless of whether they are newer than those in Package.resolved.')
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

        args = parser.parse_args()

        all_versions = args.all
        header_text = "All versions and their release notes:" if all_versions else "Versions different from those in your Package.resolved:"

        file_path = find_package_resolved()
        if not file_path:
            console.print("Package.resolved file not found in any .xcworkspace directory. Please ensure you are executing the command from the root of your project.", style="bold red")
            sys.exit(1)

        packages = read_package_resolved(file_path)
        versions_info = check_new_versions(packages, all_versions)
        
        console.print(f"\n{header_text}\n", style="bold")
        for name, info in versions_info.items():
            version = info['version']
            notes = info['notes']
            url = info['url']
            console.print(f"{name} ({version})", style="bold")
            console.print(Markdown(f"Release notes:\n{notes}\n\n[View on GitHub]({url})\n\n---"))

    except KeyboardInterrupt:
        console.print("\nOperation cancelled by the user.\n", style="bold yellow")
        sys.exit(1)


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
        response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json", "Authorization": f"Bearer {github_token}"})
        response.raise_for_status()
        release_data = response.json()
        return {'tag_name': release_data.get('tag_name'), 'body': release_data.get('body', 'No release notes found.'), 'url': f"https://github.com/{owner_repo}/releases"}
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
            
            if all_versions or latest_version != current_version:
                new_versions[package_name] = {
                    'version': latest_version,
                    'notes': release_data.get('body'),
                    'url': release_data.get('url')
                }
            progress.update(task, advance=1)

    return new_versions

if __name__ == '__main__':
    main()
