# -*- coding: utf-8 -*-
"""上傳單一檔案到 Google Drive 根目錄（或指定資料夾）。

用法：
  python drive_upload.py <本機檔案路徑> [--folder <Drive 資料夾 ID>]

例：
  python drive_upload.py "output/美安事業原音逐字稿_純淨版_115年.m4a"
  python drive_upload.py "output/foo.m4a" --folder 1aBcDeFgHiJkL
"""
import os
import sys
import io
import argparse
import mimetypes

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_DIR = os.path.join(os.path.expanduser("~"), ".credentials")
CREDENTIALS_FILE = os.path.join(
    CREDENTIALS_DIR,
    next(f for f in os.listdir(CREDENTIALS_DIR) if f.startswith("client_secret") and f.endswith(".json")),
)
TOKEN_FILE = os.path.join(CREDENTIALS_DIR, "token_upload.json")


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
        with open(TOKEN_FILE, "w") as fh:
            fh.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def upload_file(local_path: str, folder_id: str | None = None):
    if not os.path.isfile(local_path):
        print(f"找不到檔案：{local_path}")
        sys.exit(1)

    filename = os.path.basename(local_path)
    mime_type, _ = mimetypes.guess_type(local_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    metadata = {"name": filename}
    if folder_id:
        metadata["parents"] = [folder_id]

    service = get_service()
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    print(f"上傳中：{filename}  ({os.path.getsize(local_path) / 1024:.0f} KB)")

    request = service.files().create(body=metadata, media_body=media, fields="id,name,webViewLink")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  進度：{int(status.progress() * 100)}%", end="\r")

    print(f"\n完成！")
    print(f"  檔名：{response['name']}")
    print(f"  連結：{response.get('webViewLink', '（無預覽連結）')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="本機檔案路徑")
    parser.add_argument("--folder", default=None, help="目標 Drive 資料夾 ID（省略 = 根目錄）")
    args = parser.parse_args()
    upload_file(args.file, args.folder)
