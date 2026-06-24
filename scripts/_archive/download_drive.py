import os
import io
import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

creds_path = 'C:/Users/kevin/.credentials/token.json'
base_dir = 'C:/Users/kevin/Desktop/Taospace/references/雲端研習資料下載_1150615'
os.makedirs(base_dir, exist_ok=True)

if not os.path.exists(creds_path):
    print('token.json not found')
    sys.exit(1)

creds = Credentials.from_authorized_user_file(creds_path, ['https://www.googleapis.com/auth/drive.readonly'])
service = build('drive', 'v3', credentials=creds)

mime_map = {
    'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
    'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
    'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
}

def download_file(file_id, file_name, mime_type, target_dir):
    try:
        if mime_type in mime_map:
            export_mime, ext = mime_map[mime_type]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            file_path = os.path.join(target_dir, file_name + ext)
        elif mime_type == 'application/vnd.google-apps.folder':
            return # handled separately
        else:
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join(target_dir, file_name)
            
        print(f"Downloading {file_name} to {file_path}...")
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        print(f"Downloaded {file_name}")
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")

def download_folder(folder_id, current_dir):
    os.makedirs(current_dir, exist_ok=True)
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    
    items = results.get('files', [])
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            download_folder(item['id'], os.path.join(current_dir, item['name']))
        else:
            download_file(item['id'], item['name'], item['mimeType'], current_dir)

print("Starting download...")
# 114 班務傳題講師研習 folder
download_folder('1hFMeE62HJyJwY76DgWMoM0CdF8tW9I4i', os.path.join(base_dir, '114_班務傳題講師研習'))
# 111暑期班務經營及傳題研習 folder
download_folder('1UBAViLNMviEO7LTTATXUQRGskT-mSH2Y', os.path.join(base_dir, '111_暑期班務經營及傳題研習'))
# 114年暑期各組研習報名表
file = service.files().get(fileId='1-cYUTVR8A7UybTm2HRbmXoJZgnSOe1vY5R-e_1kw7hI').execute()
download_file(file['id'], file['name'], file.get('mimeType'), base_dir)
# 114年暑期-班務組研習
file = service.files().get(fileId='1cRIFqHiLrQtaVoN7GextMeSKMBf9ZA7ZcSp9wUt997Q').execute()
download_file(file['id'], file['name'], file.get('mimeType'), base_dir)

print("All downloads completed.")
