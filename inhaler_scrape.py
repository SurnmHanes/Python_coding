import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.rightbreathe.com/?s='

html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

# print(soup)


# print('Classses of each h23: ')
# for table in soup.find_all('h3'):
#     print(table.get('class'))

title = []
table = soup.find_all('h3', class_ = 'MedicineDeviceSummary-title')

for item in table:
     title.append(item.text.strip())
# print(title)
subtitle = []

table = soup.find_all('h4')
for item in table:
    subtitle.append(item.text.strip())

# print(subtitle)
data=[]
table=soup.find_all(class_ = 'MedicineDeviceSummary-info')
for item in table:
    data.append(item.text.strip())
df = pd.DataFrame(columns=['Title', 'Subtitle', 'Data'])


# add title data as column to dataframe
df = df.assign(Title=title)


# add subtitle data as column to dataframe
df = df.assign(Subtitle=subtitle)


# add data as column to dataframe
df=df.assign(Data=data)

# split data by new line character
df['Data'] = df['Data'].str.split('\n')

# df = df.explode('Data')
# print(df)

# df.to_csv('inhalers.csv')
# print('csv updated')

# split data column into separate columns based on new lines
df1 = pd.DataFrame(df['Data'].values.tolist())

# join dataframe and new columns together in columns
df1 = pd.concat([df, pd.DataFrame(df['Data'].values.tolist())], axis=1)
# print(df1)

# drop original data column (which was a list)
df_adj=df1.drop(df1.columns[2], axis=1)
# print(final_df)

df_adj.to_excel('inhalers.xlsx', index=False)
print('xlsx updated')