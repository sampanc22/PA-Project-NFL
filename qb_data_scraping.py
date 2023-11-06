from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

homepage = "https://www.pro-football-reference.com/years/2023/passing.htm"
url = urlopen(homepage)
stats = BeautifulSoup(url)

col_headers = stats.find_all('tr')[0]
col_headers = [i.getText() for i in col_headers.findAll('th')]

rows = stats.find_all('tr')[1:]
qb_data = []

for i in range(41):
    if i % 29 != 0:
        qb_data.append([col.getText() for col in rows[i].findAll('td')])

qb_df = pd.DataFrame(qb_data, columns=col_headers[1:])
qb_df.columns.values[-6] = 'YdsSk'
# filter out irrelevant statistics (such as non-aggregated stats)
qb_df.drop(columns=["QBrec", "Lng", "Pos", "1D", "4QC", "GWD", "NY/A",
                    "G", "GS", "Cmp", "Att", "Yds", "TD", "Int", "Sk", "YdsSk", "ANY/A"], inplace=True)
print(qb_df.to_string())
