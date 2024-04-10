#!/usr/bin/env python3

from setuptools import setup, find_packages
from spm_release_tracker.version import __version__

setup(
    name="spm_release_tracker",
    version=__version__,
    packages=find_packages(),
    install_requires=["requests", "rich", "argparse", "requests_cache", "pytz"],
    entry_points={"console_scripts": ["spm-updates=spm_release_tracker:main"]},
)
