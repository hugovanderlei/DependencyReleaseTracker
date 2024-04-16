import yaml
import os
import requests
from dependency_release_tracker.dependency_readers.base_reader import (
    DependencyReaderBase,
)
from dependency_release_tracker.models.dependency import Dependency
from bs4 import BeautifulSoup
from datetime import datetime


class FlutterDependencyReader(DependencyReaderBase):
    def __init__(self, project_path):
        super().__init__(project_path)
        self.pubspec_path = os.path.join(self.project_path, "pubspec.yaml")
        self.pubspec_lock_path = os.path.join(self.project_path, "pubspec.lock")

    def read_dependencies(self):
        """
        Read dependencies from pubspec.yaml and pubspec.lock to get current and locked versions.
        """
        dependencies = self.read_yaml_dependencies()
        lock_versions = self.read_lock_versions()
        for dep in dependencies:
            if dep.name in lock_versions:
                dep.current_version = lock_versions[dep.name]
        return dependencies

    def read_yaml_dependencies(self):
        """
        Read dependencies from pubspec.yaml to get the desired versions.
        """
        with open(self.pubspec_path, "r") as file:
            pubspec = yaml.safe_load(file)
            dependencies = pubspec.get("dependencies", {})
            dev_dependencies = pubspec.get("dev_dependencies", {})
            all_dependencies = {**dependencies, **dev_dependencies}
            return [
                Dependency(name=name, current_version=version, repo_url=None)
                for name, version in all_dependencies.items()
                if isinstance(version, str)
            ]

    def read_lock_versions(self):
        """
        Read actual installed versions from pubspec.lock.
        """
        with open(self.pubspec_lock_path, "r") as file:
            lock_data = yaml.safe_load(file)
            lock_versions = {}
            for package, details in lock_data.get("packages", {}).items():
                lock_versions[package] = details["version"]
            return lock_versions

    def fetch_changelog(self, package_name):
        """
        Fetch the changelog of the latest version of a package from its pub.dev changelog page.
        """
        url = f"https://pub.dev/packages/{package_name}/changelog"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            changelog_section = soup.find(
                "div", class_="detail-container"
            )  # Adjust class as needed based on actual page structure
            if changelog_section:
                return changelog_section.get_text(strip=True)
        return "Changelog not found."

    def fetch_latest_version(self, package_name):
        """
        Fetch the latest version of a package from pub.dev, including the publication date.
        """
        url = f"https://pub.dev/api/packages/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            package_data = response.json()
            version = package_data["latest"]["version"]
            published_at = package_data["latest"].get("published")
            if published_at:
                # Convert the ISO 8601 string to a datetime object and remove timezone information
                published_at = datetime.fromisoformat(published_at.rstrip("Z")).replace(
                    tzinfo=None
                )
            return version, published_at
        return None, None

    def check_updates(self, dependencies, all_versions=False):
        self.start_progress(total=len(dependencies))
        updated_dependencies = []
        for dependency in dependencies:
            try:
                latest_version, published_at = self.fetch_latest_version(
                    dependency.name
                )
                if latest_version and (
                    all_versions or latest_version != dependency.current_version
                ):
                    dependency.latest_version = latest_version
                    dependency.published_at = published_at
                    dependency.notes = (
                        self.fetch_changelog(dependency.name)
                        if latest_version != dependency.current_version
                        else dependency.notes
                    )
                    updated_dependencies.append(dependency)
            except requests.RequestException as e:
                dependency.notes = f"Error checking updates: {e}"
            finally:
                self.update_progress()  # Ensure progress is updated regardless of success or error

        self.complete_progress()  # Ensure the progress is completed after all dependencies are processed
        return updated_dependencies
