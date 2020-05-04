# Usage

DAME was designed to test and run the different models available for execution in [MINT](https://models.mint.isi.edu). We distinguish [model configurations](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration), which allow for users to select the files needed in the execution; and  [model configuration setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup), which are already prepared with default files and parameters to run.

!!! warning
    DAME will download the Docker images and files required for each execution. This may take a while if the files or Docker image selected have a considerable size.

## DAME Commands

Type: `dame --help` to show the list of available commands:
```bash
Usage: dame [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  browse               Open the Model Catalog in your browser
  configure            Configure credentials
  model-configuration  Manages model configurations
  run                  Run a model configuration or model configuration...
  setup                Manages model configuration setup
  version              Show dame-cli version.
```

## Browse and search a Model Configuration

You can list [model configurations](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration) availables 


```bash
$ dame model-configuration list
```

the [model configuration setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup)

```bash
$ dame setup list
```


To explore a list of available models and their metadata, you can go to the website [https://models.mint.isi.edu/](https://models.mint.isi.edu) or type:

```bash
$ dame browse
```

### Show details


#### Model Configurations

You can obtain details about a Model Configuration

```bash
$ dame model-configure show <ID>
```

#### Model Configuration Setup

Or a Setup

```bash
$ dame setup show <ID>
```

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

Inputs
- input-dem: No information

Parameters
- threshold: 500

Docker Image
- Name: mintproject/hand:v2.1.0 - https://hub.docker.com/r/mintproject/hand

Component Location
- Link: https://github.com/mintproject/HAND-TauDEM/raw/v2.1.4/hand_v2_mint_component.zip

To run this model configuration, a input-dem file (.tif file) is required.
Please enter a url for it: https://data.mint.isi.edu/files/hand-dem/GIS-Oromia/Awash/Awash-border_DEM_buffer.tif
```

DAME is requesting the input DEM required to run the model. In this example, we used: [https://data.mint.isi.edu/files/hand-dem/GIS-Oromia/Awash/Awash-border_DEM_buffer.tif](https://data.mint.isi.edu/files/hand-dem/GIS-Oromia/Awash/Awash-border_DEM_buffer.tif)

After inserting the input, DAME displays all the details of the execution and prompts for confirmation, showing the invocation line that will be used:

```bash
The information needed to run the model is complete, and I can execute the model as follows:

Invocation commands
cd executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/hand_v2_mint_component/src
/usr/bin/singularity exec docker://mintproject/hand:v2.1.0 ./run  -i1 Awash-border_DEM_buffer.tif  -o1 distance-down.tif -o3 shape.shp -o4 geojson.json -o2 distance-down-raster.tif  -p1 500
Do you want to proceed and submit it for execution? [Y/n]:Y
```
When confirmed, DAME will display where to find the execution logs and execution results:

```bash
INFO     Execution hand_v2_raster running,  check the logs on executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/output.log
[hand_v2_raster] The execution has been successful
[hand_v2_raster] Results available at: executions/hand_v2_raster_706c74de-835b-11ea-9d3d-f8f21e3c1558/hand_v2_mint_component/src
```

!!! info
    DAME will currently run all parameters of a configuration or setup with their default values.

## Run a Model Configuration Setup

Some [model configuration setups](https://mintproject.readthedocs.io/en/latest/modelcatalog/#model-configuration-setup) have all input files assigned by expert users and are ready to run.

For example, the model configuration setup [cycles-0.10.2-alpha-collection-oromia-single-point](https://models.mint.isi.edu/models/explore/CYCLES/cycles_v0.10.2_alpha/cycles-0.10.2-alpha-collection/cycles-0.10.2-alpha-collection-oromia-single-point) is already prepared to execute an agriculture model in a specific region of Ethiopia. The following code snippet illustrates how DAME shows the setup information (including inputs, parameters, Docker image, etc.) and executes the model:

``` bash
$ dame run cycles-0.10.2-alpha-collection-oromia-single-point
Information about the model configuration

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

Invocation Commands:
cd executions/cycles-0.10.2-alpha-collection-oromia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/cycles-0.10.2-alpha-collection/src
/usr/bin/singularity exec docker://mintproject/cycles:0.10.2-alpha ./run  -i1 Arsi_Amigna_7.884865046N_40.19527054E.zip
-i2 crops.crop  -o1 cycles_soilProfile.dat -o9 cycles_outputs.txt -o3 cycles_crop.dat -o5 cycles_season.dat -o2 cycles_som.dat -o8 cycles_water.dat -o4 cycles_nitrogen.dat -o7 cycles_weatherOutput.dat -o6 cycles_summary.dat  -p4 100 -p2 2017 -p6 0 -p3 Maize -p5 149 -p8 FALSE -p7 0.05 -p1 2000
Do you want to proceed and submit it for execution? [Y/n]:
```
After typing `Y` (for Yes), DAME shows the execution status and where to find the results:

```bash
Do you want to proceed and submit it for execution? [Y/n]:Y
root         INFO     Execution cycles-0.10.2-alpha-collection-oromia-single-point running,  check the logs on executions/cycles-0.10.2-alpha-collection-oromia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/output.log
[cycles-0.10.2-alpha-collection-oromia-single-point] The execution has been successful
[cycles-0.10.2-alpha-collection-oromia-single-point] Results available at: executions/cycles-0.10.2-alpha-collection-oro
mia-single-point_4139f83c-835e-11ea-a111-f8f21e3c1558/cycles-0.10.2-alpha-collection/src
```


!!! info
    You can use the `--non-interactive` option (`dame run <id> --non-interactive`) if you want to directly run a model configuration setup from the command line. This will work only if all inputs have been predefined in a model configuration setup.

<!--[![asciicast](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj.svg)](https://asciinema.org/a/ZhVn1dI5NBIzaaWGaIlD563Cj)-->
