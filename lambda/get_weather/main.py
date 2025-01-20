import json
import requests
import boto3
import datetime
import logging

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Logging the function invocation
    logger.info("Lambda function invoked with event: %s", event)
    
    # 1. Configure city and API key
    city = "Wroclaw,PL"
    api_key = "eb56bc94ccae31d4198ed456691e8d30"  
    bucket_name = "weather-project-raw-data"     
    s3 = boto3.client("s3")

    # 2. Build the API URL (with the units=metric parameter)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    # 3. Fetch data from OpenWeatherMap
    response = requests.get(url)
    data = response.json()
    
    # Log the fetched data
    logger.info("Fetched weather data: %s", data)

    # 4. Prepare the file name (key) for saving in S3
    now = datetime.datetime.utcnow().isoformat()
    # e.g., "raw/wroclaw,pl/2025-01-10T12:34:56.789012.json"
    object_key = f"raw/{city.lower()}/{now}.json"

    # Log the generated file name
    logger.info("Generated S3 object key: %s", object_key)

    # 5. Save the data to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    
    # Log the success of the data storage in S3
    logger.info("Successfully stored data in S3: %s/%s", bucket_name, object_key)

    # Return the response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully stored weather data for {city} at {now}",
            "s3_object": object_key
        })
    }
