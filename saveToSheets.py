# importing the required libraries

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/


def saveToGoogleSheets(userData):
	'''
	userData is a 2-D list
	ex: [["email1","text1"],["email2","text2"]]
	'''
	# Define the scope of the application
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	# add credentials to the account
	creds = ServiceAccountCredentials.from_json_keyfile_name('KPOP101-395016011ef1.json', scope)
	# authorize the clientsheet 
	client = gspread.authorize(creds)
	# get the instance of the Spreadsheet
	sheet = client.open('KPOP101 Newsletter list')
	# get the first sheet of the Spreadsheet
	sheet_instance = sheet.get_worksheet(0)
	# print(sheet_instance.col_count)
	# print(sheet_instance.get_all_records())
	
	# saves the data 
	sheet_instance.insert_rows(userData)