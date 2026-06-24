import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds_path = 'C:/Users/kevin/.credentials/token.json'
if os.path.exists(creds_path):
    creds = Credentials.from_authorized_user_file(creds_path, ['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)
    
    file_id = '1cRIFqHiLrQtaVoN7GextMeSKMBf9ZA7ZcSp9wUt997Q'
    file = service.files().get(fileId=file_id).execute()
    mime_type = file.get('mimeType')
    print(f"File: {file.get('name')}, MimeType: {mime_type}")
    
    try:
        if 'document' in mime_type:
            content = service.files().export(fileId=file_id, mimeType='text/plain').execute()
            print(content.decode('utf-8'))
        elif 'spreadsheet' in mime_type:
            content = service.files().export(fileId=file_id, mimeType='text/csv').execute()
            print(content.decode('utf-8'))
        else:
            print("Cannot export this mime type.")
    except Exception as e:
        print(f"Error exporting: {e}")
else:
    print('token.json not found')
