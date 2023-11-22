import math
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from college_qb_data_scraping import qb_list

# set up Beautiful Soup for quarterback data
homepage = "https://www.sports-reference.com/cfb/years/2023-rushing.html"
url = urlopen(homepage)
stats = BeautifulSoup(url, features='lxml')

col_headers = stats.find_all('tr')[1]
col_headers = [i.getText() for i in col_headers.findAll('th')]
rows = stats.find_all('tr')[2:]
rb_data = []

# parse through data of quarterbacks and add to a list
for i in range(100):
    if rows[i].find('td') is None:
        continue
    player = rows[i].find('td').getText()
    if player in qb_list:
        continue
    rb_data.append([col.getText() for col in rows[i].findAll('td')])

rb_df = pd.DataFrame(rb_data, columns=col_headers[1:])
rb_df.columns.values[7] = 'RushTD'
rb_df.columns.values[6] = 'RushAvg'
rb_df.columns.values[5] = 'RushYds'
rb_df.columns.values[4] = 'RushAtt'
rb_df.columns.values[11] = 'RecTD'
rb_df.columns.values[10] = 'RecAvg'
rb_df.columns.values[9] = 'RecYds'
rb_df.columns.values[8] = 'Rec'

# filter out irrelevant statistics (such as non-aggregated stats)
relevant_stats = ['RushAtt', 'RushYds', 'RushAvg', 'RushTD', 'Rec', 'RecYds', 'RecAvg', 'RecTD']
rb_df = rb_df[['Player', 'School'] + relevant_stats]

# convert data objects to numerical values


for i in range(len(rb_df['RecAvg'])):
    if (rb_df['RecAvg'][i]) == '':
        rb_df['RecAvg'][i] = 0.0
    else:
        continue

for i in relevant_stats:
    rb_df[i] = pd.to_numeric(rb_df[i])

# filter out quarterbacks with less than 1000 passing yards
# rb_df = rb_df.query('RushAtt >= 125')

rb_df.drop(columns=['RushAtt'], inplace=True)

# rank each quarterback according to every statistic
for column in rb_df:
    if column == 'Player' or column == 'School':
        continue
    else:
        rb_df[column + ' Rank'] = rb_df[column].rank(ascending=False).astype(int)

print(rb_df.to_string())

