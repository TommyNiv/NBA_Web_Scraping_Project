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
driver.get("https://stats.nba.com/teams/traditional")

#create empty lists to store data
team_ids = []
team_names = []
team_stats = []
team_season = []


#take to data from 2018 - 1996 season
for i in range(2,25):
    #need to find appropriate year and regular season stats
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' +str(i) +']').click()
    wait_table = WebDriverWait(driver, 10)
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]').click()

    ##find season
    season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' + str(i) + ']').text
    ##stats data table
    #pause for table to load
    table = wait_table.until(EC.presence_of_element_located((By.CLASS_NAME,'nba-stat-table__overflow'))).text

    #split table into headers, team names and stats
    for line_id, lines in enumerate(table.split('\n')):
        if line_id==0:
            column_names = lines.split(' ')[1:]
        else:
            if line_id % 3 == 1:
                team_season.append(season)
                team_ids.append(lines)
            if line_id % 3 == 2:
                team_names.append(lines)
            if line_id % 3 == 0:
                team_stats.append([float(i) for i in lines.split(' ')])

#add data to pandas data frame
teamData = pd.DataFrame({ 'Season': team_season,
                    'Team': team_names,
                    'GP': [i[0] for i in team_stats],
                    'W': [i[1] for i in team_stats],
                    'L': [i[2] for i in team_stats],
                    'Win%': [i[3] for i in team_stats],
                    'Min': [i[4] for i in team_stats],
                    'PTS': [i[5] for i in team_stats],
                    'FGM': [i[6] for i in team_stats],
                    'FGA': [i[7] for i in team_stats],
                    'FG%': [i[8] for i in team_stats],
                    '3PM': [i[9] for i in team_stats],
                    '3PA': [i[10] for i in team_stats],
                    '3P%': [i[11] for i in team_stats],
                    'FTM': [i[12] for i in team_stats],
                    'FTA': [i[13] for i in team_stats],
                    'FT%': [i[14] for i in team_stats],
                    'ORB': [i[15] for i in team_stats],
                    'DREB': [i[16] for i in team_stats],
                    'REB': [i[17] for i in team_stats],
                    'AST': [i[18] for i in team_stats],
                    'TOV': [i[19] for i in team_stats],
                    'STL': [i[20] for i in team_stats],
                    'BLK': [i[21] for i in team_stats],
                    'BLKA': [i[22] for i in team_stats],
                    'PF': [i[23] for i in team_stats],
                    'PFD': [i[24] for i in team_stats],
                    '+/-': [i[25] for i in team_stats],
                    })


teamData.to_csv('NBA_Team_Stats.csv',index=True)
driver.close()
