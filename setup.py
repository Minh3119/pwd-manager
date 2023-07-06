from setuptools import setup, find_packages

setup(
    name="Pwd Manager",
    version='0.0.1',
    py_modules=['src'],
    install_requires=[
        'Click',
    ],
    requires = ["setuptools"],
    entry_points={
        'console_scripts': [
            'vaulty = src.pw:main'
        ]
    },
    packages=find_packages(
        where='src',
    ),
)