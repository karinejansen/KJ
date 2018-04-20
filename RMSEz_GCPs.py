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
rastersList = open(HomeDir + '/Python/AM_input/raster_file.txt').read().splitlines()
rastersList[0] = 'walk_DEM'

# Assign the filename: file
file = HomeDir + '/Python/AM_output/extracted_points_GCPs.csv'

# Read the file into a DataFrame : df
df = pd.read_csv(file, header=0)

#calculate rmse in vertical direction
RMSEz_GCP = {}
for item in rastersList:
    RMSEz_GCP[item] = sqrt(mean_squared_error(df['Field5'], df[item]))

print 'RMSEz_GCP'
print RMSEz_GCP

# calculate median absolute error
MAEz_GCP = {}
for item in rastersList:
    MAEz_GCP[item]= median_absolute_error(df['Field5'], df[item])

print 'Median Absolute Error, z GCP ='
print MAEz_GCP
