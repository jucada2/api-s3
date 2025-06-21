import boto3
import json

def lambda_handler(event, context):
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)

    bucket_name = body.get('bucket')
    if not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Falta el nombre del bucket'})
        }

    s3 = boto3.client('s3')

    try:
        s3.create_bucket(Bucket=bucket_name)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Bucket "{bucket_name}" creado correctamente'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }
