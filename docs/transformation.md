## Browse and search a Data Transformation

You can list available data transformations


```bash
$  dame transformation list
```
which will show a table such as the one below:

```bash
$ dame transformation list 
+--------------------------------------+------------------------+
|                  Id                  |      Description       |
+======================================+========================+
| 045c9eb2-a20b-4095-af95-30bb00d944fe | topoflow_dt            |
+--------------------------------------+------------------------+
| f10c8645-ccee-4d3a-8ed8-0c558b7dc726 | gldas_to_daily_average |
+--------------------------------------+------------------------+

```


## Run a Data Transformation

You can run the transformation using DAME.

```bash
$ dame transformation run --help
Usage: dame transformation run [OPTIONS] DATA_TRANSFORMATION_ID

  You must pass the argument ID (ID of the transformation)

  For example:

  dame transformation run topoflow_climate

Options:
  -p, --profile <profile-name>
  --help                        Show this message and exit.
```

In the following example, DAME is executing the Topoflow DT

```bash
$ dame transformation run 045c9eb2-a20b-4095-af95-30bb00d944fe
Information about the model configuration
Parameters
- DEM_xres_arcsecs: 30
- end_date: 2014-08-02 00:00:00
- start_date: 2014-08-01 00:00:00
- data_set_id: 5babae3f-c468-4e01-862e-8b201468e3b5
- unit_multifier: 3600
- DEM_yres_arcsecs: 30
- variable: atmosphere_water__rainfall_mass_flux
- bounding_box: 23.995416666666,6.532916666667,28.020416666666,9.566250000000
Docker Image
- Name: mosorio/topoflow_dt:20.7.16 - https://hub.docker.com/r/mosorio/topoflow_dt
Component Location
- Link: https://raw.githubusercontent.com/sirspock/topoflow_dt/master/mint_component.zip
Do you want to edit the parameters? [y/N]:
```

In this example, the Data Transformation is going to read the parameters and download the required files. The user can edit the parameters to use the transformation in a different region (bounding box) and period (start_date, end_date)

!!! info
    The parameter `data_set_id` is the identifier in the DataCatalog. Please [here](https://data-catalog.mint.isi.edu/datasets/5babae3f-c468-4e01-862e-8b201468e3b5) for more information.


If the execution has ended correctly, DAME is going to print the path where the files are.

```bash
[045c9eb2-a20b-4095-af95-30bb00d944fe] The execution has been successful
[045c9eb2-a20b-4095-af95-30bb00d944fe] Results available at: executions/045c9eb2-a20b-4095-af95-30bb00d944fe_70aa349a-caaa-11ea-aae3-faffc21691f4/topoflow_dt/src
```