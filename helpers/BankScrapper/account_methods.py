from time import sleep

def get_accounts_reports(self):
  
  for i in range(self.debit_accounts):

    go_account_download(self.driver, i)

    account_download(self.driver)

    sleep(5)

    self.go_back_to_home()

    print(f"Sucesss account {i}")

    sleep(5)


def account_download(driver):
  """
  From the download page of the account, downloads the CSV report of the account.
  """

  driver.find_element_by_id("ctl00_MainHolder_period_dateTextBoxDateFrom").send_keys("01/01/2018")

  element = driver.find_element_by_id("ctl00_MainHolder_period_linkButtonConsultar")

  driver.execute_script("arguments[0].click();", element)

  driver.find_element_by_id("toggle").click()

  # Download CSV
  element = driver.find_element_by_id("ctl00_MainHolder_AccountTransactionGrid_linkButtonCSV")
  driver.execute_script("arguments[0].click();", element)


def go_account_download(driver, i: int):
  """
  Goes to account download page from main screen.
  """
  driver.switch_to.frame("mainFrame")

  sleep(5)

  driver.find_element_by_id("showLinkAccounts").click()

  driver.find_element_by_id(f"dk_container_ctl00_MainHolder_AccountGridCP_AccountView_cell{i}_5_AccountsListAcctions").click()

  element = driver.find_elements_by_xpath("//a[@data-dk-dropdown-value='/TuBancoPersonas/Pages/Common/ProductStatus.aspx']")[i]

  sleep(5)

  driver.execute_script("arguments[0].click();", element)
