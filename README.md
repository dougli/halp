# halp

AI help with running terminal commands when you forget the exact incantations.

## Install

```sh
pip install halp-plz
```

Ensure you either have `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` set. Halp will use
whatever is available, with OpenAI taking precedence if both are set. Or, see
the [configuration](#configuration) section if you wish to use a more exotic LLM
provider.

## Usage

```sh
halp make a tarball out of the stuff directory
```

<img width="715" alt="Screenshot 2025-03-19 at 22 23 13" src="https://github.com/user-attachments/assets/76009b02-9a6e-447d-906d-0a150b0f27cf" />

Results will stream to the terminal. If there is a command, `halp` will ask if you'd like
to run it.

Halp concatenates all shell args together; this avoids the need to escape args with
quotes in most cases, and makes it a bit easier to use.

## Configuration

To override the default model (either `gpt-4o` or `claude-3-7-sonnet-latest`), set
`HALP_MODEL` to any other string.

If you wish to use another API entirely, set `HALP_API_KEY`, `HALP_BASE_URL`, and `HALP_MODEL`.

## Disclaimer

LLMs can make mistakes. Verify commands before executing.
