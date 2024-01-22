from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# set up Beautiful Soup for quarterback data
homepage = "https://www.pro-football-reference.com/players/J/JackLa00.htm"
url = urlopen(homepage)
stats = BeautifulSoup(url, features='html.parser')

col_headers = stats.find_all('tr')[1]
col_headers = [i.getText() for i in col_headers.findAll('th')]
col_headers[2] = "Home/Away"

rows = stats.find_all('tr')[1:]
qb_data = []

# parse through regular season weeks
for i in range(1, 18):
    row_data = []
    for col in rows[i].findAll(['th', 'td']):
        row_data.append(col.getText())
    if row_data[0] == '':
        continue
    qb_data.append(row_data)

# rename columns appropriately
qb_df = pd.DataFrame(qb_data, columns=col_headers[0:])
qb_df.columns.values[-2] = 'Rush Y/A'
qb_df.columns.values[-4] = 'RushTD'
qb_df.columns.values[-5] = 'RushYds'
qb_df.columns.values[-6] = 'RushAtt'

# filter for relevant stats
relevant_stats = ['Date', 'Team', 'Home/Away', 'Opp', 'Result', 'Cmp%', 'Yds', 'TD', 'TD%', 'Int%',
                  'Y/A', 'Rate', 'Sk%', 'RushAtt', 'RushYds', 'RushTD', 'Rush Y/A', 'Fmb']

qb_df = qb_df[relevant_stats]

# update home/away games column
for i in range(len(qb_df['Home/Away'].values)):
    if qb_df['Home/Away'].values[i] == '@':
        qb_df['Home/Away'].values[i] = 'Away'
    else:
        qb_df['Home/Away'].values[i] = 'Home'

print(qb_df.to_string())
