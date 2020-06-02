## Browse and search a Data Transformation

You can list available data transformations


```bash
$  dame transformation list
```
which will show a table such as the one below:

```bash
$ dame  transformation list
+------------------+----------------------------------------------------------------------------------+
|        Id        |                             Description                                          |
+==================+==================================================================================+
| topoflow_climate | Data transformation to generate TopoFlow-ready precipitation files               |
|                  | (RTS) from Global Precipitation Measurement (GPM) data sources                   |
|                  | Available datasets:                                                              |
|                  | https://data-catalog.mint.isi.edu/datasets/ea0e86f3-9470-4e7e-a581-df85b4a7075d  |
+------------------+----------------------------------------------------------------------------------+
```


## Run a Data Transformation

You can run the transformation using DAME.

First, you must download the datasets to transform in a directory. You can find this information in the description of the transformation.

```bash
$ dame  transformation run --help  
Usage: dame transformation run [OPTIONS] ID

  You must pass the argument ID (ID of the transformation)

  And the directory using the option -i/--input_dir

  For example:

  dame transformation run topoflow_climate -i data/

Options:
  -i, --input_dir PATH  [required]
  --help                Show this message and exit.
```

Finally, you must pass the argument ID (ID of the transformation) and the directory using the option `-i/--input_dir` 

```bash
$ dame  transformation run topoflow_climate -i data/
Running transformation
The outputs are available: executions/topoflow_climate_35ee167c-a47c-11ea-9ec5-acde48001122/tmp/outputs
```