#Author: Tomas Nivon
#This python file was used to conduct all the analysis for the Team data

import pandas as pd

teamStats = pd.read_csv('NBA_Team_Stats.csv',index_col = 0)
teamStatsAdv = pd.read_csv('NBA_Team_Stats_Advanced.csv', index_col = 0)
team4Fac = pd.read_csv('NBA_Team_Stats_FourFactors.csv', index_col = 0)
teamStatsComplete = pd.merge(teamStats,teamStatsAdv,left_index = True, right_index = True)
teamStatsmerged = teamStatsComplete.rename(columns= {'Season_x':'Season', 'Team_x':'Team','GP_x':'GP','W_x':'W', 'L_x':'L','Min_x':'Min'})
playerStats = pd.read_csv('NBA_Player_Stats.csv',index_col = 0)
player1819 = playerStats[playerStats['Season'] == '2018-19']
playerAdvStats = pd.read_csv('NBA_Player_Advanced_Stats.csv',index_col = 0)

#function to calculate VOP
def VOP(pts,fga,orb,tov,fta):
    lg_pts = math.log(pts)
    lg_fga = math.log(fga)
    lg_ORB = math.log(orb)
    lg_tov = math.log(tov)
    lg_fta = math.log(fta)

    vop = (lg_pts/(lg_fga-lg_ORB + lg_tov+0.44*lg_fta))
    return vop

def factor_(ast,fg,ft):
    lg_ast = math.log(ast)
    lg_fg = math.log(fg)
    lg_ft = math.log(ft)
    fac = (2/3) - (0.5*(lg_ast/lg_fg))/(2*(lg_fg/lg_ft))
    return fac

def dfbPct(orb,trb):
    lg_trb = math.log(trb)
    lg_orb = math.log(orb)
    dfb_pct = (lg_trb - lg_orb)/lg_trb
    return dfb_pct

teamStatsmerged[['Season','Season_y','Team','Team_y','GP','GP_y','W','W_y','L','L_y','Min','Min_y']].head()

import datetime
date_time_str = '2018'
date_time_obj = datetime.datetime.strptime(date_time_str,'%Y')
fullTeamStatsDF['Season_Yr'] = pd.to_datetime(fullTeamStatsDF['Season_Yr'], format='%Y')
fullTeamStatsDF['Season_Yr'] = pd.DatetimeIndex(fullTeamStatsDF['Season_Yr']).year
teamStats2006pres = fullTeamStatsDF[fullTeamStatsDF['Season_Yr'] >=2006]
team4Fac = team4Fac.rename(columns= {'Min':'Total_Min'})
teamStatsNew = pd.merge(teamStats2006pres,team4Fac,left_index = True, right_index = True)
teamStatsNew = teamStatsNew.drop(columns = ['Season_y','Team_y','GP_y','W_y','L_y','TOV_PCT_y','OREB_PCT_y'])
teamStatsNew = teamStatsNew.rename(columns= {'Season_x':'Season','Team_x':'Team','GP_x':'GP','W_x':'W','L_x':'L','OREB_PCT_x':'OREB_PCT','TOV_PCT_x':'TOV_PCT'})
teamStatsNew2017 = teamStatsNew[teamStatsNew['Season_Yr'] == 2017]

teamStatsNew2017 = teamStatsNew2017.assign(OPP_EFGPCT = teamStatsNew2017['OPP_EFGPCT']/100)
teamStatsNew2017=teamStatsNew2017.assign(OREB_PCT = teamStatsNew2017['OREB_PCT']/100)
teamStatsNew2017=teamStatsNew2017.assign(EFG_Pct = teamStatsNew2017['EFG_Pct']/100)
teamStatsNew2017=teamStatsNew2017.assign(TOV_PCT = teamStatsNew2017['TOV_PCT']/100)
teamStatsNew2017=teamStatsNew2017.assign(OPP_TOVPCT = teamStatsNew2017['OPP_TOVPCT']/100)
teamStatsNew2017=teamStatsNew2017.assign(DREB_PCT = teamStatsNew2017['DREB_PCT']/100)

