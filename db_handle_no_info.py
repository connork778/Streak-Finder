import psycopg2
import numpy as np
from psycopg2 import Error


conn = psycopg2.connect(database="Redsox_B_2021",
                        user="********",
                        password="*******",
                        host="*******",
                        port="****")


def open_datab(db_name):
    conn = psycopg2.connect(database=db_name,
                            user="*******",
                            password="*********",
                            host="******",
                            port="****")
    open_datab.variable = conn.cursor()
    open_datab.variable2 = conn


def close_datab():
    conn.commit()
    conn.close()


def create_table_Bplayer(name):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE {tab}
        (Rk         SMALLINT    NOT NULL,
        DATE        DATE        NOT NULL,
        OPP         CHAR(3)     NOT NULL,
        LOCATION    VARCHAR(1)  NOT NULL,
        AB          SMALLINT    NOT NULL,
        RUNS        SMALLINT    NOT NULL,
        HITS        SMALLINT    NOT NULL,
        DOUBLE      SMALLINT    NOT NULL,
        TRIPLE      SMALLINT    NOT NULL,
        HR          SMALLINT    NOT NULL,
        RBI         SMALLINT    NOT NULL,
        BB          SMALLINT    NOT NULL,
        SO          SMALLINT    NOT NULL,
        HBP         SMALLINT    NOT NULL,
        BA          FLOAT(24)   NOT NULL,
        OBP         FLOAT(24)   NOT NULL,
        SLG         FLOAT(24)   NOT NULL,
        OPS         FLOAT(24)   NOT NULL,
        DK_POINTS   TEXT,
        FD_POINTS   TEXT);'''.format(tab=name))
    cur.close()
    conn.commit()
#Some games dont show fd or dk points for some players and it doesnt retrun null so I changed those columns to text instead. Just have to account for that when querying later.


def create_links_table():
    open_datab("Redsox_B_2021")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE LINKS
        (LAST    VARCHAR    NOT NULL,
        FIRST   VARCHAR    NOT NULL,
        LINK    VARCHAR     NOT NULL);''')
    cur.close()
    conn.commit()


def insert_links_table(last, first, links): 
    open_datab("Redsox_B_2021")
    cur = conn.cursor()
    for i in range(len(links)):
        query = """INSERT INTO links VALUES (%s, %s, %s)"""
        data = (last[i], first[i], links[i])
        cur.execute(query, data)
    cur.close
    close_datab()



def get_player_names():
    open_datab("Redsox_B_2021")
    cur = open_datab.variable
    conn = open_datab.variable2
    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'
       AND NOT table_name = 'links' """)
    player_tables = cur.fetchall()
    player_tables = [list(x) for x in player_tables]
    cur.close()
    conn.commit()
    return player_tables
    

def last_10_avg(players):
    open_datab("Redsox_B_2021")
    cur = open_datab.variable
    conn = open_datab.variable2
    avg_list = []
    for i in range(len(players)):
       cur.execute('SELECT hits, ab FROM {tab} ORDER BY rk DESC LIMIT 10'.format(tab=players[i][0]))
       result = cur.fetchall()
       hits = 0
       ab = 0 
       for j in range(len(result)):
              hits += result[j][0]
              ab += result[j][1]
       avg = round(hits/ab, 3)
       avg_list.append(avg)
    cur.close()
    conn.commit()
    return avg_list


def stats_highest_avg(players, avg_list):
    open_datab("Redsox_B_2021")
    cur = open_datab.variable
    conn = open_datab.variable2
    cur.execute('SELECT ab, hits, runs, double, triple, hr, rbi, bb, so FROM {tab} ORDER BY rk DESC LIMIT 10'.format(tab=players[np.argmax(avg_list)][0]))
    ten_day_stats = cur.fetchall()
    cur.close()
    conn.commit()
    total = [0,0,0,0,1,0,0,0,0] #Place holder 1 in triples spot until stats with zeros are handled and dont causes errors with the graphs
    for arr in ten_day_stats:
       for x in range(len(arr)):
              total[x] += arr[x]
    return total


#Will be replaced with a better system
'''Code used to create links and insert into db. To be used on scrape.py
testing_list = ["Vazquez", "Christian", "Dalbec", "Bobby", "Arroyo", "Christian", "Bogaerts", "Xander", "Devers", "Rafael", "Verdugo", "Alex", "Hernandez", "Enrique", "Renfroe", "Hunter", "Martinez", "JD", "Plawecki", "Kevin", "Schwarber", "Kyle", "Iglesias", "Jose", "Shaw", "Travis"]
last = ["Vazquez", "Dalbec", "Arroyo", "Bogaerts", "Devers", "Verdugo", "Hernandez", "Renfroe", "Martinez", "Plawecki", "Schwarber", "Iglesias", "Shaw"]
first = ["Christian", "Bobby", "Christian", "Xander", "Rafael", "Alex", "Enrique", "Hunter", "JD", "Kevin", "Kyle", "Jose", "Travis"]

insert_links_table(last, first, find_list_of_players(testing_list, "Boston Red Sox", "2021"))
'''