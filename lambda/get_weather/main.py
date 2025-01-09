import json
import requests
import boto3
import datetime

def lambda_handler(event, context):
    # 1. Konfiguracja miasta i klucza API
    city = "Wroclaw,PL"
    api_key = "eb56bc94ccae31d4198ed456691e8d30"  # Pamiętaj o bezpieczeństwie w praktyce!
    bucket_name = "weather-project-raw-data"     # Nazwa Twojego bucketu S3
    s3 = boto3.client("s3")

    # 2. Budowa adresu API (z parametrem units=metric)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    # 3. Pobranie danych z OpenWeatherMap
    response = requests.get(url)
    data = response.json()
    
    # Opcjonalny print do logów (sprawdzenie):
    print("Pobrane dane:", data)

    # 4. Przygotowanie nazwy pliku (klucza) do zapisu w S3
    now = datetime.datetime.utcnow().isoformat()
    # np. "raw/wroclaw,pl/2025-01-10T12:34:56.789012.json"
    object_key = f"raw/{city.lower()}/{now}.json"

    # 5. Zapis danych do S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully stored weather data for {city} at {now}",
            "s3_object": object_key
        })
    }
