from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import os
import pandas as pd
from xlsxwriter.utility import xl_rowcol_to_cell
import win32com.client as win32
import shutil

def download_and_move_file(download_button):
        
        # click the button to download
        download_button.click()
        
        # ensure file downloads completely
        seconds = 0
        dl_wait = True
        
        # create while loop using two variables
        while dl_wait:
            
            # wait a second
            sleep(1)
            
            # check download file to see if .crdownload file still exists -> indicates file is not fully downloaded yet
            # if it does exist increment seconds by 1 and continue round loop 
            dl_wait = False
            for fname in os.listdir(r'C:\Users\NeilHanes\Downloads'):
                if fname.endswith('.crdownload'):
                    dl_wait = True
                    seconds += 1
        
        # create list of all files in download folder
        paths = [os.path.join(r'C:\Users\NeilHanes\Downloads', basename) for basename in os.listdir(r'C:\Users\NeilHanes\Downloads')] 
        
        # find latest file and isolate the file name
        source = max(paths, key = os.path.getctime)
        source_name = os.path.basename(source)

        # destination folder to be AY Projects
        destination_folder = r'C:\Users\NeilHanes\NeoHealth Hub Ltd\NeoSypher - 08 - Cosmos\AY Projects'
        
        # create name of destination file
        destination = destination_folder + "\\" + source_name

        # move file from downloads to AY Projects
        shutil.move(source, destination)

def get_scotland():

    # Scottish prescribing data
    url = 'https://www.opendata.nhs.scot/ne/dataset/prescriptions-in-the-community'

    # message to user
    print('processing Scotland...')

    # navigate to Scottish NHS Data Extract page
    driver.get(url)

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

        # use function to download new file
        download_and_move_file(csv_url)
        
        # set Status
        Status = "new file downloaded"
    else:
        print("no new Scottish file")
        Status = "no new file"

    # create dictionary item using this 
    Scot_mth = dict(Country="Scotland", Current_Month=month, Status=Status, Latest_Check=datetime.datetime.now().strftime("%a %d %b %Y  %H:%M"))
                
    # add dictionary item to details list
    return Scot_mth 


def get_england():

   # English prescribing data
    url = 'https://opendata.nhsbsa.net/dataset/english-prescribing-data-epd'

    # message to user
    print('processing England...')

    # navigate to web page
    driver.get(url)

       # scroll down on web page
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")
   
    # collate a list of datasets
    data = driver.find_elements(By.XPATH, '//*[@id="dataset-resources"]/ul/li')
   
    # pick out first item in data list (which will be the latest months data)
    results = data[0]
   
    # store the name of the latest month
    eng_month = results.text
    
    # split it into three by "-" delimiter
    head, sep, tail = eng_month.partition("-")
    tail = tail.replace("Explore", "").strip()
    
    sleep(3)
    
    if not ( ( df['Country'] == 'England' ) & ( df['Current_Month'].str.contains(tail[:3]))).any():
        
        # click the accept cookies button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ccc-recommended-settings"]'))).click()
            
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

        # use function to download zip folder
        download_and_move_file(zip_file)
        
        # set Status
        Status = "new file downloaded"
    else:
        print("no new English file")
        Status = "no new file"       
        
    # create dictionary item using current month and status as per above
    England_mth = dict(Country="England", Current_Month=tail.strip(), Status=Status, Latest_Check=datetime.datetime.now().strftime("%a %d %b %Y  %H:%M"))

    return England_mth                
   
def get_nire():   
    
    # N Ireland prescribing data
    url_ire = 'https://www.opendatani.gov.uk/dataset/gp-prescribing-data'

    # message to user
    print('processing N Ireland...')

    # navigate to N Ireland NHS Data Extract page
    driver.get(url_ire)

    # find first row of data using XPATH address
    first_row = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/div[2]/a')

    # convert webelement list object into text string
    latest_month = first_row.text

    # split out string into 3 parts and only take last part (this is the part after the comma and represents the date)
    first_part, sep, last_part = latest_month.partition(",")

    month = last_part.strip()

    # compare the month obtained from web against the month showing in dataframe by comparing first 3 letters of both
    if not ( ( df['Country'] == 'N Ireland' ) & ( df['Current_Month'].str.contains(month[:3]))).any():

        # if the months differ find all elements whose link text has Download in it
        link = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Download')
        
        # maximise window in order to see Download buttons
        driver.maximize_window()

        # pause
        sleep(3)
        
        # then click on the first elements in this list and use function to download file
        first_link = link[0]
        download_and_move_file(first_link)
        
        # pause to allow download to begin
        sleep(5)

        Status = "new file downloaded"
    else:
        print("no new N Irish file")
        Status = "no new file"

    # create dictionary item using this 
    NI_mth = dict(Country="N Ireland", Current_Month=month, Status=Status, Latest_Check=datetime.datetime.now().strftime("%a %d %b %Y  %H:%M"))

    return NI_mth         

def get_wales():
   
    # run Welsh prescribing data extraction
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
        
        # use function to download file
        download_and_move_file(h1[0])
        
        # set Status
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
    Welsh_mth = dict(Country="Wales", Current_Month=month, Status=Status, Latest_Check=datetime.datetime.now().strftime("%a %d %b %Y  %H:%M"))
    
    return Welsh_mth   

# open existing excel so we can compare latest month data
df = pd.read_excel(r'C:\Users\NeilHanes\python\tutorial\Latest_Month.xlsx')

# added this to ensure when run on system didn't crash. Not sure what it does!
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')
driver=webdriver.Chrome(options=options)

# create a list of responses from the 4 countries (which will be 4 dictionaries)
responses = [ 
    get_scotland(), 
    get_england(), 
    get_nire(), 
    get_wales()
]

# create an empty list
dataframes = []

# iterate through the responses list converting the dictionary elements into dataframes
for response in responses:
    df = pd.DataFrame(response, index = [0])

    # then append those dataframes to the list (so now have list of dataframes)
    dataframes.append(df)

# concatenate the dataframes elements in the list into one dataframe
df = pd.concat(dataframes)
 
with pd.ExcelWriter(r'C:\Users\NeilHanes\python\tutorial\Latest_Month.xlsx', engine = 'xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='output')
    workbook = writer.book
    worksheet = writer.sheets['output']
    worksheet.set_zoom(90)
    sheet_format = workbook.add_format({ 'align': 'center', 'font_name': 'Century Gothic'})
    worksheet.set_column('A:D', 25, sheet_format)

# send dataframe as an email
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'neilhanes@neosypher.com'
mail.Subject = 'GP Prescribing Data Status'
# mail.Body = 'This is a test'
mail.HTMLBody = df.to_html(index=False) #this field is optional
        
mail.Send()
    
print("process completed")
