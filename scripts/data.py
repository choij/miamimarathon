import csv
import re
import datetime

def gender( g ):
  if (g == 'M'):
    return 1
  else:
    return 0

def getData():
  filename = '../data.csv'
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        # Add race time in seconds
        h,m,s = row[5].split(':')
        seconds = int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
        row.append(seconds)

        # Transform M/F to 1/0
        row.append( gender(row[3]) )
        print row

#def timeToSeconds:
 
getData() 
