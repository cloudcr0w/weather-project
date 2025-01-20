import json
import boto3
import datetime
import logging
from decimal import Decimal

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Helper function to convert Decimal to float (for JSON serialization)
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    logger.info("Lambda function invoked with event: %s", event)
    
    # Initialize S3 and DynamoDB clients
    s3 = boto3.client('s3')
    dynamo = boto3.resource('dynamodb')

    bucket_name = "weather-project-raw-data"
    table_name = "WeatherStats"

    # Fetching the list of objects from the S3 bucket
    logger.info("Listing objects in S3 bucket: %s with prefix 'raw/'", bucket_name)
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="raw/")
    if "Contents" not in response:
        logger.warning("No files found in bucket: %s", bucket_name)
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "No files found in the bucket"})
        }

    # Finding the latest file based on LastModified
    latest_object = max(response['Contents'], key=lambda obj: obj['LastModified'])
    object_key = latest_object['Key']
    logger.info("Latest file found: %s", object_key)

    # Fetching data from the latest file in S3
    logger.info("Fetching data from S3: Bucket=%s, Key=%s", bucket_name, object_key)
    s3_response = s3.get_object(Bucket=bucket_name, Key=object_key)
    raw_data = s3_response['Body'].read()
    data = json.loads(raw_data, parse_float=Decimal)
    logger.info("Data fetched successfully: %s", data)

    # Extracting necessary information from the data
    city_name = data.get("name", "UnknownCity")
    main_data = data.get("main", {})
    temp = Decimal(main_data.get("temp", 0))
    temp_min = Decimal(main_data.get("temp_min", 0))
    temp_max = Decimal(main_data.get("temp_max", 0))
    logger.info("Extracted data - City: %s, Temp: %s, Temp_min: %s, Temp_max: %s",
                city_name, temp, temp_min, temp_max)

    # Setting the current date
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Saving data to DynamoDB
    logger.info("Saving data to DynamoDB table: %s", table_name)
    table = dynamo.Table(table_name)
    item = {
        "City": city_name,
        "Date": current_date,
        "temp": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
    }
    table.put_item(Item=item)
    logger.info("Data saved successfully to DynamoDB: %s", item)

    # Returning the result (converting Decimal to float for JSON serialization)
    response_body = {
        "message": "Stats saved",
        "item": item
    }
    logger.info("Lambda function executed successfully. Response: %s", response_body)
    return {
        "statusCode": 200,
        "body": json.dumps(response_body, default=decimal_default)
    }
