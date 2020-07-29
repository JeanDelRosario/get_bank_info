import pandas as pd

from typing import List

def combine_similar_dfs(df_list:List[pd.DataFrame], type_of_account:str) -> pd.DataFrame:

  account_df_list = []

  for df in df_list:
    
    if df.shape[0] != 0:
      if df.TIPO_CUENTA[0] == type_of_account:
        account_df_list.append(df)
  
  df = account_df_list[0]
  for i in range(len(account_df_list) - 1):
    df = df.append(account_df_list[i+1])

  return df


def add_meta_info_df(df: pd.DataFrame, filename: str, dollar_saving_account: List[str]) -> pd.DataFrame:
  """
  Adds a column indicating which type of account it is based in the file name.
  If dollar_saving_account is provided, if a file has it in its name, adds the dolar currency to saving accounts.
  """
  if 'CuentaMovimientos' in filename:
    for d in dollar_saving_account:
      if d in filename:
        df['Currency'] = 'Dolar'
        break
      else:
        df['Currency'] = 'PesoDominicano'
      
    df['TIPO_CUENTA'] = 'Ahorros'
  elif 'TarjetaDeCredito' in filename:
    df['TIPO_CUENTA'] = 'Tarjeta de Credito'

  return df


def check_df_bad_read(df: pd.DataFrame) -> bool:
  """
  Checks if a pandas dataframe was correctly read. If it was, returns True, else False.
  As of now it only checks if the entire dataframe is Nan.
  """
  if df.shape[0] != 0 and df.iloc[:,0].isnull().all():
    return False
  
  return True


def try_read_csv(csv_path: str, encoding:str) -> pd.DataFrame:
  """
  Tries to read csv file with provided encoding.
  If it errors out or returns a bad data frame, the functions returns None.
  """
  try:
    df = pd.read_csv(csv_path, encoding=encoding, thousands=',')

    if check_df_bad_read(df):
      print(f"Good encoding {encoding}")

      return df
    else:
      print("bad encoding")

  except Exception:
    return None
