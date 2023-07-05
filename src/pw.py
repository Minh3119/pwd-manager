import click
import json
import pyperclip
import io
from src.helper import jsonFileCheck, encrypt_password, decrypt_password


NAME_PROMPT = "Username/Email"
PASSWORD_PROMPT = "Password"
PASSWORDS_FILE = "passwords.json"


@click.group()
def main():
    jsonFileCheck("", "bank.json")
    jsonFileCheck("", "passwords.json")

@main.command()
@click.option('name', '-n', '-u', '-e', '--name', '--username', '--email', default=None, help="The username/email of an account you're adding")
@click.option('-p', '--password', default=None, help="Password of the account")
def add(name, password):
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not password:
        password = click.prompt(PASSWORD_PROMPT, hide_input=True, confirmation_prompt=True)    
    if get_pwd(name):
        click.echo("An account with this username/email has already exists. Try `vaulty modify` instead.")
        return
    
    add_pwd(name, password)
    click.echo(f"Added {name}.")

@main.command()
@click.option('name', '-n', '-u', '-e', '--name', '--username', '--email', default=None, help="The username/email of an account")
def get(name):
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email. Try `vaulty add` instead.")
        return
    pwd = get_pwd(name)
    copy2clipboard(pwd)
    click.echo("Copied password to clipboard.")

@main.command()
@click.option('name', '-n', '-u', '-e', '--name', '--username', '--email', default=None, help="The username/email of an account you're modifying")
@click.option('-p', '--password', default=None, help="Password of the account")
def modify(name, password):
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not password:
        password = click.prompt("New Password", hide_input=True, confirmation_prompt=True)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email. Try `vaulty add` instead.")
        return
    change_pwd(name, password)
    click.echo(f"Modified {name}.")

@main.command()
@click.option('name', '-n', '-u', '-e', '--name', '--username', '--email', default=None, help="The username/email of an account you're modifying")
def delete(name):
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email, it might have been deleted.")
        return
    click.confirm(f'Are you sure you want to delete {name}', abort=True)
    delete_account(name)
    click.echo(f"Deleted {name}.")

@main.command(name="list")
def get_list():
    data = get_list_acc()
    ss = io.StringIO()
    for index, value in enumerate(data):
        ss.write(str(index+1) + ". " + str(value) + "\n")
    click.echo(ss.getvalue())



def copy2clipboard(text):
    pyperclip.copy(text)

def add_pwd(name, pwd):
    name = name.lower()
    with open(PASSWORDS_FILE, "r") as f:
        data = json.load(f)
    data[name] = encrypt_password(pwd)
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(data, f)

def get_pwd(name) -> str:
    name = name.lower()
    with open(PASSWORDS_FILE, "r") as f:
        data = json.load(f)
        try:
            data[name]
        except:
            result = None
        else:
            result = decrypt_password(data[name])
    return result

def change_pwd(name, new_pwd):
    name = name.lower()
    with open(PASSWORDS_FILE, "r") as f:
        data = json.load(f)
    data[name] = encrypt_password(new_pwd)
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(data, f)

def delete_account(name):
    name = name.lower()
    with open(PASSWORDS_FILE, "r") as f:
        data = json.load(f)
        data.pop(name)
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(data, f)

def get_list_acc():
    with open(PASSWORDS_FILE, "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    main()
