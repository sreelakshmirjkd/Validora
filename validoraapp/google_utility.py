
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from google.oauth2.service_account import Credentials
import gspread



def get_gspread_client():
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=settings.SCOPES
    )
    client = gspread.authorize(creds)
    return client

SCOPES=settings.SCOPES

def get_google_credentials():

    json_key_str = settings.GOOGLE_SERVICE_ACCOUNT_FILE

    if not json_key_str:

        raise Exception("Google credentials not set in environment variables.")
    
    info = json.loads(json_key_str)

    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    return credentials

def get_sheets_service():

    creds = get_google_credentials()

    return build('sheets', 'v4', credentials=creds)

def get_drive_service():
    

    creds = get_google_credentials()
    
    return build('drive', 'v3', credentials=creds)









