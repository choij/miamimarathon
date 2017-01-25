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
import sys
sys.setrecursionlimit(10000)

from functions import multiply, inverse, subtract, transpose, addOnes, weights, gradError, getData, addition


        
def sigmoid (a):
    return 1/(1+np.exp(-a))

def check(w):
    numData, age, gender, time, numRace, yearLast, Y = getData() 
    X = [0 for i in range(6)] 
    error = 0
    for i in range(numData):
        X[0] = age[i]
        X[1] = (gender[i])
        X[2] = (time[i])
        X[3] = (numRace[i])
        X[4] = (yearLast[i]) 
        X[5] = 1
        
        a = multiply(transpose(w),X)
        proby1 = multiply(Y[i],math.log(sigmoid(a)))
        proby0 = multiply(1-Y[i],math.log(1-sigmoid(a)))

        error += proby1 + proby0
    return error

def sinErr(X,Y,w):
    w = np.matrix(w)
    X = np.matrix(X)
    X = transpose(X)    
    diff = Y - sigmoid(multiply(transpose(w),X))
    sinError = multiply(X,diff)

    return sinError

def errDer(w):
    numData, age, gender, time, numRace, yearLast, Y = getData() 
    X = [0 for i in range(6)]
    errorDer = [[0] for i in range(6)]    
    for i in range(numData):
        X[0] = age[i]
        X[1] = (gender[i])
        X[2] = (time[i])
        X[3] = (numRace[i])
        X[4] = (yearLast[i])  
        X[5] = 1
        errorDer += sinErr (X,Y[i],w)

    return errorDer    

def weight(wCurr,epsilon):
    for i in range(100):    
        error = errDer(wCurr)
        print i
        print wCurr
        alpha = 0.001
        wNew = addition(wCurr,(multiply(alpha,error)))
        #print wNew
        if (abs(subtract(wNew,wCurr)).all() < epsilon):
            return wNew
        wCurr = wNew
    return wCurr
#    weight(wCurr,epsilon)
    
wCurr = [[0] for x in range (6)]
w = weight(wCurr,1e-6)
print w
print check(w)



