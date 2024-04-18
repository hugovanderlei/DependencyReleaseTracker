from abc import ABC, abstractmethod
from dependency_release_tracker.display.dependency_display import (
    DependencyDisplay,
)
from dependency_release_tracker.utils.progress_manager import ProgressManager


class DependencyReaderBase(ABC):
    def __init__(self, project_path):
        self.project_path = project_path
        self.dependency_display = DependencyDisplay()
        self.progress_manager = ProgressManager()

    @abstractmethod
    def read_dependencies(self):
        """
        Reads dependency information from the project's dependency management file.
        Returns a list of Dependency objects.
        """
        pass

    @abstractmethod
    def check_updates(self, dependencies, all_versions=False):
        """
        Checks for updates for the provided list of dependencies.
        Returns an updated list of Dependency objects with new version information if available.
        """
        pass

    def process(self, all_versions=False, simple_output=False):
        dependencies = self.read_dependencies()
        if dependencies:
            self.start_progress(total=len(dependencies))
            try:
                updated_dependencies = self.check_updates(
                    dependencies, all_versions=all_versions
                )
            finally:
                self.complete_progress()
            self.dependency_display.display(
                updated_dependencies, simple_output=simple_output
            )
        else:
            print("No dependencies found.")

    def start_progress(self, total):
        self.progress_manager.start_task("[cyan]Checking versions...", total)

    def update_progress(self):
        self.progress_manager.advance()

    def complete_progress(self):
        self.progress_manager.finish()
