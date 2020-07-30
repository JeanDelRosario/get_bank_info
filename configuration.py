import yaml
import os

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

user = os.environ[cfg['bank_login']['user_var']]
password = os.environ[cfg['bank_login']['password_var']]

reports_download_directory = 'helpers/DataCreator/downloads'

debit_accounts =  cfg['bank_scrapper']['debit_accounts'] # How many accounts you have. If this number is set incorrectly, the script can crash and/or give innacurate information.
credit_accounts = cfg['bank_scrapper']['credit_accounts'] # How many credit card accounts you have.

dollar_saving_accounts = cfg['data_creator']['dollar_saving_accounts']
dollar_saving_accounts = [str(acct) for acct in dollar_saving_accounts]

dollar_to_usd_rate = cfg['data_creator']['dollar_to_usd_rate']
rules_path = cfg['data_creator']['rules_path']

Gsheet_upload_enabled = cfg['Gsheet']['enabled']

if Gsheet_upload_enabled:
  Gsheet_credentials_file = cfg['Gsheet']['Gsheet_credentials_file']
  Gsheet_Id = cfg['Gsheet']['Gsheet_Id']
