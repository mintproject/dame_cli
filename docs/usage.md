# Usage

## Browse and search a Model Configuration

To explore the models in MINT Model Catalog. You can go to the website [https://models.mint.isi.edu/](https://models.mint.isi.edu) or type:

```bash
$ dame browse
```


Select the [Model Configuration](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration) or the [Model Configuration Setup](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup) to run


## Run a Model Configuration 

Open a terminal and type:

```bash
$ dame run <model id>
```
Where `<model id>` correspods to the id of the model configuration you want to run. For example, the id `modflow_2005_cfg` will prepare the execution of the MODFLOW 2005 ground water model by asking for the required input files.

### Run a fully configured Model Configuration Setup

Since some [Model Configuration Setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup) have all input files assigned by expert users, you don't have to provide the location of the inputs.

For example, the Model Configuration Setup [cycles-0.10.2-alpha-collection-oromia-single-point](https://models.mint.isi.edu/models/explore/CYCLES/cycles_v0.10.2_alpha/cycles-0.10.2-alpha-collection/cycles-0.10.2-alpha-collection-oromia-single-point) is already prepared to execute an agriculture model in a specific region of Ethiopia. The following video shows how DAME would excute the model.

[![asciicast](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj.svg)](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj)
