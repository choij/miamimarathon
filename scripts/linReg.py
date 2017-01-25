#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Comp 551
Assignment 1
Functions required for the assignment
Author: Sharhad, Jonathan, Mathieu
Created on Fri Jan 13, 2017
"""

import csv
import datetime
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt 
from numpy.linalg import linalg
import seaborn as sns

from functions import multiply, inverse, subtract, transpose, addOnes, weights, gradError, getData
    
def ageVpace():
    ID,age,gender,rank,time,pace,year = getData()    
    plt.scatter(age,pace)    
    print ("Age vs. Pace")
    #w = weights (age,pace)
    w = gradError(age,pace,2)
    print w
    plt.show()

def yearVpace():
    ID,age,gender,rank,time,pace,year = getData()    
    plt.scatter(year,pace)    
    print ("Year vs. Pace")
    w = weights(year,pace)
    #print w
    plt.show()
    
def numOfMarVpace():
    ID,age,gender,rank,time,pace,year = getData() 
    rep = [[]for x in range(13)]
    maxID = int(ID[len(ID)-1])
    for i in range (1,maxID):
        index = ID.count(float(i))
        
        if (index == 1):
            rep[0].append(pace[ID.index(i)])
        elif (index == 2):
            rep[1].append(pace[ID.index(i)])
        elif (index == 3):
            rep[2].append(pace[ID.index(i)])
        elif (index == 4):
            rep[3].append(pace[ID.index(i)])
        elif (index == 5):
            rep[4].append(pace[ID.index(i)])
        elif (index == 6):
            rep[5].append(pace[ID.index(i)])
        elif (index == 7):
            rep[6].append(pace[ID.index(i)])
        elif (index == 8):
            rep[7].append(pace[ID.index(i)])
        elif (index == 9):
            rep[8].append(pace[ID.index(i)])
        elif (index == 10):
            rep[9].append(pace[ID.index(i)])
        elif (index == 11):
            rep[10].append(pace[ID.index(i)])
        elif (index == 12):
            rep[11].append(pace[ID.index(i)])
        elif (index == 13):
            rep[12].append(pace[ID.index(i)])

#    for i in range(13):
#        sns.stripplot(x=i, y="pace", data=rep[i]);   
#    print ("# of appareance  vs. Pace")
#    plt.show
    print rep
    
#ageVpace()
#yearVpace()    
numOfMarVpace()        


       
