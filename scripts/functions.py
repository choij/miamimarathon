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

#Multiply matricies        
def multiply(A,B):
    return np.dot(A,B)

#Inverse matrix
def inverse (A):
    m = 10^-6
    Ainv = linalg.inv(A + np.eye(A.shape[1]) * m)
    return Ainv

#Add matricies
def addition(A,B):
    return np.add(A,B)
    
#subtract matricies    
def subtract(A,B):
    return np.subtract(A,B)

#Transpose matricies
def transpose (A):
    return np.transpose(A)  

#add rows of 1        
def addOnes(X,size):
    length = len(X)
    newX = [[1 for i in range (length)] for j in range (size)]
    for i in range(length):
        newX[0][i] = X[i]
    return newX
         
#Calculate the weights
def weights(X,Y):
#w = (X^T*X)^-1X^T*Y
    X = addOnes(X,2)
    X = transpose(X)

    Xt = transpose(X)

    temp1 = inverse(multiply(Xt,X))
    temp2 = multiply(Xt,Y)
    w = multiply(temp1,temp2)
    return w

#Calculate the gradient error 
def gradError(w,X,Y):
#Err(w) = 2*(X^T*X*w - X^T*Y)
    w = weights(X,Y)
    Xt =  transpose(X)
    temp1 = multiply(multiply(Xt,X),w)
    temp2 = multiply(Xt, Y)
    err = subtract(temp1,temp2)
    return multiply(2,err)

def getData():
    data = np.loadtxt(open("../data/data.csv","rb"),delimiter=",",skiprows=1)
    numData = len(data)
    ID = []
    age = []
    gender = []
    rank = []
    time = []
    pace = []
    year = []
    for i in range(numData):
        if (data[i][3] !=2016 and data[i][6] == 1):
        #if (data[i][6] == 1):
            ID.append     (data[i][0])
            age.append    (data[i][1])
            rank.append   (data[i][2])
            year.append   (data[i][3])
            time.append   (data[i][4])
            pace.append   (data[i][5])
            gender.append (data[i][6])
        
    return ID,age,gender,rank,time,pace,year
    



       
