import csv
import datetime
import numpy as np
import pprint
import matplotlib.pyplot as plt

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

def ageOutliers():
  return 
 
def cleanData():
  x,y = getDataLinearRegression()
  zeroage = getZeroAgeId().keys()

  for i in range (x.shape[0]):
    if(x[i][1] != 0 and str(x[i][0]) in zeroage):
      #print x[i]
      continue
    if(x[i][0] in [5143,10179]):
      print x[i]

if __name__ == "__main__":
  histogramAge()
  #cleanData()
