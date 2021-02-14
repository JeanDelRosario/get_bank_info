import pandas as pd

def implement_rules(self, df: pd.DataFrame, rules_path:str='rules.txt') -> pd.DataFrame:
  """
  Implements the rules for categorizing transactions and adding other columns, as specified in rules.txt, to a dataframe.
  Rules.txt structure is (query) | column_to_transform, value
  Where query is optional and it must be a valid pandas query.
  """
  df = df.reset_index()

  with open(rules_path) as f:
    for line in f:

      if not line.strip():
        continue

      flag = line[:2]

      if flag == '-s':
        df = set_flag(df, line)
      elif flag == '-l':
        df = like_flag(df, line)
      elif flag == '-a':
        df = array_flag(df, line)
      elif flag == '-r':
        df = raw_flag(df, line)
      else:
        print("No flags in line to process in rules.txt")

  return df
      
    
def set_flag(df: pd.DataFrame, line: str) -> pd.DataFrame:
  """
  Creates the column specified
  """

  line = line[2:]

  arguments = line.split('|')

  if len(arguments) != 2:
    print("Error in -s flag rules.txt, needs 2 arguments")

  column, value = [arg.strip() for arg in arguments]

  df[column] = value

  return df


def like_flag(df: pd.DataFrame, line: str) -> pd.DataFrame:

  line = line[2:]

  arguments = line.split('|')

  if len(arguments) != 4:
    print("Error in -l flag rules.txt")

  word, column_filter, column, value = [arg.strip() for arg in arguments]

  index_to_change = df[df[column_filter].str.upper().str.contains(word)].index.values.tolist()

  df.loc[index_to_change, column] = value

  return df


def array_flag(df: pd.DataFrame, line: str) -> pd.DataFrame:

  line = line[2:]

  arguments = line.split('|')

  if len(arguments) != 4:
    print("Error in -a flag rules.txt")

  array, column_filter, column, value = [arg.strip() for arg in arguments]

  array = array.split(',')

  df.loc[df[column_filter].isin(array), column] = value

  return df


def raw_flag(df: pd.DataFrame, line: str) -> pd.DataFrame:

  line = line[2:]

  arguments = line.split('|')

  if len(arguments) != 3:
    print("Error in -r flag rules.txt")

  query, column, value = [arg.strip() for arg in arguments]

  index_to_change = df.query(query, engine='python').index.values.tolist()

  df.loc[index_to_change, column] = value

  return df
