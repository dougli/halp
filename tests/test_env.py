import importlib
import os

import pytest

from halp import env


@pytest.fixture(autouse=True)
def clean_env():
    # Store original environment
    original_env = dict(os.environ)
    # Clear relevant environment variables
    for key in [
        "HALP_API_KEY",
        "HALP_BASE_URL",
        "HALP_MODEL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
    ]:
        os.environ.pop(key, None)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
    # Reload env module to reset state
    importlib.reload(env)


def test_check_env_missing_api_key():
    importlib.reload(env)
    with pytest.raises(
        ValueError, match="No OPENAI_API_KEY, ANTHROPIC_API_KEY, or HALP_API_KEY set"
    ):
        env.check_env()


def test_check_env_missing_base_url():
    os.environ["HALP_API_KEY"] = "test_key"
    importlib.reload(env)
    with pytest.raises(ValueError, match="HALP_BASE_URL is not set"):
        env.check_env()


def test_check_env_missing_model_name():
    os.environ["HALP_API_KEY"] = "test_key"
    os.environ["HALP_BASE_URL"] = "test_url"
    importlib.reload(env)
    with pytest.raises(ValueError, match="HALP_MODEL is not set"):
        env.check_env()


def test_check_env_openai_fallback():
    os.environ["OPENAI_API_KEY"] = "test_openai_key"
    importlib.reload(env)

    env.check_env()
    assert env.HALP_API_KEY == "test_openai_key"
    assert env.HALP_BASE_URL == "https://api.openai.com/v1/"
    assert env.HALP_MODEL == "gpt-4o"


def test_check_env_anthropic_fallback():
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"
    importlib.reload(env)

    env.check_env()
    assert env.HALP_API_KEY == "test_anthropic_key"
    assert env.HALP_BASE_URL == "https://api.anthropic.com/v1/"
    assert env.HALP_MODEL == "claude-3-7-sonnet-latest"
