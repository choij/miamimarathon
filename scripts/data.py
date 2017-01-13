import csv
import re
import datetime

def gender( g ):
  if (g == 'M'):
    return 1
  else:
    return 0

def toSeconds(h,m,s):
  return int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())

def getData():
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

        # Add race time in seconds
        h,m,s = row[5].split(':')
        seconds = toSeconds(h,m,s)
        row.append(seconds)

        pace_m, pace_s = row[6].split(':')
        pace_seconds = toSeconds(0,pace_m,pace_s)
        row.append(pace_seconds)

        # Transform M/F to 1/0
        row.append( gender(row[3]) )
        row.pop(6)
        row.pop(5)
        row.pop(3)
        row.pop(1)
        writer.writerow( row )

#def timeToSeconds:
 
getData() 
