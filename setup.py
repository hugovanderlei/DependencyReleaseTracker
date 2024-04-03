from setuptools import setup, find_packages
from version import __version__

setup(
    name='spm_release_tracker', 
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich',
        'argparse',
        'requests_cache'
    ],
    entry_points={
        'console_scripts': [
            'spm-updates=spm_release_tracker:main' 
        ]
    }
)
