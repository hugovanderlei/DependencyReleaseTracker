import os
from .dependency_manager_types import DependencyManager


class DependencyManagerDetector:
    def __init__(self, path):
        self.path = path

    def detect(self):
        """Detects the dependency manager by checking for specific files or directories."""
        # Checking for Swift Package Manager
        for root, dirs, _ in os.walk(self.path):
            if any(dir.endswith(".xcworkspace") for dir in dirs):
                xcworkspace_path = os.path.join(
                    root, [dir for dir in dirs if dir.endswith(".xcworkspace")][0]
                )
                if os.path.exists(
                    os.path.join(
                        xcworkspace_path, "xcshareddata", "swiftpm", "Package.resolved"
                    )
                ):
                    return DependencyManager.SWIFT

        # Checking for npm
        if os.path.exists(os.path.join(self.path, "package.json")):
            return DependencyManager.NPM

        # Checking for Gradle
        if os.path.exists(os.path.join(self.path, "build.gradle")) or os.path.exists(
            os.path.join(self.path, "build.gradle.kts")
        ):
            return DependencyManager.ANDROID

        return DependencyManager.UNKNOWN
