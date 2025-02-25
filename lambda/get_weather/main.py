import json
import requests
import boto3
import datetime
import logging

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")  # Dodaj inicjalizację DynamoDB

# Configuration
city = "Wroclaw,PL"
api_key = "eb56bc94ccae31d4198ed456691e8d30"
bucket_name = "weather-project-raw-data"
table_name = "WeatherStats"  # Nazwa Twojej tabeli DynamoDB

def lambda_handler(event, context):
    logger.info("Lambda function invoked with event: %s", event)
    
    # 1. Build the API URL (with the units=metric parameter)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    # 2. Fetch data from OpenWeatherMap
    response = requests.get(url)
    data = response.json()
    
    # Log the fetched data
    logger.info("Fetched weather data: %s", data)

    # 3. Prepare the file name (key) for saving in S3
    now = datetime.datetime.utcnow().isoformat()
    object_key = f"raw/{city.lower()}/{now}.json"
    
    # 4. Save the data to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    
    logger.info("Successfully stored data in S3: %s/%s", bucket_name, object_key)

    # 5. Save data to DynamoDB
    try:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                "City": {"S": city},
                "Date": {"S": now.split("T")[0]},  # YYYY-MM-DD
                "temp": {"N": str(data["main"]["temp"])},
                "temp_max": {"N": str(data["main"]["temp_max"])},
                "temp_min": {"N": str(data["main"]["temp_min"])}
            }
        )
        logger.info("Successfully stored data in DynamoDB: %s", table_name)
    except Exception as e:
        logger.error("Failed to store data in DynamoDB: %s", str(e))

    # 6. Return the response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully stored weather data for {city} at {now}",
            "s3_object": object_key
        })
    }
