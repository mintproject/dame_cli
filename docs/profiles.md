
DAME can obtain the metadata about your models from different ModelCatalog or users using profiles

## Configure your profile

To configure your profile, you must use the command `configure` and the option `-p <profile>`

!!! info
    The default values are between the bracket symbols. You don't need to know about it.


```bash
$ dame configure -p default
Model Catalog API [https://api.models.mint.isi.edu/v1.4.0]:
Username [mint@isi.edu]:
Success
```

For example, I use the profile `personal` for my account

```bash
$ dame configure -p personal
Model Catalog API [https://api.models.mint.isi.edu/v1.4.0]:
Username [mint@isi.edu]: mosorio@isi.edu
Success
```


## Run your models

I have created a new model (id: `05641ef5-3937-47bd-b91a-4b5cd0ab615c`).

If I try to run it with the default profile (`mint@isi.edu`) is going to fail because the profile doesn't have the model.

```bash
$ dame setup show 05641ef5-3937-47bd-b91a-4b5cd0ab615c
NOT FOUND

```

If I use the profile `personal`, it works.

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
