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
driver.get("https://stats.nba.com/teams/advanced")

#create empty lists to add data
team_ids = []
team_names = []
team_stats = []
team_season = []


for i in range(2,25):
    #need to find appropriate year and regular season stats
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' +str(i) +']').click()
    wait_table = WebDriverWait(driver, 10)
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]').click()
    #pause for browser to load
    ##find season
    season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' + str(i) + ']').text
    ##stats data table
    table = wait_table.until(EC.presence_of_element_located((By.CLASS_NAME,'nba-stat-table__overflow'))).text


    for line_id, lines in enumerate(table.split('\n')):
        if line_id==0:
            column_names = lines.split(' ')[1:]
        else:
            if line_id % 3 == 1:
                team_season.append(season)
                team_names.append(lines)
            if line_id % 3 == 2:
                team_stats.append(lines)


team_season = team_season[1:]
team_names = team_names[1:]
team_stats = team_stats[1:]

df = pd.DataFrame(team_stats)[0].str.split(expand=True)
df.columns = ['GP','W','L','Min','OFFRTG','DEFRTG','NETRTG','AST_PCT','AST/TO','AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TOV_PCT','EFG_PCT','TS_PCT','PACE','PIE']

for col in df.columns:
    df[col] = df[col].astype(float)


print(len(team_season))
print(len(team_names))
statsDF = pd.DataFrame({ 'Season': team_season,
                    'Team': team_names
                    })

finalStats = pd.merge(statsDF,df, left_index = True, right_index = True)
#print(finalStats)
finalStats.to_csv('NBA_Team_Stats_Advanced.csv',index=True)
driver.close()
