# utils/dependency_manager_types.py

from enum import Enum, auto


class DependencyManager(Enum):
    SWIFT = auto()
    ANDROID = auto()
    FLUTTER = auto()
    NPM = auto()
    UNKNOWN = auto()