import statsmodels.formula.api as sm
import statsmodels.formula.api as smf

result = smf.ols(formula = "W ~ EFG_Pct +TOV_PCT+ OREB_PCT + FTA_Rate + OPP_EFGPCT + OPP_TOVPCT + DREB_PCT + OPP_FTARATE -1", data= teamStatsNew2017).fit()
result.summary()
teamStatsNew2017['Estimate_Wins'] = result.predict()
teamStatsNew2017 = teamStatsNew2017.assign(Wins_Delta = teamStatsNew2017['W'] - teamStatsNew2017['Estimate_Wins'])
teamStatsNew2017.agg(['mean','std'])['Wins_Delta']

teamStatsNew = teamStatsNew.assign(OPP_EFGPCT = teamStatsNew['OPP_EFGPCT']/100)
teamStatsNew=teamStatsNew.assign(OREB_PCT = teamStatsNew['OREB_PCT']/100)
teamStatsNew=teamStatsNew.assign(EFG_Pct = teamStatsNew['EFG_Pct']/100)
teamStatsNew=teamStatsNew.assign(TOV_PCT = teamStatsNew['TOV_PCT']/100)
teamStatsNew=teamStatsNew.assign(OPP_TOVPCT = teamStatsNew['OPP_TOVPCT']/100)
teamStatsNew=teamStatsNew.assign(DREB_PCT = teamStatsNew['DREB_PCT']/100)

fourFactorModel = smf.ols(formula = "W ~ EFG_Pct +TOV_PCT+ OREB_PCT + FTA_Rate + OPP_EFGPCT + OPP_TOVPCT + DREB_PCT + OPP_FTARATE -1", data= teamStatsNew).fit()
fourFactorModel.summary()
teamStatsNew['Estimate_Wins'] = fourFactorModel.predict()
teamStatsNew = teamStatsNew.assign(Wins_Delta = teamStatsNew['W'] - teamStatsNew['Estimate_Wins'])
teamStatsNew.agg(['mean','std','max','min'])['Wins_Delta']
teamStatsNew.loc[teamStatsNew['Wins_Delta'].idxmin()]

abbreviatedNames = {'Milwaukee Bucks':'MIL','Toronto Raptors':'TOR','Golden State Warriors':'GSW','Denver Nuggets':'DEN','Houston Rockets':'HOU',
                   'Portland Trail Blazers':'POR','Philadelphia 76ers':'PHI','Utah Jazz':'UTA','Boston Celtics':'BOS','Oklahoma City Thunder':'OKC','Indiana Pacers':'IND',
                   'LA Clippers':'LAC','San Antonio Spurs':'SAS','Brooklyn Nets':'BKN','Orlando Magic':'ORL','Detroit Pistons':'DET','Charlotte Hornets':'CHA',
                   'Miami Heat':'MIA','Sacramento Kings':'SAC','Los Angeles Lakers':'LAL','Minnesota Timberwolves':'MIN','Dallas Mavericks':'DAL','Memphis Grizzlies':'MEM',
                   'New Orleans Pelicans':'NOP','Washington Wizards':'WAS','Atlanta Hawks':'ATL','Chicago Bulls':'CHI','Cleveland Cavaliers':'CLE','Phoenix Suns':'PHX',
                   'New York Knicks':'NYK'}
#remove 2011-12 season due to shortened season, there was a lockout this year...model is off my -21 games for philly, season was shortened 20 games
teamStatsNew2 = teamStatsNew[teamStatsNew['Season_Yr'] != 2011]

