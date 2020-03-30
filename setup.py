from setuptools import setup

setup(
    name='raa',
    packages=['raa'],
    include_package_data=True,
    install_requires=[
    'flask',
    'flask_sqlalchemy',
    'sqlalchemy-json-querybuilder'
    ],
)
