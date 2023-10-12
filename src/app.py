# -*- coding: utf-8 -*-
"""
Created on Thu Mar 06 16:10:27 2023

@author: ADMIN
"""
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_table
import urllib.parse


data_table_resum_col = ['Categoría', 'Parámetro', 'ES 202X', 'Promedio', 'Mínimo', 'Máximo']
data_table_tp_col = ['Muestra', 'Promedio', 'SD', 'Mínimo', 'Máximo']

# Inicia la app
app = dash.Dash()
server = app.server


colors = {
    'text': 'rgb(134, 7, 14)',
    'plot_color': '#C0C0C0',
    'paper_color': '#ff0000'
}

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app.layout = html.Div([

    html.H1(children='Análisis de disminución de muestra para el ES',  # Título del dashboard
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),

    html.Br(),

    html.Div(className='row',
             children=[
                 html.Div([
                     dcc.Markdown('''
                                        **Datos para gráficar**

                                        Seleccionar la información que aparecerá en la gráfica:

                                        ''')
                 ], className='three columns')
             ]),
    html.Label('Escoge un país'),
    html.Br(),
    dcc.RadioItems(

        id='radio_pais',
        options=[
            {'label': 'México', 'value': 'mx'},
            #{'label': ' ', 'value': 'rd'}
        ],
        value='mx'),

    html.Br(),
    html.Br(),

    # Desplegar para elegir dominios
    html.Label('Escoge un dominio'),

    dcc.Dropdown(
        id='dropdown1',
        # options=[
        #     {'label': 'AMCM', 'value': 'AMCM'},
        #     {'label': 'Monterrey', 'value': 'MTY'},
        #     {'label': 'Guadalajara', 'value': 'GDL'},
        #     {'label': '25 Ciudades', 'value': 'PROV'},
        #     {'label': '28 Ciudades', 'value': '28 CDS'}
        # ],
        # value='AMCM'
    ),

    html.Br(),
    html.Br(),

    # Inicio de los Tabs
    dcc.Tabs(
        colors={
            "border": "white",
            "primary": "gold",
            "background": "cornsilk"},
        children=[

            # Primer tab
            dcc.Tab(label='Estimación de proporciones',

                    selected_style={'fontWeight': 'bold'},

                    children=[

                        html.Br(),

                        html.Div(
                            children='Estimación de proporciones por nivel socieconómico, '
                                     'televisión de paga y operadores de TV de paga',
                            style={
                                'textAlign': 'center',
                                'color': colors['text']
                            }
                        ),

                        html.Br(),

                        html.Div(id='muestra_text1',
                                 style={
                                     'textAlign': 'center',
                                     'color': colors['text']
                                 }
                                 ),

                        html.Div(id='muestra_text2',
                                 style={
                                     'textAlign': 'center',
                                     'color': colors['text']
                                 }
                                 ),

                        html.Br(),
                        html.Br(),

                        # Desplegar para elegir bases de parámetros
                        html.Label('Escoge una opción'),
                        dcc.Dropdown(
                            id='dropdown2',

                        ),
                        html.Br(),
                        html.Br(),

                        # Primer control deslizante para seleccionar el número de muestras
                        html.Label('Elija el número de muestras (arrastre la barra)'),

                        dcc.RangeSlider(
                            id='Slider1',
                            step=1,
                            value=[1, 2]
                        ),

                        html.Div([
                            dcc.Markdown(id='tit_graf1')
                        ]),

                        # Primera gráfica: De puntos
                        html.Div([
                            dcc.Graph(
                                id='scatter_chart')
                        ]),

                        html.Br(),
                        html.Br(),

                        # Segunda gráfica: Box-plot
                        html.Div([
                            dcc.Graph(
                                id='box_plot')
                        ]),

                        html.Br(),
                        html.Br(),

                        html.Label('Escoge un parámetro'),

                        # Checklist para la tabla 1
                        dcc.Checklist(
                            id='checklist1',
                            options=[
                                {'label': 'Proporcion', 'value': 'proporcion'},
                                {'label': 'SE', 'value': 'SE'},
                                {'label': 'SD', 'value': 'sd'},
                                {'label': 'CV', 'value': 'cv'},
                                {'label': 'deff', 'value': 'deff'},
                                {'label': 'Número de hogares', 'value': 'n'}
                            ],
                            value=['proporcion', 'SE']),

                        html.Br(),
                        html.Br(),

                        # Tabla 1
                        html.Div([
                            dash_table.DataTable(
                                id='table1',
                                columns=[{"name": i, "id": i} for i in data_table_resum_col],
                                style_as_list_view=True,
                                style_cell={'padding': '4px'},
                                style_header={
                                    'backgroundColor': 'rgb(210, 210, 210)',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_cell_conditional=[
                                    {'if': {'column_id': 'Categoría'},
                                     'width': '30%'},
                                    {'if': {'column_id': 'Parámetro'},
                                     'width': '30%'},
                                    {'textAlign': 'center'}
                                ],
                            )
                        ]),

                        html.Br(),

                        html.Div([
                            html.A(children='Descargar tabla',
                                   id='download-link',
                                   download="tabla_parametros.csv",
                                   href="",
                                   target="_blank")
                        ]),

                        html.Br(),

                    ]
                    ),

            # Segundo tab
            dcc.Tab(label='Tasa de respuesta',

                    selected_style={'fontWeight': 'bold'},

                    children=[

                        html.Br(),
                        html.Div(children='Cálculo de la tasa de respuesta de las muestras obtenidas'
                                          ' con el ES 202X',
                                 style={
                                     'textAlign': 'center',
                                     'color': colors['text']
                                 }
                                 ),

                        html.Br(),

                        html.Div(id='muestra_text3',
                                 style={
                                     'textAlign': 'center',
                                     'color': colors['text']
                                 }
                                 ),

                        html.Div(id='muestra_text4',
                                 style={
                                     'textAlign': 'center',
                                     'color': colors['text']
                                 }
                                 ),

                        html.Br(),

                        # Desplegar para elegir bases de parámetros
                        html.Label('Escoge una opción'),
                        dcc.Dropdown(
                            id='dropdown3',

                        ),
                        html.Br(),

                        # Segundo control deslizante para seleccionar el número de muestras
                        html.Label('Elija el número de muestras (arrastre la barra)'),

                        dcc.RangeSlider(
                            id='Slider2',
                            step=1,
                            value=[1, 1]
                            # marks = {i : i for i in [min_muestra_tp,max_muestra_tp]}
                        ),

                        html.Br(),

                        html.Div([
                            dcc.Markdown(id='tit_graf2')
                        ]),
                        html.Br(),

                        # Tercera gráfica: Histograma
                        html.Div([
                            dcc.Graph(
                                id='histogram')
                        ]),

                        # Tabla 2
                        html.Div([
                            dash_table.DataTable(
                                id='table2',
                                columns=[{"name": i, "id": i} for i in data_table_tp_col],
                                style_as_list_view=True,
                                style_cell={'padding': '4px'},
                                style_header={
                                    'backgroundColor': 'rgb(210, 210, 210)',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_cell_conditional=[
                                    {'if': {'column_id': 'Muestra'},
                                     'width': '60%'},
                                    {'textAlign': 'center'}
                                ],
                            )
                        ]),

                        html.Br(),
                        html.Br()

                    ]
                    )  # Fin del segundo Tab
        ])  # Fin de los Tabs
])  # Fin de la app


@app.callback(
    [dash.dependencies.Output("dropdown1", "options"),
     dash.dependencies.Output("dropdown1", "value"),
     dash.dependencies.Output('dropdown2', 'options'),
     dash.dependencies.Output('dropdown2', 'value'),
     dash.dependencies.Output('dropdown3', 'options'),
     dash.dependencies.Output('dropdown3', 'value')],
    [dash.dependencies.Input("radio_pais", "value")]
)
def update_drop_options(country):
    if country == 'mx':
        options1 = [
            {'label': 'AMCM', 'value': 'AMCM'},
            {'label': 'Monterrey', 'value': 'MTY'},
            {'label': 'Guadalajara', 'value': 'GDL'},
            {'label': '25 Ciudades', 'value': 'PROV'},
            {'label': '28 Ciudades', 'value': '28 CDS'}
        ]
        value1 = 'AMCM'

        options2 = [
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 20% UPMs / GDL y MTY COMPLETOS', 'value': 'option1_GDL_MTY_c.csv'},
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 25% UPMs / GDL y MTY COMPLETOS', 'value': 'option2_GDL_MTY_c.csv'},
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 50% UPMs / GDL y MTY COMPLETOS', 'value': 'option3_GDL_MTY_c.csv'},
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 20% UPMs', 'value': 'option 1.csv'},
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 25% UPMs', 'value': 'option 2.csv'},
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 50% UPMs', 'value': 'option 3.csv'},
            {'label': 'ES23 Primera Ola - Opción: AMCM y 25 CDS 20% UPMs / GDL y MTY COMPLETOS', 'value': 'option1_23_1_GDL_MTY_c.csv'},
            {'label': 'ES23 Primera Ola - Opción: AMCM y 25 CDS 25% UPMs / GDL y MTY COMPLETOS', 'value': 'option2_23_1_GDL_MTY_c.csv'},
        ]
        value2 = 'option 1.csv'

        options3 = [
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 20% UPMs', 'value': 'tasas_option 1.csv'},
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 25% UPMs', 'value': 'tasas_option 2.csv'},
            {'label': 'ES22 Anual - Opción: AMCM, 25 CDS, GDL y MTY 50% UPMs', 'value': 'tasas_option 3.csv'},
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 20% UPMs / GDL y MTY COMPLETOS','value': 'tasas_option1_cm1000_c.csv'},
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 25% UPMs / GDL y MTY COMPLETOS', 'value': 'tasas_option2_cm1000_c.csv'},
            {'label': 'ES22 Anual - Opción: AMCM y 25 CDS 50% UPMs / GDL y MTY COMPLETOS', 'value': 'tasas_option3_cm1000_c.csv'},
            #{'label': 'ES23 Primera Ola - Opción: AMCM y 25 CDS 20% UPMs / GDL y MTY COMPLETOS','value': ''},
            #{'label': 'ES23 Primera Ola - Opción: AMCM y 25 CDS 25% UPMs / GDL y MTY COMPLETOS', 'value': ''},
            
        ]
        value3 = 'tasas_option 1.csv'

    else:
        options1 = [
            {'label': 'Santiago', 'value': 'ST'},
            {'label': 'Santo Domingo', 'value': 'SD'},
            {'label': 'Distrito Nacional', 'value': 'DN'},
            {'label': 'Total República Dominicana', 'value': 'Total RD'}
        ]
        value1 = 'ST'

        options2 = [
          {'label': 'ES 2019 - 50% República Dominicana', 'value': 'rd_escenario_1.csv'}]
        value2 = 'rd_escenario_1.csv'

        options3 = [
          {'label': 'ES 2019 - 50% República Dominicana', 'value': 'rd_escenario_1_tasa.csv'}]
        value3 = 'rd_escenario_1_tasa.csv'

    return options1, value1, options2, value2, options3, value3


# Para RangeSlider1
@app.callback(
    [dash.dependencies.Output("Slider1", "min"),
     dash.dependencies.Output("Slider1", "max"),
     dash.dependencies.Output('muestra_text1', 'children'),
     dash.dependencies.Output('muestra_text2', 'children')],
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("dropdown2", "value")]
)
# Definicion de funcion: Para el callback del Slider
def update_slide1(dominio, base):
    # Base con los parámetros estimados
    nom_base_estimaciones0 = base
    data_par = pd.read_csv(DATA_PATH.joinpath(nom_base_estimaciones0))
    data_par['e'] = data_par['ic_sup'] - data_par['proporcion']
    min_muestra = data_par.Muestra.min() + 1
    max_muestra = data_par.Muestra.max()
    n_muestra = data_par[data_par.Muestra == 1].cant_upms.max()

    data_par_filt = data_par[data_par.Muestra == 1].copy()
    #data_par_filt = data_par_filt[data_par_filt.categoria == 'tv_rest'].copy()
    data_par_filt = data_par_filt[data_par_filt.DOMINIO == dominio].copy()
    dom_upms = data_par_filt.cant_upms.max()

    if dominio == 'PROV':
        dom = '25 CDS'
        children2 = 'Muestra ' + dom + ': ' + str(dom_upms) + ' UPMs'
    else:
        children2 = 'Muestra ' + dominio + ': ' + str(dom_upms) + ' UPMs'

    children1 = 'Muestra total: ' + str(n_muestra) + ' UPMs'

    return min_muestra, max_muestra, children1, children2


# Para RangeSlider2
@app.callback(
    [dash.dependencies.Output("Slider2", "min"),
     dash.dependencies.Output("Slider2", "max"),
     dash.dependencies.Output("muestra_text3", "children"),
     dash.dependencies.Output("muestra_text4", "children")
     ],
    [dash.dependencies.Input("radio_pais", "value"),
     dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("dropdown3", "value")]
)
# Definicion de funcion: Para el callback del Slider
def update_slide1(country, dominio, base):
    nom_base_tasas = base
    data_tasa_resp = pd.read_csv(DATA_PATH.joinpath(nom_base_tasas))
    min_muestra_tp = data_tasa_resp.muestra.min() + 1
    max_muestra_tp = data_tasa_resp.muestra.max()

    data_tasa_resp_filt = data_tasa_resp[data_tasa_resp.muestra == 1].copy()
    if country == 'mx':
        n_muestra = data_tasa_resp_filt[{'28 CDS_upm'}].reset_index().loc[0, '28 CDS_upm']
        dom_upms = data_tasa_resp_filt[{dominio + '_upm'}].reset_index().loc[0, dominio + '_upm']

    else:
        n_muestra = data_tasa_resp_filt[{'total_upm'}].reset_index().loc[0, 'total_upm']
        if dominio == 'Total RD':
            dom_upms = data_tasa_resp_filt[{'total_upm'}].reset_index().loc[0,'total_upm']
        else:
            dom_upms = data_tasa_resp_filt[{dominio + '_upm'}].reset_index().loc[0, dominio + '_upm']

    if dominio == 'PROV':
        dom = '25 CDS'
        children4 = 'Muestra ' + dom + ': ' + str(dom_upms) + ' UPMs'
    else:
        children4 = 'Muestra ' + dominio + ': ' + str(dom_upms) + ' UPMs'

    children3 = 'Muestra total: ' + str(n_muestra)+' UPMs'

    return min_muestra_tp, max_muestra_tp, children3, children4


# Primer callback: Para gráfica de puntos
@app.callback([dash.dependencies.Output('tit_graf1', 'children'),
               dash.dependencies.Output("scatter_chart", "figure")],
              [dash.dependencies.Input("dropdown1", "value"),
               dash.dependencies.Input("Slider1", "value"),
               dash.dependencies.Input("dropdown2", "value")]
              )
# Primera definicion de funcion: para el primer callback
def update_fig(drop_value, slide_value, base):
    # Base con los parámetros estimados
    nom_base_estimaciones = base
    data_par = pd.read_csv(DATA_PATH.joinpath(nom_base_estimaciones))

    data_par['e'] = data_par['ic_sup'] - data_par['proporcion']
    data_par0_filt = data_par[data_par.Muestra == 0].copy()

    slide_value = np.arange(slide_value[0], slide_value[1] + 1, 1)
    data_par_filt = data_par[data_par.Muestra.isin(slide_value)].copy()
    data_par_filt2 = data_par_filt[data_par_filt.DOMINIO == drop_value].copy()
    data_par0_filt2 = data_par0_filt[data_par0_filt.DOMINIO == drop_value].copy()

    data = []

    graf_dom = go.Scatter(name='ES 202X',
                          x=data_par0_filt2.categoria,
                          y=data_par0_filt2.proporcion,
                          mode='markers',
                          error_y=dict(type='data',
                                       array=data_par0_filt2.e,
                                       thickness=1.5,
                                       width=10),
                          marker_color='rgba(152,0,0,.8)',
                          marker_line_width=2, marker_size=8)

    graf_dom2 = go.Scatter(name='Muestra',
                           x=data_par_filt2.categoria,
                           y=data_par_filt2.proporcion,
                           mode='markers',
                           marker_size=4
                           # marker_color = data_par_filt2.prop,
                           # text = data_par_filt2.prop.round(1)
                           )

    data.append(graf_dom)
    data.append(graf_dom2)

    layout = {'title': 'Gráfica de dispersión de las proporciones estimadas',
              'xaxis': {'title': 'Categoría'},
              'yaxis': {'title': 'Proporción estimada',
                        'range': [0, 1]}}

    num_muestra = slide_value.max() + 1 - slide_value.min()
    children_markd = '  **Resumen estadístico de las** ' + str(num_muestra) + ' **réplicas seleccionadas**'

    return [children_markd, {'data': data, 'layout': layout}]


# Segundo callback: Para box-plot
@app.callback(
    dash.dependencies.Output("box_plot", "figure"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider1", "value"),
     dash.dependencies.Input("dropdown2", "value")]
)
# Segunda definicion de funcion: para el segundo callback
def update_fig2(drop_value, slide_value, base):
    #    # Base con los parámetros estimados
    nom_base_estimaciones = base
    data_par = pd.read_csv(DATA_PATH.joinpath(nom_base_estimaciones))
    data_par['e'] = (data_par['ic_sup'] - data_par['proporcion']) / 1.96

    slide_value = np.arange(slide_value[0], slide_value[1] + 1, 1)
    data_par_filt_b = data_par[data_par.Muestra.isin(slide_value)].copy()
    data_par_filt2_b = data_par_filt_b[data_par_filt_b.DOMINIO == drop_value].copy()

    data2 = []

    graf_dom_box = go.Box(x=data_par_filt2_b.categoria,
                          y=data_par_filt2_b.proporcion,
                          boxpoints='all',  # can also be outliers, or suspectedoutliers, or False
                          jitter=0.4,  # add some jitter for a better separation between points
                          pointpos=-1.8,
                          marker_color='rgb(107,174,214)',
                          line_color='rgb(8,81,156)',
                          marker_size=3,
                          boxmean=True)  # relative position of points wrt box)

    data2.append(graf_dom_box)

    layout2 = {'title': 'Box-plot de las proporciones estimadas',
               'xaxis': {'title': 'Categoría'},
               'yaxis': {'title': 'Proporción estimada',
                         'range': [0, 1]}}

    return {
        'data': data2,
        'layout': layout2
    }


# Tercer callback: Para tabla
@app.callback([
    dash.dependencies.Output("table1", "data"),
    dash.dependencies.Output('download-link', 'href')],
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider1", "value"),
     dash.dependencies.Input("checklist1", "value"),
     dash.dependencies.Input("dropdown2", "value")]
)
# Tercera definicion de funcion: para el tercer callback
def update_fig3(drop_value_c, slide_value_c, check_value_c, base):
    # Base con los parámetros estimados
    nom_base_estimaciones = base
    data_par = pd.read_csv(DATA_PATH.joinpath(nom_base_estimaciones))
    data_par['SE'] = (data_par['ic_sup'] - data_par['proporcion']) / 1.96

    slide_value_c = np.arange(slide_value_c[0], slide_value_c[1] + 1, 1)
    data_table = data_par[data_par.Muestra.isin(slide_value_c)].copy()
    columnas = ['Muestra', 'DOMINIO', 'categoria', 'proporcion', 'cv', 'sd', 'deff', 'n', 'tm', 'SE']

    data_table = data_table[columnas]
    data_table = data_table[data_table.DOMINIO == drop_value_c]

    data_table_melt = data_table.melt(id_vars=['Muestra', 'DOMINIO', 'categoria'],
                                      value_vars=['proporcion', 'cv', 'sd', 'deff', 'n', 'tm', 'SE'])

    data_table_resum = data_table_melt.groupby(["categoria", "variable"])['value'].agg([
        ('promedio', 'mean'),
        ('minimo', min),
        ('maximo', max)
    ]).reset_index()
    data_table_resum['promedio'] = data_table_resum.promedio.round(4)
    data_table_resum['minimo'] = data_table_resum.minimo.round(4)
    data_table_resum['maximo'] = data_table_resum.maximo.round(4)

    data_table_0 = data_par[data_par.Muestra == 0].copy()
    data_table_0 = data_table_0[columnas]
    data_table_0 = data_table_0[data_table_0.DOMINIO == drop_value_c]
    data_table_melt_0 = data_table_0.melt(id_vars=['Muestra', 'DOMINIO', 'categoria'],
                                          value_vars=['proporcion', 'cv', 'sd', 'deff', 'n', 'tm', 'SE'])
    data_table_melt_0['value'] = data_table_melt_0.value.round(4)
    data_table_resum = pd.merge(data_table_resum, data_table_melt_0, on=['categoria', 'variable'])
    data_table_resum = data_table_resum.rename(columns={'value': 'ES 202X'})

    data_table_resum = data_table_resum[data_table_resum.variable.isin(check_value_c)]
    data_table_resum = data_table_resum.rename(
        columns={'categoria': 'Categoría', 'variable': 'Parámetro', 'promedio': 'Promedio', 'minimo': 'Mínimo',
                 'maximo': 'Máximo'})

    cleanup_nums = {
        "Categoría": {"NSE_1": "NSE 1", "NSE_2": "NSE 2", "NSE_3": "NSE 3", "NSE_4": "NSE 4", "tv_rest": "TV Paga",
                      "sky": "SKY", "dish": "Dish", "cable": "Cable"},
        "Parámetro": {"proporcion": "Proporcion", "sd": 'SD', "cv": 'CV', "n": 'Número de hogares'}}

    data_table_resum.replace(cleanup_nums, inplace=True)

    data_table_update = data_table_resum.to_dict("rows")

    colum_tabla_csv = ['DOMINIO', 'Categoría', 'Parámetro', 'ES 202X', 'Promedio', 'Mínimo', 'Máximo', ]

    csv_string = data_table_resum[colum_tabla_csv].to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    return data_table_update, csv_string


