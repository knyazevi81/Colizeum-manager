import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import config


def get_service_simple():
    return build('sheets', 'v4', developerKey=config.test_token)


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


# service = get_service_simple()
service = get_service_sacc()
sheet = service.spreadsheets()

# https://docs.google.com/spreadsheets/d/xxx/edit#gid=0


# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
# response = sheet.values().get(spreadsheetId=config.test_sheet, range="Лист1!A1:D1").execute()

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
response = sheet.values().batchGet(spreadsheetId=config.test_sheet, ranges=["Лист1"]).execute()

print(response)