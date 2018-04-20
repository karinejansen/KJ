# This script produces profile plots at differenct sections along the beach of Forstescue for three different layers

# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#from cycler import cycler
#plt.rc('axes', prop_cycle= (cycler('color', ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']) + cycler('linestyle', ['--', '-', '-', '-', '-', '-', '-', '-'])))
# DEFINE STUFF
# Define: Home directory (later this is referred at ".")???
HomeDir = 'D:/Karine/ArcGIS/Deal/PostStorm03112018'

# Define: sections
sectionList = [1,2,3,4,5,6,7,8]
print sectionList

# Define: list of layers
layerList = open(HomeDir + '/Python/AM_input/raster_file.txt').read().splitlines()
print layerList

# Assign the filename: file
file = HomeDir + '/Python/AM_output/transect_table.csv'

# Read the file into a DataFrame using only columns 1,2,5 & 8: df
df = pd.read_csv(file, usecols =(1,2,5,8))

# Rename column headings
df.columns = ['distance', 'elevation', 'section', 'layer']

# Group by section and layer at once
df_grouped = df.groupby(['section', 'layer'])

# create line colors
Color_Dict = {}
Color_Dict[layerList[0]]='r--'
Color_Dict[layerList[1]]='b'
Color_Dict[layerList[2]]='c'
Color_Dict[layerList[3]]='m'
Color_Dict[layerList[4]]='b:'
Color_Dict[layerList[5]]='c:'
Color_Dict[layerList[6]]='m:'


# loops to get per section data and per layer and make plots
Layer = dict()

for s in sectionList:
    fig, ax = plt.subplots()
    for item in layerList:
        Layer[item] = df_grouped.get_group((s,item))
        ax.plot(Layer[item].loc[:,'distance'],Layer[item].loc[:,'elevation'], Color_Dict[item], label=item)
        #ax.plot(Layer[item].loc[:,'distance'],Layer[item].loc[:,'elevation'], label=item)
    legend = ax.legend(loc='lower left', shadow=True)    
    plt.xlabel('Distance [ft]')
    plt.ylabel('Elevation [ft]')
    plt.title('Transect %i' % (s))
    plt.grid(True)
plt.show()

# 3th try: all in one figure
#Layer = dict()
#plt.figure(1)
#for s in sectionList:
#	plt.subplot(len(sectionList),1,int(s)+1)
#	for item in layerList:
#		Layer[item] = df_grouped.get_group((s,item))
#		plt.plot(Layer[item].loc[:,'distance'],Layer[item].loc[:,'elevation'], Color_Dict[item], label=item)
#	plt.title('Section %i' % (s))
#	plt.grid(True)
#legend = ax.legend(loc='upper left', shadow=True)
#plt.show()
