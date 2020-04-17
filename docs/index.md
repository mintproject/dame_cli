The Desktop Application for Model Execution (DAME) is an application for executing environmental models in any local environment or server through a command line interface.

DAME contains a registry of model containers and input data files, as well as metadata about what input data needs to be loaded to run regional configurations and setups of any given model.

Given a model identifier (e.g., TopoFlow for the Awash region: `topoflow36_2.1.0_Awash`), DAME downloads the model container and its execution environment, and fetches the datasets needed (e.g., soil data, elevation data, etc). Then users can run the model with different input scenarios.

DAME works in Linux and OSX (currently being tested on Windows).  It is installed through a simple pip command.


## Requirements

DAME has the following requirements:

1. Singularity
2. Python >= 3.6

### Singularity 

DAME uses Singularity to run the containers of the executed components. Follow the next steps to install Singularity:

- [Installation on Linux](https://sylabs.io/guides/3.5/admin-guide/installation.html#)
- [Installation on Windows](https://sylabs.io/guides/3.5/admin-guide/installation.html#windows)
- [Installation on Mac](https://sylabs.io/singularity-desktop-macos/)


!!! question
    If you would like independent support for Docker, please let us know. [Add support to Docker](https://github.com/mintproject/dame_cli/issues/15)

### Python 3

DAME uses Python. Please, follow the steps bellow to install it:

- [Installation on Linux](https://realpython.com/installing-python/#linux)
- [Installation on Windows](https://realpython.com/installing-python/#windows)
- [Installation on Mac](https://realpython.com/installing-python/#macos-mac-os-x)

## Installation

To install DAME, open a terminal and run:

```bash
pip install dame-cli
```

You did it!

## Issues and Troubleshooting

If you experience any issues when using DAME, please open an issue on our  [GitHub repository](https://github.com/mintproject/dame_cli/issues).
