from time import sleep

def get_credit_cards_reports(self):
  """
  Downloads all the credit card reports that were configured by self.credit_accounts.
  """
  for i in range(self.credit_accounts):

    go_credit_card_download(self.driver, i, self.debit_accounts)

    credit_card_download(self.driver, "DOP")

    self.go_back_to_home()

    sleep(5)

    go_credit_card_download(self.driver, i, self.debit_accounts)

    credit_card_download(self.driver, "USD")

    self.go_back_to_home()
    
    print(f"Sucesss credit account {i}")

    sleep(5)


def credit_card_download(driver, currency:str="DOP"):
    """
    From the download page of the credit card, downloads the CSV report of the credit card by the chosen
    currency. Only supports DOP and USD.
    """
    if currency == "USD":
      sleep(5)
      
      element = driver.find_element_by_xpath("//a[@data-dk-dropdown-value='US']")
      sleep(5)
      driver.execute_script("arguments[0].click();", element)

    driver.find_element_by_id("ctl00_MainHolder_periodCreditCard_dateTextBoxDateFrom").send_keys("01/01/2018")

    element = driver.find_element_by_id("ctl00_MainHolder_periodCreditCard_linkButtonConsultar")

    driver.execute_script("arguments[0].click();", element)

    driver.find_element_by_id("toggle").click()

    sleep(5)

    # Download CSV
    element = driver.find_element_by_id("ctl00_MainHolder_CreditCardMovements_linkButtonCSV")
    driver.execute_script("arguments[0].click();", element)

    sleep(10)


def go_credit_card_download(driver, i: int, debit_accounts: int):
  """
  Goes to credit card download page from main screen
  """
  driver.switch_to.frame("mainFrame")

  sleep(5)

  driver.find_element_by_id("showLinkCredits").click()
  sleep(2)

  driver.find_element_by_id(f"ctl00_MainHolder_CreditCardGridCP_CreditcardsView_tccell{i}_5").click()
  sleep(5)
  
  element = driver.find_elements_by_xpath("//a[@data-dk-dropdown-value='/TuBancoPersonas/Pages/Common/ProductStatus.aspx']")[i + debit_accounts]

  sleep(5)

  driver.execute_script("arguments[0].click();", element)

