from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# set up Beautiful Soup for quarterback data
homepage = "https://www.sports-reference.com/cfb/years/2023-passing.html"
url = urlopen(homepage)
stats = BeautifulSoup(url, features='html.parser')

col_headers = stats.find_all('tr')[1]
col_headers = [i.getText() for i in col_headers.findAll('th')]
rows = stats.find_all('tr')[1:]
qb_data = []

# parse through data of quarterbacks and add to a list
for i in range(100):
    qb_data.append([col.getText() for col in rows[i].findAll('td')])

qb_df = pd.DataFrame(qb_data, columns=col_headers[1:])
qb_df.columns.values[-1] = 'RushTD'
qb_df.columns.values[-2] = 'RushAvg'
qb_df.columns.values[-3] = 'RushYds'
qb_df.columns.values[-4] = 'RushAtt'
#
# # filter out irrelevant statistics (such as non-aggregated stats)
relevant_stats = ['G', 'Att', 'Pct', 'Yds', 'Y/A', 'AY/A', 'TD', 'Int', 'Rate', 'RushYds', 'RushTD']
qb_df = qb_df[['Player', 'School'] + relevant_stats]
#
# convert data objects to numerical values
for i in relevant_stats:
    qb_df[i] = pd.to_numeric(qb_df[i])

# filter out quarterbacks with less than 1000 passing yards
qb_df = qb_df.query('Yds >= 1000')

qb_df['Int%'] = round(qb_df['Int'] / qb_df['Att'] * 100, 2)
qb_df['Y/G'] = round(qb_df['Yds'] / qb_df['G'], 2)
qb_df.drop(columns=['G', 'Att', 'Yds', 'TD', 'Int'], inplace=True)

# rank each quarterback according to every statistic
for column in qb_df:
    if column == 'Player' or column == 'School':
        continue
    elif column == 'Int%' or column == 'Sk%':
        qb_df[column + ' Rank'] = qb_df[column].rank(ascending=True).astype(int)
    else:
        qb_df[column + ' Rank'] = qb_df[column].rank(ascending=False).astype(int)

qb_list = []
for qb in qb_df['Player']:
    qb_list.append(qb)

# print(qb_df.to_string())

