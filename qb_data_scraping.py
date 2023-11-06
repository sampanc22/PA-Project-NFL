from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# set up Beautiful Soup for quarterback data
homepage = "https://www.pro-football-reference.com/years/2023/passing.htm"
url = urlopen(homepage)
stats = BeautifulSoup(url)

col_headers = stats.find_all('tr')[0]
col_headers = [i.getText() for i in col_headers.findAll('th')]

rows = stats.find_all('tr')[1:]
qb_data = []

# parse through data of quarterbacks and add to a list
for i in range(35):
    qb_data.append([col.getText() for col in rows[i].findAll('td')])

qb_df = pd.DataFrame(qb_data, columns=col_headers[1:])
qb_df.columns.values[-6] = 'YdsSk'

# filter out irrelevant statistics (such as non-aggregated stats)
relevant_stats = ['Yds', 'Cmp%', 'TD%', 'Int%', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'QBR', 'Sk%']
qb_df = qb_df[['Player', 'Tm', 'Age'] + relevant_stats]

# convert data objects to numerical values
for i in relevant_stats:
    qb_df[i] = pd.to_numeric(qb_df[i])

# filter out quarterbacks with less than 1000 passing yards
qb_df = qb_df.query('Yds >= 1000')

# rank each quarterback according to every statistic
for column in qb_df:
    if column == 'Player' or column == 'Tm' or column == 'Age':
        continue
    elif column == 'Int%' or column == 'Sk%':
        qb_df[column + ' Rank'] = qb_df[column].rank(ascending=True).astype(int)
    else:
        qb_df[column + ' Rank'] = qb_df[column].rank(ascending=False).astype(int)

print(qb_df.to_string())

