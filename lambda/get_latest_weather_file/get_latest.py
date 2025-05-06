import boto3
import json

s3 = boto3.client('s3')
BUCKET = 'weather-project-raw-data'
PREFIX = 'raw/wroclaw,pl/'

def lambda_handler(event, context):
    response = s3.list_objects_v2(
        Bucket=BUCKET,
        Prefix=PREFIX
    )

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No files found'})
        }

    latest = max(response['Contents'], key=lambda x: x['LastModified'])

    latest_url = f"https://{BUCKET}.s3.amazonaws.com/{latest['Key']}"

    return {
        'statusCode': 200,
        'body': json.dumps({'latest_url': latest_url})
    }
