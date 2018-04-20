# This script determines the slope vs error on walker data

# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv


# DEFINE STUFF
# Define: Home directory (later this is referred at ".")???
HomeDir = 'D:/Karine/ArcGIS/Deal/PostStorm03112018'

# define: who was walking
persons = ['MJ', 'LK']
color = ['r', 'b']

# Assign the filename: file
file = HomeDir + '/Python/AM_output/extracted_points_walker.csv'

# Read the file into a DataFrame using only columns 1,2,5 & 8: df
df = pd.read_csv(file)

# add data columns
df.loc[:,'distance'] = 0
df.loc[:,'slope'] = 9999

df2 = df.sort_values(['Field5', 'Field1'])
df2 = df2.reset_index(drop=True)

# calculate distance and slope 
for i in range(len(df2['Field3'])-1):
    df2.loc[i+1,'distance'] = math.sqrt((df2.loc[i+1,'Field3']-df2.loc[i,'Field3'])**2 + (df2.loc[i+1,'Field2']-df2.loc[i,'Field2'])**2 )
    if df2.loc[i+1,'distance'] > 35 or df2.loc[i,'Field1']+1 != df2.loc[i+1,'Field1']:
        df2.loc[i+1,'distance'] = 0
    if df2.loc[i+1,'distance'] != 0:
        df2.loc[i+1,'slope'] = (df2.loc[i+1,'Field4'] - df2.loc[i,'Field4']) / df2.loc[i+1,'distance']
    
#print df2[['FID_walker_data', 'Field1', 'distance', 'slope']]

# plot slope vs error (DEM_380ft_15GCP)
df3 = df2.groupby(['Field5'])

# export df to csv
df_export = df2.sort_values(['Field5', 'slope'])
df_export = df_export.reset_index(drop=True)
df_export.to_csv(HomeDir + '/Python/AM_output/slope_error_df.csv')

# create plot
fig, (ax1, ax2) = plt.subplots(1,2,sharey=True)
for p in range(len(persons)):
    df4 = df3.get_group(persons[p])
    df4 = df4.sort_values(['slope'])
    df4 = df4.reset_index(drop=True)
    x_slope_up = []
    y_error_up = []
    x_slope_down = []
    y_error_down = []
    for i in range(len(df4['slope'])):
        if df4.loc[i,'slope'] != 9999 and df4.loc[i,'slope'] < 0.75 and df4.loc[i,'slope'] > -0.75:
            if df4.loc[i,'slope'] <= 0 and df4.loc[i,'diff_DEM_380ft_21GCP'] > -1.5:
                x_slope_down.append(df4.loc[i,'slope'])
                y_error_down.append(df4.loc[i,'diff_DEM_380ft_21GCP'])
            if df4.loc[i,'slope'] >= 0 and df4.loc[i,'diff_DEM_380ft_21GCP'] > -1.5:
                x_slope_up.append(df4.loc[i,'slope'])
                y_error_up.append(df4.loc[i,'diff_DEM_380ft_21GCP'])
                                    
    #with open(HomeDir + '/Python/AM_output/slope_error_' + persons[p] + '.csv', 'wb') as myfile:
    #    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #    wr.writerow(x_slope_down)
    #    wr.writerow(y_error_down)
    #    wr.writerow(x_slope_up)
    #    wr.writerow(y_error_up)
    # scatter plots
    ax1.scatter(x_slope_down, y_error_down, c = color[p] , marker="o", label= persons[p])
    ax2.scatter(x_slope_up, y_error_up, c = color[p] , marker="o", label= persons[p])
    # linear trendlines
    z_down = np.polyfit(x_slope_down,y_error_down,1)
    p_down = np.poly1d(z_down)
    ax1.plot(x_slope_down, p_down(x_slope_down),'--', c = color[p], label = "y=%.6fx+(%.6f)"%(z_down[0],z_down[1]))
    z_up = np.polyfit(x_slope_up,y_error_up,1)
    p_up = np.poly1d(z_up)
    ax2.plot(x_slope_up, p_up(x_slope_up),'--', c = color[p], label = "y=%.6fx+(%.6f)"%(z_up[0],z_up[1]))
        
ax1.set(title = 'Difference in elevation measured by walker and drone vs slope of the surface', ylabel='Elevation difference [ft]', xlabel = 'negative slope [-]', xlim = [-0.75,0]) #title='Negative slope',
ax2.set(xlabel = 'positive slope [-]', xlim = [0.0, 0.75]) #title='Positive slope', 
plt.ylim([-1.1, 0.2])
ax1.grid()
ax2.grid()
#plt.title('Error between walker and drone elevation vs slope of the surface')
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
plt.show()


