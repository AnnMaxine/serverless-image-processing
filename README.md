# Serverless Image Processing Pipeline

## 1. Project Overview

This project is a serverless image processing application built using Amazon Web Services (AWS).

The application allows users to upload original images to an Amazon S3 bucket. AWS Step Functions coordinates the processing workflow, and an AWS Lambda function uses Python and Pillow to resize images into thumbnails. The resized images are saved in a separate S3 bucket.

An API Gateway endpoint also allows users to trigger the image processing workflow through an HTTP POST request.

## 2. AWS Services Used

- **Amazon S3:** Stores original images and resized thumbnails.
- **AWS Lambda:** Processes images and creates thumbnails using Pillow.
- **AWS Step Functions:** Coordinates the image processing workflow.
- **Amazon EventBridge:** Detects new image uploads and automatically starts the workflow.
- **Amazon API Gateway:** Provides a POST endpoint to trigger the workflow.
- **Amazon CloudWatch:** Stores Lambda execution logs for monitoring and troubleshooting.
- **AWS IAM:** Controls permissions between AWS services.

## 3. Architecture

The application has two ways to start image processing:

1. An image is uploaded to the original S3 bucket. EventBridge detects the upload and starts the Step Functions workflow.
2. A POST request is sent to API Gateway. API Gateway starts the same Step Functions workflow.

Step Functions invokes the Lambda function. Lambda retrieves the original image, resizes it to a maximum dimension of 200 × 200 pixels, and saves the thumbnail in the destination S3 bucket.

## 4. S3 Buckets

**Original images:**
`image-originals-annamarie-2026`

**Resized images:**
`image-thumbnails-annamarie-2026`

Generated thumbnails are stored in the `thumbnails/` folder in the destination bucket.

## 5. Lambda Function

**Function name:** `ImageResizerFunction`

**Runtime:** Python 3.12

**Image library:** Pillow

The Lambda function:
- Receives the source bucket and image filename.
- Retrieves the original image from S3.
- Resizes the image to fit within 200 × 200 pixels while maintaining its aspect ratio.
- Uploads the resized image to the destination S3 bucket.
- Returns a success or failure result.

## 6. Step Functions Workflow

**State machine:** `ImageProcessingStateMachine`

The workflow contains four states:

1. **ProcessImage:** Invokes the Lambda function.
2. **CheckResult:** Checks the Lambda function's processing result.
3. **Success:** Ends the workflow when processing succeeds.
4. **Failure:** Ends the workflow with a failure when processing is unsuccessful.

## 7. API Gateway

**API name:** `ImageProcessingAPI`

**Method:** POST

**Resource path:** `/process-image`

**Endpoint:**
https://s378ik66e3.execute-api.us-east-2.amazonaws.com/prod/process-image

Example request body:

```json
{
  "source_bucket": "image-originals-annamarie-2026",
  "object_key": "74165-nature-HDR-river-trees-mountain-landscape.jpg"
}
```

The endpoint starts the `ImageProcessingStateMachine` workflow.

## 8. Testing and Results

The application was tested using the following methods:

- Uploaded an image to the original S3 bucket and verified that EventBridge automatically started the workflow.
- Confirmed that the Step Functions execution completed successfully.
- Verified that the resized thumbnail was created in the destination S3 bucket.
- Tested the API Gateway POST endpoint and received an HTTP 200 response.
- Confirmed that the API-triggered Step Functions execution completed successfully.

## 9. Project Files

The repository contains the following files:

```text
serverless-image-processing/
├── lambda/
│   └── image_resizer.py
├── step-functions/
│   └── image_processing_state_machine.json
└── README.md
```

## 10. Setup and Configuration

To configure the application in AWS:

1. Create two Amazon S3 buckets for original and resized images.
2. Create an AWS Lambda function using Python 3.12.
3. Install and attach the Pillow library as a Lambda layer.
4. Configure the `DESTINATION_BUCKET` environment variable with the name of the destination S3 bucket.
5. Give the Lambda execution role permission to read objects from the original bucket and write objects to the destination bucket.
6. Create the Step Functions state machine using the JSON definition in the `step-functions` folder.
7. Configure API Gateway to invoke the Step Functions `StartExecution` action.
8. Configure EventBridge to detect new image uploads in the original S3 bucket.

The Lambda function requires the Pillow library. The AWS IAM roles must also have the appropriate permissions for the services to communicate.

## 11. Project Conclusion

The serverless image processing pipeline was successfully implemented and tested. It demonstrates how AWS services can work together to automate image processing without requiring a continuously running server.
