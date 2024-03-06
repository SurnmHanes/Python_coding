
#%%
import pandas as pd
import json
from glob import glob

#%%
def extract_to_csv(d):
    # create a dataframe of the innings data
    # create another dataframe for the dates - test matches played over 5 successive days
    # obtain the list of teams involved 
    df = pd.DataFrame(d['innings'])
    df_dates = pd.DataFrame( d['info']['dates'])
    team_list = d['info']['teams']

    all_innings = []
    
    # first check that England is one of the teams involved. Otherwise can just skip.
    # df['overs'] is the ball by ball list per innings. So we need to iterate over each of the innings
    if 'England' in team_list:    
        
        for i in range( len(df['overs'])):
        
            innings = df['overs'][i]
                        
            # flatten the innings and including the deliveries dict
            df_innings = pd.json_normalize(innings, "deliveries")

            # choose specific columns and ensure each innings dataframe only has these columns
            columns = ['batter', 'bowler', 'non_striker', 'runs.batter', 'runs.total', 'wickets' ]
            df_innings = df_innings.reindex(columns=columns)

            # add three additional columns: the match innings, the match date and the team who are batting
            df_innings['innings'] = i + 1
            df_innings['startdate'] = df_dates[0][0]
            df_innings['team'] = df['team'][i]
            
            # add innings to all_innings list
            all_innings.append(df_innings)

    # all_innings is a list of dataframes which we then concatenate: 
        whole_test = pd.concat(all_innings)
    
    # export to csv
        whole_test.to_csv('WholeMatch.csv', index=False, mode='a', header=['batter', 'bowler', 'non_striker', 'runs.batter', 'runs.total', 'wickets', 'innings', 'startdate', 'team'])

# %%

# iteate over each json file in the folder and run the extract_to_csv function defined above
for fname in glob("C:/Users/NeilHanes/Downloads/tests_male_json/*.json"):
    with open(fname, 'r') as json_data:
        d = json.load(json_data)
        extract_to_csv(d)


# %%
