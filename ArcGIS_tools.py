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
#chunkList = open(chunks_file).read().splitlines()
## Hook into the data frame where you want to add the layer  
df  = arcpy.mapping.ListDataFrames(mapdoc, 'Layers')[0]  
#for item in chunkList:
#    # Create a Layer object  
#    lyr_DEM = arcpy.mapping.Layer(HomeDir+'/Python/DEMs/DEM_' + item + '.tif')
#    lyr_orthomosaic = arcpy.mapping.Layer(HomeDir+'/Python/OrthoMosaics/OrthoMosaic_' + item + '.tif')
#    # Add the layer object to the map  
#    arcpy.mapping.AddLayer(df, lyr_DEM, 'BOTTOM')
#    arcpy.mapping.AddLayer(df, lyr_orthomosaic, 'BOTTOM')

## change appearance of orthomosaic to show RGB composite and DEMs + change layer names to exclude .tif + save DEMs files
DEM_file = PyFolder + '/AM_input/DEM_file.txt'             # lists all DEMs
raster_file = PyFolder + '/AM_input/raster_file.txt'            # includes walker_tin
#Dfile = open(DEM_file, 'w')
#Rfile = open(raster_file, 'w')
#Rfile.write(walk_tin + '\n')
#layers = arcpy.mapping.ListLayers(mapdoc)
#for layer in layers:
#    if not 'example' in str(layer):
#        layer.name = str(layer).replace('.tif', '')
#        #updatelayer = arcpy.mapping.Layer(layer)
#        if 'DEM' in str(layer):
#            sourcelayer = arcpy.mapping.Layer(HomeDir +'/ArcFiles/DEM_example.lyr')
#            arcpy.mapping.UpdateLayer(df, layer, sourcelayer, True)
#            Dfile.write(layer.name + '\n')
#            Rfile.write(layer.name + '\n')
#        if 'OrthoMosaic' in str(layer):
#            sourcelayer = arcpy.mapping.Layer(HomeDir +'/ArcFiles/OrthoMosaic_example.lyr')
#            arcpy.mapping.UpdateLayer(df, layer, sourcelayer, True)
#Dfile.close()
#Rfile.close()


# CREATE PROFILE PLOTS

# Stack profile tool
surfaces = open(raster_file).read()
##print DEMs
stack_input_lf = profiles          
##print stack_input_lf
stack_profile_targets = surfaces.replace('\n', ';')
##print stack_profile_targets
stack_output = HomeDir + '/DealPostStorm.gdb/stack_table'
arcpy.StackProfile_3d(stack_input_lf, stack_profile_targets, stack_output,"#")        

## export the table to a CSV file
outputCSV = PyFolder + '/AM_output/transect_table.csv' 
with open(outputCSV, "w") as csvfile:  
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')  
    ## Write field name header line  
    fields = ['ObjectID','First_Dist', 'First_Z', 'Sec_Dist', 'Sec_Z', 'Line_ID', 'SRC_Type', 'SRC_ID', 'SRC_Name']  
    csvwriter.writerow(fields)  
    ## Write data rows  
    with arcpy.da.SearchCursor(stack_output, fields) as s_cursor:  
        for row in s_cursor:  
            csvwriter.writerow(row)

# Extract multi values to points: walker data 
# open file with only the DEM layers
DEMs = open(PyFolder + '/AM_input/DEM_file.txt').read()
DEMsList = DEMs.splitlines()

# first create layer with walker data within the polygon
WalkerDataOverlap = HomeDir + '/DealPostStorm.gdb/extracted_points_walker'
arcpy.Intersect_analysis(WalkerData + ' #;' + Overlapping_Polygon + ' #',WalkerDataOverlap,"ALL","#","POINT")

# extract multi values to points -> create those points in the walker data table!
ext_pts_input = "extracted_points_walker"     
ext_pts_raster = DEMs.replace('\n', ';')
arcpy.gp.ExtractMultiValuesToPoints_sa(ext_pts_input,ext_pts_raster,"BILINEAR")

