import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds_path = 'C:/Users/kevin/.credentials/token.json'
if os.path.exists(creds_path):
    creds = Credentials.from_authorized_user_file(creds_path, ['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)
    
    folder_id = '1UBAViLNMviEO7LTTATXUQRGskT-mSH2Y'
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=20,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])
    if not items:
        print('No files found in folder.')
    else:
        print('Files in folder:')
        for item in items:
            print(f"{item['name']} ({item['id']}) - {item['mimeType']}")
else:
    print('token.json not found')
