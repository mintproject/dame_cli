# mint_cli
[![asciicast](https://asciinema.org/a/VY41zVL6997RTNRwp3OjpxF2p.svg)](https://asciinema.org/a/VY41zVL6997RTNRwp3OjpxF2p)


## Installation

```bash
pip install mint-ci
```

## CLI

mint_cli is a cli to `run` setups define on the model catalog.
The setups are defined using YAML files.

### Execution

You can run a setup

```bash
$ mint run topoflow/topoflow_cfg_advanced_Baro.yaml
``` 

Or, you can run multiple setups. The setups must be inside on a directory.

```bash
$ ls setups/hand_v1_simple/
hand_v1_simple_awash.yaml    hand_v1_simple_beko-tippi.yaml  hand_v1_simple_guder.yaml  hand_v1_simple_shebelle.yaml
hand_v1_simple_baro.yaml     hand_v1_simple_ethiopia.yaml    hand_v1_simple_jamma.yaml  hand_v1_simple_texas.yaml
hand_v1_simple_bashilo.yaml  hand_v1_simple_ganale.yaml      hand_v1_simple_muger.yaml
```

```bash
$ mint run setups/hand_v1_simple/
Execution hand_v1_simple_bashilo, check the logs on executions/hand_v1_simple_bashilo_c241473a-1b64-11ea-8100-f8f21e3c1558/output.log
Execution hand_v1_simple_jamma, check the logs on executions/hand_v1_simple_jamma_c2f7e080-1b64-11ea-8100-f8f21e3c1558/output.log
Execution hand_v1_simple_shebelle, check the logs on executions/hand_v1_simple_shebelle_c36e4202-1b64-11ea-8100-f8f21e3c1558/output.log
``` 

## Setup files

Sadly, this version does not download the setup files. You can use [mint_setup_runner](https://github.com/sirspock/mint_setup_runner)

