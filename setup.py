from setuptools import setup

setup(
    name="Pwd Manager",
    version='0.0.1',
    py_modules=['pw','src'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'vaulty = src.pw:main'
        ]
    }
)