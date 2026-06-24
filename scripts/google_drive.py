import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_DIR = os.path.join(os.path.expanduser('~'), '.credentials')
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, next(
    f for f in os.listdir(CREDENTIALS_DIR) if f.startswith('client_secret') and f.endswith('.json')
))
TOKEN_FILE = os.path.join(CREDENTIALS_DIR, 'token.json')

EXPORT_MIME = {
    'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
    'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
    'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
}


def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def search_files(keyword, max_results=50):
    service = get_service()
    query = f"name contains '{keyword}' and trashed = false"
    results = service.files().list(
        q=query,
        pageSize=max_results,
        fields="files(id, name, mimeType, size, modifiedTime)"
    ).execute()
    return results.get('files', [])


def download_file(service, file_info, dest_dir):
    file_id = file_info['id']
    file_name = file_info['name']
    mime = file_info['mimeType']
    os.makedirs(dest_dir, exist_ok=True)

    if mime in EXPORT_MIME:
        export_mime, ext = EXPORT_MIME[mime]
        if not file_name.endswith(ext):
            file_name += ext
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    elif mime == 'application/vnd.google-apps.folder':
        return
    else:
        request = service.files().get_media(fileId=file_id)

    dest_path = os.path.join(dest_dir, file_name)
    with io.FileIO(dest_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    print(f"  已下載：{file_name}")


def list_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, mimeType, size)"
    ).execute()
    return results.get('files', [])


def download_folder_recursive(service, folder_id, folder_name, dest_dir):
    current_dest = os.path.join(dest_dir, folder_name)
    os.makedirs(current_dest, exist_ok=True)
    items = list_folder(service, folder_id)
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            download_folder_recursive(service, item['id'], item['name'], current_dest)
        else:
            try:
                download_file(service, item, current_dest)
            except Exception as e:
                print(f"  跳過 {item['name']}：{e}")


if __name__ == '__main__':
    keyword = '排課'
    dest = os.path.join(BASE_DIR, 'Taofiles', '雲端排課檔案')

    print(f"搜尋「{keyword}」...\n")
    files = search_files(keyword)
    service = get_service()

    if not files:
        print("找不到相關檔案。")
    else:
        print(f"找到 {len(files)} 個項目，開始下載...\n")
        for f in files:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                print(f"進入資料夾：{f['name']}")
                download_folder_recursive(service, f['id'], f['name'], dest)
            else:
                try:
                    download_file(service, f, dest)
                except Exception as e:
                    print(f"  跳過 {f['name']}：{e}")

    print("\n完成。")
