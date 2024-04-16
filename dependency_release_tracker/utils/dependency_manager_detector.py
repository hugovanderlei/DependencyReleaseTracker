import os
from .dependency_manager_types import DependencyManager


class DependencyManagerDetector:
    def __init__(self, path):
        self.path = path

    def detect(self):
        """Detects the dependency manager by checking for specific files or directories."""
        # Checking for Swift Package Manager
        for root, dirs, files in os.walk(self.path):
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

            # Checking for Flutter
            if "pubspec.yaml" in files:
                return DependencyManager.FLUTTER

        return DependencyManager.UNKNOWN
