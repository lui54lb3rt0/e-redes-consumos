import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurations here
usr = InsertYourNIFHere
psw = InsertYourPSWHere
dwnPath = "//mnt//c//Users//lsilva//Downloads//"

now = datetime.datetime.now()
date_string = now.strftime("%Y%m%d")
filename = "Consumos_"+date_string+".xlsx"
fp = dwnPath +filename

# Create a new Chrome browser
chrome_options = webdriver.ChromeOptions()

"""
# Headless option not working
# Headless option
chrome_options.add_argument('--headless')

# Enable the file download dialog
chrome_options.add_experimental_option("prefs", {
  "download.prompt_for_download": True,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
}) 
"""

driver = webdriver.Chrome(".//chromedriver.exe",chrome_options=chrome_options)

driver.get("https://balcaodigital.e-redes.pt/consumptions/history")

items = driver.find_elements(By.XPATH, '//button')
for item in items:
    #print(item.text)
    if item.text == "Aceitar todos os cookies":
        item.click()


WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-default/main/nz-content/div/div[2]/section[1]/div[2]/div/div/ul/li[1]/div[2]'))

btnParticular = driver.find_elements(By.XPATH, '/html/body/app-root/nz-layout/app-default/main/nz-content/div/div[2]/section[1]/div[2]/div/div/ul/li[1]/div[2]')

for x in range(len(btnParticular)):
    #print(btnParticular[x].text)
    if btnParticular[x].text == "Particular":
        btnParticular[x].click()

WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.XPATH, '//*[@id="username"]'))
username = driver.find_element(By.XPATH, '//*[@id="username"]')
username.send_keys(usr)

pw = driver.find_element(By.XPATH, '//*[@id="labelPassword"]')
pw.send_keys(psw) 

btnClick = driver.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-default/main/nz-content/div/div[2]/section[1]/app-sign-in/div/div/form/div[2]/div/button/span')
btnClick.click()

WebDriverWait(driver, timeout=40).until(lambda d: d.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-history/app-masterpage/main/nz-layout/nz-content/section/div[3]/div/app-premises/app-cards/div/section[2]/div[1]/nz-card/div'))
local = driver.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-history/app-masterpage/main/nz-layout/nz-content/section/div[3]/div/app-premises/app-cards/div/section[2]/div[1]/nz-card/div/div[2]/ul')
local.click()

WebDriverWait(driver, timeout=50).until(lambda d: d.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-history/app-masterpage/main/nz-layout/nz-content/app-consumptions-chart/section/div/div/div/div[2]/div[2]/p/a/strong'))
download = driver.find_element(By.XPATH, '/html/body/app-root/nz-layout/app-history/app-masterpage/main/nz-layout/nz-content/app-consumptions-chart/section/div/div/div/div[2]/div[2]/p/a/strong')
download.click()

# Wait 2s to finish download
time.sleep(2)

driver.quit()

# read by default 1st sheet of an excel file
dataframe1 = pd.read_excel(fp)
print(dataframe1)

# Delete file
os.unlink(fp)
