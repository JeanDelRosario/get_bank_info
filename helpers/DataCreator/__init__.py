import os
import shutil
import sys
import pandas as pd
import numpy as np
import codecs
from csv import reader
from pathlib import Path
from typing import List

bank_scrapper_path = Path("helpers/DataCreator")

sys.path.append(str(bank_scrapper_path))

class DataCreator():

  from implement_rules import implement_rules
  from Google.upload import upload_df_to_gsheet
  from data_manipulation.data_manipulation import read_csv, combine_credit_cards_df, combine_savings_df, handle_date_and_dollars

  def __init__(self, csv_path:str, dollar_to_dop:float, dollar_saving_accounts:List[str]=None, rules_path:str='rules.txt'):
    self.dollar_saving_accounts = dollar_saving_accounts
    self.dollar_to_dop = dollar_to_dop
    self.df_list = []
    self.csv_path = csv_path
    self.rules_path = rules_path
    self.final_df = None


  def process(self):

    self.read_csv(self.dollar_saving_accounts, self.csv_path)

    credit_card_df = self.combine_credit_cards_df()

    savings_df = self.combine_savings_df()

    df = pd.concat([credit_card_df, savings_df])

    self.test_df(df)

    self.final_df = self.handle_date_and_dollars(df, self.dollar_to_dop)

    self.final_df = self.implement_rules(self.final_df, self.rules_path)

    self.final_df = self.final_df.sort_values(by=['Date', 'Debit'], ascending=[False, False])

    cols = list(self.final_df.columns)
    cols = [cols[-1]] + cols[:-1]
    self.final_df = self.final_df[cols]

    database_path = Path("database")

    if not os.path.exists(database_path):
        os.mkdir(database_path)

    self.final_df.to_csv( str(database_path / 'bank_transactions.csv') )

    self.clean_directory(self.csv_path)


  def test_df(self, df: pd.DataFrame):
    """
    Test Dataframe to check whether or not it has the expected columns.
    """
    if self.df_has_good_format(df):
      print("Success, resulting data frame is what is expected.")

    else:
      print("Error, resulting data frame is not what is expected. Instead got:")
      print(a.columns)


  def df_has_good_format(self, df:pd.DataFrame) -> bool:

    expected_columns = ['Product', 'Date', 'Reference', 'Concept', 'Currency', 'Debit',
       'Credit', 'TIPO_CUENTA', 'Unnamed: 7', 'Transaction id', 'Balance',
       'Description', 'Unnamed: 9']

    return np.array_equal(np.sort(df.columns), np.sort(expected_columns))

  def clean_directory(self, directory_path:str):
    """
    Cleans specified directory if it exists. If it doesn't exists, it doesn't do anything.
    """
    if os.path.exists(directory_path):
      shutil.rmtree(directory_path)
