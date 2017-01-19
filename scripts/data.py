import csv
import datetime
import numpy as np
import pprint

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





if __name__ == "__main__":
  x,y = getDataLinearRegression()
  getAvgTime()
  print x.shape
  print y.shape
