import matplotlib.pyplot as plt
import sqlite3
from APIs_and_Soup import setup_db

global_tier_list = ['Uber', 'OU', 'UUBL', 'UU', 'RU', 'NU', 'PU', 'ZU']

def make_averages_list(cur, conn):
    """
    Uses the database info to calculate each pokemon's average stats and put it into a list

    ARGUMENTS
        database cursor and connection

    RETURNS
        a list of Pokemon average stats (in order of the database rows)
    """
    averages = []
    cur.execute('''SELECT hp, attack, special_attack, defense, special_defense, speed FROM Stats''')
    stats = cur.fetchall()
    for stats_tup in stats:
        average_stats = round((sum(stats_tup) / 6), 2)
        averages.append(average_stats)
    
    return averages

def make_tier_list(cur, conn):
    """
    Joins the stats table and the tiers table from the database to select each pokemon 
    tier and put it into a list

    ARGUMENTS
        database cursor and connection

    RETURNS
        a list of Pokemon tiers in order of the database rows
    """
    tier_list = []
    cur.execute('''SELECT Tiers.tier from Tiers JOIN Stats ON Tiers.id = Stats.tier_id''')
    tiers = cur.fetchall()
    for tier_tup in tiers:
        tier_list.append(tier_tup[0])

    return tier_list

def write_calculations(averages, tiers, cur, conn):
    cur.execute('''SELECT name FROM Stats ORDER BY row_id ASC''')
    names = cur.fetchall()

    with open("calculations.txt", "w") as file:
        for i in range(len(names)):
            file.write(f"{names[i][0]}'s average stats value is {averages[i]} and its tier is {tiers[i]}\n")
    
def tier_counts(tier_list):
    """
    Uses the list returned from make_tier_list() to make a dictionary that holds each tier as the key 
    and the number of times it is in the database as values
    ARGUMENTS
        tier_list

    RETURNS
        a dict ist of Pokemon tiers and counts
    """
    tier_dic = {}
    for tier in tier_list:
        tier_dic[tier] = tier_dic.get(tier, 0) + 1
    return tier_dic

def graph_tier_counts(tier_dic):
    """
    Uses the dict returned from tier_counts() to create a bar graph of tiers and their corresponding counts
    ARGUMENTS
        tier_dic

    RETURNS
        None
    """
    tiers = list(tier_dic.keys())
    counts = list(tier_dic.values())
    fig, ax = plt.subplots()
    ax.bar(tiers, counts, color = 'slateblue', edgecolor = 'darkcyan')
    ax.set_xlabel('Tiers')
    ax.set_ylabel('Count')
    ax.set_title('Pokemon Tier Counts')
    plt.savefig("tiers.png")
    plt.show()



def graph_tier_by_avgstat(averages, tiers):
    """
    Uses the lists returned from make_averages_list() and make_tier_list() to create a scatter plot tiers 
    and the average stats of different pokemon from each of those tiers
    ARGUMENTS
        averages list, tiers list

    RETURNS
        None
    """
    fig, ax = plt.subplots()
    ax.scatter(tiers, averages, c = averages, cmap = 'plasma')
    ax.set_xlabel('Tiers')
    ax.set_ylabel('Average Stats')
    ax.set_title('Pokemon Tiers by Average Stats')
    unique_tiers = ['ZU', 'PU', 'NU', 'RU', 'UU', 'UUBL', 'OU', 'Uber']
    ax.set_xticks(unique_tiers)
    ax.set_xticklabels(unique_tiers)
    ax.grid()
    plt.savefig("statsvtiers.png")
    plt.show()


def main():
    cur, conn = setup_db()
    average_stats = make_averages_list(cur, conn)
    tier_list = make_tier_list(cur, conn)
    write_calculations(average_stats, tier_list, cur, conn)
    tier_dic = tier_counts(tier_list)
    graph_tier_by_avgstat(average_stats, tier_list)
    graph_tier_counts(tier_dic)
    conn.close()
    
if __name__ == '__main__':
    main()  