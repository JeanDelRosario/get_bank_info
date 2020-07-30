import os

from helpers.BankScrapper import BankScrapper
from helpers.DataCreator import DataCreator

user = os.environ['BUSER']
password = os.environ['BPASSWORD']

reports_download_directory = 'helpers/DataCreator/downloads'

debit_accounts = 2 # How many accounts you have. If this number is set incorrectly, the script can crash and/or give innacurate information.
credit_accounts = 2 # How many credit card accounts you have.

dollar_saving_accounts = ['9600863829']
dollar_to_usd_rate = 57.20
rules_path = 'rules.txt'

Gsheet_credentials_file = 'credentials.json'
Gsheet_Id = '1I-DXBkhXE6TAtmhzgEF-RmUrZDlKrWexEJXYdJXiYho'

bank_scrapper = BankScrapper(download_directory=reports_download_directory, debit_accounts=debit_accounts, credit_accounts=credit_accounts)
bank_scrapper.login(user, password)
bank_scrapper.get_accounts_reports()
bank_scrapper.get_credit_cards_reports()
bank_scrapper.close()

data_creator = DataCreator(reports_download_directory, dollar_to_usd_rate, dollar_saving_accounts, rules_path)
data_creator.process()
data_creator.upload_df_to_gsheet(Gsheet_credentials_file, Gsheet_Id)
