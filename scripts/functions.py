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

#Multiply matricies        
def multiply(A,B):
    return np.dot(A,B)

#Inverse matrix
def inverse (A):
    if (len(A) == len(A[0])):
        return inv(A)
    else:
        print ("Matrix cannot be inverted")
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
    Xt = transpose(X)
    temp1 = inverse(multiply(Xt,X))
    temp2 = multiply(temp1,Xt)
    w = multiply(temp2,Y)
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
    
        


       
