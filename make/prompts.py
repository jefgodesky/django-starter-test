from getpass import getpass
from inspect import cleandoc


def prompt(msg: str, prompt_text: str, required: bool = False, options: dict = None):
    print("\n" + msg)
    while True:
        value = input(prompt_text)
        if options:
            if value in options:
                return options[value]
        elif required and not value.strip():
            pass
        else:
            return value


def prompt_password(msg: str, prompt_text: str):
    print("\n" + msg)
    return getpass(prompt_text)


def get_project(default_value: str):
    msg = "What would you like to call your project?"
    prompt_text = f"Project name ({default_value}): "
    valid = False
    while not valid:
        input_value = prompt(msg, prompt_text) or default_value
        all_lower = input_value == input_value.lower()
        no_dashes = "-" not in input_value
        valid = all_lower and no_dashes
        if valid:
            return input_value


def get_repo(default_value: str):
    msg = "What is the name of your GitHub repository?"
    prompt_text = f"Repository ({default_value}): "
    return prompt(msg, prompt_text) or default_value


def get_deployer():
    msg = """You’ll want to create a non-root user on your DigitalOcean droplet
      who has all the permissions it needs to deploy your Docker containers.
      This should be an account separate from any human user, one dedicated entirely
      to automated, continuous delivery. What is this user’s user name?"""
    prompt_text = "Deployment username: "
    return prompt(cleandoc(msg), prompt_text, required=True)


def get_users_appname():
    msg = "What would you like to call the app that handles your users?"
    prompt_text = "Users app (users): "
    return prompt(cleandoc(msg), prompt_text) or "users"


def get_database(env: str):
    msg_before = "What is the name of the database that you would like to use in your"
    msg = f"{msg_before} {env} environment?"
    prompt_text = f"{env.capitalize()} database: "
    return prompt(cleandoc(msg), prompt_text, required=True)


def get_database_user(env: str):
    msg_before = "What is the name of the database user for your"
    msg = f"{msg_before} {env} environment database?"
    prompt_text = f"{env.capitalize()} database user: "
    return prompt(cleandoc(msg), prompt_text, required=True)


def get_database_password(env: str):
    msg_before = "What is the password for the database user for your"
    msg = f"{msg_before} {env} environment database?"
    prompt_text = f"{env.capitalize()} database user password: "
    return prompt_password(cleandoc(msg), prompt_text)


def get_api_only():
    msg = """Are you creating a standalone API? If yes, we’ll start a new API
        project. If no, we’ll start a new project that’s set up to be built
        API-first, but will also contain templates for traditional HTML
        responses using the same models."""
    prompt_text = "Standalone API? [y/N]: "
    affirmations = ["y", "yes"]
    value = prompt(cleandoc(msg), prompt_text)
    return True if value.lower() in affirmations else False


def underscores_for_dashes(dashed: str):
    return dashed.replace("-", "_")