## adding fields to the table for differences (differences: walker - DEM)
table = "extracted_points_walker"
for item in DEMsList:
    addField = 'diff_'+item
    #print addField
    arcpy.AddField_management(table, addField,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    math = "!Field4! - !"+item+"!"          ## NB: check that height field in walker data layer is field 4!!!
    arcpy.CalculateField_management(table, addField,math,"PYTHON_9.3","#")

## export the table to a CSV file
outputCSV = PyFolder + '/AM_output/extracted_points_walker.csv' 
with open(outputCSV, "w") as csvfile:  
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')  
    ## Write field name header line  
    fields = ['ObjectID', 'Shape', 'FID_walker_data', 'Field1', 'Field2', 'Field3', 'Field4', 'Field5', 'FID_beach_polygon'] + DEMsList + ['diff_'+DEM for DEM in DEMsList]  
    csvwriter.writerow(fields)  
    ## Write data rows  
    with arcpy.da.SearchCursor(WalkerDataOverlap, fields) as s_cursor:  
        for row in s_cursor:  
            csvwriter.writerow(row)

## Extract multi values to points: GCPs 
# open file with all raster layers
rasters = open(PyFolder + '/AM_input/raster_file.txt').read()
rastersList = rasters.splitlines()

# first create layer with walker data within the polygon
GCPsOverlap = HomeDir + '/DealPostStorm.gdb/extracted_points_GCPs'
arcpy.Intersect_analysis(GCPs + ' #;' + Overlapping_Polygon + ' #',GCPsOverlap,"ALL","#","POINT")

# Create walk DEM from the TIN so we can do calculations
Walk_TIN = rastersList[0]

# TIN to raster for walking data
Walk_DEM = HomeDir + '/DealPostStorm.gdb/walk_DEM'
arcpy.TinRaster_3d(Walk_TIN ,Walk_DEM, "FLOAT","LINEAR","CELLSIZE 0.1","1")

# change the rasterlist so that walk_DEM is used instead of walk_tin
rastersList[0] = 'walk_DEM'

# extract multi values to points -> create those points in the GCPs table!
ext_pts_input = "extracted_points_GCPs"     
ext_pts_raster = ';'.join(rastersList)
arcpy.gp.ExtractMultiValuesToPoints_sa(ext_pts_input,ext_pts_raster,"BILINEAR")

# adding fields to the table for differences (differences: walker - DEM)
table = "extracted_points_GCPs"
for item in rastersList:
    addField = 'diff_'+item
    #print addField
    arcpy.AddField_management(table, addField,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    math = "!Field5! - !"+item+"!"          ## NB: check that height field in GCPs layer is field 5!!!
    arcpy.CalculateField_management(table, addField,math,"PYTHON_9.3","#")

## export the table to a CSV file
outputCSV = PyFolder + '/AM_output/extracted_points_GCPs.csv' 
with open(outputCSV, "w") as csvfile:  
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')  
    ## Write field name header line  
    fields = ['ObjectID', 'Shape', 'FID_GCPs', 'Field1', 'Field2', 'Field3', 'Field4', 'Field5', 'Field6', 'FID_beach_polygon'] + rastersList + ['diff_'+raster for raster in rastersList]
    csvwriter.writerow(fields)  
    ## Write data rows  
    with arcpy.da.SearchCursor(GCPsOverlap, fields) as s_cursor:  
        for row in s_cursor:  
            csvwriter.writerow(row)

# VOLUMES
# extract by mask & surface volume tool (mask environment does not work, so need to first extract DEMs by mask)
mask = Overlapping_Polygon
#ExtractList = DEMsList[:]
#ExtractList[0] = 'walk_DEM'
for item in rastersList:
    extract_input = item
    extract_output = HomeDir + '/DealPostStorm.gdb/Extract_' + item
    arcpy.gp.ExtractByMask_sa(extract_input,mask,extract_output)
    volume_input = 'Extract_'+item
    volume_output = PyFolder + '/AM_output/Volume/volume_'+item+'.txt'
    arcpy.SurfaceVolume_3d(volume_input,volume_output,"ABOVE","-4","1","0")

    
#mapdoc.save()
#del mapdoc

