import dash
from dash.dependencies import Input, Output
import map
import pollutants as ps
import json
from GUI import GUI
from datetime import datetime as dt


class App(dash.Dash):
    def __init__(self):
        dash.Dash.__init__(self)
        with open("../data/config.json", "r") as read_file:
            pollutants_json = json.load(read_file)
            self.pollutants = ps.Pollutants(pollutants_json['pollutants_nc'], pollutants_json['pollutants_csv'])


        self.map = map.Map(self.pollutants)
        self.layout =\
            GUI(self.map).layout()



        @self.callback(
            Output(component_id='slider-output', component_property='children'),
            [Input(component_id='slider', component_property='value')])
        def update_date(input_data):
            self.pollutants.setCurrentDate(self.pollutants.getCurrentDate().replace(hour=int(input_data)))
            return str(self.pollutants.getCurrentDate())

        @self.callback(
            Output(component_id='map', component_property='srcDoc'),
            [Input(component_id='slider', component_property='value')])
        def update_map(input_data):
            self.map.generateRasters()
            return open(self.map.html,'r').read()

        @self.callback(
            Output('my-date-picker-single-output', component_property='children'),
            [Input('my-date-picker-single', 'date')])
        def update_output(date):
            string_prefix = 'Vybral si: '
            if date is not None:
                date = dt.strptime(date, '%Y-%m-%d')
                date_string = date.strftime('%B %d, %Y')
                return string_prefix + date_string


dash.Dash()

if __name__ == "__main__":
    app = App()
    app.run_server(debug=True)
