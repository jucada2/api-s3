import boto3
import json

def lambda_handler(event, context):
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)

    bucket_name = body.get('bucket')
    folder_name = body.get('folder')

    if not bucket_name or not folder_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan bucket o folder'})
        }

    # En S3, los "directorios" se crean como claves que terminan en "/"
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key=f"{folder_name}/")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Directorio "{folder_name}/" creado en bucket "{bucket_name}"'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }
