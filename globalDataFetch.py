from matplotlib.pyplot import figure
import json
import pandas as pd
import requests 
from pandas.io.json import json_normalize
import dateutil.parser
from datetime import datetime
from pprint import pprint
import matplotlib.pyplot as plt 
import calendar

def fetchDataGlobalCount(dataset):

    parameters = {
        'dataset':dataset,
        'sort':'date',
        'x':'date',
        'precision':'month',
        'y.count.func':'COUNT',
        } 

    response = requests.get(url = 'https://data.sncf.com/api/records/1.0/analyze/' , params = parameters) 
    requestedData = response.json()
    data = json_normalize(requestedData)

    data['datetime'] = data['x.year'].astype(str) + '-' + data['x.month'].astype(str)
    data['datetime'] = pd.to_datetime(data['datetime'])
    
    data = data.drop(['x.year', 'x.month'], axis=1)

    return data

def fetchDataGlobalGivenBack():

    parameters = {
        'dataset':'objets-trouves-restitution',
        'sort':'date',
        'x':'gc_obo_date_heure_restitution_c',
        'precision':'month',
        'y.count.func':'COUNT',
        } 

    response = requests.get(url = 'https://data.sncf.com/api/records/1.0/analyze/' , params = parameters) 
    requestedData = response.json()
    data = json_normalize(requestedData)

    data['datetime'] = data['x.year'].astype(str) + '-' + data['x.month'].astype(str)
    data['datetime'] = pd.to_datetime(data['datetime'])
    
    data = data.drop(['x.year', 'x.month'], axis=1)

    return data


def fetchDataAggPeriodicMonthly():

    parameters = {
        'dataset':'objets-trouves-gares',
        'sort':'date',
        'exclude.date':[2013,2014,2020],
        'x':'date',
        'precision':'month',
        'y.count.func':'COUNT',
        } 

    response = requests.get(url = 'https://data.sncf.com/api/records/1.0/analyze/' , params = parameters) 
    requestedData = response.json()
    data = json_normalize(requestedData)

    aggData = data.groupby('x.month').mean()['count']
    stdData = data.groupby('x.month').std()['count']
    
    x = aggData.index.tolist()
    
    for i in range(len(x)):
        x[i] = calendar.month_abbr[x[i]].capitalize()

    result = {
        'x': x,
        'aggData':aggData,
        'stdData':stdData,
    }

    return result

def fetchDataAggPeriodicDaily():

    parameters = {
        'dataset':'objets-trouves-gares',
        'sort':'date',
        'exclude.date':[2013,2014,2020],
        'x':'date',
        'precision':'day',
        'y.count.func':'COUNT',
        } 

    response = requests.get(url = 'https://data.sncf.com/api/records/1.0/analyze/' , params = parameters) 
    requestedData = response.json()
    data = json_normalize(requestedData)

    data['datetime'] = data['x.year'].astype(str) + '-' + data['x.month'].astype(str) + '-' + data['x.day'].astype(str)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['dayName'] = data['datetime'].dt.weekday

    aggData = data.groupby('dayName').mean()['count']
    stdData = data.groupby('dayName').std()['count']
    
    x = aggData.index.tolist()
    
    for i in range(len(x)):
        x[i] = calendar.day_abbr[x[i]].capitalize()

    result = {
        'x': x,
        'aggData':aggData,
        'stdData':stdData,
    }

    return result


def fetchDataAggType(dataset):

    parameters = {
        'dataset':dataset,
        'exclude.date':[2013,2014,2020],
        'x':['date','gc_obo_type_c'],
        'precision':'month',
        'y.count.func':'COUNT',
        } 

    response = requests.get(url = 'https://data.sncf.com/api/records/1.0/analyze/' , params = parameters) 
    requestedData = response.json()
    data = json_normalize(requestedData)

    data['datetime'] = data['x.date.year'].astype(str) + '-' + data['x.date.month'].astype(str)
    data['datetime'] = pd.to_datetime(data['datetime'])

    data = data.pivot(index='datetime', columns='x.gc_obo_type_c', values='count')

    return data
