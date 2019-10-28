from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time
import pandas as pd

#set chrome driver
driver = webdriver.Chrome(r'C:\Users\tnivo\ChromeDriver\chromedriver.exe')
#get nba team stats page for traditional stats
driver.get("https://stats.nba.com/leaders")

player_ids = []
player_names = []
player_stats = []
player_season = []




for i in range(2,25):
    #need to find appropriate year and regular season stats
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' +str(i) +']').click()
    wait_table = WebDriverWait(driver, 10)
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]').click()
    wait_all = WebDriverWait(driver,10)

    #pause for browser to load
    wait_table.until(EC.presence_of_element_located((By.CLASS_NAME,'nba-stat-table__overflow')))
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]').click()

    ##find season
    season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' + str(i) + ']').text
    ##stats data table
    table = wait_table.until(EC.presence_of_element_located((By.CLASS_NAME,'nba-stat-table__overflow'))).text

    #print(table)
    for line_id, lines in enumerate(table.split('\n')):
        if line_id==0:
            column_names = lines.split(' ')[1:]
        else:
            if line_id % 3 == 1:
                player_season.append(season)
                player_ids.append(lines)
            if line_id % 3 == 2:
                player_names.append(lines)
            if line_id % 3 == 0:
                player_stats.append([float(i) for i in lines.split(' ')])
#print(player_ids)
#print(player_names)
print(player_stats)

#add player stats to pandas dataframe
playerData = pd.DataFrame({ 'Season': player_season,
                    'Player': player_names,
                    'GP': [i[0] for i in player_stats],
                    'Min': [i[1] for i in player_stats],
                    'Pts': [i[2] for i in player_stats],
                    'FGM': [i[3] for i in player_stats],
                    'FGA': [i[4] for i in player_stats],
                    'FG%': [i[5] for i in player_stats],
                    '3PM': [i[6] for i in player_stats],
                    '3PA': [i[7] for i in player_stats],
                    '3P%': [i[8] for i in player_stats],
                    'FTM': [i[9] for i in player_stats],
                    'FTA': [i[10] for i in player_stats],
                    'FT%': [i[11] for i in player_stats],
                    'OREB': [i[12] for i in player_stats],
                    'DREB': [i[13] for i in player_stats],
                    'REB': [i[14] for i in player_stats],
                    'AST': [i[15] for i in player_stats],
                    'STL': [i[16] for i in player_stats],
                    'BLK': [i[17] for i in player_stats],
                    'TOV': [i[18] for i in player_stats],
                    'EFF': [i[19] for i in player_stats]
                    })

#export to csv
playerData.to_csv('NBA_Player_Stats.csv',index=True)
