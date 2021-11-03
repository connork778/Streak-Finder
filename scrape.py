'''
All statistics are being scraped from Baseball-Reference.com
'''
import requests
from bs4 import BeautifulSoup
from csv_handle import new_player, update_csv, populate_csv
from db_handle import  open_datab, create_table_Bplayer, insert_links_table, close_datab, get_player_names, last_10_avg, stats_highest_avg
from sqlalchemy import create_engine
import pandas as pd
import re
import psycopg2
import time

# - Start using year variable. Going to be static for now but im going to need to use it in the future so might as well add it now

def format_date(date, year):
    date_formatted = ""
    months = {
        "Mar": "3",
        "Apr": "4",
        "May": "5",
        "Jun": "6",
        "Jul": "7",
        "Aug": "8",
        "Sep": "9",
        "Oct": "10",
        "Nov": "11"
    }
    if len(date) >= 6:
        date_formatted = year + "-" + months.get(date[:3]) + "-" + date[4:6]
    else:
        date_formatted = year + "-" + months.get(date[:3]) + "-" + date[4] 
    return date_formatted


def scrape_insert_stats(db_name, player_name, link):
    open_datab("Redsox_B_2021")
    cur = open_datab.variable
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    tr = list(soup.find_all("tr", id=re.compile("^batting"))) 
    desired_stats = [3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 22, 23, 24, 25, 32, 33]
    stat_list = []
    for x in range(len(tr)):
        get_rank = tr[x].find(class_="right").get_text()
        get_date = tr[x].find_all(class_="left")[0].get_text()
        opp_team = tr[x].find_all(class_="left")[2].get_text()
        stat_list.append(get_rank)
        stat_list.append(format_date(get_date, "2021"))
        stat_list.append(opp_team)
        for i in desired_stats:
            stat = tr[x].find_all(class_="right")[i].get_text()
            stat_list.append(stat)
        cur.execute('INSERT INTO {tab} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.format(tab=player_name), stat_list)
        stat_list = []
        open_datab.variable2.commit()
    
    
    print("Connection closed. Function has inserted " + player_name + "s stats")


def insert_season_stats(): #Takes list of names and links from db, scrapes season stats and inserts them into respective tables in db
    open_datab("Redsox_B_2021")
    cur = open_datab.variable
    conn = open_datab.variable2
    cur.execute('''SELECT * FROM links''')
    player_rows = cur.fetchall()
    for i in range(len(player_rows)):
        last = player_rows[i][0]
        first = player_rows[i][1]
        link = player_rows[i][2]
        full_name = first + "_" + last
        create_table_Bplayer(full_name.lower())
        scrape_insert_stats("Redsox_B_2021", full_name.lower(), link)
    conn.commit()
    conn.close()
    return print("Complete")


#insert_season_stats()


###################Used with insert_links_table######################
def scrape_team_name(link, team):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find("div", id="meta")
    get_team = div.find('a', text=team)
    try:
        if get_team.get_text() != team:
            return ""
    except AttributeError: #Attribute error raised when the player is retired as it doesn't list a team for retired players
        return ""
    return get_team.get_text()

def find_player_link(last, first, team, year):
    url_begin = "https://www.baseball-reference.com/players/gl.fcgi?id="
    url_end = "&t=b&year="
    name = last[:5] + first[:2]
    identifier = "01"
    url_complete = url_begin + name.lower() + identifier + url_end + year
    count = 1
    cur = scrape_team_name(url_complete, team)
    while cur != team and count < 5: #count < 5 is a placeholder until a better solution is implemented. Makes sure I dont infinitely scrape the page
        count += 1
        identifier = "0" + str(count)
        url_complete = url_begin + name.lower() + identifier + url_end + year
        cur = scrape_team_name(url_complete, team)
    return url_complete

def find_all_links(players, team, year):
    list_links = []
    for i in range(0, len(players[:-1]), 2):
        list_links.append(find_player_link(players[i], players[i+1], team, year))
    return list_links
#insert_links_table(last, first, find_all_links(players, "Boston Red Sox", "2021"))
#Right now players, last, first are just lists of names inside the code, that will changed to a better system in the future
#####################################################################


def scrape_name(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find("h1").get_text()
    return name


'''
first_game.find_all(class_="right")[x].get_text() list indicies
0.  Rk
1.  Gcar
2.  Gtm
3.  Date. Doesn't work beacuse the td has a child a tag that holds the date text.
4.  PA
5.  AB
6.  R
7.  H
8.  2B
9.  3B
10. HR
11. RBI
12. BB
13. IBB
14. SO
15. HBP
16. SH
17. SF
18. ROE
19. GDP
20. SB
21. CS
22. BA
23. OBP
24. SLG
25. OPS
'''

'''
All statistics are being scraped from Baseball-Reference.com
'''