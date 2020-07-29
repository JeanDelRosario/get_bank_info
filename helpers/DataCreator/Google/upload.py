import pandas as pd
import numpy as np

from Google.Google import Create_Service
from oauth2client.service_account import ServiceAccountCredentials

def upload_df_to_gsheet(self, CLIENT_SECRET_FILE: str, gsheetId: str):
  """
  Uploads a pandas DataFrame specified in the class self.final_df attribute 
  to a Google Sheet specified by the gsheeId.
  CLIENT_SECRET_FILE specifies the filename of a Json file with the credentials necessary
  to authorize the access to Gsheet.
  """

  upload_to_gsheet(self.final_df, CLIENT_SECRET_FILE, gsheetId)
  

def upload_to_gsheet(df: pd.DataFrame, CLIENT_SECRET_FILE: str, gsheetId: str):
  """
  Uploads a pandas DataFrame to a Google Sheet specified by the gsheeId.
  CLIENT_SECRET_FILE specifies the filename of a Json file with the credentials necessary
  to authorize the access to Gsheet.
  """

  API_SERVICE_NAME = 'sheets'
  API_VERSION = 'v4'
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  df.replace(np.nan, '', inplace=True)

  service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

  response_date = service.spreadsheets().values().update(
    spreadsheetId = gsheetId,
    valueInputOption='RAW',
    range='Sheet1!A1',
    body=dict(
      majorDimension='ROWS',
      values=df.T.reset_index().T.values.tolist())
  ).execute()
