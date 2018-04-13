# Python script to execute ArcMAP tasks to compare UAV DEMs to walker data

# import stuff
import arcpy
#import os
#import glob
import csv


# DEFINE STUFF
# Define: Home directory (later this is referred at ".")???
HomeDir = 'D:/Karine/ArcGIS/Deal/PostStorm03112018'

# Define: python folder
PyFolder = HomeDir + '/Python_380ft_15GCP'

# Define: input chunk names file location
chunks_file = PyFolder + '/AM_input/input_chunks.txt'

# Define: ArcMap map document
mapdoc = arcpy.mapping.MapDocument(HomeDir+'/Maps/Deal03112018_15GCP.mxd')

# Set the environment (???)
arcpy.env.workspace = HomeDir + '/DealPostStorm.gdb' 

# Define: walker surface in map document
walk_tin = 'walk_tin'
profiles = 'beach_transects'
GCPs = 'GCPs'
WalkerData = 'walker_data'
Overlapping_Polygon = 'beach_polygon'

# START ACTUAL SCRIPT (DO NOT EDIT ANYTHING BELOW THIS!)
# turn extentions on (3D and spatial analyst)
arcpy.CheckOutExtension('3D')
arcpy.CheckOutExtension('Spatial')

## Add DEMs from photoscan
chunkList = open(chunks_file).read().splitlines()
# Hook into the data frame where you want to add the layer  
df  = arcpy.mapping.ListDataFrames(mapdoc, 'Layers')[0]  
for item in chunkList:
    # Create a Layer object  
    lyr_DEM = arcpy.mapping.Layer(PyFolder +'/DEMs/DEM_' + item + '.tif')
    lyr_orthomosaic = arcpy.mapping.Layer(PyFolder + '/OrthoMosaics/OrthoMosaic_' + item + '.tif')
    # Add the layer object to the map  
    arcpy.mapping.AddLayer(df, lyr_DEM, 'BOTTOM')
    arcpy.mapping.AddLayer(df, lyr_orthomosaic, 'BOTTOM')

## change appearance of orthomosaic to show RGB composite and DEMs + change layer names to exclude .tif + save DEMs files
DEM_file = PyFolder + '/AM_input/DEM_file.txt'             # lists all DEMs
raster_file = PyFolder + '/AM_input/raster_file.txt'            # includes walker_tin
Dfile = open(DEM_file, 'w')
Rfile = open(raster_file, 'w')
Rfile.write(walk_tin + '\n')
layers = arcpy.mapping.ListLayers(mapdoc)
for layer in layers:
    if not 'example' in str(layer):
        layer.name = str(layer).replace('.tif', '')
        #updatelayer = arcpy.mapping.Layer(layer)
        if 'DEM' in str(layer):
            sourcelayer = arcpy.mapping.Layer(HomeDir +'/ArcFiles/DEM_example.lyr')
            arcpy.mapping.UpdateLayer(df, layer, sourcelayer, True)
            Dfile.write(layer.name + '\n')
            Rfile.write(layer.name + '\n')
        if 'OrthoMosaic' in str(layer):
            sourcelayer = arcpy.mapping.Layer(HomeDir +'/ArcFiles/OrthoMosaic_example.lyr')
            arcpy.mapping.UpdateLayer(df, layer, sourcelayer, True)
Dfile.close()
Rfile.close()

   
mapdoc.save()
del mapdoc
