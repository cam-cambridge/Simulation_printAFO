# Importing required modules
import math
import random
import matplotlib.pyplot as plt

# Define function
def function1(x):
    value = -x**2
    return value

def function2(x):
    value = -(x-2)**2
    return value

# Function to find index of list
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
            return -1

'''list1=[1,2,3,4,5,6,7,8,9]
value=[1,5,6,7]
sort_list=[1,5,6,7]'''
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
            values[index_of(min(values),values)] = math.inf
 #     infinited    return sorted_list
