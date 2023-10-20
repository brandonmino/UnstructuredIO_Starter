# Imports
import json

from unstructured.ingest.interfaces import ProcessorConfig, PartitionConfig, ReadConfig
from unstructured.ingest.runner.sharepoint import SharePointRunner
from unstructured.ingest.runner.local import LocalRunner
from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict

# Required for Unstructured on Windows
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Sharepoint processing variables
SHAREPOINT_CLIENT_ID: str = ""
SHAREPOINT_CLIENT_SECRET: str = ""
SHAREPOINT_PERMISSIONS_APPLICATION_ID: str = ""
SHAREPOINT_PERMISSIONS_CLIENT_SECRET: str = ""
SHAREPOINT_PERMISSIONS_TENANT: str = ""
SHAREPOINT_SITE_URI: str = ""
SHAREPOINT_INPUT_DIR: str = ""
SHAREPOINT_OUTPUT_DIR: str = "sharepoint-ingest-output"

# Local processing variables
LOCAL_INPUT_DIRECTORY: str = "./input_documents"
LOCAL_OUTPUT_DIRECTORY: str = "./output_documents"

# Partition documents from local recursively (all sub folders/files)
def local_partition_process_recursive(input_dir: str, output_dir: str) -> None:
    # Iterate through folders in root folder
    for root, dirs, files in os.walk(input_dir):
        # Perform action for each file found
        for index, file in enumerate(files):
            # Process the file
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                # Partition the file (from file to memory)
                elements = partition(file=f)

                # Convert partition to dictionary
                d = convert_to_dict(elements)

                # Write partition dictionary back to file
                output_dir = f"{output_dir}/{str(index)}.json"
                with open(output_dir, "w") as fp:
                    json.dump(d, fp)

                # Print each element from the dictionary
                for element in d:
                    print(f"{element} \n")
                print("\n")

# Partition documents from local machine using Unstructured Local Connector
def local_partition_connector(input_dir: str, output_dir: str) -> None:
    # Create processor config
    processor_config = ProcessorConfig(
        verbose = True,
        output_dir = output_dir,
        num_processes = 2,
        raise_on_error = True
    )

    # Create read config
    read_config = ReadConfig()

    # Create partition config
    partition_config = PartitionConfig()

    # Create Local Runner
    runner = LocalRunner(
        processor_config=processor_config,
        read_config=read_config,
        partition_config=partition_config
    )

    # Run the Local Runner and get result
    output = runner.run(
        input_path=input_dir,
        recursive=True
    )

    # Display the output (should be None since it will write the output to a file locally)
    print(output)

# Partition from Sharepoint using Unstructured Sharepoint Connector
def sharepoint_partition_connector(
        input_dir: str, 
        output_dir: str, 
        sharepoint_client_id: str, 
        sharepoint_client_secret: str, 
        sharepoint_permissions_application_id: str,
        sharepoint_permissions_client_secret: str,
        sharepoint_permissions_tenant: str,
        sharepoint_site_uri: str
        ) -> None:
    # Create processor config
    processor_config = ProcessorConfig(
        verbose = True,
        output_dir = output_dir,
        num_processes = 2,
        raise_on_error = True
    )

    # Create read config
    read_config = ReadConfig()

    # Create partition config
    partition_config = PartitionConfig()

    # Create Sharepoint Runner
    runner = SharePointRunner(
        processor_config=processor_config,
        read_config=read_config,
        partition_config=partition_config
    )

    # Run the Sharepoint Runner and get result
    output = runner.run(
        client_id=sharepoint_client_id,
        client_cred=sharepoint_client_secret,
        permissions_application_id=sharepoint_permissions_application_id,
        permissions_client_cred=sharepoint_permissions_client_secret,
        permissions_tenant=sharepoint_permissions_tenant,
        site=sharepoint_site_uri,
        # Flag to process only files within the site(s)
        files_only=True,
        # Sharepoint folder path
        path=input_dir,
        # Recursively go through sub folders to get sub files from root path
        recursive=False,
    )

    # Display the output
    print(output)

# Run selected function when running the python script
if __name__ == "__main__":
    # Local recursive partition
    local_partition_process_recursive(input_dir=LOCAL_INPUT_DIRECTORY, output_dir=LOCAL_OUTPUT_DIRECTORY)

    # Local connector partition
    # local_partition_connector(input_dir=LOCAL_INPUT_DIRECTORY, output_dir=LOCAL_OUTPUT_DIRECTORY)

    # Sharepoint partition
    # sharepoint_partition_connector(
    #     input_dir = SHAREPOINT_INPUT_DIR, 
    #     output_dir = SHAREPOINT_OUTPUT_DIR, 
    #     sharepoint_client_id = SHAREPOINT_CLIENT_ID, 
    #     sharepoint_client_secret = SHAREPOINT_CLIENT_SECRET, 
    #     sharepoint_permissions_application_id = SHAREPOINT_PERMISSIONS_APPLICATION_ID,
    #     sharepoint_permissions_client_secret = SHAREPOINT_PERMISSIONS_CLIENT_SECRET,
    #     sharepoint_permissions_tenant = SHAREPOINT_PERMISSIONS_TENANT,
    #     sharepoint_site_uri = SHAREPOINT_SITE_URI
    #     )