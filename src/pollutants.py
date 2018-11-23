import ncreader as ncr
import csvreader as csvr


class Pollutants:
    class _Pollutant:
        def __init__(self, nc_path, csv_path):
            '''
            :param nc_path: netcdf file path
            :param csv_path: csv file path or None
            '''
            self.nc = ncr.NcPollutantReader(nc_path)
            self.csv = None
            if csv_path is not None:
                self.csv = csvr.CsvReader(csv_path)

        def getModeled(self, datetime):
            return self.nc.getRasterAtDateTime(datetime)

        def getMeasured(self, datetime, station):
            if self.csv is None:
                return None
            return self.csv.getConcentration(datetime,station)

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
            self._pollutants[pol] = self._Pollutant(pollutants_nc[pol],pollutants_csv.get(pol,None))
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




