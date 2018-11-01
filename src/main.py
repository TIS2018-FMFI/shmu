import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import map
import nchelper as nh

class App(dash.Dash):
    def __init__(self):
        dash.Dash.__init__(self)
        self.ncHelper = nh.NcHelper("../data/GRIDCRO2D_01012015.nc", "../data/LIFEIP_Small_NO2_2015.nc")

        self.map = map.Map(self.ncHelper)
        self.slider = self.createSlider()
        self.output = html.P(id="slider-output")
        self.mapFrame = html.Iframe(id="map", srcDoc=open(self.map.html,'r').read(),width='100%', height='600')

        self.layout = html.Div(children =[
            html.H1("Vyzualizacia mapy"),
            self.mapFrame,
            self.slider,
            self.output
            ]
        )

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


    def createSlider(self):
        slider = dcc.Slider(
            id="slider",
            min=0,
            max=24,#self.ncHelper.getTimeEndIndex(),
            step=1,
            value=0
        )
        return slider









dash.Dash()

if __name__ == "__main__":
    app = App()
    app.run_server(debug=True)
