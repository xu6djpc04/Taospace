import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds_path = 'C:/Users/kevin/.credentials/token.json'
if os.path.exists(creds_path):
    creds = Credentials.from_authorized_user_file(creds_path, ['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        q="name contains '暑期研習' or name contains '班務研習' or name contains '暑期班務'",
        pageSize=20,
        fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")
else:
    print('token.json not found')