# Cuarto callback: Para histograma
@app.callback([
    dash.dependencies.Output("histogram", "figure"),
    dash.dependencies.Output("tit_graf2", "children")],
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider2", "value"),
     dash.dependencies.Input("dropdown3", "value")]
)
# Cuarta definicion de funcion: para el cuarto callback
def update_fig4(drop_value_d, slide_value_d, base):
    # Base tasa de respuesta
    nom_base_tasas = base
    data_tasa_resp = pd.read_csv(DATA_PATH.joinpath(nom_base_tasas))

    slide_value_d = np.arange(slide_value_d[0], slide_value_d[1] + 1, 1)
    data_tp_filt = data_tasa_resp[data_tasa_resp.muestra.isin(slide_value_d)].copy()
    data_tp_filt2 = data_tp_filt[drop_value_d].copy()

    data3 = []

    histo_dom = go.Histogram(
        x=data_tp_filt2,
        xbins=dict(  # bins used for histogram
            start=.30,
            end=1,
        ),
        marker_color='#330C73',
        opacity=0.75
    )

    data3.append(histo_dom)

    num_muestra_d = slide_value_d.max() + 1 - slide_value_d.min()
    children_markd_d = '  **Resumen estadístico de las** ' + str(num_muestra_d) + ' **réplicas seleccionadas**'

    return [{'data': data3}, children_markd_d]


