import prompts
import pytest


def mock_empty_prompt(msg, prompt_text):
    print("\n" + msg)
    return ""


@pytest.fixture
def prompt_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    test_msg = "Test message."
    test_prompt = "Test: "
    result = prompts.prompt(test_msg, test_prompt)
    captured = capsys.readouterr().out
    return captured, result, test_msg, test_input


def test_prompt_show_message(prompt_setup):
    captured, _, test_msg, _ = prompt_setup
    assert test_msg in captured


def test_prompt_gets_input(prompt_setup):
    _, result, _, test_input = prompt_setup
    assert result == test_input


def test_prompt_requires_input(monkeypatch):
    input_generator = iter(["", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.prompt("Message", "Prompt: ", required=True)
    assert result == "test"


def test_prompt_requires_option(monkeypatch):
    input_generator = iter(["x", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.prompt("Message", "Prompt: ", options={"y": True, "n": False})
    assert result is True


@pytest.fixture
def prompt_password_setup(monkeypatch, capfd):
    test_msg = "Test message."
    test_password = "password"
    monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
    result = prompts.prompt_password(test_msg, "Password: ")
    out, err = capfd.readouterr()
    return out, err, result, test_msg, test_password


def test_prompt_password_show_message(prompt_password_setup):
    out, _, _, test_msg, _ = prompt_password_setup
    assert test_msg in out


def test_prompt_password_password_not_shown(prompt_password_setup):
    _, err, _, _, test_password = prompt_password_setup
    assert test_password not in err


def test_prompt_password_password_returned(prompt_password_setup):
    _, _, result, _, test_password = prompt_password_setup
    assert test_password == result


@pytest.fixture
def get_project_setup(monkeypatch, capsys):
    test_input = "test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_project("")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_project_show_message(get_project_setup):
    captured, _, _ = get_project_setup
    assert "What would you like to call your project?" in captured


def test_get_project_gets_input(get_project_setup):
    _, result, test_input = get_project_setup
    assert result == test_input


def test_get_project_gets_default(monkeypatch):
    default_value = "default"
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_project(default_value)
    assert result == default_value


def test_get_project_rejects_capitals(monkeypatch):
    input_generator = iter(["Test", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.get_project("myproject")
    assert result == "test"


def test_get_project_rejects_dashes(monkeypatch):
    input_generator = iter(["test-example", "test_example"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.get_project("myproject")
    assert result == "test_example"


@pytest.fixture
def get_repo_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_repo("")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_repo_show_message(get_repo_setup):
    captured, _, _ = get_repo_setup
    assert "What is the name of your GitHub repository?" in captured


def test_get_repo_gets_input(get_repo_setup):
    _, result, test_input = get_repo_setup
    assert result == test_input


def test_get_repo_gets_default(monkeypatch):
    default_value = "default"
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_repo(default_value)
    assert result == default_value


@pytest.fixture
def get_deployer_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_deployer()
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_deployer_show_message(get_deployer_setup):
    captured, _, _ = get_deployer_setup
    assert "You’ll want to create a non-root user" in captured


def test_get_deployer_gets_input(get_deployer_setup):
    _, result, test_input = get_deployer_setup
    assert result == test_input


def test_get_deployer_required(monkeypatch):
    input_generator = iter(["", "d"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.get_deployer()
    assert result == "d"


@pytest.fixture
def get_users_appname_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_users_appname()
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_users_appname_show_message(get_users_appname_setup):
    captured, _, _ = get_users_appname_setup
    expected = "What would you like to call the app that handles your users?"
    assert expected in captured


def test_get_users_appname_gets_input(get_users_appname_setup):
    _, result, test_input = get_users_appname_setup
    assert result == test_input


def test_get_users_appname_gets_default(monkeypatch):
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_users_appname()
    assert result == "users"


@pytest.fixture
def get_database_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_database("test")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_database_show_message(get_database_setup):
    captured, _, _ = get_database_setup
    assert "in your test environment?" in captured


def test_get_database_gets_input(get_database_setup):
    _, result, test_input = get_database_setup
    assert result == test_input


def test_get_database_required(monkeypatch):
    input_generator = iter(["", "db"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.get_database("test")
    assert result == "db"


@pytest.fixture
def get_database_user_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_database_user("test")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_database_user_show_message(get_database_user_setup):
    captured, _, _ = get_database_user_setup
    assert "for your test environment database?" in captured


def test_get_database_user_gets_input(get_database_user_setup):
    _, result, test_input = get_database_user_setup
    assert result == test_input


def test_get_database_user_required(monkeypatch):
    input_generator = iter(["", "db_user"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
    result = prompts.get_database_user("test")
    assert result == "db_user"


@pytest.fixture
def get_database_password_setup(monkeypatch, capfd):
    test_password = "password"
    monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
    result = prompts.get_database_password("test")
    out, err = capfd.readouterr()
    return out, err, result, test_password


def test_get_database_password_show_message(get_database_password_setup):
    out, _, _, _ = get_database_password_setup
    assert "for your test environment database?" in out


def test_get_database_password_password_not_shown(get_database_password_setup):
    _, err, _, test_password = get_database_password_setup
    assert test_password not in err


def test_get_database_password_gets_input(get_database_password_setup):
    _, _, result, test_input = get_database_password_setup
    assert result == test_input


def test_get_api_only_shows_message(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    prompts.get_api_only()
    captured = capsys.readouterr().out
    assert "Are you creating a standalone API?" in captured


def test_get_api_only_defaults_false(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "x")
    result = prompts.get_api_only()
    assert result is False


def test_get_api_only_takes_n(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    result = prompts.get_api_only()
    assert result is False


def test_get_api_only_takes_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "No")
    result = prompts.get_api_only()
    assert result is False


def test_get_api_only_takes_y(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    result = prompts.get_api_only()
    assert result is True


def test_get_api_only_takes_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "YeS")
    result = prompts.get_api_only()
    assert result is True


def test_underscores_for_dashes():
    actual = prompts.underscores_for_dashes("dashed-example-string")
    assert actual == "dashed_example_string"
