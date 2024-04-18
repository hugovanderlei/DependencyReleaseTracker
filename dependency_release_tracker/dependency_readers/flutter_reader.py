import yaml
import os
import requests
from dependency_release_tracker.dependency_readers.base_reader import (
    DependencyReaderBase,
)
from dependency_release_tracker.models.dependency import Dependency
from datetime import datetime
import tarfile
from io import BytesIO
import re
from tempfile import NamedTemporaryFile
from rich.console import Console


class FlutterDependencyReader(DependencyReaderBase):
    def __init__(self, project_path):
        super().__init__(project_path)
        self.pubspec_path = os.path.join(self.project_path, "pubspec.yaml")
        self.pubspec_lock_path = os.path.join(self.project_path, "pubspec.lock")
        self.console = Console()

    def read_dependencies(self):
        """
        Read dependencies from pubspec.yaml and pubspec.lock to get current and locked versions.
        If the .lock file does not exist or an error occurs reading it, this will handle it gracefully.
        """
        dependencies = self.read_yaml_dependencies()
        lock_versions = self.read_lock_versions()

        if not lock_versions:
            self.console.print(
                "Warning: No lock versions found. This may be due to a missing or unreadable pubspec.lock file.",
                style="bold orange",
            )

            return dependencies  # Returns only the dependencies from pubspec.yaml if .lock file is missing

        for dep in dependencies:
            if dep.name in lock_versions:
                dep.current_version = lock_versions[dep.name]
            else:
                print(
                    f"Warning: {dep.name} not found in lock file. Current version may be inaccurate."
                )

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
        try:
            with open(self.pubspec_lock_path, "r") as file:
                lock_data = yaml.safe_load(file)
                lock_versions = {}
                for package, details in lock_data.get("packages", {}).items():
                    lock_versions[package] = details["version"]
                return lock_versions
        except FileNotFoundError:
            print(f"Error: The file '{self.pubspec_lock_path}' does not exist.")
            return {}

    def fetch_changelog_from_archive(self, archive_url):
        """
        Fetch the changelog of the latest version of a package by downloading and inspecting the tarball.
        """
        try:
            with NamedTemporaryFile() as temp_file:
                response = requests.get(archive_url, stream=True)
                if response.status_code == 200:
                    for chunk in response.iter_content(chunk_size=1024):
                        temp_file.write(chunk)
                    temp_file.flush()  # Ensure all data is written to the file
                    temp_file.seek(0)  # Reset file pointer to the beginning

                    with tarfile.open(fileobj=temp_file, mode="r:gz") as tar:
                        changelog_files = [
                            m for m in tar.getmembers() if "CHANGELOG" in m.name.upper()
                        ]
                        if changelog_files:
                            changelog_file = tar.extractfile(changelog_files[0])
                            changelog_content = changelog_file.read().decode("utf-8")
                            return self.parse_changelog(changelog_content)
        except Exception as e:
            print(f"Failed to process the changelog from the archive: {str(e)}")
        return "Changelog not found."

    def parse_changelog(self, content):
        """
        Extract the first version's changelog from the changelog content.
        This version handles various formats including '## X.X.X', '# X.X.X', 'vX.X.X', '[X.X.X]' directly,
        and versions enclosed in brackets like '## [X.X.X]'.
        """
        pattern = r"(^|\n)(##?\s*|v)?\s*\[?(\d+\.\d+\.\d+)\]?(.*?)(?=(\n(##?\s*|v)?\s*\[?\d+\.\d+\.\d+\]?))"
        matches = re.finditer(pattern, content, re.S)

        for match in matches:
            return match.group(0).strip()

        return "No detailed changelog available."

    def fetch_latest_version(self, package_name):
        """
        Fetch the latest version of a package from pub.dev, including the publication date,
        archive URL, and attempt to capture the repository URL from the package metadata.
        """
        url = f"https://pub.dev/api/packages/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            package_data = response.json()
            version = package_data["latest"]["version"]
            published_at = package_data["latest"].get("published")
            archive_url = package_data["latest"].get("archive_url")
            pubspec = package_data["latest"].get("pubspec", {})
            homepage_url = pubspec.get("homepage")
            repo_url = pubspec.get("repository", homepage_url if homepage_url else None)

            if published_at:
                published_at = datetime.fromisoformat(published_at.rstrip("Z")).replace(
                    tzinfo=None
                )
            return version, published_at, archive_url, repo_url
        return None, None, None, None

    def check_updates(self, dependencies, all_versions=False):
        """
        Check for updates for each dependency. Fetch the latest version
        and publication date for each dependency and update the dependency object if newer versions are found.
        Display release notes for all dependencies if 'all_versions' is True, or only for those with updates if False.
        """
        self.start_progress(total=len(dependencies))
        updated_dependencies = []
        for dependency in dependencies:
            try:
                latest_version, published_at, archive_url, repo_url = (
                    self.fetch_latest_version(dependency.name)
                )
                if latest_version:
                    dependency.latest_version = latest_version
                    dependency.published_at = published_at
                    dependency.url = repo_url

                    # Always fetch release notes for the latest version
                    dependency.notes = self.fetch_changelog_from_archive(archive_url)

                    # Append to updated_dependencies if all_versions is True or there's an actual update
                    if all_versions or latest_version != dependency.current_version:
                        updated_dependencies.append(dependency)
                    else:
                        # If there's no update and all_versions is False, do not append
                        # Could set notes to a different message if needed
                        continue

            except requests.RequestException as e:
                dependency.notes = f"Error checking updates: {e}"
            finally:
                self.update_progress()  # Ensure progress is updated regardless of success or error

        self.complete_progress()  # Ensure the progress is completed after all dependencies are processed
        return updated_dependencies
