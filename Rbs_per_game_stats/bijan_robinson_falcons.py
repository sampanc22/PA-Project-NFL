from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# set up Beautiful Soup for quarterback data
homepage = "https://www.pro-football-reference.com/players/R/RobiBi01.htm"
url = urlopen(homepage)
stats = BeautifulSoup(url, features='html.parser')

col_headers = stats.find_all('tr')[1]
col_headers = [i.getText() for i in col_headers.findAll('th')]
col_headers[2] = "Home/Away"

rows = stats.find_all('tr')[1:]
rb_data = []

# parse through regular season weeks

for i in range(1, 18):
    row_data = []
    for col in rows[i].findAll(['th', 'td']):
        row_data.append(col.getText())
    if row_data[0] == '':
        continue
    rb_data.append(row_data)

# rename columns appropriately
rb_df = pd.DataFrame(rb_data, columns=col_headers[0:])

rb_df.columns.values[12] = 'RecYds'
rb_df.columns.values[14] = 'RecTD'
rb_df.columns.values[-7] = 'Catch%'

# filter for relevant stats
relevant_stats = ['Date', 'Team', 'Home/Away', 'Opp', 'Result', 'Att', 'Yds', 'TD', 'Y/A',
                  'Tgt', 'Rec', 'RecYds', 'Y/R', 'RecTD', 'Catch%', 'Touch', 'Y/Tch', 'YScm', 'Fmb']

rb_df = rb_df[relevant_stats]

# update home/away games column
for i in range(len(rb_df['Home/Away'].values)):
    if rb_df['Home/Away'].values[i] == '@':
        rb_df['Home/Away'].values[i] = 'Away'
    else:
        rb_df['Home/Away'].values[i] = 'Home'

print(rb_df.to_string())
