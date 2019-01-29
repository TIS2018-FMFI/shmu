import stations as s
import ncreader
import numpy as np

from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr

class Map:
    def __init__(self, pollutants, config):
        self.colorsLocs = {"U":"red", "S":"green", "R":"blue"}
        self.colorsStats = {"B":"red", "T":"green", "I":"blue"}

        #self.stations = s.Stations("../data/stanice_shp/stanice_projekt.shp")
        self.pollutants = pollutants
        self.grid = ncreader.NcGridReader(config['grid'])

        self.lon, self.lat = self.grid.getLon(), self.grid.getLat()
        self.generateRasters()

    def createPopUp(self):
        for stanica in self.stations.getStations():
            fol.CircleMarker(location = [stanica.getY(), stanica.getX()],
                        radius=15,
                        color = self.colorByStationLocation(stanica),
                        fill = True,
                        fill_color = self.colorByStationType(stanica),
                        popup = self.createPopUpHTML(stanica)
                       ).add_to(self.map)


    def colorByStationType(self, station):
        return self.colorsStats.get(station.getTypeStation(),"black")

    def colorByStationLocation(self, station):
        return self.colorsLocs.get(station.getTypeLocation(),"black")

    def createPopUpHTML(self, station):
        parser = "<p><b>x: </b>{:} <b>y: </b>{:}<br>" \
                 "<b>Name: </b>{:} <br>" \
                 "<b>Station location: </b> {:} <br> " \
                 "<b>Station type: </b> {:} <br>" \
                 "<b>Measured concentration: </b> {:}</p>".format(station.getX(),
                                                                  station.getY(),
                                                                  station.getName(),
                                                                  station.getTypeLocation(),
                                                                  station.getTypeStation(),
                                                                  self.pollutants.getCurrentMeasured(station.getName()))
        return parser
    

    def generateRasters(self):
        for h in range(24):
            self.pollutants.setCurrentDate(self.pollutants.getCurrentDate().replace(hour=h))
            self.pollutantData = self.pollutants.getCurrentModeled()
            self.makeTiff(h)
        self.pollutants.setCurrentDate(self.pollutants.getCurrentDate().replace(hour=0))
        

    def makeTiff(self, hour):
        array = np.flip(self.pollutantData, 0)

        xmin,ymin,xmax,ymax = [self.lon.min(),self.lat.min(),self.lon.max(),self.lat.max()]
        nrows,ncols = np.shape(array)
        xres = (xmax-xmin)/float(ncols)
        yres = (ymax-ymin)/float(nrows)
        geotransform=(xmin,xres,0,ymax,0, -yres)   

        tiff_path = './generated/raster' + str(hour) + '.tiff'
        print(tiff_path)
        output_raster = gdal.GetDriverByName('GTiff').Create(tiff_path, ncols, nrows, 1 ,gdal.GDT_Float32)
        output_raster.SetGeoTransform(geotransform)  
        srs = osr.SpatialReference()                 
        srs.ImportFromEPSG(4326)                     
                                                     
                                                     
        output_raster.SetProjection( srs.ExportToWkt() )
                                                        
        output_raster.GetRasterBand(1).WriteArray(array) 

        output_raster.FlushCache()

