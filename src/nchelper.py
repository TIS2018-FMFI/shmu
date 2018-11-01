import netCDF4 as nc
import numpy as np

class NcHelper:
    def __init__(self, grid_path, pollutant_path):
        self.grid = nc.Dataset(grid_path)
        self.pollutant = nc.Dataset(pollutant_path)

    def getStartCoords(self):
        return [np.array(self.grid.variables['LAT'][0,0,:,:]).mean(), np.array(self.grid.variables['LON'][0,0,:,:]).mean()]

    def getTimeEndIndex(self):
        return len(self.pollutant.variables['TFLAG'])

    def getTimeAtIndex(self, idx):
        return self.pollutant.variables['TFLAG'][idx]

    def getLon(self):
        return np.array(self.grid.variables['LON'][0,0,:,:])

    def getLat(self):
        return np.array(self.grid.variables['LAT'][0,0,:,:])

    def getRasterAtTimeIndex(self, idx):
        return np.array(self.pollutant.variables['NO2'][idx,0,:,:])
