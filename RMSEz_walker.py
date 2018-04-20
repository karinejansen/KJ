# Import modules
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from math import sqrt
import matplotlib.pyplot as plt

# DEFINE STUFF
# Define: Home directory (later this is referred at ".")???
HomeDir = 'D:/Karine/ArcGIS/Deal/PostStorm03112018'

#rms = sqrt(mean_squared_error(y_actual, y_predicted))

# List of sections and list of layers
DEMsList = open(HomeDir + '/Python/AM_input/DEM_file.txt').read().splitlines()

# Assign the filename: file
file = HomeDir + '/Python/AM_output/extracted_points_walker.csv'

# Read the file into a DataFrame : df
df = pd.read_csv(file, header=0)

#calculate rmse in vertical direction
RMSEz_walker = {}
for item in DEMsList:
    RMSEz_walker[item] = sqrt(mean_squared_error(df['Field4'], df[item]))

print "RMSEz_walker ="
print RMSEz_walker

# calculate median absolute error
MAEz_walker = {}
for item in DEMsList:
    MAEz_walker[item]= median_absolute_error(df['Field4'], df[item])

print 'Median Absolute Error, z walker ='
print MAEz_walker
