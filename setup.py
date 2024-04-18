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
    author="Hugo Vanderlei",
    author_email="hugocvcosta@gmail.com",
    description="An advanced dependency management tool designed to streamline and simplify the update tracking process for various programming environments. This tool extends support beyond Swift to include Flutter, handling both direct and transitive dependencies efficiently. By automating the update checks and changelog retrievals, it ensures developers can easily maintain their projects with the latest library versions, enhancing project stability and feature integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hugovanderlei/DependencyReleaseTracker",
)
