import dash_core_components as dcc
import dash_html_components as html

class GUI():
    def __init__(self, map):
        self.header = self.createHeader()
        self.slider = self.createSlider()
        self.mapFrame = self.createMapFrame(map)
        self.output = self.createOutput()
        
    def layout(self):
        """"Returns layaout of all page in Div component."""
        
        layout = html.Div(
            children = [
                self.header,
                self.mapFrame,
                self.slider,
                self.output
            ]
        )
        return layout


    def createHeader(self):
        """Returns header of page."""
        
        header = html.H1('Vizualizácia emisií')
        return header
    

    def createSlider(self):
        """Returns timeline slider."""
        
        slider = dcc.Slider(
            id="slider",
            min=0,
            max=24,#self.ncHelper.getTimeEndIndex(),
            step=1,
            value=0
        )
        return slider


    def createMapFrame(self, map):
        """Returns iFrame with generated map."""
        
        mapFrame = html.Iframe(
            id="map",
            srcDoc=open(map.html,'r').read(),
            width='80%',
            height='400'
        )
        return mapFrame


    def createOutput(self):
        """Returns output."""
        
        output = html.P(
            id="slider-output"
        )
        return output
