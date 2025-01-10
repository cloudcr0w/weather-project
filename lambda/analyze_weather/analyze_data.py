import json
import boto3
import datetime
from decimal import Decimal

# helper function to convert Decimal to float (or throw a TypeError if unsupported)
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamo = boto3.resource('dynamodb')

    bucket_name = "weather-project-raw-data"
    object_key = "raw/wroclaw,pl/2025-01-10T10:00:27.036611.json"
    table_name = "WeatherStats"

    # get the data from the s3 bucket
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    raw_data = response['Body'].read()
    data = json.loads(raw_data, parse_float=Decimal)  # parse float values as Decimal

    # extract necessary information
    city_name = data.get("name", "UnknownCity")
    main_data = data.get("main", {})
    temp = Decimal(main_data.get("temp", 0))
    temp_min = Decimal(main_data.get("temp_min", 0))
    temp_max = Decimal(main_data.get("temp_max", 0))

    # set the current date
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # save the data in dynamodb
    table = dynamo.Table(table_name)
    item = {
        "City": city_name,       
        "Date": current_date,    
        "temp": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
    }
    table.put_item(Item=item)

    # return the result (converting Decimal for JSON serialization)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Stats saved", "item": item}, default=decimal_default)
    }
