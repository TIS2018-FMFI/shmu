import dash
from dash.dependencies import Input, Output
import map
import nchelper as nh
from GUI import GUI

import time

class App(dash.Dash):
    def __init__(self):
        dash.Dash.__init__(self)
        self.ncHelper = nh.NcHelper("../data/GRIDCRO2D_01012015.nc", "../data/LIFEIP_Small_NO2_2015.nc")

        self.map = map.Map(self.ncHelper)
        self.layout = GUI(self.map).layout()

        @self.callback(
            Output(component_id='slider-output', component_property='children'),
            [Input(component_id='slider', component_property='value')])
        def update_date(input_data):
            datetime = self.ncHelper.getTimeAtIndex(int(input_data))
            return "Date: {:} time: {:}".format(datetime[0][0], datetime[0][1])

        @self.callback(
            Output(component_id='map', component_property='srcDoc'),
            [Input(component_id='slider', component_property='value')])
        def update_map(input_data):
            self.map.generateRasters(int(input_data))
            return open(self.map.html,'r').read()


dash.Dash()

if __name__ == "__main__":
    app = App()
    app.run_server(debug=True)
