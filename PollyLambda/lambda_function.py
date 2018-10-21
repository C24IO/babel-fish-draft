import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#TODO
#This function should get in the input (event) following parameters: text, language, correlationId. Example input:
#{
#  "text": "This is simple text",
#  "language": "en",
#  "correlationId": "42535425"
#}
#The function should save new created audio file in the bucket, and should return the JSON with a link to the file as a response.


def lambda_handler(event, context):
    
    logger.info(">> Converting to audio")
    logger.info('Input event{}'.format(event))


    response = {}
    response["link"] = "ReInvent 2018: Implementation TODO (Text-To-Speech Lambda)

    return json.dumps(response);
