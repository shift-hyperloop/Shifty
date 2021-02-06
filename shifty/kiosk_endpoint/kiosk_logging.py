import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

def log_everything(product_name, username, stock_change, price, user_balance_before, user_balance_after, stock_before_change, stock_after_change):
	"""
	Inputs:
	product name
	username            = name of user buying
	stock_change         = How many products are bought
	price                = current price of product
	user_balance_after   = balance of user after purchase
	user_balance_before  = balance of user before purchase
	stock_before_change  = stock before purchase
	stock_after_purchase = stock after purchase
	"""
	#Authorize the API
	scope = [
	    'https://www.googleapis.com/auth/drive',
	    'https://www.googleapis.com/auth/drive.file'
	    ]
	file_name = 'client_id.json'
	creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
	client = gspread.authorize(creds)
	sheet = client.open("Kiosk Log").sheet1


	row = [datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), username, product_name, stock_change, price, user_balance_before, user_balance_after, stock_before_change, stock_after_change]
	sheet.insert_row(row, 2) #Insert row as number 2

def log_new_products(name):
	scope = [
	    'https://www.googleapis.com/auth/drive',
	    'https://www.googleapis.com/auth/drive.file'
	    ]
	file_name = 'client_id.json'
	creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
	client = gspread.authorize(creds)
	sheet = client.open('Kiosk Log').worksheet('New products')

	row = [datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), name]
	sheet.insert_row(row, 2) #Insert row as number 2