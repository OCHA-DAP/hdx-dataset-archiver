### Dataset Archiver
[![Build Status](https://github.com/OCHA-DAP/hdx-dataset-archiver/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/OCHA-DAP/hdx-dataset-archiver/actions/workflows/run-python-tests.yml) [![Coverage Status](https://coveralls.io/repos/github/OCHA-DAP/hdx-dataset-archiver/badge.svg?branch=main&ts=1)](https://coveralls.io/github/OCHA-DAP/hdx-dataset-archiver?branch=main)

This set of scripts identifies and archives datasets on HDX that meet certain criteria.
- ./analysis/get_datasets_archive.ipynb  - This script filters the list of all datasets on HDX by the archiving criteria coded in the script and outputs output.csv. 
- ./archive_dpt/archive_dpt_datasets.py  - This script iterates over the output from above and archives each dataset there using the HDX CLI, HOWEVER, it may be more convenient to run this using HDX CLI using a CSV as input. This is safer in that an UNDO file is generated which can be used to reverse the archiving if needed. To run it this way:
- - after it is checked by DPT, copy output.csv to the archive_dpt folder and rename datasets-to-archive.csv
- - edit the file to have 3 fields and values as shown in the example below:
dataset_name,key,new_value
ipi-peacekeeping-database,archived,True
gdp-annual-growth,archived,True
people-killed-in-natural-disasters,archived,True

Run >>hdx-toolkit update --hdx_site=prod --from_path=datasets-to-archive.csv --output_path=archived_datasets_UNDO_[todays date].csv


Below is the documentation of the older (now deprecated) archiving script.
### Usage (deprecated)

    python run.py

For the script to run, you will need to have a file called .hdx_configuration.yml in your home directory containing your HDX key eg.

    hdx_key: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    hdx_read_only: false
    hdx_site: prod
    
 You will also need to supply the universal .useragents.yml file in your home directory as specified in the parameter *user_agent_config_yaml* passed to facade in run.py. The collector reads the key **hdx-dataset-archiver** as specified in the parameter *user_agent_lookup*.
 
 Alternatively, you can set up environment variables: USER_AGENT, HDX_KEY, HDX_SITE, TEMP_DIR, LOG_FILE_ONLY
