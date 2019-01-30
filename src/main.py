import map
import pollutants as ps
import stations
import json
import os
import pandas as pd
from http.server import BaseHTTPRequestHandler, HTTPServer

class Data:
    
    def __init__(self):
        '''
        load config, create classes Pollutants, Stations, Map
        '''
        
        print('nacitavam data')
        with open("../data/config.json", "r") as read_file:
            self.config = json.load(read_file)
            self.pollutants = ps.Pollutants(self.config['pollutants_nc'], self.config['pollutants_csv'])
            self.stations = stations.Stations(self.config['stanice'])
            
        self.map = map.Map(self.pollutants, self.config)
        self.generateCurrentJsons()
        print('koniec nacitavania dat')

    def generateCurrentJsons(self):
        self.pollutants.createJsonForStations(self.stations.getStations())
        self.pollutants.createJsonForPollutantNames()
        self.pollutants.createJsonForMinMaxDate() 


class RequestHandler(BaseHTTPRequestHandler):
    '''
    handles requests from clients
    '''

    data = Data()

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def _set_headers(self, responseType='html'):
        
        headerValue = 'text/html'
        if responseType == 'css':
            headerValue='text/css'
            
        self.send_response(200)
        self.send_header('Content-type', headerValue)
        self.end_headers()

    def do_GET(self):
        response, contentType = self.get_response()
        self._set_headers(contentType)
        self.wfile.write(response)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        return

    def get_response(self):
        '''
        :return appropriate data based on request in byte form  and type of response
        '''
        
        url = self.path.split('?')
        path = url[0]
        responseType = 'html'
        params = {}
        if len(url) > 1:
            params = self.parseGetParams(url[1])

        splitPath = path.split('.')
        baseName = path[0]
        suffix = ''
        if len(splitPath) > 1:
            suffix = splitPath[1]

        if suffix == 'css':
            responseType = 'css'
            
        if suffix == 'json' or suffix == 'tiff':
            res_path = './generated' + path
            if os.path.exists(res_path):
                return open(res_path, 'rb').read(), responseType
            
        if suffix == 'jpg' or suffix == 'png':
            res_path = './web/images' + path
            if os.path.exists(res_path):
                return open(res_path, 'rb').read(), responseType


        if path == '/setDate':
            response = 'true'
            date = params.get('date', False)
            if date is not False:
                if date == '0000-00-00':
                    finalTimestamp = RequestHandler.data.pollutants.getCurrentMinDate()
                else:
                    dateWithTime = date + ' 00:00:00'
                    finalTimestamp = pd.Timestamp(dateWithTime)
                RequestHandler.data.pollutants.setCurrentDate(finalTimestamp)
                RequestHandler.data.generateCurrentJsons()
                RequestHandler.data.map.generateRasters()
            else:
                response = 'false'
            return bytes(response, 'UTF-8'), responseType
        

        if path == '/setPollutant':
            response = 'true'
            pollutant = params.get('pollutant', False)
            if pollutant is not False:
                RequestHandler.data.pollutants.setCurrentPollutant(pollutant)
                RequestHandler.data.generateCurrentJsons()
            else:
                response = 'false'
            return bytes(response, 'UTF-8'), responseType
                
            
        if path == '/':
            res_path = './web/index.html'
            oldPollutant = RequestHandler.data.pollutants.getCurrentPollutant()
            oldDate = RequestHandler.data.pollutants.getCurrentDate()
            
            RequestHandler.data.pollutants.setCurrentDefault()

            newPollutant = RequestHandler.data.pollutants.getCurrentPollutant()
            newDate = RequestHandler.data.pollutants.getCurrentDate()

            if oldPollutant != newPollutant or oldDate != newDate:
                RequestHandler.data.map.generateRasters()
                RequestHandler.data.generateCurrentJsons()
        else:
            res_path = './web' + path
        
        if os.path.exists(res_path):
            return bytes(open(res_path).read(), 'UTF-8'), responseType
        print(self.path + " not found!")
        return bytes(self.path + " not found!", 'UTF-8'), responseType

    def respond(self, response):
        self.wfile.write(bytes(response, 'UTF-8'))

    def parseGetParams(self, paramsData):
        '''
        :param paramsData: part of url with params
        :return: dict with parsed params key: value
        '''
        params = {}
        for p in paramsData.split('&'):
            p = p.split('=')
            params[p[0]] = p[1]
        return params
        
        
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    '''
    Starts server with overrided handler
    '''
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    RequestHandler(None, None, None)                    #first call of Handlera, which take longer, because of loading files

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
