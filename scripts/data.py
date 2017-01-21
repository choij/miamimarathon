import csv
import datetime
import numpy as np
import pprint
import matplotlib.pyplot as plt
import pandas as pd

#================================================================================
#                    NUMERIC REPRESENTATION OF GENDER DATA
#================================================================================
def gender( g ):
  if (g == 'M'):
    return 1
  else:
    return 0

#================================================================================
#                      CHANGE TIME FROM HH:MM:SS TO SECONDS
#================================================================================
def toSeconds(h,m,s):
  return int(datetime.timedelta(hours=int(h),minutes=int(m),
             seconds=int(s)).total_seconds())

#================================================================================
#                       WRITING DATA FILE FROM RAW DATA
#================================================================================
def transformRawData():
  with open('../data/Project1_data.csv', 'rb') as f:
    with open('../data/data.csv', 'w') as csvoutput:
      writer = csv.writer(csvoutput)
      reader = csv.reader(f)

      firstline = True
      for row in reader:
        if firstline:
          firstline = False
          writer.writerow( ['Id','Age','Rank','Year','Time','Pace','Sex'] )
          continue

        # Add race/pace time in seconds
        h,m,s = row[5].split(':')
        seconds = toSeconds(h,m,s)
        row.append(seconds)

        pace_m, pace_s = row[6].split(':')
        pace_seconds = toSeconds(0,pace_m,pace_s)
        row.append(pace_seconds)

        # Transform M/F to 1/0
        row.append( gender(row[3]) )

        # Remove redundant data
        row.pop(6)
        row.pop(5)
        row.pop(3)
        row.pop(1)
        writer.writerow( row )

#================================================================================
#                         READ DATA INTO NUMPY MATRIX
#================================================================================
def readData():
  d = np.loadtxt(open("../data/data.csv","rb"),delimiter=",",skiprows=1)
  return d

#================================================================================
#               GET AVERAGE MARATHON COMPLETION TIME PER YEAR
#                           >> { year: avg time } 
#================================================================================
def getAvgTime():
  d = readData()
  n = d.shape[0]
  
  years = {}
  for i in range (n):
    if str(d[i][3]) in years.keys():
      years[str(d[i][3])][0] += 1
      years[str(d[i][3])][1] += d[i][4]
    else:
      years[str(d[i][3])] = [ 1, d[i][4] ]
  for year in years.keys():
    years[year] = (years[year][1]/years[year][0])

  return years

#================================================================================
# Returns X matrix (n x m)
#   >> Features: Id, Age, Year, Time, Pace, Sex
# Returns Y matrix (n x 1)
#   >> Rank
#================================================================================
def getDataLinearRegression():
  x = readData()
  y = x[:,[2]]
  x = np.delete(x, 2, axis=1)
  return x,y

def getZeroAgeId():
  x,y = getDataLinearRegression()
  ids = {}
  for i in range (x.shape[0]):
    #if(x[i][1] != 0 and x[i][0] in zeroage):
    if(x[i][1] == 0):
      ids[str( x[i][0] )] = x[i][2]
  return ids

def histogramAge():
  x,y = getDataLinearRegression()
  age = x[:,[1]]
  age = np.transpose(x[:,[1]])[0]

  histogram = plt.figure()
  plt.hist(age, bins=range(100), facecolor='grey')
  plt.title('Histogram of Runners\' Ages from Entire Dataset')
  plt.xlabel('Age')
  plt.ylabel('Number of Runners')
  print max(age)    # only id's 5143 and 10179 have age>90
  plt.show()

def correctSingleInstanceAge(runnerId,data):
    rank = int(data[data['Id'] == runnerId]['Rank'])
    year = int(data[data['Id'] == runnerId]['Year'])
    rangeOfRunners = data[(data['Rank']>rank-50) & (data['Rank']<rank+50)& (data['Year'] == year)]
    avgAge = rangeOfRunners['Age'].sum()/rangeOfRunners['Age'].size

    index = data[data['Id']==runnerId].index
    data.set_value(index, 'Age', avgAge)
    return

def offsetAge(idRecorded,idError,data):
    ageRecorded = data.loc[idRecorded]['Age']
    yearRecorded = data.loc[idRecorded]['Year']
    yearError = data.loc[idError]['Year']
    offset = yearError - yearRecorded
    data.set_value(idError, 'Age', ageRecorded+offset)
    return

def yearsSinceLastRace(runnerId,year,data):
    runnerAllYears = data[(data['Id']==runnerId) & (data['Year']<year)].sort_values(by='Year')['Year']
    if( runnerAllYears.size == 0 ):
        lastYear = year
    else:
        lastYear = max(runnerAllYears)
    return year-lastYear
   
def fullMarathonTime(halfMarathonTime,data):
    return np.round(halfMarathonTime*((26.219/13.095)**1.06))
 
def cleanData():
  data = pd.read_csv('../data/data.csv')
  zeroAge = data[data['Age'] == 0].index.tolist()
  runnerId = [data.iloc[x]['Id'] for x in zeroAge]
  
  ageCorrectionRunnerIds = [16673,16954,17902,18202,22942]
  for n in ageCorrectionRunnerIds:
      correctSingleInstanceAge(n,data)

  zeroAge = data[(data['Age'] == 0)&(data['Id'] != 26270) &(data['Id'] != 23714) ].index.tolist()
  runnerId = [data.iloc[x]['Id'] for x in zeroAge]
  for i in runnerId:
      print data[data['Id'] == i].sort_values(by='Year')

  offsetAge(488,489,data)
  offsetAge(2049,2046,data)
  offsetAge(10743,10745,data)
  offsetAge(13066,13065,data)
  offsetAge(24232,24231,data)
  data = data.drop([31786])

  print "Floor ages to increments of 5"
  for i in range (data['Age'].size):
    data.iloc[i]['Age'] = data.iloc[i]['Age'] - data.iloc[i]['Age']%5

  # Add Temperature Data
  print "Adding Temperature"
  temp = {
      '2003':10.6,
      '2004':20.6,
      '2005':18.9,
      '2006':21.1,
      '2007':22.2,
      '2008':17.8,
      '2009':14.4,
      '2010':21.7,
      '2011':11.1,
      '2012':20.6,
      '2013':19.4,
      '2014':22.8,
      '2015':11.7,
      '2016':12.2
  }
  data['Temp'] = 0.

  for i in data.index.tolist():
    year = str(int(data.loc[i]['Year']))
    data.set_value(i,'Temp',temp[year])

  # Add Number of Races
  print "Adding number of Races"
  data['raceCount'] = 0
  for i in data.index.tolist():
    runnerId = data.loc[i]['Id']
    count = int(data[data['Id']==runnerId]['Id'].size)
    data.set_value(i,'raceCount',count)

  for i in data.index.tolist():
    runnerId = data.loc[i]['Id']
    year = data.loc[i]['Year']
    #data.set_value(i,'totalNumRaces',count)
    data.set_value(i,'yrsSinceLast',int(yearsSinceLastRace(runnerId,year,data)))

  # Riegel's Formula
  print "Editing 2013 half marathon data"
  halfMarathonId = data[data['Year']==2013].index.tolist()
  data['halfMarathonTime'] = np.NaN

  for i in halfMarathonId:
    time = data.loc[i]['Time']
    data.set_value(i,'halfMarathonTime',time)
    data.set_value(i,'Time',int(fullMarathonTime(time,data)))

if __name__ == "__main__":
  #histogramAge()
  cleanData()
