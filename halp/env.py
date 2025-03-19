import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

HALP_API_KEY = os.environ.get("HALP_API_KEY")
HALP_BASE_URL = os.environ.get("HALP_BASE_URL")
HALP_MODEL = os.environ.get("HALP_MODEL")

if HALP_BASE_URL is None:
    if OPENAI_API_KEY:
        HALP_API_KEY = OPENAI_API_KEY
        HALP_BASE_URL = "https://api.openai.com/v1/"
        HALP_MODEL = "gpt-4o" if HALP_MODEL is None else HALP_MODEL
    elif ANTHROPIC_API_KEY:
        HALP_API_KEY = ANTHROPIC_API_KEY
        HALP_BASE_URL = "https://api.anthropic.com/v1/"
        HALP_MODEL = "claude-3-7-sonnet-latest" if HALP_MODEL is None else HALP_MODEL


def check_env():
    if HALP_API_KEY is None:
        raise ValueError("No OPENAI_API_KEY, ANTHROPIC_API_KEY, or HALP_API_KEY set")
    if HALP_BASE_URL is None:
        raise ValueError("HALP_BASE_URL is not set")
    if HALP_MODEL is None:
        raise ValueError("HALP_MODEL is not set")
