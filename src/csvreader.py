import pandas as pd


class CsvReader:

    def __init__(self, path):
        '''
        :param path: csv file path
        '''
        self.df = pd.read_csv(path, sep=';')
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        self.df = self.df.set_index('dtvalue')

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
        return self.df.loc[datetime,station]



ps = {"NO2":"../data/csv_pollutants/NO2_2003_2017.csv"}

p = CsvReader(ps["NO2"])













