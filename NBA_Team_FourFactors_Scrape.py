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
driver.get("https://stats.nba.com/teams/four-factors")

#create empty lists to store season stats
team_names = []
team_gp = []
team_W = []
team_L = []
team_WinPct = []
team_Min = []
team_EFGPct = []
team_FtaRate = []
team_tovPCt = []
team_ORBpct = []
team_OppEFGpct = []
team_OppFTARate = []
team_OppTobpct = []
team_OppOrebpct = []
team_season = []


for i in range(2,15):
    #need to find appropriate year and regular season stats
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' +str(i) +']').click()
    wait_table = WebDriverWait(driver, 10)
    driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/label/select/option[2]').click()
    #pause for browser to load
    ##find season
    season = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' + str(i) + ']').text
    ##stats data table
    #wait for table to load
    wait_table = WebDriverWait(driver, 10)
    table = wait_table.until(EC.presence_of_element_located((By.CLASS_NAME,'nba-stat-table__overflow'))).text

    for j in range(1,31):
        team_season.append(season)
        team_names.append(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[2]').text)
        team_gp.append(int(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[3]').text))
        team_W.append(int(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[4]').text))
        team_L.append(int(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[5]').text))
        team_WinPct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[6]').text))
        team_Min.append(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[7]').text)
        team_EFGPct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[8]').text))
        team_FtaRate.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[9]').text))
        team_tovPCt.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[10]').text))
        team_ORBpct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[11]').text))
        team_OppEFGpct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[12]').text))
        team_OppFTARate.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[13]').text))
        team_OppTobpct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[14]').text))
        team_OppOrebpct.append(float(driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(j) + ']/td[15]').text))

#add lists to dataframe
statsDF = pd.DataFrame({ 'Season': team_season,
                    'Team': team_names,
                    'GP': team_gp,
                    'W': team_W,
                    'L': team_L,
                    'Win_Pct': team_WinPct,
                    'Min':team_Min,
                    'EFG_Pct': team_EFGPct,
                    'FTA_Rate': team_FtaRate ,
                    'TOV_PCT': team_tovPCt ,
                    'OREB_PCT': team_ORBpct,
                    'OPP_EFGPCT': team_OppEFGpct,
                    'OPP_FTARATE': team_OppFTARate,
                    'OPP_TOVPCT': team_OppTobpct,
                    'OPP_ORBPCT': team_OppOrebpct
                    })

#print(statsDF)
#export statsdf to csv file
statsDF.to_csv('NBA_Team_Stats_FourFactors.csv',index=True)

driver.close()
