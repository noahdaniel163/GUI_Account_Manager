from setuptools import setup, find_packages

setup(
    name="SIMO_GUI_Enhanced",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "pyodbc",
        "requests",
        "openpyxl",
        "pydantic",
    ],
    entry_points={
        'console_scripts': [
            'simo_gui=main:main',
        ],
    },
)