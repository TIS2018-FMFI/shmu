from src.pollutants import Pollutants
from src.stations import Stations
import geopandas as gpd
import json
import os
import src.map as map


def removeFileIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def testGeneratingRasters(path, map):
    for i in range(24):
        tiffName = 'raster' + str(i) + '.tiff'
        removeFileIfExist(path + tiffName)

    map.generateRasters()

    for i in range(24):
        tiffName = 'raster' + str(i) + '.tiff'
        if not os.path.exists(path + tiffName):
            print('Generating rasters Failed')
            return
    print('Generating rasters OK')


def testGeneratingJsons(path, pollutants, stations):
    testOk = True
    names = ['stations.json', 'pollutantNames.json', 'dates.json']

    for name in names:
        jsonPath = path + name
        removeFileIfExist(jsonPath)

    pollutants.createJsonForStations(stations.getStations())
    pollutants.createJsonForPollutantNames()
    pollutants.createJsonForMinMaxDate()

    for name in names:
        if not os.path.exists(path + name):
            print('Generating jsons Failed')
            return
    print('Generating jsons OK')

def checkMinDate(pollutants):
    if str(pollutants.getCurrentMinDate()) != '2015-01-01 00:00:00':
        print("Min date Failed")
        return
    print("Min date OK")

def checkMaxDate(pollutants):
    if str(pollutants.getCurrentMaxDate()) != "2015-12-31 23:00:00":
        print("Max date Failed")
        return
    print("Max date OK")

def checkStations(stations,config):
    shpFile = gpd.read_file(config['stanice'], encoding='UTF-8')
    if len(shpFile) == len(stations.getStations()):
        print("Stations OK")
        return
    print("Stations Failed")


with open("../data/config.json", "r") as read_file:
    config = json.load(read_file)
    pollutants = Pollutants(config['pollutants_nc'], config['pollutants_csv'])
    stations = Stations(config['stanice'])
    generatedPath = './generated/'
    map = map.Map(pollutants, config)
    checkMinDate(pollutants)
    checkMaxDate(pollutants)
    checkStations(stations,config)
    testGeneratingJsons(generatedPath, pollutants, stations)
    testGeneratingRasters(generatedPath, map)




