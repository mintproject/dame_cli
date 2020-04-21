# Usage

DAME was designed to test and run the different models available for execution in the [MINT model catalog](https://models.mint.isi.edu). We distinguish [model configurations](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration), which allow for users to select the files needed in the execution; and  [model configuration setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup), which are already prepared with default files and parameters to run.

!!! warning
    DAME will download the Docker images and files required for each execution. This may take a while if the files or Docker image selected have a considerable size.

## DAME options

Type: `dame --help` to show the list of available commands:
```bash
$ dame --help
Usage: dame [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.
Commands:
  browse   Open the Model Catalog in your browser
  run      Run a model configuration or model configuration setup
  version  Show wcm version.
```

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
Where `<model id>` correspods to the id of the model configuration you want to run. For example, the id `hand_v2_raster` will prepare the execution details of the HAND model by asking for the required input file (in this case, a digital elevation model):

```bash
$ dame run hand_v2_raster
```
Dame response:

```bash
Information about the model configuration

nputs
- input-dem: No information

Parameters
- threshold: 500

Docker Image
- Name: mintproject/hand:v2.1.0 - https://hub.docker.com/r/mintproject/hand

Component Location
- Link: https://github.com/mintproject/HAND-TauDEM/raw/v2.1.4/hand_v2_mint_component.zip

To run this model configuration, a input-dem file (.tif file) is required.
Please enter a url for it: https://github.com/dhardestylewis/HAND-TauDEM/raw/master/regions/Texas/Travis-10m/Travis-DEM-10m-HUC120902050408buf.tif
```

In this case, DAME is requesting the input DEM required to run the model. In this example, we used: [https://github.com/dhardestylewis/HAND-TauDEM/raw/master/regions/Texas/Travis-10m/Travis-DEM-10m-HUC120902050408buf.tif](https://github.com/dhardestylewis/HAND-TauDEM/raw/master/regions/Texas/Travis-10m/Travis-DEM-10m-HUC120902050408buf.tif)

After inserting the input, DAME displays all the details of the execution and prompts for confirmation and showing the invocation line that will be used:

```bash
The information of the setup is complete

Execution line
cd executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/hand_v2_mint_component/src
/usr/bin/singularity exec docker://mintproject/hand:v2.1.0 ./run  -i1 Travis-DEM-10m-HUC120902050408buf.tif  -o1 distance-down.tif -o3 shape.shp -o4 geojson.json -o2 distance-down-raster.tif  -p1 500
Do you want to run the setup? [Y/n]:Y
```
When confirmed, DAME will display where to find the execution logs and execution results:

```bash
INFO     Execution hand_v2_raster running,  check the logs on executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/output.log
[hand_v2_raster] The execution has been successful
[hand_v2_raster] Results available at: executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/hand_v2_mint_component/src
```

!!! info
    DAME will currently run all parameters of a configuration or setup with their default values.

## Run a fully configured Model Configuration Setup

Since some [Model Configuration Setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup) have all input files assigned by expert users, you don't have to provide the location of the inputs.

For example, the Model Configuration Setup [cycles-0.10.2-alpha-collection-oromia-single-point](https://models.mint.isi.edu/models/explore/CYCLES/cycles_v0.10.2_alpha/cycles-0.10.2-alpha-collection/cycles-0.10.2-alpha-collection-oromia-single-point) is already prepared to execute an agriculture model in a specific region of Ethiopia. The following code snippet illustrates how DAME shows the setup information (including inputs, parameters, Docker image, etc.) and executes the model:

``` bash
$ dame run cycles-0.10.2-alpha-collection-oromia-single-point
Information about the model configuration

Inputs
- cycles_weather_soil: https://data.mint.isi.edu/files/cycles-input-data/oromia/weather-soil/Arsi_Amigna_7.884865046N_40Information about the model configuration
Inputs
- cycles_weather_soil: https://data.mint.isi.edu/files/cycles-input-data/oromia/weather-soil/Arsi_Amigna_7.884865046N_40.19527054E.zip
- cycles_crops: https://raw.githubusercontent.com/pegasus-isi/pegasus-cycles/master/data/crops.crop

Parameters
- start_planting_day: 100
- end_year: 2017
- fertilizer_rate: 0
- crop_name: Maize
- end_planting_day: 149
- use_forcing: FALSE
- weed_fraction: 0.05
- start_year: 2000

Docker Image
- Name: mintproject/cycles:0.10.2-alpha - https://hub.docker.com/r/mintproject/cycles

Component Location
- Link: https://github.com/mintproject/MINT-WorkflowDomain/raw/master/WINGSWorkflowComponents/cycles-0.10.2-alpha-collection/cycles-0.10.2-alpha-collection.zip
The information of the setup is complete

Execution line
cd executions/cycles-0.10.2-alpha-collection-oromia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/cycles-0.10.2-alpha-collection/src
/usr/bin/singularity exec docker://mintproject/cycles:0.10.2-alpha ./run  -i1 Arsi_Amigna_7.884865046N_40.19527054E.zip
-i2 crops.crop  -o1 cycles_soilProfile.dat -o9 cycles_outputs.txt -o3 cycles_crop.dat -o5 cycles_season.dat -o2 cycles_som.dat -o8 cycles_water.dat -o4 cycles_nitrogen.dat -o7 cycles_weatherOutput.dat -o6 cycles_summary.dat  -p4 100 -p2 2017 -p6 0 -p3 Maize -p5 149 -p8 FALSE -p7 0.05 -p1 2000
Do you want to run the setup? [Y/n]:
```
After typing `Y` (for Yes), DAME shows the execution status and where to find the results:

```bash
Do you want to run the setup? [Y/n]: Y
root         INFO     Execution cycles-0.10.2-alpha-collection-oromia-single-point running,  check the logs on executions/cycles-0.10.2-alpha-collection-oromia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/output.log
[cycles-0.10.2-alpha-collection-oromia-single-point] The execution has been successful
[cycles-0.10.2-alpha-collection-oromia-single-point] Results available at: executions/cycles-0.10.2-alpha-collection-oro
mia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/cycles-0.10.2-alpha-collection/src
```


!!! info
    You can use the `--non-interactive` option (`dame run <id> --non-interactive`) if you want to directly run a prepared model configuration from the command line. This will work only if all inputs are completed in a setup.

<!--[![asciicast](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj.svg)](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj)-->
