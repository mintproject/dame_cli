# Desktop Application for Model Execution (DAME) 
[![Build Status](https://travis-ci.com/mintproject/dame_cli.svg?branch=master)](https://travis-ci.com/mintproject/dame_cli) [![codecov](https://codecov.io/gh/mintproject/dame_cli/branch/master/graph/badge.svg)](https://codecov.io/gh/mintproject/dame_cli)

The Desktop Application for Model Execution (DAME) is an application for executing environmental models in any local environment or server through a command line interface.

DAME contains a registry of model containers and input data files, as well as metadata about what input data needs to be loaded to run regional configurations and setups of any given model.

Given a model identifier (e.g., TopoFlow for the Awash region: `topoflow36_2.1.0_Awash`), DAME downloads the model container and its execution environment, and fetches the datasets needed (e.g., soil data, elevation data, etc). Then users can run the model with different input scenarios.

DAME works in Linux, MacOS and Windows.  It is installed through a simple pip command.


## Requirements

DAME can work in two main configurations, which have different requirements: 

### Singularity Configuration [Linux- RECOMMENDED]:

1. Singularity
2. Python >= 3.6

### Docker Configuration (BETA) [MacOS, Windows, Linux]:

1. Docker
2. Python >= 3.6

### Singularity 

DAME uses Singularity to manage and run the containers of software components. To install Singularity, please follow the steps below:

- [Installation on Linux](https://sylabs.io/guides/3.5/admin-guide/installation.html#)


### Docker 

DAME can use Docker to manage and run containers of software components. 

- [Installation on Linux](https://docs.docker.com/engine/install/)
- [Installation on MacOS](https://docs.docker.com/docker-for-mac/install/)
- [Installation on Windows](https://docs.docker.com/docker-for-windows/install/)

### Python 3

DAME uses Python. To install Python, just follow the steps below:

- [Installation on Linux](https://realpython.com/installing-python/#linux)
- [Installation on MacOS](https://realpython.com/installing-python/#macos-mac-os-x)
- [Installation on Windows](https://realpython.com/installing-python/#windows)


## Installation

To install the latest version of DAME, open a terminal and run:

```bash
pip install dame-cli
```


## Documentation
Full documentation of the CLI, including usage examples, can be found at: https://dame-cli.readthedocs.io/en/latest/
