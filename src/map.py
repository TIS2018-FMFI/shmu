import stations as s
import folium as fol
from pyproj import Proj
import matplotlib.pyplot as plt

import time

class Map:
    def __init__(self,ncHelper):
        self.colorsLocs = {"U":"red", "S":"green", "R":"blue"}
        self.colorsStats = {"B":"red", "T":"green", "I":"blue"}
        self.html = "./generated/map.html"

        self.stations = s.Stations("../data/stanice_shp/stanice_nove.shp")
        self.ncHelp = ncHelper

        self.map = fol.Map(location= self.ncHelp.getStartCoords(), zoom_start=7, tiles='Stamen Terrain')
        self.createPopUp()

        self.map.save(self.html)

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
                 "<b>Station type: </b> {:}</p>".format(station.getX(), station.getY(), station.getName(), station.getTypeLocation(), station.getTypeStation())
        return parser
    

    def generateRasters(self, timeIdx):
        #tu som iba skopiroval kod z jeho githubu nerozumiem moc co tam robi a asi to ani neni dobre umiestnene
        #bude traba to treba spravit asi uplne inac 
        
        self.map = fol.Map(location=self.ncHelp.getStartCoords(), zoom_start=7, tiles='Stamen Terrain')

        p = Proj("+init=EPSG:3857")

        x_L, y_L = p(self.ncHelp.getLon(), self.ncHelp.getLat(), inverse=False)
        
        no2 = self.ncHelp.getRasterAtTimeIndex(timeIdx)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.pcolormesh(x_L[:], y_L[:], no2[:])
        
        plt.xlim(1300000, 2530000)
        plt.ylim(6000000, 6650000)
        plt.axis('off')


        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        
        plt.savefig('./generated/rastre.png', dpi=300, bbox_inches='tight', pad_inches=-0.1)

        min_lon, min_lat = p(1300000, 6000000, inverse=True)
        max_lon, max_lat = p(2530000, 6650000, inverse=True)


        datas = plt.imread('./generated/rastre.png')
        
        child = fol.raster_layers.ImageOverlay(datas,opacity=0.8,bounds=[[min_lat,min_lon],[max_lat,max_lon]])
        
        self.map.add_child(child)
        
        self.createPopUp()
        
        self.map.save(self.html)

