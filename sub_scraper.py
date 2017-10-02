#!/usr/bin/python

# scrape subterfuge leaderboards

import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# url to leaderboard
url = 'http://subterfuge-game.com/leaderboards.html'

#get html of webpage, beautify it
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'lxml')

# extract table html
table = soup.findAll('tr')

# select only elements i want
elem_keep = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

rank = []
player = []
rating = []
gold = []
silver = []
bronze = []
rated_games = []
total_games = []
finished = []
eliminated = []
resigned = []
joined = []

for r in range(1, len(table)):
    row = []
    for k in elem_keep:
        row.append(str(table[r]).split('>')[k][:-4])

    rank.append(row[0])
    player.append(row[1])
    rating.append(row[2])
    gold.append(row[3])
    silver.append(row[4])
    bronze.append(row[5])
    rated_games.append(row[6])
    total_games.append(row[7])
    finished.append(row[8])
    eliminated.append(row[9])
    resigned.append(row[10])
    joined.append(row[11])

# make it a df
df = pd.DataFrame({
    'rank':rank,
    'player':player,
    'rating':rating,
    'gold':gold,
    'silver':silver,
    'bronze':bronze,
    'rated_games':rated_games,
    'total_games':total_games,
    'finished':finished,
    'eliminated':eliminated,
    'resigned':resigned,
    'joined':joined
})

# reorder the columns
cols = ['rank', 'player','rating','gold','silver','bronze',
        'rated_games','total_games','finished','eliminated',
        'resigned','joined']
df = df[cols]

# add date scraped columns
df['date_scraped'] = datetime.date.today().strftime("%d %b %Y")
df['time_scraped'] = datetime.datetime.now().strftime("%H:%M")

# save to csv
today = datetime.date.today().strftime("%d%b%Y")
df.to_csv('~/Documents/subterfuge/data/sub_' + str(today) + '.csv', index=False)
