import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

transcribe = boto3.client("transcribe")


def lambda_handler(event, context):
    """
    @TODO: Parse data from S3 event to get audio file link and transcribe it with Amazon Transcribe.
    """

    return True
