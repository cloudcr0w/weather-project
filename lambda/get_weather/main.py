import json
import requests

def lambda_handler(event, context):
    # Tymczasowy endpoint (np. London) – docelowo parametry można przekazywać z event.
    city = "London"
    api_key = "TU_WSTAW_SWÓJ_API_KEY"

    url = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    # Prosty log:
    print(f"Response for {city}: {data}")

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
