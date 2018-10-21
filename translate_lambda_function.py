import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

translate = boto3.client("translate")
s3 = boto3.client("s3")


def lambda_handler(event, context):
    # Parse data from S3 event
    record, = event["Records"]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    logger.info("Processing data [{}] from bucket [{}]...".format(key, bucket))

    # Get request data from filename
    request_name = os.path.splitext(os.path.basename(key))[0]
    input_lang, output_lang = request_name.split("-", 2)[:2]

    # Download and parse transcribe result from S3
    tmp_json = "/tmp/{}".format(key)
    s3.download_file(bucket, key, tmp_json)
    with open(tmp_json) as f:
        transcribe_data = json.load(f)
    logger.info("Downloaded transcribe result [{}] from bucket [{}]".format(tmp_json, bucket))

    # Define necessary translation steps
    # English is required at one side of translation
    if "en" in (input_lang, output_lang):
        translation_steps = [(input_lang, output_lang)]
    else:
        translation_steps = [(input_lang, "en"), ("en", output_lang)]
    logger.info("Defined translation steps [{}]".format(translation_steps))

    # Perform translation with Amazon Translate
    translation = transcribe_data["results"]["transcripts"][0]["transcript"]
    for step in translation_steps:
        logger.info("Translation input [{}]".format(translation))
        response = translate.translate_text(
            Text=translation,
            SourceLanguageCode=step[0],
            TargetLanguageCode=step[1],
        )
        translation = response["TranslatedText"]
        logger.info("Translation output [{}]".format(translation))

    # Write and upload translate result to S3
    key_txt = "{}.txt".format(request_name)
    tmp_txt = "/tmp/{}".format(key_txt)
    with open(tmp_txt, "w") as f:
        f.write(translation)
    s3.upload_file(tmp_txt, bucket, key_txt)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key_txt)
    logger.info("Uploaded translate result [{}] to bucket [{}].".format(key_txt, bucket))

    return True
