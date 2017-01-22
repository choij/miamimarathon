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
import math

from functions import multiply, inverse, subtract, transpose, addOnes, weights, gradError, getData

     

    
def naive (X,n):
    ID,age,gender,rank,time,pace,year = getData()
    temp = []
    variance = []
    meanX = []
    X = transpose(X)
    covar = [[0 for i in range (n)]for j in range (n)]
    
    variance.append(np.var(age))
    meanX.append(np.mean(age))
    
    variance.append(np.var(gender))
    meanX.append(np.mean(gender))
    
    variance.append(np.var(pace))
    meanX.append(np.mean(pace))
    
    variance.append(np.var(year))
    meanX.append(np.mean(year))
    
    for i in range (n):
        covar[i][i] = variance[i]

    for i in range (len(X)):
        temp.append(X[i] - meanX[i])
    
    covarInv = inverse(covar)
    num = math.exp(multiply(-0.5,(multiply(transpose(temp),multiply(covarInv,temp)))))
    den = ((math.pi)**0.5) * ((np.linalg.det(covar))**0.5)
    
    return num/den

X = [17,1,580,2015]
print naive(X,4)       
