from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
import numpy as np

start = time.time()

url = 'https://www.whocc.no/atc_ddd_index/'
initial = []

page = requests.get(url).text

doc = BeautifulSoup(page, "html.parser")

paragraph = doc.find_all("p")[1]
contents = paragraph.contents

for i in range( 0, len(contents), 3):
    initial.append(contents[i])

print("step 1 complete")

# step 2

three_chars = []

for x in initial:
    url2 = f"https://www.whocc.no/atc_ddd_index/?code={x.strip()}&showdescription=no"
    step2_page = requests.get(url2).text
    step2_doc = BeautifulSoup(step2_page, "html.parser")
    step2_paragraph = step2_doc.find_all("p")[1]
    step2_contents = step2_paragraph.contents

    for y in range( 0, len(step2_contents), 3):
        three_chars.append(step2_contents[y].strip())

new_three_chars = [x for x in three_chars if x != '']
new_three_chars.sort()

print("step 2 complete")

# step 3 

four_chars = []

for a in new_three_chars:
    step3_url = f"https://www.whocc.no/atc_ddd_index/?code={a.strip()}&showdescription=no"
    step3_page = requests.get(step3_url).text
    step3_doc = BeautifulSoup(step3_page, "html.parser")
    step3_paragraph = step3_doc.find_all("p")[1]
    step3_contents = step3_paragraph.contents
    for b in range(0, len(step3_contents), 3):
        four_chars.append(step3_contents[b].strip())

new_four_chars = [x for x in four_chars if x != '']
new_four_chars.sort()
print("step 3 complete")

# step 4
print( "processing step 4...")
five_chars = []

for a in new_four_chars:
    
    step4_url = f"https://www.whocc.no/atc_ddd_index/?code={a.strip()}&showdescription=no"
    step4_page = requests.get(step4_url).text
    step4_doc = BeautifulSoup(step4_page, "html.parser")
    step4_paragraph = step4_doc.find_all("p")[1]
    step4_content = step4_paragraph.contents
    for b in range (0, len(step4_content), 3):
        five_chars.append(step4_content[b].strip())
    
final_list = [ x for x in five_chars if x != '']
final_list.sort()

print(final_list)
print()
print(len(final_list))

# final step 
print("processing final step...")
l = []
counter = 1
for a in final_list:
    print(f"collating record: {counter}")
    try:
        # navigate to URL
        step5_url = f"https://www.whocc.no/atc_ddd_index/?code={a.strip()}&showdescription=no"
        step5_page = requests.get(step5_url).text
        step5_doc = BeautifulSoup(step5_page, "html.parser")
        step5_paragraph = step5_doc.find_all("div", id = "content")
        trimmed_text = [n.text.strip() for n in step5_paragraph]
        for t in trimmed_text:
            t = t.split('\n')
            x = [x.replace('New search\xa0\xa0\xa0\xa0Show text from Guidelines', '') for x in t]
        
        headings = x[0:4]

        # find table within html
        tbody = step5_doc.find("table")
        
        # collate all rows
        rows = tbody.find_all('tr')

        first_row = rows[1].text

        # check whether the first item of the first row matches the items in the new_list
        # this is to stop the situation where the first row of table for a given code has no ATC code
        # and therefore gets the wrong info when we fill down later 
        m = any(item in first_row for item in final_list)

         # only if the first item in the first row is an ATC code, continue
        if str(m)=="True":
                
            # iterate through rows
            for r in rows:

                # find all the data tags in the row
                d = r.find_all('td')

                # for each data tag, extract the stripped text and create a list 
                row = [x.text.strip() for x in d] + headings
                l.append(row)   
    except:
        pass
    counter = counter + 1   

# transfer list to dataframe
df = pd.DataFrame(l)

# take first row at headers
new_header = df.iloc[0]

# convert header data to a list
new_header = list(new_header)

# change the 7 - 10th elements to header titles (rather than header data) 
new_header[6:10] = ['Anatomical Main Group', 'Therapeutic Subgroup' , 'Pharmacological subgroup' , 'Chemical subgroup']

# adjust dataframe by removing first (header) row
df = df[1:]

# add back in first row as header
df.columns = new_header

# filter ATC code column to remove any rows where entry = "ATC code"
df = df.loc[df['ATC code'] != 'ATC code']

# isolate columns we need to fill down
cols = ['ATC code', 'Name']

# transform empty string values into NaN (so we can fill down later)
df = df.replace(r'^\s*$', np.nan, regex=True)

# fill down columns
df.loc[:,cols] = df.loc[:,cols].ffill()

# split newly created columns into two - first the code, then the name
df[['Anatomical Main Group Code','Anatomical Main Group Name' ]] = df['Anatomical Main Group'].str.split(' ', 1, expand=True)
df[['Therapeutic Subgroup Code', 'Therapeutic Subgroup Name'  ]] = df['Therapeutic Subgroup'].str.split(' ', 1, expand=True)
df[['Pharmacological Subgroup Code', 'Pharmacological Subgroup Name'  ]] = df['Pharmacological subgroup'].str.split(' ', 1, expand=True)
df[['Chemical Subgroup Code', 'Chemical Subgroup Name'  ]] = df['Chemical subgroup'].str.split(' ', 1, expand=True)

# drop the original columns now they've been split out
df.drop(["Anatomical Main Group", 'Therapeutic Subgroup', 'Pharmacological subgroup','Chemical subgroup'], axis = 1, inplace=True)

# change font from capitals to Title case 
df['Anatomical Main Group Name'] = df['Anatomical Main Group Name'].str.title()
df['Therapeutic Subgroup Name'] = df['Therapeutic Subgroup Name'].str.title()
df['Pharmacological Subgroup Name'] = df['Pharmacological Subgroup Name'].str.title()
df['Chemical Subgroup Name'] = df['Chemical Subgroup Name'].str.title()

# transfer to csv
df.to_csv('ATC_Codes.csv', index = False)

print('Completed')
end = time.time()

print(end - start)