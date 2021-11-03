import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_handle import open_datab, get_player_names, last_10_avg, stats_highest_avg

player_tables = get_player_names()
avg_list = last_10_avg(player_tables)
total = stats_highest_avg(player_tables, avg_list)

#Player Averages Chart
player_list = [''.join(x) for x in player_tables] #Convert player_tables into list of strings from a list of lists
for num, x in enumerate(player_list):
       player_list[num] = x[x.index('_')+1:]  
all_data = pd.DataFrame({'Players':player_list,
                         'Avg':avg_list})

sns.set(font_scale=0.75)
avg_bar = sns.barplot(
       data= all_data,
       x = 'Players',
       y = 'Avg')
plt.show()


#Devers stats over 10 games
labels_only = ["Hits", "Runs", "Doubles", "Triples", "HRs", "RBIs", "BBs", "SOs"]
stats_no_ab = pd.DataFrame({'Label': labels_only,
                            'Value': total[1:]})

sns.set(font_scale=0.75)
ten_game_stats = sns.barplot(
       data=stats_no_ab,
       x='Label',
       y='Value')
plt.show()
