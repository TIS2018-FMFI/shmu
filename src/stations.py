import geopandas as gpd

class Stations:
    class Station:
        def __init__(self, series):
            '''
            :param series: pandas series of station attributes
            '''
            self.types = {"B":"Pozaďová", "T":"Dopravná","I":"Priemyslená"}
            self.typeslocation = {"U":"Mestská", "S":"Predmestská", "R":"Vidiecka"}
            self.station = series.to_dict()

        def getName(self):
            '''
            :return: name of station
            '''
            return self.station['Umiestneni']

        def getX(self):
            '''
            :return: latitude of station
            '''
            return self.station['X']

        def getY(self):
            '''
            :return: longitude of station
            '''
            return self.station['Y']

        def getTypeStation(self):
            '''
            :return: type of station
            '''
            return "/".join([self.types[char] for char in self.station['Typ stanic'].split("/")])

        def getTypeLocation(self):
            '''
            :return: type of geographic location for station
            '''
            return self.typeslocation[self.station['Typ oblast']]



    def __init__(self, path):
        '''
        :param path: shapefile stations path
        '''
        self.stations = gpd.read_file(path, encoding='UTF-8')


    def getStationsNames(self):
        '''
        :return: series of station names
        '''
        return self.stations['Umiestneni']

    def getStation(self, name):
        return self.stations.loc[self.stations.Umiestneni == name].iloc[0]

    def getStations(self):
        '''
        :return: list of Stations
        '''
        stations_list = []
        for i in range(len(self.stations)):
            stations_list.append(self.Station(self.stations.iloc[i]))
        return stations_list






