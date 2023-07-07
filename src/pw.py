from src import click, json, pyperclip, io
from src.helper import jsonFileCheck, encrypt_password, decrypt_password, gen_password, generate_xkcd_password


NAME_PROMPT = "Username/Email"
PASSWORD_PROMPT = "Password"
PASSWORDS_FILE = "passwords.json"


class SimpleAliases(click.Group):
    def command(self, *args, **kwargs):
        aliases = kwargs.pop('aliases', [])
        def decorator(f):
            cmd = click.decorators.command(*args, **kwargs)(click.pass_context(f))
            self.add_command(cmd)
            for alias in aliases:
                g = click.pass_context(f)
                g.__doc__ = '+ alias for `{}`'.format(cmd.name)
                alias_cmd = click.decorators.command(*args, **kwargs)(g)
                alias_cmd = self.add_command(alias_cmd, name=alias)
            return cmd
        return decorator


@click.group(cls=SimpleAliases)
def main():
    """
    Vaulty - CLI password manager.
    Features: Password inputs/outputs are hidden from the UI. Also supports password generator, password encryption (beta)
    """
    jsonFileCheck("bank.json")
    jsonFileCheck("passwords.json")

@main.command(name="add", aliases=["create"])
@click.option('name', '-n', '--name', '--username', '--email', default=None, help="The username/email of an account you're adding")
@click.option('-p', '--password', default=None, help="Password of the account")
def add(ctx:click.core.Context, name, password):
    """
    Add an account username + password to the vault.
    """
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not password:
        password = click.prompt(PASSWORD_PROMPT, hide_input=True, confirmation_prompt=True)    
    if get_pwd(name):
        click.echo("An account with this username/email has already exists. Try `vaulty modify` instead.")
        return
    
    add_pwd(name, password)
    click.echo(f"Added {name}.")

@main.command(name="get", aliases=["g", "copy", "password"])
@click.option('name', '-n', '--name', '--username', '--email', default=None, help="The username/email of an account")
def get(ctx:click.core.Context, name):
    """
    Get saved password in vault and copy it to your clipboard.
    """
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email. Try `vaulty add` instead.")
        return
    pwd = get_pwd(name)
    copy2clipboard(pwd)
    click.echo("Copied password to clipboard.")

@main.command(name="modify", aliases=["change", "edit"])
@click.option('name', '-n', '--name', '--username', '--email', default=None, help="The username/email of an account you're modifying")
@click.option('-p', '--password', default=None, help="Password of the account")
def modify(ctx:click.core.Context, name, password):
    """
    Change password.
    """
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not password:
        password = click.prompt("New Password", hide_input=True, confirmation_prompt=True)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email. Try `vaulty add` instead.")
        return
    change_pwd(name, password)
    click.echo(f"Modified {name}.")

@main.command(name="delete", aliases=["remove"])
@click.option('name', '-n', '--name', '--username', '--email', default=None, help="The username/email of an account you're modifying")
def delete(ctx:click.core.Context, name):
    """
    Delete an account from the vault.
    """
    if not name:
        name = click.prompt(NAME_PROMPT)
    if not get_pwd(name):
        click.echo("Couldn't find an account with that username/email, it might have been deleted.")
        return
    click.confirm(f'Are you sure you want to delete {name}', abort=True)
    delete_account(name)
    click.echo(f"Deleted {name}.")

@main.command(name="list", aliases=["accounts", "saved"])
def get_list(ctx:click.core.Context, ):
    """
    Get a list of usernames represents saved accounts.
    """
    data = get_list_acc()
    ss = io.StringIO()
    for index, value in enumerate(data):
        ss.write(str(index+1) + ". " + str(value) + "\n")
    click.echo(ss.getvalue())

@main.command(name="generate", aliases=["gen"])
@click.option('-n', '--numwords', default=5, help="Number of words to generate (default=6)")
@click.option('--min', '--min_length', 'min_length', default=3, help="Minimum length of each word (default=5)")
@click.option('--max', '--max_length', 'max_length', default=9, help="Maximum length of each word (default=9)")
@click.option('-d', '--delimiter', default=".", help="Delimiter between words (default=.)")
def get_new_password(ctx:click.core.Context, numwords:int, min_length:int, max_length:int, delimiter:str):
    """
    Generate a new xkcd password and copy it to clipboard.
    E.g: vaulty gen -n=5 --min=4 --max=8 -d=/
    """
    new_pw = generate_xkcd_password(numwords=numwords, min_word_length=min_length, max_word_length=max_length, delimiter=delimiter)
    click.echo("Copied new password to clipboard.")
    copy2clipboard(new_pw)


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
