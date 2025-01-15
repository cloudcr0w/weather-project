import json
import boto3
import datetime
from decimal import Decimal

# Helper function to convert Decimal to float (for JSON serialization)
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamo = boto3.resource('dynamodb')

    bucket_name = "weather-project-raw-data"
    table_name = "WeatherStats"

    # Get the list of objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="raw/")
    if "Contents" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "No files found in the bucket"})
        }

    # Find the latest file based on LastModified
    latest_object = max(response['Contents'], key=lambda obj: obj['LastModified'])
    object_key = latest_object['Key']

    # Get the data from the S3 bucket
    s3_response = s3.get_object(Bucket=bucket_name, Key=object_key)
    raw_data = s3_response['Body'].read()
    data = json.loads(raw_data, parse_float=Decimal)  # Parse float values as Decimal

    # Extract necessary information
    city_name = data.get("name", "UnknownCity")
    main_data = data.get("main", {})
    temp = Decimal(main_data.get("temp", 0))
    temp_min = Decimal(main_data.get("temp_min", 0))
    temp_max = Decimal(main_data.get("temp_max", 0))

    # Set the current date
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Save the data in DynamoDB
    table = dynamo.Table(table_name)
    item = {
        "City": city_name,
        "Date": current_date,
        "temp": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
    }
    table.put_item(Item=item)

    # Return the result (converting Decimal for JSON serialization)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Stats saved", "item": item}, default=decimal_default)
    }
