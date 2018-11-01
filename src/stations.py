import geopandas as gpd
'''
typy stanic 
B:pozadova
T:dopravna
I:priemyselna

typy oblast
U:mestska
S:predmestska
R:vidiecka
'''
class Stations:
    class Station:
        def __init__(self, series):
            self.station = series.to_dict()

        def getName(self):
            return self.station['Umiestneni']

        def getX(self):
            return self.station['X']

        def getY(self):
            return self.station['Y']

        def getTypeStation(self):
            return self.station['Typ stanic']

        def getTypeLocation(self):
            return self.station['Typ oblast']



    def __init__(self, path):
        self.stations = gpd.read_file(path, encoding='UTF-8')


    def getStationsNames(self):
        return self.stations['Umiestneni']

    def getStation(self, name):
        return self.stations.loc[self.stations.Umiestneni == name].iloc[0]

    def getStations(self):
        stations_list = []
        for i in range(len(self.stations)):
            stations_list.append(self.Station(self.stations.iloc[i]))
        return stations_list