# Quinto callback: Para segunda tabla
@app.callback(
    dash.dependencies.Output("table2", "data"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider2", "value"),
     dash.dependencies.Input("dropdown3", "value")]
)
def update_fig5(drop_value_d, slide_value_d, base):
    # Base tasa de respuesta
    nom_base_tasas = base
    data_tasa_resp = pd.read_csv(DATA_PATH.joinpath(nom_base_tasas))
    data_tasa_resp_0 = data_tasa_resp[data_tasa_resp.muestra == 0].copy()

    slide_value_d = np.arange(slide_value_d[0], slide_value_d[1] + 1, 1)
    data_table_tp = data_tasa_resp[data_tasa_resp.muestra.isin(slide_value_d)].copy()
    data_table_tp = data_table_tp[{'muestra', drop_value_d}]

    data_table_tp0 = data_tasa_resp_0[{'muestra', drop_value_d}].copy()
    data_table_tp0 = data_table_tp0.rename(columns={drop_value_d: 'Promedio'})
    data_table_tp0['Promedio'] = data_table_tp0.Promedio.round(4)
    data_table_tp0['muestra'] = 'ES 202X'
    data_table_tp0['Mínimo'] = 0
    data_table_tp0['Máximo'] = 0
    data_table_tp0['SD'] = 0

    data_table_tp['muestra'] = 1
    data_table_tp_resum = data_table_tp.groupby(["muestra"])[drop_value_d].agg([
        ('promedio', 'mean'),
        ('SD', 'std'),
        ('minimo', min),
        ('maximo', max)
    ]).reset_index()
    data_table_tp_resum['promedio'] = data_table_tp_resum.promedio.round(4)
    data_table_tp_resum['SD'] = data_table_tp_resum.SD.round(4)
    data_table_tp_resum['minimo'] = data_table_tp_resum.minimo.round(4)
    data_table_tp_resum['maximo'] = data_table_tp_resum.maximo.round(4)
    data_table_tp_resum = data_table_tp_resum.rename(
        columns={'promedio': 'Promedio', 'minimo': 'Mínimo', 'maximo': 'Máximo'})
    data_table_tp_resum['muestra'] = 'Muestras'

    frame = [data_table_tp0, data_table_tp_resum]
    data_table_resum_muest = pd.concat(frame)
    data_table_resum_muest = data_table_resum_muest.rename(columns={'muestra': 'Muestra'})

    data_table_update2 = data_table_resum_muest.to_dict("rows")

    return data_table_update2


if __name__ == '__main__':
    app.run_server(debug=True)
