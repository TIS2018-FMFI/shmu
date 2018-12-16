import pandas as pd
import numpy as np

class CsvReader:

    def __init__(self, path):
        '''
        :param path: csv file path
        '''
        self.df = pd.read_csv(path, sep=';')
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        self.df = self.df.set_index('dtvalue')

    def getConcentrationsForDay(self,datetime,station):
        date = pd.to_datetime(datetime.date())
        day = []
        for i in range(24):
            date += pd.Timedelta(hours=1)
            day.append(self.getConcentration(date,station))
        return day

    def getConcentration(self, datetime, station):
        '''
        :param datetime:
        :param station:
        :return: measured value fo datetime and station
        '''
        if station not in self.df.keys():
            return None
        if not (self.df.index.min() <= datetime and datetime <= self.df.index.max()):
            return None
        value = self.df.loc[datetime,station]
        if np.isnan(value):
            return -1
        return value














