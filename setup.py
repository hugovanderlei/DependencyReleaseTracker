from setuptools import setup, find_packages

setup(
    name='package_check_updates', 
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'package_check_updates=package_check_updates:main' 
        ]
    }
)
