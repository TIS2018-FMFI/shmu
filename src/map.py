import stations as s
import ncreader
import numpy as np

from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr

class Map:
    def __init__(self, pollutants, config):
        '''
        creates tiff rasters from np arrays
        '''
        self.colorsLocs = {"U":"red", "S":"green", "R":"blue"}
        self.colorsStats = {"B":"red", "T":"green", "I":"blue"}

        self.pollutants = pollutants
        self.grid = ncreader.NcGridReader(config['grid'])

        self.lon, self.lat = self.grid.getLon(), self.grid.getLat()
        self.generateRasters()

    def generateRasters(self):
        '''
        creates 24 tiff rasters for every hour
        '''
        for h in range(24):
            self.pollutants.setCurrentDate(self.pollutants.getCurrentDate().replace(hour=h))
            self.pollutantData = self.pollutants.getCurrentModeled()
            self.makeTiff(h)
        self.pollutants.setCurrentDate(self.pollutants.getCurrentDate().replace(hour=0))
        

    def makeTiff(self, hour):
        '''
        create tiff for specific hour from np array with data and lot, lan coordinates
        '''
        array = np.flip(self.pollutantData, 0)

        xmin,ymin,xmax,ymax = [self.lon.min(),self.lat.min(),self.lon.max(),self.lat.max()]
        nrows,ncols = np.shape(array)
        xres = (xmax-xmin)/float(ncols)
        yres = (ymax-ymin)/float(nrows)
        geotransform=(xmin,xres,0,ymax,0, -yres)   

        tiff_path = './generated/raster' + str(hour) + '.tiff'
        output_raster = gdal.GetDriverByName('GTiff').Create(tiff_path, ncols, nrows, 1 ,gdal.GDT_Float32)
        output_raster.SetGeoTransform(geotransform)  
        srs = osr.SpatialReference()                 
        srs.ImportFromEPSG(4326)                     
                                                     
                                                     
        output_raster.SetProjection( srs.ExportToWkt() )
                                                        
        output_raster.GetRasterBand(1).WriteArray(array) 

        output_raster.FlushCache()