teamStatsNew2 = teamStatsNew2.drop(columns = ['Estimate_Wins','Wins_Delta'])
fourFacmodel2 = smf.ols(formula = "W ~ EFG_Pct +TOV_PCT+ OREB_PCT + FTA_Rate + OPP_EFGPCT + OPP_TOVPCT + DREB_PCT + OPP_FTARATE -1", data= teamStatsNew2).fit()
teamStatsNew2['Estimate_Wins'] = fourFacmodel2.predict()
teamStatsNew2 = teamStatsNew2.assign(Wins_Delta = teamStatsNew2['W'] - teamStatsNew2['Estimate_Wins'])
teamStatsNew2.agg(['mean','std','max','min'])['Wins_Delta']
fourFacmodel2.summary()
teamStatsNew2.loc[teamStatsNew2['Wins_Delta'].idxmin()]
teamStatsNew2.loc[teamStatsNew2['Wins_Delta'].idxmax()]

season2018 = teamStatsNew2[teamStatsNew2['Season_Yr']==2018]
season2017 = teamStatsNew2[teamStatsNew2['Season_Yr']==2017]

season2017['Rank'] = (season2017['W']+season2017['Estimate_Wins']).rank(method='dense',ascending = True).astype(int)
season2017['Short_Name'] = season2017['Team'].map(abbreviatedNames)
season2017 = season2017.reset_index()

season2016 = teamStatsNew2[teamStatsNew2['Season_Yr']==2016]
season2016['Rank'] = (season2016['W']+season2016['Estimate_Wins']).rank(method='dense',ascending = True).astype(int)
season2016['Short_Name'] = season2016['Team'].map(abbreviatedNames)
season2016 = season2016.reset_index()
season2015 = teamStatsNew2[teamStatsNew2['Season_Yr']==2015]
season2015['Rank'] = (season2015['W']+season2015['Estimate_Wins']).rank(method='dense',ascending = True).astype(int)
season2015['Short_Name'] = season2015['Team'].map(abbreviatedNames)
season2015 = season2015.reset_index()
season2014 = teamStatsNew2[teamStatsNew2['Season_Yr']==2014]
season2014['Rank'] = (season2014['W']+season2014['Estimate_Wins']).rank(method='dense',ascending = True).astype(int)
season2014['Short_Name'] = season2014['Team'].map(abbreviatedNames)
season2014 = season2014.reset_index()
season2018['Rank'] = (season2018['W']+season2018['Estimate_Wins']).rank(method='dense',ascending = True).astype(int)
season2018['Short_Name'] = season2018['Team'].map(abbreviatedNames)

import matplotlib.pylab as plt
import seaborn as sns

sns.set_style("darkgrid")
plt.figure(figsize=(15,8))
pltEstAct = sns.regplot(data = season2018, x = 'Rank', y= 'Estimate_Wins',fit_reg=False,label = "Estimate Wins")
pltAct = sns.regplot(data=season2018, x='Rank',y='W',fit_reg = False, color = 'red', label = "Actual Wins")

for line in range(0,season2018.shape[0]):
    pltEstAct.text(season2018.Rank[line]+0.2,season2018.Estimate_Wins[line],season2018.Short_Name[line], horizontalalignment = 'left',size = 'small', color = 'black', weight = 'semibold')

pltEstAct.legend(loc=2)
pltAct.legend(loc=2)
#labels = ['Estimated Wins', 'Actual Wins']

#pltEstAct._legend.texts[0].set_text(labels[0])
#pltAct._legend.texts[0].set_text(labels[1])

pltEstAct.set(xlabel= "Team Rank", ylabel = "Wins", title = "2018 Wins vs Estimate Wins - 8 factor Model")

AEW = pltEstAct.get_figure()
AEW.savefig("Actual_Vs_Estimate_Wins.png")

sns.set_style("darkgrid")
plt.figure(figsize=(15,8))
pltEstAct2016 = sns.regplot(data = season2016, x = 'Rank', y= 'Estimate_Wins',fit_reg=False,label = "Estimate Wins")
pltAct2016 = sns.regplot(data=season2016, x='Rank',y='W',fit_reg = False, color = 'red', label = "Actual Wins")

