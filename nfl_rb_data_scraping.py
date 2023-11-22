from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# set up Beautiful Soup for running back data
homepage = "https://www.pro-football-reference.com/years/2023/rushing.htm"
url = urlopen(homepage)
stats = BeautifulSoup(url, features='lxml')

col_headers = stats.find_all('tr')[1]
col_headers = [i.getText() for i in col_headers.findAll('th')]

rows = stats.find_all('tr')[2:]
rb_data = []

# parse through data of running backs and add to a list
for i in range(50):
    if i != 0 and i % 29 == 0:
        continue
    rb_data.append([col.getText() for col in rows[i].findAll('td')])

rb_df = pd.DataFrame(rb_data, columns=col_headers[1:])

# filter out irrelevant statistics
relevant_stats = ['G', 'GS', 'TD', 'Y/A', 'Y/G', 'Fmb']
rb_df = rb_df[['Player', 'Tm', 'Age', 'Pos'] + relevant_stats]

# convert data objects to numerical values
for i in relevant_stats:
    rb_df[i] = pd.to_numeric(rb_df[i])

# filter out non-running backs and running backs with less than 5 GS
rb_df = rb_df.query('GS >= 5')
rb_df = rb_df[rb_df['Pos'] == 'RB']

# rank each running back according to every statistic
for column in rb_df:
    if column == 'Player' or column == 'Tm' or column == 'Age' or column == 'Pos' or column == 'G' or column == 'GS':
        continue
    elif column == 'Fmb':
        rb_df[column + ' Rank'] = rb_df[column].rank(ascending=True).astype(int)
    else:
        rb_df[column + ' Rank'] = rb_df[column].rank(ascending=False).astype(int)

print(rb_df.to_string())


