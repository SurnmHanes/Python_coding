from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date
import os
import pandas as pd

df = pd.read_csv(r'C:\Users\NeilHanes\python\tutorial\Latest Months2.csv')

# TODO: run it headlessly so browser doesn't open

# added this to ensure when run on system didn't crash. Not sure what it does!
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(options=options)

# Scottish prescribing data
url = 'https://www.opendata.nhs.scot/ne/dataset/prescriptions-in-the-community'

# message to user
print('processing Scotland...')

# navigate to Scottish NHS Data Extract page
driver.get(url)

# initiate an empty list
details = []

# find first row of data using XPATH address
month = driver.find_element(By.XPATH, "//*[@id='dataset-resources']/ul/li")

# split the first item by carriage return to get list and bring back the first item in that list
month = month.text.split("\n")[0]

# split the string into 3 based on white space and pick out the 3rd item (which will be the latest month) 
month = month.split(" ",2)[2]
month = month.strip()

if not ( ( df['Country'] == 'Scotland' ) & ( df['Current_Month'].str.contains(month[:3]))).any():

    # now find all elements whose link text has Prescribing Data in 
    link = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Prescribing Data')

    # click on the first elements in this list
    link[0].click()

    # on new webpage, find the csv URL by XPATH
    csv_url = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/section/div/p/a')

    # and download the csv
    csv_url.click()

    # ensure csv downloads completely
    seconds = 0
    dl_wait = True

    # create while loop using two variables
    while dl_wait and seconds < 120:
        
        # wait a second
        sleep(1)
        print(seconds)
        # check download file to see if .crdownload file still exists -> indicates file is not fully downloaded yet
        # if it does exist increment seconds by 1 and continue round loop 
        dl_wait = False
        for fname in os.listdir(r'C:\Users\NeilHanes\Downloads'):
            if fname.endswith('.crdownload'):
                dl_wait = True
                seconds += 1
    Status = "new file downloaded"
else:
    print("no new Scottish file")
    Status = "no new file"

# create dictionary item using this 
Scot_mth = dict(Country="Scotland", Current_Month=month, Status=Status, Latest_Check=date.today())
            
# add dictionary item to details list
details.append(Scot_mth)

# English prescribing data
url2 = 'https://opendata.nhsbsa.net/dataset/english-prescribing-data-epd'

# message to user
print('processing England...')

# navigate to web page
driver.get(url2)

# scroll down on web page
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")

# collate a list of datasets
data = driver.find_elements(By.XPATH, '//*[@id="dataset-resources"]/ul/li')

# pick out last item in data list (which will be the latest months data)
results = data[-1]

# store the name of the latest month
eng_month = results.text

# split it into three by "-" delimiter
head, sep, tail = eng_month.partition("-")
tail = tail.replace("Explore", "").strip()

results = data[-1]

if not ( ( df['Country'] == 'England' ) & ( df['Current_Month'].str.contains(tail[:3]))).any():

    # click on link related to latest month's data
    results.click()

    # wait for new web page to load
    sleep(3)

    # find on page dropdown button / chevron to access menu where zip file to be downloaded can be found
    dropdown_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/section/div/div[1]/ul/li[1]/div/button')

    # click on this dropdown button / chevron
    dropdown_btn.click()

    # wait to ensure dropdown menu loads fully
    sleep(1)

    # locate zip file download link (as second item in dropdown menu now visible)
    zip_file = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/section/div/div[1]/ul/li[1]/div/ul/li/a[2]')

    # click to download zip file
    zip_file.click()

    # ensure zip downloads completely
    seconds = 0
    dl_wait = True

    # create while loop using two variables
    while dl_wait and seconds < 300:
        
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
    print("no new English file")
    Status = "no new file"       

# create dictionary item using current month and status as per above
England_mth = dict(Country="England", Current_Month=tail.strip(), Status=Status, Latest_Check=date.today())
            
# add dictionary item to details list
details.append(England_mth)

# run Welsh prescribing data extraction
import GPWales

# add welsh dictionary item to details list
details.append(GPWales.Welsh_mth)

# initiate dataframe from details list       
df = pd.DataFrame(details)

# export dataframe to csv file
df.to_csv(r'C:\Users\NeilHanes\python\tutorial\Latest Months2.csv', index=False)

print("process completed")
