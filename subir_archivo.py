import boto3
import base64
import json

def lambda_handler(event, context):
    # Parsear el body (string o dict)
    raw_body = event.get('body', {})
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Body inválido, debe ser JSON'})
            }
    else:
        body = raw_body

    bucket = body.get('bucket')
    folder = body.get('folder')
    filename = body.get('filename')
    base64_content = body.get('base64')

    # Validación de campos
    if not bucket or not folder or not filename or not base64_content:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan campos: bucket, folder, filename o base64'})
        }

    # Construir ruta final: folder/filename
    s3_path = f"{folder.rstrip('/')}/{filename}"

    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket, s3_path).put(Body=base64.b64decode(base64_content))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Archivo subido correctamente',
                'bucket': bucket,
                'path': s3_path
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
