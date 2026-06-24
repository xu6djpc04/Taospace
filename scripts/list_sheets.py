from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = r'C:\Users\kevin\.credentials\token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1nvY4Axa1xTC_I3qcYa4qt6GS4ghOuUsu'

meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = meta.get('sheets', [])
for s in sheets:
    props = s['properties']
    print(f"GID={props['sheetId']}  名稱={props['title']}  列數={props.get('gridProperties',{}).get('rowCount','?')}")
