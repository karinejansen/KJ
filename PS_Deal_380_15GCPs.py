# Python script to export DEMs, orthomosaics and estimated marker locations and errors of the Deal_altitude_checkpoints PhotoScan file

# Current PhotoScan Project ( is now defined with PhotoScan Project File!!)
#doc = PhotoScan.app.document

# Define: Home directory (later this is referred at ".") (this is where I want to save all the products of this script)
HomeDirectory = 'F:/Karine/ArcGIS/Deal/PostStorm03112018/Python_380ft_15GCP'

# Define: PhotoScan Project File
PhotoScanProjectFile = 'E:/Karine/PhotoScan/Deal_380ft_15GCPpsx'

# Define: Coordinate system
CoordinateSystemEPSG = 'EPSG::6527'

# Define: DEMResolutions (in meters??), 
# 0 == GSD resolution
#DEMResolutions = [1.00, 0]

# Define: OrthoImageResolutions (in meters??)
# 0 == GSD resolution
#OrthoMosaicResolutions = [1.00, 0]

# START ACTUAL SCRIPT (DO NOT EDIT ANYTHING BELOW THIS!)

# INIT ENVIRONMENT
# import stuff
import os
import glob
#import PhotoScan
import math

# Set home folder
os.chdir(HomeDirectory) 
print("Home directory: " + HomeDirectory )

# get main app objects
doc = PhotoScan.app.document
app = PhotoScan.Application()

# loop through all the chunks (and find best pixel sizes, and export DEM, orthomosaic and marker errors)
for chunk in doc.chunks:
    Resolution_DEM = chunk.elevation.resolution * (1/0.3048)    # converted from m/pix to ft/pix
    Resolution_orthomosaic = chunk.orthomosaic.resolution * (1/0.3048)  # converted from m/pix to ft/pix

    # EXPORT SHAPEFILE
    #print ("---Exporting Report...")
    #FileName = './Shapefile_markers/marker_error' + chunk.label + '.shp'
    #print("File: " + FileName)
    #chunk.exportShapes(FileName, )

    # EXPORT REPORTS
    print ("---Exporting Report...")
    FileName = './PS_Reports/Report_' + chunk.label + '.pdf'
    print("File: " + FileName)
    chunk.exportReport(FileName, page_numbers=True)
    
    # EXPORT DEM
    print("---Exporting Digital Elevation Model...")
    FileName = './DEMs/DEM_' + chunk.label + '.tif'
    print("File: " + FileName)
    chunk.exportDem(FileName,
                    image_format = PhotoScan.ImageFormatTIFF, 
                    format = PhotoScan.RasterFormatTiles,
                    raster_transform=PhotoScan.RasterTransformNone,
                    nodata=-32767,
                    write_kml=False,
                    write_world=False,
                    projection=PhotoScan.CoordinateSystem(CoordinateSystemEPSG),
                    dx=Resolution_DEM,
                    dy=Resolution_DEM)       
        
    # EXPORT ORTHOMOSAIC
    print("---Exporting OrthoMosaic...")
    FileName = './OrthoMosaics/OrthoMosaic_' + chunk.label + '.tif' 
    print("File: " + FileName)
    chunk.exportOrthomosaic(FileName,
                            image_format = PhotoScan.ImageFormatTIFF,
                            format = PhotoScan.RasterFormatTiles,
                            projection=PhotoScan.CoordinateSystem(CoordinateSystemEPSG), 
                            dx=Resolution_orthomosaic,
                            dy=Resolution_orthomosaic)                   
    
    # EXPORT CHECKPOINT ERRORS
    print("---Exporting marker error files...")
    FileName = './Markers/CheckPoints_' + chunk.label + '.txt'
    f = open(FileName, 'w')
    for marker in chunk.markers:
        est = chunk.crs.project(chunk.transform.matrix.mulp(marker.position))  # Gets estimated marker coordinate
        ref = marker.reference.location

        if est and ref and not marker.reference.enabled:
            error = (est - ref) #.norm()  # The .norm() method gives the total error. Removing it gives X/Y/Z error
            # Marker metadata: marker x,y,z, x-error, y-error, z-error, total-error
            f.write(marker.label + ',' + str(ref[0]) + ',' + str(ref[1]) + ',' + str(ref[2]) + ',' + str(error[0]) + ',' + str(error[1]) + ',' + str(error[2]) + ',' + str(error.norm()) + '\n')
    f.close()

    # EXPORT GCP ERRORS
    print("---Exporting marker error files...")
    FileName = './Markers/GCPs_' + chunk.label + '.txt'
    f = open(FileName, 'w')
    for marker in chunk.markers:
        est = chunk.crs.project(chunk.transform.matrix.mulp(marker.position))  # Gets estimated marker coordinate
        ref = marker.reference.location

        if est and ref and marker.reference.enabled:
            error = (est - ref) #.norm()  # The .norm() method gives the total error. Removing it gives X/Y/Z error
            # Marker metadata: marker x,y,z, x-error, y-error, z-error, total-error
            f.write(marker.label + ',' + str(ref[0]) + ',' + str(ref[1]) + ',' + str(ref[2]) + ',' + str(error[0]) + ',' + str(error[1]) + ',' + str(error[2]) + ',' + str(error.norm()) + '\n')
    f.close()

    # EXPORT MARKER ERRORS
    print("---Exporting marker error files...")
    FileName = './Markers/Markers_' + chunk.label + '.txt'
    f = open(FileName, 'w')
    for marker in chunk.markers:
        est = chunk.crs.project(chunk.transform.matrix.mulp(marker.position))  # Gets estimated marker coordinate
        ref = marker.reference.location

        if est and ref:
            error = (est - ref) #.norm()  # The .norm() method gives the total error. Removing it gives X/Y/Z error
            # Marker metadata: marker x,y,z, x-error, y-error, z-error, total-error
            f.write(marker.label + ',' + str(ref[0]) + ',' + str(ref[1]) + ',' + str(ref[2]) + ',' + str(error[0]) + ',' + str(error[1]) + ',' + str(error[2]) + ',' + str(error.norm()) + '\n')
    f.close()

    # EXPORT FILE WITH OUTPUT NAMES
    print("---Exporting chunk names...")
    FileName = './AM_input/input_chunks.txt'
    f = open(FileName, 'a')
    f.write(chunk.label + '\n')
    f.close()

