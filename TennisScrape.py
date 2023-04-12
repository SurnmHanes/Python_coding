from bs4 import BeautifulSoup
import pandas as pd

def get_mens_rankings():

    # go to URL
    url = "https://www.espn.com/tennis/rankings"
    
    # find all tables in URL
    tables = pd.read_html(url)

    # limit to first table and put into dataframe
    df = pd.DataFrame(tables[0])

    # limit to first 20 rows only
    df  = df.head(20)

    # drop the second column
    df.drop(df.columns[1], axis = 1, inplace=True)

    # export to csv
    df.to_csv('Mens_Tennis_Ranks.csv', index = False)

def get_womens_rankings():

    # go to URL
    url = "https://www.espn.com/tennis/rankings/_/type/wta"
    
    # find all tables in URL
    tables = pd.read_html(url)

    # limit to first table and put into dataframe
    df = pd.DataFrame(tables[0])

    # limit to first 20 rows only
    df  = df.head(20)

    # drop the second column
    df.drop(df.columns[1], axis = 1, inplace=True)

    # export to csv
    df.to_csv('Womens_Tennis_Ranks.csv', index = False)


get_mens_rankings()
get_womens_rankings()

print("Data Extracts complete")



 


