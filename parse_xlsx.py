import os
import random
from random import randrange
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import config


def get_service_sacc():
    """
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    :return:
    """
    creds_json = os.path.dirname(__file__) + "/colizeum-manager-62d9eeec649e.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


def get_request_to_sheet(current_month: str):
    sheet = get_service_sacc().spreadsheets()
    response = sheet.values().get(spreadsheetId=config.test_expenses_sheet,
                                  range=f"{current_month}!A1:C100").execute()
    return response


def append_values_to_expenses(information: list):
    sheet = get_service_sacc().spreadsheets()
    response = sheet.values().append(spreadsheetId=config.test_expenses_sheet,
                                     range='март!A1',
                                     valueInputOption='RAW',
                                     body={'values': information}
                                     ).execute
    print(information)


#append_values_to_expenses([[random.randrange(10, 90) for i in range(3)]])
print(get_request_to_sheet('Март'))