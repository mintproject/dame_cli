The Desktop Application for Model Execution (DAME) is an application for executing environmental models in any local environment or server through a command line interface.

DAME contains a registry of model containers and input data files, as well as metadata about what input data needs to be loaded to run regional configurations and setups of any given model.

Given a model identifier (e.g., TopoFlow for the Awash region: `topoflow36_2.1.0_Awash`), DAME downloads the model container and its execution environment, and fetches the datasets needed (e.g., soil data, elevation data, etc). Then users can run the model with different input scenarios.

DAME works in Linux, with partial support in MacOS (currently being tested on Windows).  It is installed through a simple pip command.

!!! warning
    [April, 2020] Singularity is in BETA in MacOS, and we have recently detected [issues](https://github.com/mintproject/dame_cli/issues/50) when executing certain model setups (in particular, in those images that require Conda). **We recommend using DAME in Linux**.

!!! info
    DAME users should be experienced with container environments (in particular Singularity) and basic Python.


## Requirements

DAME has the following requirements:

1. Singularity
2. Python >= 3.6

### Singularity 

DAME uses Singularity to manage and run the containers of software components. To install Singularity, please follow the steps below:

- [Installation on Linux (Recommended)](https://sylabs.io/guides/3.5/admin-guide/installation.html#)
- [Installation on MacOS](https://sylabs.io/singularity-desktop-macos/)
- [Installation on Windows](https://sylabs.io/guides/3.5/admin-guide/installation.html#windows)



!!! question
    If you would like independent support for Docker, please let us know [on our current discussion on GitHub](https://github.com/mintproject/dame_cli/issues/15)

### Python 3

DAME uses Python. To install Python, just follow the steps below:

- [Installation on Linux (Recommended)](https://realpython.com/installing-python/#linux)
- [Installation on MacOS](https://realpython.com/installing-python/#macos-mac-os-x)
- [Installation on Windows](https://realpython.com/installing-python/#windows)


## Installation

To install the latest version of DAME, open a terminal and run:

```bash
pip install dame-cli
```

You did it!

## Issues, Troubleshooting and Feature Requests

If you experience any issues when using DAME, or if you would like us to support additional exciting features, please open an issue on our [GitHub repository](https://github.com/mintproject/dame_cli/issues).

## Code Releases and Next Updates

The [latest release of DAME is available in GitHub](https://github.com/mintproject/dame_cli/releases/latest). You can check the issues and updates we are working on for the next releases [here](https://github.com/mintproject/dame_cli/milestones).
