import netCDF4 as nc
import numpy as np
import pandas as pd
import datetime as dt


class NcReader:
    def __init__(self, path):
        '''
        :param path: netcdf file path
        '''
        self.ds = nc.Dataset(path)


class NcPollutantReader(NcReader):
    def __init__(self, pollutant_path, pol_name):
        '''
        :param pollutant_path: netcdf pollutant path
        '''
        super(NcPollutantReader, self).__init__(pollutant_path)
        self.pol_name = pol_name

    def _getTimeIndex(self, datetime):
        delta = datetime - self.getMinDate()
        idx = delta.days * 24 + delta.seconds // 3600
        return idx

    def getMinDate(self):
        '''
        :return: minimal datetime
        '''
        startYYYYDDD = self.ds.variables['TFLAG'][0][0][0]
        startHHMMSS = self.ds.variables['TFLAG'][0][0][1]
        startYear = startYYYYDDD // 1000
        startDayofYear = startYYYYDDD % 1000
        startHour = startHHMMSS // 10000
        dat = dt.date(startYear, 1, 1) + dt.timedelta(int(startDayofYear) - 1)
        result = pd.Timestamp(dat.year, dat.month, dat.day, startHour)
        return result

    def getMaxDate(self):
        '''
        :return: maximal datetime
        '''
        endidx = len(self.ds.variables['TFLAG']) - 1
        endYYYYDDD = self.ds.variables['TFLAG'][endidx][0][0]
        endHHMMSS = self.ds.variables['TFLAG'][endidx][0][1]
        endYear = endYYYYDDD // 1000
        endDayofYear = endYYYYDDD % 1000
        endHour = endHHMMSS // 10000
        dat = dt.date(endYear, 1, 1) + dt.timedelta(int(endDayofYear) - 1)
        result = pd.Timestamp(dat.year, dat.month, dat.day, endHour)
        return result

    def getRasterAtDateTime(self, datetime):
        '''
        :param datetime:
        :return: modeled values for datetime
        '''
        idx = self._getTimeIndex(datetime)
        return np.array(self.ds.variables[self.pol_name][idx, 0, :, :])


class NcGridReader(NcReader):
    def __init__(self, grid_path):
        '''
        :param grid_path: netcdf grid path
        '''
        super(NcGridReader, self).__init__(grid_path)

    def getStartCoords(self):
        '''
        :return: starting point
        '''
        return [np.array(self.ds.variables['LAT'][0, 0, :, :]).mean(),
                np.array(self.ds.variables['LON'][0, 0, :, :]).mean()]

    def getLon(self):
        '''
        :return: array of longitudes
        '''
        return np.array(self.ds.variables['LON'][0, 0, :, :])

    def getLat(self):
        '''
        :return: array of latitudes
        '''
        return np.array(self.ds.variables['LAT'][0, 0, :, :])
