# Unstructured Quick Start

###### Author: Brandon Mino
###### Last Updated: October 20, 2023

## Overview
This code will get you started ingesting files from local and Sharepoint.

There are 2 local processesors, one that processes using the automated ingestion connector (local connector), and one that uses the partition function to ingest documents from local with more control (local partition). 

There is only 1 Sharepoint processor, which is the automated ingestion connector (Sharepoint connector).

## Requirements
Python ```3.8+```  
Pip  
Unstructured ```0.10.24+```

## Setup
Follow the setup guide from the official Unstructured Documents to setup Unstructured on your machine.
https://unstructured-io.github.io/unstructured/installation/full_installation.html

## Running the app
<b><i>This app is set to run locally (not using Docker).</i></b>

All of the code for this app is located in the `main_example.py` file.

1. To start, determine the type of processor you will use (local or Sharepoint).
2. In the code, fill in all of the required variables for the type of processor you are using (**NOTE:** for local processing, the directories can be relative or full path values).
3. Open a terminal and navigate to the directory that contains the `main_example.py` file.
4. Run the following command to run the script (**NOTE:** you may need to use `python3` in the command instead of `python` depending on how your Python is setup):
```python main_example.py```
5. The script should run and display the output for the processor. Outputs that are written to files should appear in the same directory as the script.
