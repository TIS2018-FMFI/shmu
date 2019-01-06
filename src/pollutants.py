from src.ncreader import NcPollutantReader
from src.csvreader import CsvReader
import json

class Pollutants:
    class _Pollutant:
        def __init__(self, nc_path, csv_path, pol_name):
            '''
            :param nc_path: netcdf file path
            :param csv_path: csv file path or None
            '''
            self.nc = NcPollutantReader(nc_path,pol_name)
            self.csv = None
            if csv_path is not None:
                self.csv = CsvReader(csv_path)

        def getModeled(self, datetime):
            return self.nc.getRasterAtDateTime(datetime)

        def getMeasured(self, datetime, station):
            if self.csv is None:
                return None
            return self.csv.getConcentration(datetime,station)

        def getMeasuredForDay(self,datetime,station):
            if self.csv is None:
                return None
            return self.csv.getConcentrationsForDay(datetime,station)


        def getMaxDate(self):
            return self.nc.getMaxDate()

        def getMinDate(self):
            return self.nc.getMinDate()



    def __init__(self, pollutants_nc, pollutants_csv):
        '''
        :param pollutants_nc: map of pollutant netcdf file paths
        :param pollutants_csv: map of pollutant csv file paths
        '''
        self._pollutants = dict()
        self._polNames = list(pollutants_nc.keys())
        for pol in self._polNames:
            self._pollutants[pol] = self._Pollutant(pollutants_nc[pol],pollutants_csv.get(pol,None),pol)
        self._currentPollutant = self._polNames[0]
        self._currentDate = self._pollutants[self._currentPollutant].getMinDate()


    def getCurrentModeled(self):
        '''
        :return: modeled values for currently picked datetime and currently picked pollutant
        '''
        return self._pollutants[self._currentPollutant].getModeled(self._currentDate)

    def getCurrentMeasured(self, station):
        '''
        None : station never measured pollutant or station measured before or after current date
        NaN : station was inactive
        :param station: name of station
        :return: measured values for currently picked datetime and currently picked pollutant at station or None or NaN
        '''
        return self._pollutants[self._currentPollutant].getMeasured(self._currentDate, station)

    def getCurrentMeasuredForDay(self,station):
        return self._pollutants[self._currentPollutant].getMeasuredForDay(self._currentDate,station)


    def getCurrentMaxDate(self):
        '''
        :return: maximal datetime of currently picked pollutant
        '''
        return self._pollutants[self._currentPollutant].getMaxDate()

    def getCurrentMinDate(self):
        '''
        :return: minimal datetime of currently picked pollutant
        '''
        return self._pollutants[self._currentPollutant].getMinDate()

    def setCurrentPollutant(self, pollutant):
        '''
        :param pollutant: name of pollutant
        :return: None
        '''
        self._currentPollutant = pollutant

    def getCurrentPollutant(self):
        '''
        :return: name of current pollutant
        '''
        return self._currentPollutant

    def setCurrentDate(self,datetime):
        '''
        :param datetime: datetime for currentdate
        :return: None
        '''
        self._currentDate = datetime

    def getCurrentDate(self):
        '''
        :return: currente datetime
        '''
        return self._currentDate

    def getPollutants(self):
        '''
        :return: list of all pollutant names
        '''
        return self._polNames

    def _createJson(self, data,name):
        '''
        Create json with name and data
        :param data: dict keys-values
        :param name: name of json
        :return:
        '''
        json_data = json.dumps(data, ensure_ascii=False)
        with open("generated/{:}.json".format(name), "w", encoding="UTF-8") as file:
            file.write(json_data)

    def createJsonForStations(self,station_list):
        '''
        Create dict for stations.json
        :param station_list:
        :return:
        '''
        data = dict()
        data["cnt"] = len(station_list)
        stations = []
        for station in station_list:
            stationJson = dict()
            stationJson["x"] = station.getX()
            stationJson["y"] = station.getY()
            stationJson["name"] = station.getName()
            stationJson["loctype"] = station.getTypeLocation()
            stationJson["type"] = station.getTypeStation()
            stationJson["measured"] = self.getCurrentMeasuredForDay(station.getName())
            stations.append(stationJson)
        data["stations"] = stations
        self._createJson(data,"stations")



    def createJsonForPollutantNames(self):
        '''
        Create dict for "pollutantNames.json"
        :return:
        '''
        data = dict()
        names = self.getPollutants()
        data["cnt"] = len(names)
        data["pollutants"] = names
        self._createJson(data,"pollutantNames")


    def createJsonForMinMaxDate(self):
        '''
        Create dict for "dates.json"
        :return:
        '''
        data = dict()
        data["min"] = str(self.getCurrentMinDate())
        data["max"]= str(self.getCurrentMaxDate())
        self._createJson(data,"dates")
