import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy
import sqlite3

# this script is called as part of CricInfoPipeline.py and doesn't need to be run separately

database_location = "sqlite:///cricket.sqlite"
url = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=wickets;page=' 
url_part_2 = ';size=200;spanmax1=31+Dec+2022;spanmin1=01+Jan+2020;spanval1=span;team=1;template=results;type=bowling;view=innings'

# create an empty list to hold table rows
details = []

# find out how many pages will need to loop over
# go to initial page 
html = requests.get('https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=wickets;size=200;spanmax1=31+Dec+2022;spanmin1=01+Jan+2020;spanval1=span;team=1;template=results;type=bowling;view=innings').text

# change html to Python friendly format
soup = BeautifulSoup(html, 'html.parser')

# isolate area on page where page numbers are displayed
page_display = soup.find_all( 'table', class_ = 'engineTable')[1]

# return the maximum page number
max_page = page_display.find_all('b')[1].text

# convert to integer to use in range  
max_page = int(max_page)

# print(max_page)

# loop through all pages to scrape table data
for page in range(1,max_page + 1):

        
        # print progress message to user
        print("processing bowlers page " + str(page)+ " of " + str(max_page) + "..." )
        
        # navigate to web page
        html = requests.get(url + str(page)+url_part_2).text

        # change html to Python friendly format
        soup = BeautifulSoup(html, 'html.parser')

        # find relevant table in the url
        table1 = soup.find_all('table', class_ = 'engineTable')[2]

        # pick out the headers and loop through them to get list
        headers = []
        for i in table1.find_all('th'):
            title = i.text
            headers.append(title)
             
        # loop through all table rows and append to details list
        for j in table1.find_all("tr", class_ = "data1"):
            row_data = j.find_all('td') 
            row = [i.text for i in row_data]
            details.append(row)
    
# initiate the dataframe
df = pd.DataFrame(details, columns = headers)

# remove the blank column 
df_adj = df.drop(df.columns[7], axis=1)

# # filter out the rows where batter did not bowl (DNB)
df_adj = df_adj[(df_adj['Overs'] != 'DNB') & (df_adj['Overs'] != 'sub')   ]

# change data type of Start Date column to date
df_adj['Start Date'] = pd.to_datetime(df_adj['Start Date'])

# Export to csv
df_adj.to_csv('Test_Cricket_Bowlers.csv', index = False )

# connect to existing database
# engine = sqlalchemy.create_engine(database_location)
conn = sqlite3.connect("cricket.sqlite")

# # create table in database
# sql_query = """
# CREATE TABLE IF NOT EXISTS test_batting(
#     Player, VARCHAR(100),
#     Runs, VARCHAR(100)
#     Mins,VARCHAR(100)
#     BF,VARCHAR(100)
#     4s,VARCHAR(100)
#     6s,VARCHAR(100)
#     SR,VARCHAR(100)
#     Inns,VARCHAR(100)
#     Opposition,VARCHAR(100)
#     Ground,VARCHAR(100)
#     Start Date, VARCHAR(100)
# )
# """

# Export to sql database table (test_bowling)
df_adj.to_sql('test_bowling', conn, index=False, if_exists='replace')
  
# conn.commit()
conn.close()
print('Bowlers export complete')