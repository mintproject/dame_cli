
DAME can obtain model metadata from different APIs and user profiles. By default, DAME uses:

- API:https://api.models.mint.isi.edu/v1.5.0
- user: mint@isi.edu

## Configure your profile

To configure your profile, you must use the command `configure` and the option `-p <profile>`

!!! info
    Default values are shown in brackets, you don't need to worry about them. 

By running the following command and pressing enter (leaving the default values), DAME willbe configured by default:

```bash
$ dame credentials -p default
Model Catalog API [https://api.models.mint.isi.edu/v1.5.0]:
Username [mint@isi.edu]:
Success
```

To define the profile `personal`, you should type: 

```bash
$ dame credentials -p personal
Model Catalog API [https://api.models.mint.isi.edu/v1.5.0]:
Username [mint@isi.edu]: mosorio@isi.edu
Success
```

## Run models using profiles

Imagine we have created a new model configuration setup (id: `05641ef5-3937-47bd-b91a-4b5cd0ab615c`) under our user (e.g., mosorio@isi.edu).

If I try to run it with the default profile (`mint@isi.edu`) is going to fail because the profile doesn't have that model.

```bash
$ dame setup show 05641ef5-3937-47bd-b91a-4b5cd0ab615c
NOT FOUND

```

However, if I use the profile `personal`, it works correctly:

```bash
$ dame setup show 05641ef5-3937-47bd-b91a-4b5cd0ab615c -p personal
Information about the model configuration
Inputs
- cycles_soil: No information
- cycles_crops: No information
- cycles_weather: No information
Parameters
Docker Image
- Name: mintproject/cycles:0.9.4-alpha - https://hub.docker.com/r/mintproject/cycles
Component Location
- Link: https://github.com/mintproject/MINT-WorkflowDomain/blob/master/WINGSWorkflowComponents/cycles-0.9.4-alpha/cycles-0.9.4-alpha.zip?raw=true
```
