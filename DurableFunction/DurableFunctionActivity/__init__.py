# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import time
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient
import boto3
from botocore.exceptions import ClientError

def main(name: str) -> str:

    par_account_url = os.environ['account_url']
    par_storage_container = os.environ['storage_container']
    par_file_name = name # os.environ['file_name'] # todo, pass this parameter from ADFv2 or loop through storage container
    par_keyvault_url = os.environ['keyvault_url']
    par_s3_bucket = os.environ['s3_bucket']

    status = "ok"
    try:
        # Download file from Azure Storage and put it on tmp storage of Azure Function
        token_credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=par_account_url,
            credential=token_credential
        )
        blob_client = blob_service_client.get_blob_client(container=par_storage_container, blob=par_file_name)

        with open("/tmp/" + par_file_name, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

        # Upload file from Azure Function tmp storage to AWS S3
        secret_client = SecretClient(vault_url=par_keyvault_url, credential=token_credential)
        aws_access_key_id = secret_client.get_secret("aws-access-key-id").value
        aws_secret_access_key = secret_client.get_secret("aws-secret-access-key").value
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        try:
            response = s3_client.upload_file("/tmp/" + par_file_name, par_s3_bucket, par_file_name)
        except ClientError as e:
            status = str(e)

    except Exception as e:
        status = str(e)
    
    finally:
        os.remove("/tmp/" + par_file_name)
        download_stream = None

    return status