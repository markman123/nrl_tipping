# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 19:04:13 2018

@author: Mark
"""
import re

from bs4 import BeautifulSoup
import requests

def get_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, "html5lib")

def get_league_table(url):
    bs = get_page(url)
    tbl = bs.find(id='views-aggregator-datatable')
    results = []
    for row in tbl.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            who = cells[0].text.strip()
            score = cells[1].text.strip()
            tipped, from_ = re.findall('([0-9]+)\sfrom\s([0-9]+)', score)[0]
            tipped = int(tipped)
            from_ = int(from_)
            perc = tipped / from_
            out = {'who': who, 'score': score, 'tipped': tipped,
                   'from_': from_, 'perc': perc}
            results.append(out)
    return results

def get_round_tips(url):
    tips = []
    bs_glance = get_page(url_glance).find(class_='content-inner')
    for head in bs_glance.find_all('h3'):
        tips.append({'tipper': head.text.strip()})
    
    counter = 0
    for item in bs_glance.select('#block-system-main .field-content'):
        txt = item.text.strip()
        if txt != '':
            tips[counter]['tips'] = txt.replace(', ',',')
            counter+= 1
            
    print("{} tips recorded thus far".format(len(tips)))
    
    return tips

def total_table(results):
    total = []
    for r in results:
        my_keys = r.keys()
        this_line = []
        for key in my_keys:
            this_line.append(r[key])
        total.append(this_line)
    
    return total

def total_table_2(total):
    total2 = []
    for t in total:
        line = []
        for c in t:
            line.append(str(c))
        total2.append(line)
        
    return total2

def game_list(tips):
    game_list = [[] for _ in range(8)]
    for tip in tips:
        teams = tip['tips'].split(",")
        for idx, game in enumerate(teams):
            game_list[idx].append(game)
            
    return  [list(set(game)) for game in game_list]
            
url = 'https://the-thinker.org/nrl-tips/2018/round-six-selections'
results = get_league_table(url)        

url_glance = 'https://the-thinker.org/round-at-a-glance/2018-Round-06'
tips = get_round_tips(url_glance)


# Build totals for output... 
total = total_table(results)
total2 = total_table_2(total)    
game_list2 = game_list(tips)

#game_list2 = [list(set(game)) for game in game_list]
##### OUTPUT
import pyperclip


out = '\n'.join([','.join(r) for r in total2])
pyperclip.copy(out)

out2 = [tip['tipper'] + ',' + tip['tips'] for tip in tips]
out2 = '\n'.join(out2)
pyperclip.copy(out2)


#### TAB
url = 'https://api.beta.tab.com.au/v1/tab-info-service/sports/Rugby%20League/competitions/NRL?jurisdiction=NSW&numTopMarkets=5'
r = requests.get(url).json()
matches = r['matches']
out_odds = []
for match in matches:
    markets = match['markets']
    
    
    for mkt in markets:
        opt = mkt['betOption']
        
        if opt == 'Head To Head':
            print("YAY")
            match_odds = {}
            props = mkt['propositions']

            for prop in props:
                match_odds[prop['name']] = prop['returnWin']
            out_odds.append(match_odds)            