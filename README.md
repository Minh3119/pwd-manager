# pwd-manager

A simple CLI password manager.
*All data are stored locally on your machine.*


Installation
---
Project is still in development so here's how to setup things for the script to work

1. Clone the repo

2. Init python-venv for this repo
    - *(If not installed venv)*  run `sudo apt install python-venv`
    - run `python -m venv myenv`  *(myenv or whatever you like)*


3. Activate venv :
    - `source myenv/bin/activate` (for linux)
    - `myenv\Scripts\activate` (for Windows)


4. `pip install -r requirements.txt`

5. `pip install --editable .`

6. Installation should be done. Try `vaulty --help`. 

    Note: all commands and developments should be done in venv.

7. After messing around with the project, exit venv: type `deactivate`