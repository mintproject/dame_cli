# Overwriting default parameters in a model configuration setup

Many model configuration setups expose parameters that can be changed during execution time. To change a parameter value, just execute a setup as usual: 

```bash
$ dame run dsi_1.0_cfg_spi_ethiopia
```

And then DAME will ask if you want to change any default parameter:

```bash
Information about the model configuration
- data: https://data.mint.isi.edu/files/raw-data/GLDAS2.1_TP_2000_2018.nc
Parameters
- data_type: GLDAS
- data_end_year: 2017
- min_long: 23
- calibration_start_year: 2000
- max_long: 48
- distribution: gamma
- periodicity: monthly
- data_start_year: 2008
- scales: 6
- index: SPI
- min_lat: 3
- calibration_end_year: 2017
- generate_visualization: True
- max_lat: 15
Docker Image
- Name: mintproject/droughtindices:latest - https://hub.docker.com/r/mintproject/droughtindices
Component Location
- Link: https://github.com/mintproject/MINT-WorkflowDomain/raw/master/WINGSWorkflowComponents/dsi-1.0.0/dsi-1.0.0.zip
Search local files disabled. You can enable it using  option -d or --data
$ dame run id -d example_directory
The information needed to run the model is complete, and I can execute the model as follows:
Do you want to edit the parameters? [y/N]: y
```

If you select `y` (as done above), DAME will proceed to ask you which parameter you want to change:

```bash
- data_type: GLDAS
Enter the new value [GLDAS]:
- data_end_year: 2017
Enter the new value [2017]:2016
...
```

For each parameter, DAME shows the default value in brackets. For example for `data_type`, the default value is `GLDAS`, while for `data_end_year` the value is `2017`. If you want to change a parameter, you just need to insert the new value. If you don't want to change a parameter value, just hit `ENTER` and the default value will be used. In the example above, we selected the default value for `data_type`, while for `data_end_year` we selected `2016`.