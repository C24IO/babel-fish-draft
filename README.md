# Build a Babel Fish with Machine Learning Language Services

This repository contains necessary resources for AWS re:Invent 2018 workshop AIM313. In this readme you will find detailed instructions for each phase of the workshop.

## Phase 0: Environment setup

Login to your AWS Console and choose `us-east-1` (N. Virginia) region. Use CloudFormation service in the AWS Console to configure your environment with `cfn-babel-fish.yaml` template:

1. Click `Create Stack`
1. Under `Choose a template` pick `Upload a template to Amazon S3`, choose `cfn-babel-fish.yaml` file and click `Next`.
1. Give your stack a meaningful name and click `Next`.
1. On `Options` page click `Next`
1. On `Review` page acknowledge that CloudFormation might create IAM resources and click `Create`
1. Wait a few moments until status changes from `CREATE_IN_PROGRESS` to `CREATE_COMPLETE`.

Use S3 service in the AWS Console to create `input` and `output` folders in the bucket created by CloudFormation.

Check resources created by CloudFormation and update JavaScript app with your configuration data:

1. Provide correct S3 bucket name.
1. Provice correct Identity Pool ID.

## Phase 1: Convert audio to text

Use Lambda service in the AWS Console to open `TranscribeLambda` function. In the `Add triggers` section on the left configure trigger for this function:

1. Choose S3 as the trigger and go to the `Configure triggers` section.
1. Pick correct S3 bucket name.
1. Pick `PUT` as event type.
1. Put `input/` as prefix.
1. Put `.mp3` as suffix.
1. Click `Add` at the bottom of the page to add trigger.
1. Click `Save` at the top of the page to confirm changes to the function.

Repeat the steps above but this time putting `.wav` as the suffix.

Implement the function to parse data from S3 event to get audio file link and transcribe it with Amazon Transcribe.

> Hint: JavaScript app uses a following format to name the files: `xx-yy-guid.ext`, where `xx` is the input language, `yy` is the output language, `guid` is a unique identifier and `ext` is original file extension.

> Hint: Your function should request Amazon Transcribe to put results in project's S3 bucket and use the same file naming convention as JavaScript app.

> Hint: When the time is up you can ask for the password to the `transcribe_lambda_function.zip` file with a ready solution.

## Phase 2: Translate text

Use Lambda service in the AWS Console to open `TranslateLambda` function. In the `Add triggers` section on the left configure trigger for this function:

1. Choose S3 as the trigger and go to the `Configure triggers` section.
1. Pick correct S3 bucket name (S3BucketOutput from above).
1. Pick `PUT` as event type.
1. Put `.json` as suffix.
1. Click `Add` at the bottom of the page to add trigger.
1. Click `Save` at the top of the page to confirm changes to the function.

Implement the function to parse data from S3 event to get transcription result and translate it with Amazon Translate.

> Hint: Your function should put translation result to a `.txt` file in project's S3 bucket and use the same file naming convention as JavaScript app.

> When the time is up you can ask for the password to the `translate_lambda_function.zip` file with a ready solution.

## Phase 3: Convert text to audio

Use Lambda service in the AWS Console to open `PollyLambda` function. In the `Add triggers` section on the left configure trigger for this function:

1. Choose S3 as the trigger and go to the `Configure triggers` section.
1. Pick correct S3 bucket name.
1. Pick `PUT` as event type.
1. Put `.txt` as suffix.
1. Click `Add` at the bottom of the page to add trigger.
1. Click `Save` at the top of the page to confirm changes to the function.

Implement the function to parse data from S3 event to get translation result and synthesize it with Amazon Polly.

> Hint: Your function should put synthesis result to an `.mp3` file in project's S3 bucket in `output` folder and use the same file naming convention as JavaScript app.

> When the time is up you can ask for the password to the `polly_lambda_function.zip` file with a ready solution.

## Demo

It's time to let your Babel-fish out :)

## Extra task

Put the static file with JavaScript application in S3 bucket to make it available online. See [Hosting a Static Website on Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html) Developer Guide for reference.


