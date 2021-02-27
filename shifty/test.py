import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
scope = [
	    'https://www.googleapis.com/auth/drive',
	    'https://www.googleapis.com/auth/drive.file'
	    ]
file_name = 'client_id.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)
sheet = client.open('Kiosk Log').worksheet('Test')
# sheet = client.open("Kiosk Log").sheet2

row=["hello"]
sheet.insert_row(row, 2) #Insert row as number 2