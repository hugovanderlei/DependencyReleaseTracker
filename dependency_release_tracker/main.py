import argparse
import sys
from rich.console import Console
import os
from dependency_release_tracker.utils.dependency_manager_detector import (
    DependencyManagerDetector,
)
from .version import __version__
from dependency_release_tracker.dependency_readers.swift_reader import (
    SwiftDependencyReader,
)
from dependency_release_tracker.utils.dependency_manager_types import DependencyManager
import requests_cache

console = Console()

cache_dir = os.path.join(
    os.path.expanduser("~"), ".cache", "dependency_release_tracker_cache"
)
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

cache_path = os.path.join(cache_dir, "dependency_release_tracker_cache")
requests_cache.install_cache(cache_path, expire_after=1800)


def main():
    parser = argparse.ArgumentParser(
        description="Check for package updates across various package managers."
    )
    parser.add_argument(
        "--all", action="store_true", help="Show release notes for all versions."
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Display a simplified list without release notes.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--path", type=str, default=".", help="Path to the project directory"
    )
    args = parser.parse_args()

    try:
        detector = DependencyManagerDetector(args.path)
        manager_type = detector.detect()

        if manager_type == DependencyManager.SWIFT:
            reader = SwiftDependencyReader(args.path)
        else:
            console.print(
                "Supported dependency manager not found in the specified directory.",
                style="bold red",
            )
            sys.exit(1)

        reader.process(all_versions=args.all, simple_output=args.simple)

    except KeyboardInterrupt:
        console.print("\nOperation cancelled by the user.\n", style="bold yellow")
        sys.exit(1)


if __name__ == "__main__":
    main()
