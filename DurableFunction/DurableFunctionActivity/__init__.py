# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import time
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import boto3
from botocore.exceptions import ClientError

def main(name: str) -> str:

    status=""
    try:
        token_credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url="https://blogsnapshotautstor.blob.core.windows.net",
            credential=token_credential
        )
        # videos zip is 7.3GB
        blob_client = blob_service_client.get_blob_client(container="feyenoord", blob="videos.zip")

        with open("/tmp/videos.zip", "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())
        status = "ok"

        s3_client = boto3.client('s3', aws_access_key_id="<<your AWS acces key id>>", aws_secret_access_key="<<your AWS key>>")
        try:
            response = s3_client.upload_file("/tmp/videos.zip", "testrbrblobs3", "videos.zip")
        except ClientError as e:
            status = str(e)

    except Exception as e:
        status = str(e)

    return status