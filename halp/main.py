import os
import re
from typing import Any

import fire
from openai import AsyncOpenAI
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from halp import env, prompts

console = Console()


async def get_command_suggestion(prompt: str) -> list[str]:
    client = AsyncOpenAI(api_key=env.HALP_API_KEY, base_url=env.HALP_BASE_URL)

    full_response = ""
    with Live(console=console) as live:
        response = await client.chat.completions.create(
            model=env.HALP_MODEL,
            messages=[
                {"role": "system", "content": prompts.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        async for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                live.update(Markdown(full_response), refresh=True)

    # Use regex to extract all ```sh code blocks
    command_blocks: list[str] = re.findall(r"```sh(.*?)```", full_response, re.DOTALL)
    return [block.strip() for block in command_blocks]


async def main(*args: Any):
    """
    Get help with terminal commands.

    Halp helps you with terminal commands when you don't know the exact incantations.
    Simply type a description of what you want to do and Halp will suggest a command. e.g.

    halp how do i create a tarball out of this directory

    Results are streamed from an LLM provider. If there is a shell command within
    the response, Halp will ask if you would like to run it.

    By default, Halp will automatically use either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`, with
    OpenAI taking precedence if both are set.

    You can also manually set HALP_API_KEY, HALP_BASE_URL, and HALP_MODEL.
    """
    env.check_env()

    prompt = " ".join(str(arg) for arg in args)
    if not prompt:
        print("Please describe what you want to do.")
        return

    suggestion = await get_command_suggestion(prompt)
    if not suggestion:
        console.print("No suggestions found", style="red")
        return
    if len(suggestion) > 1:
        console.print("Multiple suggestions found", style="red")
        return

    text = Text.assemble(
        "\nRun this command? (",
        ("enter", "green"),
        "/",
        ("ctrl+c", "red"),
        ") ",
    )
    console.print(text, end="")

    try:
        confirm = input() == ""
    except KeyboardInterrupt:
        confirm = False
        print()  # Add newline after ^C

    if confirm:
        os.system(suggestion[0])
    else:
        console.print("Aborted", style="red")


def entrypoint():
    fire.Fire(main, name="halp")
