import os
from typing import List

import pandas as pd

from .helpers import combine_similar_dfs, add_meta_info_df, try_read_csv


def handle_date_and_dollars(df: pd.DataFrame, dollar_to_dop: float) -> pd.DataFrame:
    """
  Formats the df date to yyyy-mm-dd and transform dollar transactions to Dominican Pesos
  """

    df['Year'] = df['Date'].str[-4:]
    df['Month'] = df['Date'].str[-7:].str[:2]
    df['Day'] = df['Date'].str[:2]

    df['Date'] = df['Year'] + '-' + df['Month'] + '-' + df['Day']

    numeric = ['Debit', 'Credit', 'Balance']

    for n in numeric:
        df.loc[df['Currency'] == 'Dolar', n] = df.loc[df['Currency'] == 'Dolar', n] * dollar_to_dop

    return df


def combine_savings_df(df_list: List[pd.DataFrame]) -> pd.DataFrame:
    df = combine_similar_dfs(df_list, 'Ahorros')
    return df


def combine_credit_cards_df(df_list: List[pd.DataFrame]) -> pd.DataFrame:
    df = combine_similar_dfs(df_list, 'Tarjeta de Credito')
    return df


def read_csv(self, dollar_saving_account: List[str] = None, csv_path: str = 'downloads'):
    """
  Reads the csv files in the download directory.
  Adds a column indicating which type of account it is based in the file name.
  If dollar_saving_account is provided, if a file has it in its name, adds the dolar currency
  """
    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, csv_path)
    files = os.listdir(full_path)

    df_list = []
    encodings = ['ISO-8859', 'latin-1', 'utf-8', 'utf-16', 'utf-16-le', 'utf-16-be']

    for f in files:
        print(f"Reading file {f}")

        csv_path = os.path.join(full_path, f)

        for encoding in encodings:
            df = try_read_csv(csv_path, encoding)

            if df is None:
                continue

            break

        if dollar_saving_account:
            df = add_meta_info_df(df, f, dollar_saving_account)

        df_list.append(df)

    self.df_list = df_list
