import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

transcribe = boto3.client("translate")


def lambda_handler(event, context):
    """
    @TODO: Parse data from S3 event to get transcription result and translate it with Amazon Translate.
    """

    return True
