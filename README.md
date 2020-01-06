# mint_cli


## CLI

`mint` is a cli utility to `explore` executions on MINT.

### Installation

```bash
pip install mint-cli
```

### Executions

```bash
$ mint --help
Usage: mint [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  execution  Manages the executions
  setup      Manages a setup of a model.
```

The execution sub command is used to manages the executions

```bash
$ mint execution
Usage: mint execution [OPTIONS] COMMAND [ARGS]...

  Manages the executions

Options:
  --help  Show this message and exit.

Commands:
  download  Download the inputs
  search    List all the execution
  show      Show details of execution
```

## Example usage

[![asciicast](https://asciinema.org/a/VY41zVL6997RTNRwp3OjpxF2p.svg)](https://asciinema.org/a/VY41zVL6997RTNRwp3OjpxF2p)
