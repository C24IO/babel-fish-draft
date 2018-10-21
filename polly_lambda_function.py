import logging
import os
import boto3
from contextlib import closing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

polly = boto3.client("polly")
s3 = boto3.client("s3")

voice_map = {
    "en": "Joanna",
    "de": "Vicki",
    "fr": "Lea",
    "es": "Penelope",
    "pt": "Ines",
    "zh": "Zhiyu",
}


def lambda_handler(event, context):
    # Parse data from S3 event
    record, = event["Records"]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    logger.info("Processing data [{}] from bucket [{}]...".format(key, bucket))

    # Get request data from filename
    request_name = os.path.splitext(os.path.basename(key))[0]
    output_lang = request_name.split("-", 2)[1]

    # Download and parse translate result from S3
    tmp_txt = "/tmp/{}".format(key)
    s3.download_file(bucket, key, tmp_txt)
    with open(tmp_txt) as f:
        translation = f.read()
    logger.info("Downloaded translate result [{}] from bucket [{}]".format(tmp_txt, bucket))

    # Perform speech synthesis with Amazon Polly
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=translation,
        TextType='text',
        VoiceId=voice_map[output_lang]
    )
    logger.info("Submitted synthesis request with voice [{}]".format(voice_map[output_lang]))

    # Write and upload synthesis result to S3
    key_mp3 = "output/{}.mp3".format(request_name)
    tmp_mp3 = "/tmp/{}.mp3".format(request_name)
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as s:
            with open(tmp_mp3, "wb") as f:
                f.write(s.read())
    s3.upload_file(tmp_mp3, bucket, key_mp3)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key_mp3)
    logger.info("Uploaded synthesis result [{}] to bucket [{}].".format(key_mp3, bucket))

    return True
