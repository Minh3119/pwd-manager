from setuptools import setup, find_packages

setup(
    name="Pwd Manager",
    version='0.0.1',
    py_modules=['src.pw','src.helper'],
    install_requires=[
        'Click',
    ],
    packages=find_packages(
        where='src',
    ),
    requires = ["setuptools"],
    entry_points={
        'console_scripts': [
            'vaulty = src.pw:main'
        ]
    },
    
)