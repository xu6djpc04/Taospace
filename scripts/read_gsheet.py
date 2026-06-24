from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import openpyxl

TOKEN_PATH = r'C:\Users\kevin\.credentials\token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FILE_ID = '1nvY4Axa1xTC_I3qcYa4qt6GS4ghOuUsu'
TARGET_GID = 993832965

creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
drive = build('drive', 'v3', credentials=creds)

# 先確認檔案類型
meta = drive.files().get(fileId=FILE_ID, fields='name,mimeType').execute()
print(f"檔名：{meta['name']}")
print(f"類型：{meta['mimeType']}")

mime = meta['mimeType']

if 'google-apps.spreadsheet' in mime:
    # 原生 Google Sheets → export
    request = drive.files().export_media(
        fileId=FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    # Excel 或其他 → 直接下載
    request = drive.files().get_media(fileId=FILE_ID)

buf = io.BytesIO()
downloader = MediaIoBaseDownload(buf, request)
done = False
while not done:
    status, done = downloader.next_chunk()
    print(f"下載進度：{int(status.progress() * 100)}%")

buf.seek(0)
wb = openpyxl.load_workbook(buf, data_only=True)

# 找到對應 GID 的工作表（Excel 沒有 GID，用順序對應）
print(f"\n工作表清單：")
for i, name in enumerate(wb.sheetnames):
    print(f"  [{i}] {name}")

# 目標 GID=993832965，通常是第幾個工作表需要人確認
# 先列出第一張試試，或讓使用者指定名稱
print("\n請告訴我要讀哪張工作表的名稱或編號。")
