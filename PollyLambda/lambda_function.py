import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

polly = boto3.client("polly")


def lambda_handler(event, context):
    """
    @TODO: Parse data from S3 event to get translation result and synthesize it with Amazon Polly.
    """

    return True
