import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

transcribe = boto3.client("transcribe")


def lambda_handler(event, context):
    # Parse data from S3 event
    record, = event["Records"]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    logger.info("Processing audio [{}] from bucket [{}]...".format(key, bucket))

    # Get request data from filename
    request_name, ext = os.path.splitext(os.path.basename(key))
    input_lang = request_name.split("-", 1)[0]
    media_format = ext.strip(".")

    # Perform transcription with Amazon Transcribe
    media_file_uri = "https://s3-us-east-1.amazonaws.com/{}/{}"
    transcription_job = transcribe.start_transcription_job(
        TranscriptionJobName=request_name,
        LanguageCode="{}-US".format(input_lang),
        MediaFormat=media_format,
        Media={
            'MediaFileUri': media_file_uri.format(bucket, key)
        },
        OutputBucketName=bucket,
    )
    logger.info("Transcription job started: {}".format(transcription_job))

    return True
