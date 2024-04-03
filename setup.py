from setuptools import setup, find_packages

setup(
    name='spm_release_tracker', 
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'spm-updates=spm_release_tracker:main' 
        ]
    }
)
