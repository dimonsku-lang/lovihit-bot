import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_URL

def get_gsheet_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(GOOGLE_SHEET_URL).sheet1
    return sheet.get_all_records()

def get_categories():
    data = get_gsheet_data()
    return list(set(item['Категория'] for item in data))

def get_products_by_category(category):
    data = get_gsheet_data()
    return [item for item in data if item['Категория'] == category]
