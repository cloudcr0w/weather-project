import json
import requests
import boto3
import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")  # używamy resource, aby pracować na tabeli bezpośrednio

# Configuration
CITY = "Wroclaw,PL"
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # get API key from .env
BUCKET_NAME = os.getenv("BUCKET_NAME", "default-bucket-name")
TABLE_NAME = os.getenv("TABLE_NAME", "default-table-name")  # DynamoDB Table

def fetch_weather_data():
    """Fetch weather data from OpenWeather API with error handling"""
    logger.info(f"Using OpenWeather API key: {API_KEY}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching weather data: %s", str(e))
        return None  # return if fail

def lambda_handler(event, context):
    logger.info("Lambda function invoked with event: %s", event)
    
    # 1. Fetch data from OpenWeatherMap
    data = fetch_weather_data()
    if data is None:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch weather data"})
        }
    
    # 2. Prepare the file name (key) for saving in S3
    now = datetime.datetime.utcnow().isoformat()
    object_key = f"raw/{CITY.lower()}/{now}.json"
    
    # 3. Save the data to S3
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        logger.info("Successfully stored data in S3: %s/%s", BUCKET_NAME, object_key)
    except Exception as e:
        logger.error("Failed to store data in S3: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to store data in S3"})
        }

    # 4. Save data to DynamoDB
    table = dynamodb.Table(TABLE_NAME)  # Poprawiona inicjalizacja tabeli
    try:
        table.put_item(
            Item={
                "City": CITY,
                "Date": now.split("T")[0],  # YYYY-MM-DD
                "temp": data["main"]["temp"],
                "temp_max": data["main"]["temp_max"],
                "temp_min": data["main"]["temp_min"]
            }
        )
        logger.info("Successfully stored data in DynamoDB: %s", TABLE_NAME)
    except Exception as e:
        logger.error("Failed to store data in DynamoDB: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to store data in DynamoDB"})
        }

    # 5. Return the response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully stored weather data for {CITY} at {now}",
            "s3_object": object_key
        })
    }
