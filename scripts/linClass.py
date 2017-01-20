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

def getData():
    data = np.loadtxt(open("miamimarathon/data/data.csv","rb"),delimiter=",",skiprows=1)
    numData = len(data)
    ID = []
    age = []
    gender = []
    rank = []
    time = []
    pace = []
    year = []
    for i in range(numData):
        #if (data[i][3] !=2016 and data[i][6] == 1):
        if (data[i][6] == 1):
            ID.append     (data[i][0])
            age.append    (data[i][1])
            rank.append   (data[i][2])
            year.append   (data[i][3])
            time.append   (data[i][4])
            pace.append   (data[i][5])
            gender.append (data[i][6])
        
    return ID,age,gender,rank,time,pace,year