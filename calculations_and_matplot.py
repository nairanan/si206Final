import matplotlib.pyplot as plt
import sqlite3
from APIs_and_Soup import setup_db

global_tier_list = ['Uber', 'OU', 'UUBL', 'UU', 'RU', 'NU', 'PU', 'ZU']

def make_averages_list(cur, conn):
    averages = []
    cur.execute('''SELECT hp, attack, special_attack, defense, special_defense, speed FROM Stats''')
    stats = cur.fetchall()
    for stats_tup in stats:
        average_stats = round((sum(stats_tup) / 6), 2)
        averages.append(average_stats)
    
    return averages

def make_tier_list(cur, conn):
    tier_list = []
    cur.execute('''SELECT Tiers.tier from Tiers JOIN Stats ON Tiers.id = Stats.tier_id''')
    tiers = cur.fetchall()
    for tier_tup in tiers:
        tier_list.append(tier_tup[0])

    return tier_list
    
def tier_counts(tier_list):
    tier_dic = {}
    for tier in tier_list:
        tier_dic[tier] = tier_dic.get(tier, 0) + 1
    return tier_dic

def graph_tier_by_avgstat(averages, tiers):
    fig, ax = plt.subplots()
    ax.scatter(tiers, averages)
    ax.set_xlabel('Tiers')
    ax.set_ylabel('Average Stats')
    ax.set_title('Pokemon Tiers by Average Stats')
    unique_tiers = ['ZU', 'PU', 'NU', 'RU', 'UU', 'UUBL', 'OU', 'Uber']
    ax.set_xticks(unique_tiers)
    ax.set_xticklabels(unique_tiers)
    ax.grid()
    plt.show()


def main():
    cur, conn = setup_db()
    average_stats = make_averages_list(cur, conn)
    tier_list = make_tier_list(cur, conn)
    tier_counts(tier_list)
    graph_tier_by_avgstat(average_stats, tier_list)
    
if __name__ == '__main__':
    main()  