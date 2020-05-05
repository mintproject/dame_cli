# Using local files for execution

You may want to test some of the model configurations or setups with files stored in your own computer. In order to use files, you should use the `--data <name_directory>` option:

```
$ dame run hand_v2_raster --data data_files
```

## Example

The setup `hand_v2_raster` doesn't have information about a link `input-dem`.

```bash
$  dame setup show hand_v2_raster                                                      
Information about the model configuration
Inputs
- input-dem [.tif]: No information 
Parameters
- threshold: 500
Docker Image
- Name: mintproject/hand:v2.1.0 - https://hub.docker.com/r/mintproject/hand
Component Location
- Link: https://github.com/mintproject/HAND-TauDEM/raw/v2.1.4/hand_v2_mint_component.zip
```

Let's create the directory `data` 
```bash
$ mkdir data
```

And download a compatible file
```bash
$ cd data
$ wget https://github.com/dhardestylewis/HAND-TauDEM/raw/master/regions/Texas/Travis-10m/Travis-DEM-10m-HUC120902050408buf.tif
```

Then, we just need to run the setup

```
$ dame run hand_v2_raster  --data data
```

DAME uses the directory named `data` by default. 

For the setup `hand_v2_raster`, DAME knows that the format file must be `.tif` and it's going search all the `tif` files into the directory.
If you have one file only, DAME will select it automatically.

```bash
$ dame run hand_v2_raster                         
...

To run this model configuration, a input-dem file (.tif file) is required.
Do you want to search the file in the directory /Users/mosorio/repos/dame_cli/data [Y/n]: y
Selected from your computer /Users/mosorio/repos/dame_cli/data/Travis-DEM-10m-HUC120902050408buf.tif
The information needed to run the model is complete, and I can execute the model as follows:
```

If you have multiples files. DAME will ask you to choose the correct one:

```
$ dame run hand_v2_raster                         
...

Do you want to search the file in the directory /Users/mosorio/repos/dame_cli/data [Y/n]:
[1] /Users/mosorio/repos/dame_cli/data/Travis-DEM-10m-HUC120902050408buf.tif
[2] /Users/mosorio/repos/dame_cli/data/Baro-DEM-10m-HUC120902050408buf.tif
Select the file (1, 2):

```





