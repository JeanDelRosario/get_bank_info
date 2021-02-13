import os
from configuration import configuration as cfg

from helpers.BankScrapper import BankScrapper
from helpers.DataCreator import DataCreator

user = input("Please enter your username:\n")
password = input("Please enter your password:\n")

bank_scrapper = BankScrapper(chromedriver_path=cfg.chrome_driver_path, download_directory=cfg.reports_download_directory, debit_accounts=cfg.debit_accounts, credit_accounts=cfg.credit_accounts)
bank_scrapper.login(user, password)
bank_scrapper.get_accounts_reports()
bank_scrapper.get_credit_cards_reports()
bank_scrapper.close()

data_creator = DataCreator(cfg.reports_download_directory, cfg.dollar_to_usd_rate, cfg.dollar_saving_accounts, cfg.rules_path)
data_creator.process()

if cfg.Gsheet_upload_enabled:
  data_creator.upload_df_to_gsheet(cfg.Gsheet_credentials_file, cfg.Gsheet_Id)
