import boto3
import os
import uuid
import json
from datetime import datetime, timedelta
 
s3 = boto3.client('s3')
polly = boto3.client('polly')
 
BUCKET = os.environ['AUDIO_BUCKET']
 
def handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
 
    try:
        # Handle OPTIONS request
        if event.get('httpMethod') == 'OPTIONS':
            return {
                "statusCode": 200,
                "headers": headers,
                "body": ""
            }
        
        # Parse JSON body
        if not event.get('body'):
            raise ValueError("Request body is required")
            
        body = json.loads(event['body'])
        text = body.get('text', '').strip()
        
        if not text:
            raise ValueError("Text is required")
            
        voice = body.get('voice', 'Joanna')
        output_format = body.get('outputFormat', 'mp3')
        speed = body.get('speed', 'medium')
        
        # Map frontend format to Polly format
        format_mapping = {
            'mp3': 'mp3',
            'ogg_vorbis': 'ogg_vorbis',
            'pcm': 'pcm'
        }
        
        polly_format = format_mapping.get(output_format, 'mp3')
        
        # Get file extension
        extension_mapping = {
            'mp3': 'mp3',
            'ogg_vorbis': 'ogg',
            'pcm': 'pcm'
        }
        
        file_extension = extension_mapping.get(polly_format, 'mp3')
        
        # Wrap text with SSML for speed control
        ssml_text = f'<speak><prosody rate="{speed}">{text}</prosody></speak>'
        
        file_name = f"{uuid.uuid4()}.{file_extension}"
 
        # Call Polly
        response = polly.synthesize_speech(
            Text=ssml_text,
            TextType='ssml',
            OutputFormat=polly_format,
            VoiceId=voice
        )
 
        # Upload to S3
        s3.put_object(
            Bucket=BUCKET,
            Key=file_name,
            Body=response['AudioStream'].read(),
            ContentType=f"audio/{file_extension}"
        )
 
        # Generate signed URL
        expires_in = 3600
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET, "Key": file_name},
            ExpiresIn=expires_in
        )
        
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
 
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "success": True,
                "data": {
                    "audioUrl": url,
                    "voice": voice,
                    "format": output_format,
                    "textLength": len(text),
                    "expiresAt": expires_at.isoformat() + "Z"
                }
            })
        }
 
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "success": False,
                "error": "Invalid JSON in request body"
            })
        }
    except ValueError as e:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")  # For CloudWatch logs
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "success": False,
                "error": "Internal server error"
            })
        }