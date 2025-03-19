import os
from pathlib import Path
from typing import Optional

import fire
from openai import AsyncOpenAI

client = AsyncOpenAI()


def install_shell_integration():
    """Add halp to shell rc file for easier access"""
    shell_rc = os.path.expanduser("~/.bashrc")
    if os.path.exists(os.path.expanduser("~/.zshrc")):
        shell_rc = os.path.expanduser("~/.zshrc")

    alias_line = '\nalias halp="python3 -m halp.main"'

    with open(shell_rc, "a") as f:
        f.write(alias_line)

    print(f"Added halp alias to {shell_rc}")
    print("Please restart your shell or run 'source ~/.bashrc' to use the alias")


async def get_command_suggestion(prompt: str) -> str:
    """Get command suggestion from GPT"""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a bash expert."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()


async def main(prompt: str = "", *, install: bool = False):
    """
    halp - Get help with terminal commands

    Args:
        prompt: Question about what command you want to run
        install: Add halp to your shell configuration
    """
    if install:
        install_shell_integration()
        return

    if not prompt:
        print("Please provide a prompt describing the command you need")
        return

    suggestion = get_command_suggestion(prompt)
    print(suggestion)


if __name__ == "__main__":
    fire.Fire(main)
