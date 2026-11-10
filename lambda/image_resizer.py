
import json
import os
import boto3
from io import BytesIO
from urllib.parse import unquote_plus
from PIL import Image

# Connect to Amazon S3
s3 = boto3.client("s3")

# Get the destination bucket from Lambda environment variables
DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]


def lambda_handler(event, context):
    try:
        # Get the original bucket and image filename
        # Supports both Step Functions input and S3 upload events
        if "Records" in event:
            record = event["Records"][0]
            source_bucket = record["s3"]["bucket"]["name"]
            object_key = unquote_plus(
                record["s3"]["object"]["key"]
            )
        else:
            source_bucket = event["source_bucket"]
            object_key = event["object_key"]

        print(f"Processing image: {object_key}")
        print(f"Source bucket: {source_bucket}")

        # Download the original image from S3
        response = s3.get_object(
            Bucket=source_bucket,
            Key=object_key
        )

        image_data = response["Body"].read()

        # Open the image using Pillow
        with Image.open(BytesIO(image_data)) as image:

            # Resize while maintaining the original proportions
            image.thumbnail((200, 200))

            # Keep the original image format
            image_format = image.format or "JPEG"

            # Prepare the resized image
            output = BytesIO()
            image.save(output, format=image_format)
            output.seek(0)

            # Create a thumbnail filename
            filename = object_key.split("/")[-1]
            name, extension = os.path.splitext(filename)

            thumbnail_key = (
                f"thumbnails/{name}_thumbnail{extension}"
            )

            # Upload the resized image to the second bucket
            s3.put_object(
                Bucket=DESTINATION_BUCKET,
                Key=thumbnail_key,
                Body=output.getvalue(),
                ContentType=response.get(
                    "ContentType", "image/jpeg"
                )
            )

        print(f"Thumbnail saved: {thumbnail_key}")

        # Return success information
        return {
            "status": "SUCCESS",
            "source_bucket": source_bucket,
            "original_image": object_key,
            "destination_bucket": DESTINATION_BUCKET,
            "thumbnail": thumbnail_key
        }

    except Exception as error:
        print(f"Image processing failed: {str(error)}")

        return {
            "status": "FAILED",
            "error": str(error)
        }
