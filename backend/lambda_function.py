import json
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError 


dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')


TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ContactSubmissions')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'owner@example.com')      
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'owner@example.com') 

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps('Preflight check successful')
        }

    try:
        body = event.get('body')
        if not body:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing request body'})
            }
        
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        # Extract fields
        name = data.get('name')
        email = data.get('email')
        mobileno = data.get('mobileno')
        address = data.get('address')
        query = data.get('query')

        
        if not all([name, email, mobileno, query]):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing required fields (name, email, mobileno, query)'})
            }

        submission_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'submissionId': submission_id,
                'timestamp': timestamp,
                'name': name,
                'email': email,
                'mobileno': mobileno,
                'address': address or 'N/A',
                'query': query
            }
        )

        # SES EMAIL SEND
        email_subject = f"New Cake Query from {name}"
        email_body = f"""
        You have received a new customer query from your bakery website:

        - Name: {name}
        - Email: {email}
        - Mobile No: {mobileno}
        - Address: {address or 'N/A'}
        
        Query Details:
        {query}

        Timestamp: {timestamp}
        Submission ID: {submission_id}
        """

        try:
            ses.send_email(
                Source=SENDER_EMAIL,
                Destination={'ToAddresses': [RECIPIENT_EMAIL]},
                Message={
                    'Subject': {'Data': email_subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Text': {'Data': email_body, 'Charset': 'UTF-8'}
                    }
                }
            )
        except ClientError as e:
            print("SES Email Error:", e.response['Error']['Message'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Query submitted successfully! We will contact you soon.',
                'submissionId': submission_id
            })
        }

    except Exception as e:
        print("Internal Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
