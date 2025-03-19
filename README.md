# halp

AI help with running terminal commands when you forget the exact incantations.

## Install

```sh
pip install halp-plz
```

You will need an `OPENAI_API_KEY` set up for this in your `.bashrc` / `.zshrc` or
terminal environment.

## Usage

```sh
halp list me all files that end in .py that are longer than 100 lines
```

Halp will provide a description and you can choose to approve or reject the command.

## Disclaimer

LLMs can make mistakes. Verify commands before executing.
