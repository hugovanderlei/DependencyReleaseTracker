import requests
import os
import json
from .base_reader import DependencyReaderBase
from dependency_release_tracker.models.dependency import Dependency
from dependency_release_tracker.config import GITHUB_TOKEN
from rich.console import Console


class SwiftDependencyReader(DependencyReaderBase):
    def __init__(self, project_path):
        super().__init__(project_path)
        self.console = Console()
        # Check if the GitHub token is available
        if not GITHUB_TOKEN:
            self.console.print(
                "Warning: GITHUB_TOKEN is not set. It is required for accessing private repositories or to increase API rate limits.",
                style="bold orange",
            )

    def read_dependencies(self):
        resolved_path = self.find_package_resolved()
        if not resolved_path:
            self.console.print(
                "Package.resolved file not found in any .xcworkspace directory. Please ensure you are executing the command from the root of your project.",
                style="bold red",
            )
            return []
        return self.read_package_resolved(resolved_path)

    def find_package_resolved(self):
        for root, dirs, files in os.walk(self.project_path):
            for dir_name in dirs:
                if dir_name.endswith(".xcworkspace"):
                    path = os.path.join(
                        root, dir_name, "xcshareddata", "swiftpm", "Package.resolved"
                    )
                    if os.path.exists(path):
                        return path
        return None

    def read_package_resolved(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        dependencies = []
        for package in data["pins"]:
            package_name = package["identity"]
            repo_url = package["location"]
            current_version = package["state"].get("version", "")
            dependencies.append(
                Dependency(
                    name=package_name,
                    current_version=current_version,
                    repo_url=repo_url,
                )
            )
        return dependencies

    def check_updates(self, dependencies, all_versions=False):
        self.start_progress(total=len(dependencies))
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
        }
        updated_dependencies = []

        for dependency in dependencies:
            try:
                repo_url = dependency.repo_url.rstrip(".git")
                path_parts = repo_url.split("/")
                owner_repo = "/".join(path_parts[-2:])
                api_url = f"https://api.github.com/repos/{owner_repo}/releases/latest"

                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                release_data = response.json()

                latest_version = release_data.get("tag_name", "").lstrip("v")
                if all_versions or latest_version != dependency.current_version:
                    dependency.latest_version = latest_version
                    dependency.notes = release_data.get(
                        "body", "No release notes found."
                    )
                    dependency.url = f"https://github.com/{owner_repo}/releases"
                    dependency.published_at = release_data.get("published_at")
                    updated_dependencies.append(dependency)

            except requests.RequestException as e:
                dependency.notes = f"Error checking updates: {e}"

            finally:
                self.update_progress()

        self.complete_progress()

        return updated_dependencies
