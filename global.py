from pprint import pprint
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt 
from globalDataFetch import *
import numpy as np
from datetime import datetime

######### Figure 1 

dataGlobalCountLost = fetchDataGlobalCount('objets-trouves-gares')
dataGlobalCountFound = fetchDataGlobalCount('objets-trouves-restitution')
dataGlobalGivenBack = fetchDataGlobalGivenBack()

fig = figure(figsize=(6.5, 6.5)) 

plt.plot(dataGlobalCountLost['datetime'], dataGlobalCountLost['count'], label = 'Déclarations de perte', linewidth = 2)
plt.plot(dataGlobalCountFound['datetime'], dataGlobalCountFound['count'], label = 'Objets trouvés', linewidth = 2)
plt.plot(dataGlobalGivenBack['datetime'], dataGlobalGivenBack['count'], label = 'Objets restitués', linewidth = 2)

plt.xlabel('Date', fontsize = 14)
plt.ylabel('Nombre', fontsize = 14)
plt.xlim([dataGlobalCountLost['datetime'].tolist()[0], dataGlobalCountLost['datetime'].tolist()[-1]])
plt.ylim(bottom = 0)
plt.legend(fontsize = 10)
plt.savefig('Figure1.png' , dpi = 300)
plt.show()


######### Figure 2

dataGlobalCountLost = fetchDataGlobalCount('objets-trouves-gares')
dataGlobalCountFound = fetchDataGlobalCount('objets-trouves-restitution')
dataGlobalGivenBack = fetchDataGlobalGivenBack()

givenBackRate = np.array(dataGlobalGivenBack['count'])/np.array(dataGlobalCountFound['count'])*100
foundRate = np.array(dataGlobalCountFound['count'])/np.array(dataGlobalCountLost['count'])*100

fig = figure(figsize=(6.5, 6.5)) 

plt.plot(dataGlobalCountFound['datetime'], foundRate, label = "Taux d'objets retrouvés", linewidth = 2)
plt.plot(dataGlobalGivenBack['datetime'], givenBackRate, label = "Taux d'objets restitués", linewidth = 2)

plt.xlabel('Date', fontsize = 14)
plt.ylabel('Taux (%)', fontsize = 14)
plt.xlim([datetime.strptime('2015/01', '%Y/%m'), datetime.strptime('2020/01', '%Y/%m')])
plt.ylim([0,100])
plt.legend(fontsize = 10)
plt.savefig('Figure2.png' , dpi = 300)
plt.show()

######### Figure 3

dataAggPeriodicMonthly = fetchDataAggPeriodicMonthly()

fig = figure(figsize=(6.5, 6.5)) 

plt.step(dataAggPeriodicMonthly['x'], dataAggPeriodicMonthly['aggData'].values, where='mid', color = 'black')
plt.fill_between(dataAggPeriodicMonthly['x'], dataAggPeriodicMonthly['aggData'].values-dataAggPeriodicMonthly['stdData'].values, dataAggPeriodicMonthly['aggData'].values+dataAggPeriodicMonthly['stdData'].values, step='mid', color='k', alpha=0.15)

plt.xlabel('Mois', fontsize = 14)
plt.ylabel('Nombre de déclarations de perte', fontsize = 14)
plt.xlim([0,11])
plt.xticks(rotation=45)
plt.savefig('Figure3.png' , dpi = 300)
plt.show()

######### Figure 4

dataAggPeriodicDaily = fetchDataAggPeriodicDaily()

fig = figure(figsize=(6.5, 6.5)) 

plt.bar(dataAggPeriodicDaily['x'], dataAggPeriodicDaily['aggData'].values, yerr = dataAggPeriodicDaily['stdData'].values, color='grey', capsize=5)

plt.xlabel('Jour', fontsize = 14)
plt.ylabel('Nombre de déclarations de perte', fontsize = 14)
plt.xlim([-0.5,6.5])
plt.xticks(rotation=45)
plt.savefig('Figure4.png' , dpi = 300)
plt.show()

########## Figure 5

data = fetchDataAggType('objets-trouves-gares')

averageDict = {}

for objType in data.columns.tolist():
    averageDict.update({np.mean(np.array(data[objType])):objType})

topTen = sorted(list(averageDict.keys()), reverse = True)[0:10]

fig = figure(figsize=(8.5, 5)) 

for i in topTen:
    plt.plot(data[averageDict[i]], label = averageDict[i], linewidth = 2)

plt.xlabel('Date', fontsize = 12)
plt.ylabel('Nombre de déclarations de perte', fontsize = 12)
plt.xlim([data.index.tolist()[0],data.index.tolist()[-1]])
plt.ylim(bottom = 0)
plt.xticks(rotation=45, fontsize = 7)
plt.yticks(fontsize = 7)

leg = plt.legend(bbox_to_anchor=(1.05, 0.75), fontsize = 8)

for line in leg.get_lines():
    line.set_linewidth(4.0)

plt.tight_layout()
plt.savefig('Figure5.png' , dpi = 300)
plt.show()

########## Figure 6


dataDeclarationPerte = fetchDataAggType('objets-trouves-gares')
dataRetrouve = fetchDataAggType('objets-trouves-restitution')


for column in dataRetrouve.columns.tolist():
    dataRetrouve[column] = 100*dataRetrouve[column]/dataDeclarationPerte[column]
    dataRetrouve[column]  = dataRetrouve[column].rolling(8, win_type='gaussian').mean(std=3)

averageDict = {}

for objType in dataRetrouve.columns.tolist():
    averageDict.update({np.mean(np.array(dataRetrouve[objType])):objType})

topTen = sorted(list(averageDict.keys()), reverse = True)[0:10]

fig = figure(figsize=(8.5, 5)) 

for i in topTen:
    plt.plot(dataRetrouve[averageDict[i]], label = averageDict[i], linewidth = 2)

plt.xlabel('Date', fontsize = 12)
plt.ylabel("Taux d'objets retrouvés (%)", fontsize = 12)
plt.xlim([datetime.strptime('2015/08', '%Y/%m'), datetime.strptime('2019/12', '%Y/%m')])
plt.xticks(rotation=45, fontsize = 7)
plt.yticks(fontsize = 7)

leg = plt.legend(bbox_to_anchor=(1.05, 0.75), fontsize = 8)

for line in leg.get_lines():
    line.set_linewidth(4.0)

plt.tight_layout()
plt.savefig('Figure6.png' , dpi = 300)
plt.show()