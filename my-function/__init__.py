import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient
import logging
import os


def function():
    """
    my function, just copy-paste your script here
    :return:
    """

    # load app settings (edit them in azure portal)
    connection_to_storage = os.environ['AzureWebJobsStorage']
    my_setting = os.environ["my-setting"]

    # load some data from a blob storage
    logging.info('connect to storage %s', connection_to_storage)
    blob_service_client = BlobServiceClient.from_connection_string(connection_to_storage)
    blob_client = blob_service_client.get_blob_client(container='<my-container>', blob='<my-blob>')


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due')
    try:
        function()
    except Exception as e:
        logging.error('Error:')
        logging.error(e)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
