from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import pandas as pd
from datetime import date

# added this to ensure when run on system didn't crash. Not sure what it does!
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(options=options)

df = pd.read_csv(r'C:\Users\NeilHanes\python\tutorial\Latest Months2.csv')

print("processing Wales...")

# navigate to Wales NHS Data Extract page
driver.get(r'https://nwssp.nhs.wales/ourservices/primary-care-services/general-information/data-and-publications/prescribing-data-extracts/general-practice-prescribing-data-extract/')

sleep(3)

driver.execute_script("window.scroll(0,1800)","")

sleep(5)
# find first row of data using XPATH address
h1 = driver.find_elements(By.XPATH, '/html/body/div[8]/div[2]/div/section/div[1]/div/div/div[18]/div/div[1]/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td/a' )

# convert webelement list object h1 into text string
latest_month = h1[0].text

# split out string into 3 parts and only take first part (this gets rid of the text in parentheses)
first_part, sep, last_part = latest_month.partition("(")

# split first part into 3 to get rid of "GP Data Extract -" prefix
head, sep, tail = first_part.partition("-")

# print third part with no white space
month = tail.strip()

if not ( ( df['Country'] == 'Wales' ) & ( df['Current_Month'].str.contains(month[:3]))).any():


# From h1 list, isolate first item and click to download zip file
    h1[0].click()

# ensure csv downloads completely
    seconds = 0
    dl_wait = True

# create while loop using two variables
    while dl_wait and seconds < 120:
    
    # wait a second
        sleep(1)

    # check download file to see if .crdownload file still exists -> indicates file is not fully downloaded yet
    # if it does exist increment seconds by 1 and continue round loop 
        dl_wait = False
        for fname in os.listdir(r'C:\Users\NeilHanes\Downloads'):
            if fname.endswith('.crdownload'):
                dl_wait = True
                seconds += 1
    Status = "new file downloaded"
else:
    print("no new Welsh file")
    Status = "no new file"

# convert webelement list object h1 into text string
latest_month = h1[0].text

# split out string into 3 parts and only take first part (this gets rid of the text in parentheses)
first_part, sep, last_part = latest_month.partition("(")

# split first part into 3 to get rid of "GP Data Extract -" prefix
head, sep, tail = first_part.partition("-")

# print third part with no white space
month = tail.strip()

# convert into dictionary item
Welsh_mth = dict(Country="Wales", Current_Month=month, Status=Status, Latest_Check=date.today())

# print(Welsh_mth)