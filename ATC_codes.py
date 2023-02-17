from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import date
import os
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

start = time.time()


# STEP 1 - GET LIST OF ALL INITIAL LETTERS FOR ATC CODES
# STEP 2 - GET MAX NUMBER OF PAGES ACROSS ALL THESE INITIAL LETTERS ( By interrogating Code = "initial letter" pages, stripping back codes that are on this page for each of step 1 letters and finding max)
# STEP 3 - ASSUME FOURTH & FIFTH CHARACTERS ARE A - Z // scrape the actual letters involved, append to a list and then de-duplicate list using set() method
# STEP 4 - LOOP THROUGH URLs WITH 5 CHARACTER CODES USING STEP 2 AND STEP 3 AND BRING BACK ALL ATC CODES AND NAMES          

# added this to ensure when run on system didn't crash. Not sure what it does!
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
driver=webdriver.Chrome(options=options)


# STEP 1
# ATC code index URL
url = 'https://www.whocc.no/atc_ddd_index/'

# navigate to ATC Code start page
driver.get(url)

# initiate an empty list
details = []

# find first row of data using XPATH address
paragraph = driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div[1]/p')

# loop through all rows, splitting out text and adding to the details list
for item in paragraph:
    item = item.text.split('\n')
    for i in item:
        details.append(i[0])
# print(details)

print( "Step 1 completed")
# STEP 2

url2 = 'https://www.whocc.no/atc_ddd_index/?code=' 
url2_part2 = '&showdescription=no'

# initiate an empty list
chapter_nrs = []

# for each letter in the details list from step 1, navigate to URL
for item in details:
    driver.get(url2+str(item)+url2_part2)

    # find the paragraph block and loop through, collecting the digits
    paragraph = driver.find_elements(By.XPATH, '//*[@id="content"]/p[2]')
    for item in paragraph:
        item = item.text.split('\n')
        for i in item:
             i = i[1:3]
             # append these digits to the chapter_nrs list
             chapter_nrs.append(i)

# print(chapter_nrs)

# convert to set and back again to deduplicate elements in list
chapter_nrs = set(chapter_nrs)
chapter_nrs = list(chapter_nrs)

print("Step 2 completed")
# STEP 3

# initiate an empty list
subchapter = []

# loop through details list from step 1 and chapter_nrs list from step 2
for item in details:
    for chapter in chapter_nrs:
        # navigate to sub URLs
         driver.get(url2+str(item)+str(chapter) + url2_part2)

        # find paragraph and split out text by new line character
         paragraph = driver.find_elements(By.XPATH, '//*[@id="content"]/p[2]')
         for p in paragraph:
            p = p.text.split('\n')
            for word in p:

                # take first 4 characters only and append to subchapter list
                word = word[:4]
                subchapter.append(word)

# deduplicate list elements by converting to set and back again
subchapter = set(subchapter)
subchapter = list(subchapter)


# initiate empty list
final_list = []

# loop through elements of subchapter list
for item in subchapter:
    driver.get(url2+str(item)+ url2_part2)
    paragraph = driver.find_elements(By.XPATH, '//*[@id="content"]/p[2]')
    
    # for each element in paragraph return only first 5 characters and append to final_list
    for para in paragraph:
        para = para.text.split('\n')
        for item in para:
            item = item[:5]
            final_list.append(item)

# list comprehension to remove empty string elements in list
new_list = [x for x in final_list if x != '']
new_list.sort()

print("steps 3 and 4 completed")

# STEP 5

# initiate empty list
table = []

# loop through list created in step 4, navigate to subURL
for item in new_list:

    # some subURLs do not have a table present so have to use try/except
    try:
        driver.get(url2+str(item)+url2_part2)
        
        # collect up all rows for a given code
        k = driver.find_elements(By.XPATH, '//*[@id="content"]/ul/table/tbody/tr')
        
        # isolate first row
        l = k[1].text

        # check whether the first item of the first row matches the items in the new_list
        # this is to stop the situation where the first row of table for a given code has no ATC code
        # and therefore gets the wrong info when we fill down later 
        m = any(item in l for item in new_list)
        
        # only if the first item in the first row is an ATC code, continue
        if str(m)=="True":
            
            # find table rows and then for each one, find the table data and return the stripped text
            for j in driver.find_elements(By.XPATH,  '//*[@id="content"]/ul/table/tbody/tr'):
                row_data = j.find_elements(By.TAG_NAME, 'td') 
                row = [i.text.strip() for i in row_data]
                # append the text to the table list
                table.append(row)
    except:
            pass

# convert table list into panda dataframe
df = pd.DataFrame(table)

# promote first row to header
# grab first row
new_header = df.iloc[0]

# reset dataframe to exclude first row
df = df[1:]

# add first row back as column names
df.columns = new_header

# filter dataframe to remove rows where ATC code column = ATC code i.e. table header 
df = df.loc[df['ATC code'] != 'ATC code']
# print(df)

df.to_csv('ATC_Codes.csv', index = False )

df = pd.read_csv(r'C:\Users\NeilHanes\python\tutorial\ATC_Codes.csv')
print("intial phase completed")
print('\n')

# create a list of the columns that need to be filled down
cols = ['ATC code', 'Name']

# take all of the dataframe rows and only those columns in cols and fill down
df.loc[:,cols] = df.loc[:,cols].ffill()

df.to_csv('ATC_Codes.csv', index = False )

print('completed')
end = time.time()

print(end - start)
