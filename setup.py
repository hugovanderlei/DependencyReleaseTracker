from setuptools import setup, find_packages
from dependency_release_tracker.version import __version__

setup(
    name="dependency_release_tracker",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
        "argparse",
        "requests_cache",
        "pytz",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": ["dependency-tracker=dependency_release_tracker.main:main"]
    },
)
