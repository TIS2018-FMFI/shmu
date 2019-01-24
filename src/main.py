import map
import pollutants as ps
import stations
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class Data:
    
    def __init__(self):
        print('nacitavam data')
        with open("../data/config.json", "r") as read_file:
            self.config = json.load(read_file)
            self.pollutants = ps.Pollutants(self.config['pollutants_nc'], self.config['pollutants_csv'])
            self.stations = stations.Stations(self.config['stanice'])
            
        self.map = map.Map(self.pollutants, self.config)
        self.pollutants.createJsonForStations(self.stations.getStations())
        self.pollutants.createJsonForPollutantNames()
        self.pollutants.createJsonForMinMaxDate()
        print('koniec nacitavania dat')


class RequestHandler(BaseHTTPRequestHandler):

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
        #self.respond(response)
        #RequestHandler.data

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        #self._set_headers()
        #self.respond("<html><body><h1>POST!</h1></body></html>")
        return

    def get_response(self):
        print(self.path)
        
        url = self.path.split('?')
        path = url[0]
        responseType = 'html'
        params = {}
        if len(url) > 1:
            params = self.parseGetParams(url[1])
        
##        if 'tiff' in params:
##            res_path = './generated' + path
##            if os.path.exists(res_path):
##                return open(res_path, 'rb').read()

        splitPath = path.split('.')
        baseName = path[0]
        suffix = ''
        if len(splitPath) > 1:
            suffix = splitPath[1]

        if suffix == 'css':
            responseType = 'css'

        if suffix == 'tiff' or suffix == 'json':
            res_path = './generated' + path
            if os.path.exists(res_path):
                return open(res_path, 'rb').read(), responseType
            
        if suffix == 'jpg' or suffix == 'png':
            res_path = './web/images' + path
            if os.path.exists(res_path):
                return open(res_path, 'rb').read(), responseType
            
            
        if path == '/':
            res_path = './web/index.html'
        else:
            res_path = './web' + path
        
        if os.path.exists(res_path):
            return bytes(open(res_path).read(), 'UTF-8'), responseType
        print(self.path + " not found!")
        return bytes(self.path + " not found!", 'UTF-8'), responseType

    def respond(self, response):
        self.wfile.write(bytes(response, 'UTF-8'))

    def parseGetParams(self, paramsData):
        params = {}
        for p in paramsData.split('&'):
            p = p.split('=')
            params[p[0]] = p[1]
        return params
        
        
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    RequestHandler(None, None, None)                    #prve volanie Handlera, ktore trva dlho, koli nacitavaniu dat

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
