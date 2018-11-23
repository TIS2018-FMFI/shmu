import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

class GUI():
    def __init__(self, map):
        self.header = self.createHeader()
        self.slider = self.createSlider()
        self.mapFrame = self.createMapFrame(map)
        self.outputOne = self.createOutput()
        self.datePicker = self.createDayPicker()
        self.outputTwo = self.createOutputForDate()
        self.substancePicker = self.createSubstancePicker()
        self.Line  = self.createLine()
        
    def layout(self):
        """"Returns layaout of all page in Div component."""
        
        layout = html.Div(
            id='output-container',
            children = [
                self.header,
                self.mapFrame,
                self.slider,
                self.outputOne,
                self.Line,
                self.outputTwo

            ],
            style={'marginLeft': 150, 'marginTop': 50 ,'marginRight': 150, }
        )
        return layout


    def createHeader(self):
        """Returns header of page."""
        
        header = html.H1('Vizualizácia emisií', style={'color': 'black', 'fontSize': 36, 'textAlign': 'center', 'marginBottom': 50 } )
        return header
    

    def createSlider(self):
        """Returns timeline slider."""
        
        slider = dcc.Slider(
            id="slider",
            min=0,
            max=23,#self.ncHelper.getTimeEndIndex(),
            step=1,
            value=0,
            marks={
                0: {'label': '00:00', 'style': {'color': '#9999999'}},
                1: {'label': '01:00', 'style': {'color': '#9999999'}},
                2: {'label': '02:00', 'style': {'color': '#9999999'}},
                3: {'label': '03:00', 'style': {'color': '#9999999'}},
                4: {'label': '04:00', 'style': {'color': '#9999999'}},
                5: {'label': '05:00', 'style': {'color': '#9999999'}},
                6: {'label': '06:00', 'style': {'color': '#9999999'}},
                7: {'label': '07:00', 'style': {'color': '#9999999'}},
                8: {'label': '08:00', 'style': {'color': '#9999999'}},
                9: {'label': '09:00', 'style': {'color': '#9999999'}},
                10: {'label': '10:00', 'style': {'color': '#9999999'}},
                11: {'label': '11:00', 'style': {'color': '#9999999'}},
                12: {'label': '12:00', 'style': {'color': '#9999999'}},
                13: {'label': '13:00', 'style': {'color': '#9999999'}},
                14: {'label': '14:00', 'style': {'color': '#9999999'}},
                15: {'label': '15:00', 'style': {'color': '#9999999'}},
                16: {'label': '16:00', 'style': {'color': '#9999999'}},
                17: {'label': '17:00', 'style': {'color': '#9999999'}},
                18: {'label': '18:00', 'style': {'color': '#9999999'}},
                19: {'label': '19:00', 'style': {'color': '#9999999'}},
                20: {'label': '20:00', 'style': {'color': '#9999999'}},
                21: {'label': '21:00', 'style': {'color': '#9999999'}},
                22: {'label': '22:00', 'style': {'color': '#9999999'}},
                23: {'label': '23:00', 'style': {'color': '#9999999'}},
            },
            included=False,
        )
        return slider



    def createMapFrame(self, map):
        """Returns iFrame with generated map."""
        
        mapFrame = html.Iframe(
            id="map",
            srcDoc=open(map.html,'r').read(),
            width='100%',
            height='600',
            # style = {'marginLeft': 150, 'marginTop': 25}
        )
        return mapFrame


    def createOutput(self):
        """Returns output."""
        
        output = html.P(
            id="slider-output",
            style={ 'marginTop': 30 , 'color':'#999999', 'fontSize': 14}

        )
        return output

    def createOutputForDate(self):
        """Returns date output."""

        output = html.P(
            id="my-date-picker-single-output",
            style={'marginTop': 30, 'color': '#999999', 'fontSize': 14}

        )
        return output


    def createDayPicker(self):
        datePicekr = dcc.DatePickerSingle(
            id='my-date-picker-single',
            is_RTL=True,
            first_day_of_week=3,
            min_date_allowed=dt(2015, 1, 1),
            max_date_allowed=dt(2015, 4, 1),
            date=dt(2015, 1, 1),
            # style={'cursor': 'pointer'}
        )
        return datePicekr

    def createSubstancePicker(self):
        dropdown = dcc.Dropdown(
            options=[
                {'label': 'NO2', 'value': 'NO2' },
                {'label': 'SO2', 'value': 'SO2'},
                {'label': 'O2', 'value': 'O2'}
            ],
            value='NO2',
            id= "substance-picker",
            style = {'width':'100%', 'height':'50px', 'fontSize':'20px' }
        )
        return dropdown

    def createLine(self):
        line = html.Div([ #big block
            html.Div( self.datePicker , style={'display': 'inline-block','width': '160px', 'height': '50px' }),
            html.Div( self.substancePicker , style={'display': 'inline-block','width': '200px',  'height': '29px'}),
            html.Div(   ),
        ],
        id='my-line-one',
        # style={'display': 'inline-block', 'width': '100%', 'paddingTop': '0px', 'backgroundColor': "red"}
        )
        return line