for line2 in range(0,season2016.shape[0]):
    pltAct2016.text(season2016.Rank[line2],season2016.Estimate_Wins[line2],season2016.Short_Name[line2], horizontalalignment = 'left',size = 'small', color = 'black', weight = 'semibold')

pltEstAct2016.legend(loc=2)
pltAct2016.legend(loc=2)


pltEstAct2016.set(xlabel= "Team Rank", ylabel = "Wins", title = "2016 Wins vs Estimate Wins - 8 factor Model")

AEW16 = pltEstAct2016.get_figure()
AEW16.savefig("Actual_Vs_Estimate_Wins_2016.png")

sns.set_style("darkgrid")
plt.figure(figsize=(15,8))
pltEstAct2017 = sns.regplot(data = season2017, x = 'Rank', y= 'Estimate_Wins',fit_reg=False,label = "Estimate Wins")
pltAct2017 = sns.regplot(data=season2017, x='Rank',y='W',fit_reg = False, color = 'red', label = "Actual Wins")

for line2 in range(0,season2017.shape[0]):
    pltAct2017.text(season2017.Rank[line2],season2017.Estimate_Wins[line2],season2017.Short_Name[line2], horizontalalignment = 'left',size = 'small', color = 'black', weight = 'semibold')

pltEstAct2017.legend(loc=2)
pltAct2017.legend(loc=2)


pltEstAct2017.set(xlabel= "Team Rank", ylabel = "Wins", title = "2017 Wins vs Estimate Wins - 8 factor Model")

AEW17 = pltEstAct2017.get_figure()
AEW17.savefig("Actual_Vs_Estimate_Wins_2017.png")

sns.set_style("darkgrid")
plt.figure(figsize=(15,8))
pltEstAct2015 = sns.regplot(data = season2015, x = 'Rank', y= 'Estimate_Wins',fit_reg=False,label = "Estimate Wins")
pltAct2015 = sns.regplot(data=season2015, x='Rank',y='W',fit_reg = False, color = 'red', label = "Actual Wins")

for line2 in range(0,season2015.shape[0]):
    pltAct2015.text(season2015.Rank[line2],season2015.Estimate_Wins[line2],season2015.Short_Name[line2], horizontalalignment = 'left',size = 'small', color = 'black', weight = 'semibold')

pltEstAct2015.legend(loc=2)
pltAct2015.legend(loc=2)


pltEstAct2015.set(xlabel= "Team Rank", ylabel = "Wins", title = "2015 Wins vs Estimate Wins - 8 factor Model")

AEW15 = pltEstAct2015.get_figure()
AEW15.savefig("Actual_Vs_Estimate_Wins_2015.png")

teamStats4Fac = teamStatsNew2[['EFG_PCT','FTA_Rate','OPP_EFGPCT','OPP_FTARATE','OPP_TOVPCT','OPP_ORBPCT','OREB_PCT','DREB_PCT']]

statsCorMat = teamStats4Fac.corr()
sns.set_style("darkgrid")
plt.figure(figsize=(15,8))
mask= np.zeros_like(statsCorMat)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    p2 = sns.heatmap(statsCorMat, mask=mask, square = True, cmap='Greens')

p2.set(title="Four Factor Model Correlation Matrix")
statsCor = p2.get_figure()
statsCor.savefig("4Fac_Corr_Mat.png")

statsV2 = teamStatsNew2.iloc[0:,8:].copy()
statsV2 = statsV2.drop(columns=['Total_Min']).copy()

from sklearn.decomposition import PCA
#pca = PCA(n_components=8)
plt.figure(figsize=(15,8))
pca = PCA().fit(statsV2)
pca.explained_variance_ratio_
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')

plt.savefig("PCA_Variance.png")
