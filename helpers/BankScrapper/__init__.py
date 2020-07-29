import os
import shutil
import sys
from selenium import webdriver
from time import sleep

sys.path.append('helpers/BankScrapper')

class BankScrapper():

  from credit_card_methods import get_credit_cards_reports
  from account_methods import get_accounts_reports

  URL = 'https://www.banreservas.com.do/TuBancoPersonas/Login.aspx?ReturnUrl=%2fTuBancoPersonas%2f'

  def __init__(self, chromedriver_path:str="/usr/local/bin/chromedriver",
    download_directory:str='downloads',
    credit_accounts:int=1,
    debit_accounts:int=1):

    # Cleans download_directory before starting
    self.clean_directory(download_directory)

    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, download_directory)

    driver = self.set_up_driver(chromedriver_path, full_path)

    self.driver = driver
    self.credit_accounts = credit_accounts
    self.debit_accounts = debit_accounts
    self.download_directory = download_directory

  
  def clean_directory(self, directory_path:str):
    """
    Cleans specified directory if it exists. If it doesn't exists, it doesn't do anything.
    """
    if os.path.exists(directory_path):
      shutil.rmtree(directory_path)


  def set_up_driver(self, chromedriver_path:str, download_directory:str) -> webdriver:
    """
    Returns a Webdriver object with a configured download_directory.
    """
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_directory}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chromeOptions)

    return driver
  

  def login(self, username, password):

    self.driver.get(self.URL)

    inputElement = self.driver.find_element_by_id("ctl00_MainHolder_TextBoxUserName")
    inputElement.send_keys(username)

    sleep(5)

    self.driver.find_element_by_id("ctl00_MainHolder_linkButton_SecondStep").click()
    
    self.driver.find_element_by_id("ctl00_MainHolder_Password").send_keys(password)

    self.driver.find_element_by_id("ctl00_MainHolder_loginButton").click()

    sleep(5)


  def go_back_to_home(self):
    """
    Returns back to home.
    """

    self.driver.switch_to.default_content()

    self.driver.switch_to.frame("leftFrame")

    self.driver.find_element_by_class_name("home").click()

    self.driver.switch_to.default_content()
    
    
  def close(self):
    """
    Closes web driver.
    """
    self.driver.close()
