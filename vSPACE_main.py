import base64
import io
import numpy
import dash_table
import dash
from dash import dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash import callback_context
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import callback_context, no_update
import scipy.stats as stats
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.decomposition import PCA

external_stylesheets = ['./web_portal/assets/stylesheet_scatters.css', './web_portal/assets/bootstrap.css']
external_scripts = './web_portal/assets/userdefined_scripts.js'
external_scripts_01 = ['http://code.jquery.com/jquery-1.11.0.min.js']

#pre-load the data
# input_csv_file_pathway = './data/rpax_routes_order2.txt'
input_csv_file_directory = 'C:/Users/chz17013/PycharmProjects/2022Spring/data/cartnorm_raw/'
image_directory_1 = '/assets/images_dir/images_CartNorm1_31_F_G1/'
image_directory_2 = '/assets/images_dir/images_CartNorm2_24_M_G0/'
image_directory_3 = '/assets/images_dir/images_CartNorm3_20_M_G0/'
image_directory_4 = '/assets/images_dir/images_CartNorm4_56_M_G1_all/'
image_directory_5 = '/assets/images_dir/images_CartNorm5_49_M_G2/'
image_directory_6 = '/assets/images_dir/images_CartNorm6_27_F_G0/'
image_directory_7 = '/assets/images_dir/images_OA_PekingU/'
image_directory_8 = '/assets/images_dir/images_OA1/'
image_directory_9 = '/assets/images_dir/images_OA2/'
image_directory_10 = '/assets/images_dir/images_OA3/'
image_directory_11 = '/assets/images_dir/images_OA4/'
image_directory_12 = '/assets/images_dir/images_OA5/'
image_directory_13 = '/assets/images_dir/images_OA6/'

# df_pathway = pd.read_csv(input_csv_file_pathway, delimiter='\t', header = 0)
df_data_file_list = ['2AVGs_CartNorm1_31_F_G1.csv', '2AVGs_CartNorm2_24_M_G0.csv', '2AVGs_CartNorm3_20_M_G0.csv',
                     '2AVGs_CartNorm4_56_M_G1.csv', '2AVGs_CartNorm5_49_M_G2.csv', '2AVGs_CartNorm6_27_F_G0.csv', '2AVGs_GSE104782_PekingU.csv',
                     '2AVGs_OA1.csv', '2AVGs_OA2.csv', '2AVGs_OA3.csv', '2AVGs_OA4.csv',
                     '2AVGs_OA5.csv', '2AVGs_OA6.csv',
                     ]

app = dash.Dash(
    __name__,
    # external_stylesheets=external_stylesheets,

)

server = app.server
app.scripts.config.serve_locally = True
# suppress the exceptions
app.config.suppress_callback_exceptions = True

# global settings
lst = [i for i in range(1, 100)]
# route_list = ["Route"+str(i) for i in lst]
index_list = lst

# app layut
app.layout = html.Div([
    html.Div(className='header', children=[
        html.H2('vSPACE (Virtual Spatial Articular Cartilage Explorer)',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.2em',
                       'margin-left': '7px',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
    ]),
    dcc.RadioItems(
        id='form_selection',
        options=[
            {'label': 'Use Drag & Drop', 'value': 0},
            {'label': 'Use Sample Data', 'value': 1},
        ],
        value=0
    ),
    html.Div(
        dcc.Upload(
            id='upload-data-1',
            children=html.Div([
                'Drop main data or ',
                html.A('Select Files', href="#")
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        style=dict(width='32%', display='inline-block')
    ),
    html.Div(
        dcc.Upload(
            id='upload-data-selection',
            children=html.Div([
                'Drop selection data or ',
                html.A('Select Files', href="#")
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        style=dict(width='32%', display='inline-block')
    ),
    html.Div(
        dcc.Upload(
            id='upload-umap-data',
            children=html.Div([
                'Drop umap/tsne data or ',
                html.A('Select Files', href="#")
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        style=dict(width='32%', display='inline-block')
    ),
    html.Div(id='localdata_panel', children=[
        html.H4('Or select data from',
                style={'display': 'inline-block', 'margin-left': 10, 'margin-right': 20, 'margin-top': 0}),
        dcc.Dropdown(
            id='data_selection',
            # options=[{'label': s[0], 'value': str(s[0])}
            #          for s in zip(route_list, route_list)],
            options=[{'label': 'CartNorm1_31_F_G1', 'value': 0},
                     {'label': 'CartNorm2_24_M_G0', 'value': 1},
                     {'label': 'CartNorm3_20_M_G0', 'value': 2},
                     {'label': 'CartNorm4_56_M_G1', 'value': 3},
                     {'label': 'CartNorm5_49_M_G2', 'value': 4},
                     {'label': 'CartNorm6_27_F_G0', 'value': 5},
                     {'label': 'OA_PekingU', 'value': 6},
                     {'label': 'OA1', 'value': 7},
                     {'label': 'OA2', 'value': 8},
                     {'label': 'OA3', 'value': 9},
                     {'label': 'OA4', 'value': 10},
                     {'label': 'OA5', 'value': 11},
                     {'label': 'OA6', 'value': 12},
                     ],
            value=3,
            multi=False,
            placeholder='Please select existing data file',
            style={'width': '75%'},
        )], style=dict(width='66.5%', display='inline-block')),

    html.Div(id='viz_panel', children=[
        html.Hr(),
        dcc.RadioItems(
            id='color_selection',
            options=[
                {'label': 'Use Gradient Color(2 Genes Allowed )', 'value': 0},
                {'label': 'Use Cell Selection(Multiple Genes Allowed)', 'value': 1},
            ],
            value=0
        ),
        html.Div(dcc.Dropdown(
            id='dropdown',
            options=[{'label': s[0], 'value': str(s[0] + 2)}
                     for s in zip(index_list, index_list)],
            value='PRG4',
            # multi=True,
            multi=False,
            placeholder='Please select from options',
            style={'width': '100%'},
        ), style=dict(width='50%', display='inline-block')),

        html.Div(children=[dcc.Dropdown(
            id='dropdown_gene2',
            options=[{'label': s[0], 'value': str(s[0] + 2)}
                     for s in zip(index_list, index_list)],
            value='PRG4',
            multi=False,
            placeholder='Please select from options',
            className='red-placeholder',
            style={'width': '100%', 'color': 'red'},
        ),
            dcc.Dropdown(
                id='dropdown_geneset',
                options=[{'label': s[0], 'value': str(s[0] + 2)}
                         for s in zip(index_list, index_list)],
                value='PRG4',
                multi=True,
                placeholder='Please select from options',
                className='blue-placeholder',
                style={'width': '100%', 'color': 'blue'},
            ), ],
            style=dict(width='50%', display='inline-block')),

        html.Hr(),
        html.Div(children=[
            html.Div([
                html.H4('Y-axis H threshold', style={'display': 'inline-block', 'margin-right': 20, 'margin-top': 0}),
                dcc.Input(
                    id='threshold_YH',
                    value='0.79',
                    placeholder='0.79',
                    style=dict(width='25%'),
                )
            ], style={'width': '50%', 'display': 'inline-block'}, ),
            html.Div([
                html.H4('Y-axis L threshold', style={'display': 'inline-block', 'margin-right': 20, 'margin-top': 0}),
                dcc.Input(
                    id='threshold_YL',
                    value=-0.99,
                    placeholder='-0.99',
                    style=dict(width='25%'),
                )
            ], style={'width': '50%', 'display': 'inline-block'}, ),
            html.Div([
                html.H4('Mean without DO', style={'display': 'inline-block', 'margin-right': 35, 'margin-top': 0}),
                dcc.Input(
                    id='threshold_X',
                    value=0,
                    placeholder='0',
                    style=dict(width='25%'),
                )
            ], style={'width': '50%', 'display': 'inline-block'}, ),
            html.Div([
                html.H4('Mean with DO', style={'display': 'inline-block', 'margin-right': 35, 'margin-top': 0}),
                dcc.Input(
                    id='threshold_X_DO',
                    value=0,
                    placeholder='0',
                    style=dict(width='25%'),
                )
            ], style={'width': '50%', 'display': 'inline-block'}, ),
            html.Div([
                html.H4('Dot Size:', style={'display': 'inline-block', 'margin-right': 35, 'margin-top': 0}),
                dcc.Input(
                    id='dots_size',
                    value='5',
                    placeholder='0',
                    style=dict(width='25%'),
                )
            ], style={'width': '50%', 'display': 'inline-block'}, ),
        ]),
        dcc.RadioItems(
            id='region_selection',
            options=[
                {'label': 'High', 'value': 1},
                {'label': 'Low', 'value': 0},
                {'label': 'Absent', 'value': 2},
            ],
            value=1,
        ),
        html.Br(),
        html.B(id='display-selected-values', style={'font-size': '25px', 'display': 'inline-block',
                                                    'padding-right': '1vw', 'margin-right': 20,
                                                    }),
        html.B(id='display-selected-values-2', style={'font-size': '25px', 'display': 'inline-block',
                                                      'padding-right': '1vw'
                                                      }),
        dbc.Button("Show ALL Cases", id="open", color="primary", className="me-1",
                   style={'font-size': '25px', 'display': 'inline-block',
                          'padding-right': '1vw',
                          }),
        dbc.Button("Download Selected Cells", id="btn_csv", color="info", className="me-1",
                   style={'font-size': '25px', 'display': 'inline-block',
                          'padding-right': '1vw'
                          }),
        dbc.Button("Download Highlighted Cells", id="btn_csv_2", color="info", className="me-1",
                   style={'font-size': '25px', 'display': 'inline-block',
                          'padding-right': '1vw'
                          }),
        dbc.Modal(
            [
                # dbc.ModalHeader(" "),
                # dbc.ModalBody(" "),

                # html.Img(src=input_image_file_directory + 'ACAN.png'),
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            html.H1('CartNorm1_31_F_G1', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_1',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('CartNorm2_24_M_G0', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_2',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('CartNorm3_20_M_G0', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_3',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('CartNorm4_56_M_G1', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_4',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('CartNorm5_49_M_G2', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_5',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('CartNorm6_27_F_G0', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_cartnorm_6',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),
                        dbc.Col([
                            html.H1('OA_Peking_U', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA_Peking_U',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA1', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA1',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA2', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA2',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA3', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA3',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA4', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA4',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA5', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA5',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),

                        dbc.Col([
                            html.H1('OA6', style={'backgroundColor': 'white', 'margin': '0'}),
                            html.Img(id='img_gene_OA6',
                                     style={'width': '370px', 'height': '480px', 'display': 'inline-block'})
                        ], style={'float': 'left'}, width=2),
                    ], )
                ], fluid=True),

                dbc.ModalFooter(
                    dbc.Button("X", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        ),

        html.Hr(),

        html.Div(children=[
            dcc.Graph(id='g1',
                      style={'display': 'inline-block', 'vertical-align': 'top'},
                      config={
                          'editable': True,
                          'edits': {
                              'shapePosition': True
                          }
                      }
                      ),
            html.Div(id='table-set', children=[
                html.Div(style={'width': '50px', 'height': '50px'}, ),
                html.B(id='display-selected-values-3', style={'font-size': '25px', 'display': 'inline-block',
                                                              'padding-right': '1vw', 'margin-right': 20,
                                                              }),
                # html.Div(style={'width': '50px', 'height': '110px'}, ),
                html.Div(id='datatable_1',
                         style={'width': '30%', 'height': '40vm'}, ),
                html.Div(style={'width': '50px', 'height': '20px'}, ),

                html.Div(id='table-set-2', children=[
                    html.B(id='display-selected-values-4', style={'font-size': '25px', 'display': 'inline-block',
                                                                  }),
                    # html.Div(style={'width': '50px', 'height': '110px'}, ),
                    html.Div(id='datatable_2',
                             style={'width': '30%', 'height': '40vm'}, ),
                    html.Div(style={'width': '50px', 'height': '20px'}, ),

                ], style={'vertical-align': 'top', 'width': '70%', 'display': 'inline-block'}),


                html.B(id='display-selected-stat', style={'font-size': '25px', 'display': 'inline-block',
                                                                              'padding-right': '1vw', 'margin-right': 20,
                                                                              }),
                dbc.Button("Run", id="btn_stat_run", color="info", className="me-1",
                           style={'font-size': '25px', 'display': 'inline-block',
                                  'padding-right': '1vw'
                                  }),


                dcc.RadioItems(
                    id='stat_test_selection',
                    options=[
                        {'label': 'Spearman correlation', 'value': 0},
                    ],
                    value=0
                ),
                html.Div(style={'width': '50px', 'height': '20px'}, ),
                html.B(id='display-selected-values-3-1', style={'font-size': '25px', 'display': 'inline-block',
                                                                              'padding-right': '1vw', 'margin-right': 20,
                                                                              }),
                html.Div(id='datatable_1_1',
                         style={'width': '30%', 'height': '40vm'}, ),

            ], style={'vertical-align': 'top', 'width': '35%', 'display': 'inline-block'}),


            dcc.Graph(id="g_cluster",
                      style={'display': 'inline-block', 'vertical-align': 'top', 'display': 'none'},
                      config={
                          'editable': True,
                          'edits': {
                              'shapePosition': True
                          }
                      }
                      ),
            dcc.Graph(id="g2",
                      style={'display': 'inline-block', 'vertical-align': 'top', 'display': 'none'},
                      config={
                          'editable': True,
                          'edits': {
                              'shapePosition': True
                          }
                      }
                      ),
            dcc.Graph(id="g3",
                      style={'display': 'inline-block', 'vertical-align': 'top', 'display': 'none'},
                      config={
                          'editable': True,
                          'edits': {
                              'shapePosition': True
                          }
                      }
                      ),

        ]),
        html.Hr(),

        # temp memory
        dcc.Store(id='memory-rawdata'),
        dcc.Store(id='memory-output'),
        dcc.Store(id='memory-visulize-output'),
        dcc.Store(id='memory-printout'),

        dcc.Download(id="download-dataframe-csv"),
        dcc.Download(id="download-dataframe-csv_2"),
        dcc.Download(id="download-stat-csv"),
    ], style={'width': '100%', }),

], className="container")


def average_exclude_min(values):
    filtered_values = [value for value in values if value != min(values)]
    return sum(filtered_values) / len(filtered_values)


def update_dropout_selection(form_selection, data_selection, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None and form_selection == 0:
        filename = list_of_names[0]
        contents = parse_contents(list_of_contents[0], list_of_names, list_of_dates)
        data_dicts = contents[0]
        lst_dict = contents[2]
        if list(contents[2].values())[0] == 'pvalue':
            # remove the shit info
            lst_dict.pop('Barcode')
            lst_dict.pop('y-score')
            lst_dict.pop('label')
            # to convert lists to df
            # lst = [str(x) + '-pvalue:' + str(y) for x, y in zip(list(data_dicts.keys())[3:], list(pvalue_list[3:]))]
            # convert string to float from dict
            for k, v in lst_dict.items():
                lst_dict[k] = float(v)
            sort_lst_dict = {k: v for k, v in sorted(lst_dict.items(), key=lambda item: item[1])}
            # lst = raw_data.columns[3:]
            lst = [str(x) + '-pvalue:' + str(y) for x, y in zip(sort_lst_dict.keys(), list(sort_lst_dict.values()))]
            lst_value = list(sort_lst_dict.keys())

            return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst_value)], lst_value[0]]
        else:
            lst = list(data_dicts.keys())[3:]
            return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], lst[0]]
    elif data_selection is not None and form_selection == 1:

        raw_data = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',', header=None)
        # raw_data = df_data_list[data_selection]
        pond_length = 0
        for i, row in raw_data.iterrows():
            pond_cur = row[0]
            if "#" in pond_cur:
                pond_length += 1
            else:
                break
        raw_data = raw_data[pond_length:]
        # firstrow as new header
        # check if have p-value list
        if raw_data.iloc[0, 0] == 'pvalue':
            pvalue_lst = raw_data.iloc[0, 3:].sort_values(ascending=True)
            # lst = raw_data.columns[3:]
            lst = pvalue_lst.index + '-pvalue:' + pvalue_lst.tolist()
            lst_value = pvalue_lst.index
            return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst_value)], lst_value[0]]
        else:
            lst = [x for x in raw_data.columns[3:] if str(x) != 'nan']
            return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], lst[0]]
    else:
        return [[{'label': s[0], 'value': str(s[0] + 2)}
                 for s in zip(index_list, index_list)], ' ']


def parse_contents_df(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.ExcelFile(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


def calculate_tables(x_axis, y_axis, data, threshold_YL, threshold_YH, temp_index, sub_name):
    datapoints_samplename = dict2List(data, 'Barcode')
    # check if the datamatrix contail pvalue
    if data['Barcode'][0] == 'pvalue':
        data = data[1:]
        data = data.reset_index(drop=True)
    if data['Barcode'][0] == 'AVG1' and data['Barcode'][1] == 'AVG2':
        avg_W_DO = data[y_axis][0]
        avg_WO_DO = data[y_axis][1]
        data = data[2:]
        index = 2
    else:
        index = 0
    data['Quadrant'] = ''
    min_y_axis = min(data[y_axis])
    # calculate the avergae of z score data without zeros
    filter_list = list(filter(lambda a: a != min_y_axis, list(data[y_axis])))
    mean_list = Average(filter_list) if len(filter_list) != 0 else 0
    threshold_X = mean_list
    # n_s1 = do_s1 + n_s1 without DOs
    x_s2, y_s2, x_m2, y_m2, x_d2, y_d2, x_d1, y_d1, x_m1, y_m1, x_s1, y_s1 = [], [], [], [], [], [], [], [], [], [], [], []
    sample_s2, sample_m2, sample_d2, sample_d1, sample_m1, sample_s1 = [], [], [], [], [], []
    n_s2 = n_m2 = n_d2 = n_d1 = n_m1 = n_s1 = 0
    threshold_YH = float(threshold_YH)
    threshold_YL = float(threshold_YL)
    # threshold_X = float(threshold_X)
    do_s1, do_m1, do_d1 = 0, 0, 0
    for datapoint_x, datapoint_y in zip(data[x_axis], data[y_axis]):

        if datapoint_x >= threshold_YH and datapoint_y >= threshold_X:
            x_s2.append(datapoint_x)
            y_s2.append(datapoint_y)
            sample_s2.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'S2'
            n_s2 += 1
        elif datapoint_x <= threshold_YH and datapoint_x >= threshold_YL and datapoint_y >= threshold_X:
            x_m2.append(datapoint_x)
            y_m2.append(datapoint_y)
            sample_m2.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'M2'
            n_m2 += 1
        elif datapoint_x <= threshold_YL and datapoint_y >= threshold_X:
            x_d2.append(datapoint_x)
            y_d2.append(datapoint_y)
            sample_d2.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'D2'
            n_d2 += 1
        elif datapoint_x <= threshold_YL and datapoint_y <= threshold_X:
            x_d1.append(datapoint_x)
            y_d1.append(datapoint_y)
            sample_d1.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'D1'
            n_d1 += 1
            if datapoint_y == min_y_axis:
                do_d1 += 1
        elif datapoint_x >= threshold_YH and datapoint_y <= threshold_X:
            x_s1.append(datapoint_x)
            y_s1.append(datapoint_y)
            sample_s1.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'S1'
            n_s1 += 1
            if datapoint_y == min_y_axis:
                do_s1 += 1
        else:
            # elif datapoint_x <= threshold_YH and datapoint_x >= threshold_YL and datapoint_y <= threshold_X:
            x_m1.append(datapoint_x)
            y_m1.append(datapoint_y)
            sample_m1.append(datapoints_samplename[index])
            data.loc[index, 'Quadrant'] = 'M1'
            n_m1 += 1
            if datapoint_y == min_y_axis:
                do_m1 += 1
        index += 1
    sum_total = n_s1 + n_s2 + n_m1 + n_m2 + n_d1 + n_d2
    do_subtotal = do_s1 + do_m1 + do_d1
    NL_subtotal = n_s1 - do_s1 + n_m1 - do_m1 + n_d1 - do_d1
    NR_subtotal = n_s2 + n_m2 + n_d2
    SZ_subtotal = n_s1 + n_s2
    MZ_subtotal = n_m1 + n_m2
    DZ_subtotal = n_d1 + n_d2
    all_left_subtotal = n_s1 + n_m1 + n_d1
    all_right_subtotal = n_s2 + n_m2 + n_d2

    if temp_index == 0 or temp_index == -1:
        # df_data_distribution_table = pd.DataFrame(
        #     dict(Zone=sub_name,
        #          percentage=[percentageConverter((n_s1 + n_s2) / sum_total), percentageConverter((n_m1 + n_m2) / sum_total), percentageConverter((n_d1 + n_d2) / sum_total)]))

        # final table
        total_exp = len(data[y_axis]) * avg_W_DO
        allcell_mean_exp = sum(data[y_axis])
        df_data_Final = pd.DataFrame({
            'Item': ['scRna Total Expression', 'Mean Exp of Expressing Cells', 'Mean Exp of All Cells',
                     '%Total', '%Sup', '%Mid', '%Deep'],
            'Value': [round(total_exp, 3), round(avg_WO_DO,3), round(avg_W_DO,3),
                      percentageConverter(fractionCalculator(sum_total - do_subtotal, sum_total)),
                      percentageConverter(fractionCalculator(SZ_subtotal, SZ_subtotal + do_s1)),
                      percentageConverter(fractionCalculator(MZ_subtotal, MZ_subtotal + do_m1)),
                      percentageConverter(fractionCalculator(DZ_subtotal, DZ_subtotal + do_d1))],
        })
    return data, df_data_Final


# Python program to get average of a list
def Average(lst):
    return numpy.nansum(lst) / len(lst)


def percentageConverter(x):
    percentage = str(round(x * 100, 2)) + '%'
    return percentage


def dataframe2List(source, colName):
    return pd.DataFrame(source, columns=[colName]).values.reshape(-1, ).tolist()


def dict2List(source, colName):
    return source[colName]


def fractionCalculator(nomiator, denominator):
    return 0 if denominator == 0 else nomiator / denominator


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    data_file = str(decoded).split('\\r\\n')
    dicts = {}
    pvalue_dict = {}
    for line in data_file:
        temp = line.split(',')
        if "#" in temp[0]:
            if "type" in temp[0]:
                global_type = temp[0].split('=')[1].replace(" ", "")
            continue  # skipping the first n rows that contains #
        else:
            gene_name = temp[0]
            if gene_name != "'":
                genevalue_matrix = temp[1:]
                dicts[gene_name] = genevalue_matrix
                pvalue_dict[gene_name] = temp[1]
            else:
                break
    return [dicts, global_type, pvalue_dict]


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_1', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    return image_directory_1 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_2', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_2 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_3', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_3 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_4', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_4 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_5', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_5 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_cartnorm_6', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_6 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA_Peking_U', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    return image_directory_7 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA1', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_8 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA2', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_9 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA3', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_10 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA4', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_11 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA5', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_12 + value + '.png'


@app.callback(
    dash.dependencies.Output('img_gene_OA6', 'src'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_image_src(value):
    # print(value)
    return image_directory_13 + value + '.png'


@app.callback(
    Output('localdata_panel', 'style'),
    [Input('form_selection', 'value'), ])
def update_localdata_panel(form_selection):
    if form_selection == 1:
        return {'display': 'block', 'width': '95%', }
    else:
        return {'display': 'none'}


@app.callback(
    Output('btn_csv', 'style'),
    [Input('color_selection', 'value'), ])
def update_btn_csv(form_selection):
    if form_selection == 0:
        return {'font-size': '25px', 'display': 'inline-block',
                'padding-right': '1vw'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('btn_csv_2', 'style'),
    [Input('color_selection', 'value'), ])
def update_btn_csv_2(form_selection):
    if form_selection == 1:
        return {'font-size': '25px', 'display': 'inline-block',
                'padding-right': '1vw'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('dropdown_gene2', 'style'),
    [Input('color_selection', 'value'), ])
def update_dropdown_gene2(form_selection):
    if form_selection == 0:
        return {'width': '100%', 'color': 'red', 'display': 'inline-block', }
    else:
        return {'display': 'none'}


@app.callback(
    Output('dropdown_geneset', 'style'),
    [Input('color_selection', 'value'), ])
def update_dropdown_geneset(form_selection):
    if form_selection == 1:
        return {'width': '100%', 'color': 'blue', 'display': 'inline-block', }
    else:
        return {'display': 'none'}


@app.callback(
    Output('threshold_YH', 'value'),
    [Input('g1', 'relayoutData'), Input('upload-data-1', 'contents'), State('upload-data-1', 'filename'),
     State('upload-data-1', 'last_modified'), ], )
def g1_drag_tracker(relayoutData, list_of_contents, list_of_names, list_of_dates):
    print(0.1)
    if list(relayoutData.keys())[0] == 'shapes[0].x0':
        print(0.11)
        return relayoutData['shapes[0].y0']
    else:
        print(0.13)
        return no_update


@app.callback(
    Output('threshold_YL', 'value'),
    [Input('g1', 'relayoutData'), Input('upload-data-1', 'contents'), State('upload-data-1', 'filename'),
     State('upload-data-1', 'last_modified'), ])
def g1_drag_tracker(relayoutData, list_of_contents, list_of_names, list_of_dates):
    if list(relayoutData.keys())[0] == 'shapes[1].x0':
        return relayoutData['shapes[1].y0']
    else:
        return no_update


@app.callback(
    Output('threshold_X', 'value'),
    [Input('memory-rawdata', 'data')])
def g1_drag_tracker(df_json):
    if df_json is not None:
        data = pd.read_json(df_json[0][0])
        if data['Barcode'][0] == 'pvalue':
            if data['Barcode'][2] == 'AVG2':
                # avg = data['y-score'][0]
                avg_noDO = data.iloc[:, 1][1]
                return avg_noDO
        elif data['Barcode'][0] == 'AVG1':
            if data['Barcode'][1] == 'AVG2':
                # avg = data['y-score'][0]
                avg_noDO = data.iloc[:, 1][1]
                return avg_noDO


@app.callback(
    Output('threshold_X_DO', 'value'),
    [Input('memory-rawdata', 'data')])
def g1_drag_tracker(df_json):
    if df_json is not None:
        data = pd.read_json(df_json[0][0])
        if data['Barcode'][0] == 'pvalue':
            if data['Barcode'][1] == 'AVG1':
                avg = data.iloc[:, 1][0]
                # avg_noDO = data.iloc[:,1][1]
                return avg
        else:
            if data['Barcode'][0] == 'AVG1':
                avg = data.iloc[:, 1][0]
                # avg_noDO = data.iloc[:,1][1]
                return avg


@app.callback(
    Output('datatable_1', 'children'),
    [Input('memory-output', 'data')])
def update_datatable(df_json):
    if not df_json:
        return {}
    else:
        df_data_table = pd.read_json(df_json[1])
        return dash_table.DataTable(
            id='datatable_div',
            columns=[{"name": i, "id": i} for i in df_data_table.columns],
            data=df_data_table.to_dict('records'),
            # row_selectable="single",
        ),

@app.callback(
    Output('datatable_1_1', 'children'),
    [Input('memory-visulize-output', 'data'), Input('data_selection', 'value'), Input('color_selection', 'value'), Input('dropdown_geneset', 'value'),
     Input('stat_test_selection', 'value'), Input("btn_stat_run", "n_clicks")])
def update_datatable(df_json, data_selection, color_selection, cellgenes, stat_test_selection, n_clicks,):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    remove_genes = ['DKK3', 'LAMC1', 'LAMC3', 'LAMA2', 'LAMB1', 'LAMB3', 'LAMA1', 'LMNA', 'LMNB2']
    if df_json and color_selection == 1 and 'btn_stat_run' in changed_id:
        df = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                         index_col=0, header=0,
                         skiprows=6)
        # data contains 2 nan lines and get the first data matrix
        df_cellselection = pd.read_json(df_json[0][0])
        df_res = df[df_cellselection[df_cellselection['cell_label'] == 'P']['Barcode']][2:]
        # add cell_label
        df_res_MI = df[df_cellselection['Barcode']][2:]
        df_cellselection.set_index('Barcode', inplace=True)
        df_res_MI.loc['cell_label'] = df_cellselection['cell_label']
        df_res_MI.loc['cell_label'] = df_res_MI.loc['cell_label'].map({'A': 0, 'P': 1})
        # df_res = df[df_cellselection[df_cellselection['cell_label'] == 'P']['Barcode']][2:]
        if isinstance(cellgenes, list):
            cellgenes.append(df_cellselection.columns[0])
        else:
            cellgenes = [cellgenes]
            cellgenes.append(df_cellselection.columns[0])
        if stat_test_selection == 0:
            # spearman test
            # target_gene_expression = df_res.loc[cellgenes].astype(float).mean(axis=0)
            # PCA tansfromation
            pca = PCA(n_components=1)
            target_gene_expression = pca.fit_transform(df_res.loc[cellgenes].astype(float).T)

            target_gene_expression = target_gene_expression.ravel()
            test_results = []
            for gene in df_res.index:
                temp_df = df_res.loc[gene].dropna()
                if gene not in cellgenes and gene not in remove_genes:
                    correlation, p_value = stats.spearmanr(target_gene_expression, temp_df)
                    test_results.append((gene, p_value, correlation))

            test_df = pd.DataFrame(test_results, columns=['Gene', 'P_value', 'correlation'])
            test_df_sorted = test_df.sort_values(by='correlation', ascending=False)
            top_genes = test_df_sorted.head(10)
            top_genes_df = top_genes[['Gene', 'P_value', 'correlation']]
            top_genes_df['P_value'] = top_genes_df['P_value'].apply(lambda x: '{:.2e}'.format(x))
            top_genes_df['correlation'] = top_genes_df['correlation'].apply(lambda x: round(x,3))
            final_res = dash_table.DataTable(
                id='datatable_div',
                columns=[{"name": i, "id": i} for i in top_genes_df.columns],
                data=top_genes_df.to_dict('records'),
                # row_selectable="single",
            )
            return final_res
        elif stat_test_selection == 1:
            test_results = []
            for gene in df_res.index:
                selected_gene_expression = df_res.loc[gene].dropna()
                overall_gene_expression = df.loc[gene].dropna()
                if len(selected_gene_expression) > 0 and len(overall_gene_expression) > 0 and gene not in cellgenes:
                    statistic, p_value = stats.mannwhitneyu(selected_gene_expression.astype(float),
                                                            overall_gene_expression.astype(float),
                                                            alternative='two-sided')
                else:
                    statistic, p_value = np.nan, np.nan
                test_results.append((gene, p_value))

            test_df = pd.DataFrame(test_results, columns=['Gene', 'P_value'])
            test_df_sorted = test_df.sort_values(by='P_value', ascending=True)
            top_genes = test_df_sorted.head(10)
            top_genes_df = top_genes[['Gene', 'P_value']]
            top_genes_df['P_value'] = top_genes_df['P_value'].apply(lambda x: '{:.2e}'.format(x))
            final_res = dash_table.DataTable(
                id='datatable_div',
                columns=[{"name": i, "id": i} for i in top_genes_df.columns],
                data=top_genes_df.to_dict('records'),
                # row_selectable="single",
            ),
            return final_res

    else:
            return {}, {}

#
# @app.callback(
#     Output('datatable_1_2', 'children'),
#     [Input('memory-visulize-output', 'data'), Input('data_selection', 'value'), Input('color_selection', 'value')])
# def update_datatable(df_json, data_selection, color_selection):
#     if df_json and color_selection == 1:
#         df = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
#                          index_col=0, header=0,
#                          skiprows=6)
#         # data contains 2 nan lines and get the first data matrix
#         df_cellselection = pd.read_json(df_json[0][0])
#         df_res = df[df_cellselection[df_cellselection['cell_label'] == 'P']['Barcode']][2:]
#         # spearman test
#
#         test_results = []
#         for gene in df_res.index:
#             selected_gene_expression = df_res.loc[gene].dropna()
#             overall_gene_expression = df.loc[gene].dropna()
#             if len(selected_gene_expression) > 0 and len(overall_gene_expression) > 0:
#                 statistic, p_value = stats.mannwhitneyu(selected_gene_expression.astype(float), overall_gene_expression.astype(float),
#                                                   alternative='two-sided')
#             else:
#                 statistic, p_value = np.nan, np.nan
#             test_results.append((gene, p_value))
#
#         test_df = pd.DataFrame(test_results, columns=['Gene', 'P_value'])
#         test_df_sorted = test_df.sort_values(by='P_value', ascending=True)
#         top_genes = test_df_sorted.head(10)
#         top_genes_df = top_genes[['Gene', 'P_value']]
#         top_genes_df['P_value'] = top_genes_df['P_value'].apply(lambda x: '{:.2e}'.format(x))
#         return dash_table.DataTable(
#             id='datatable_div',
#             columns=[{"name": i, "id": i} for i in top_genes_df.columns],
#             data=top_genes_df.to_dict('records'),
#             # row_selectable="single",
#         ),
#     else:
#             return {}



@app.callback(
    Output('datatable_2', 'children'),
    [Input('memory-output', 'data'), Input('dropdown', 'value'), Input('dropdown_gene2', 'value'), Input('color_selection', 'value')])
def update_datatable(df_json, select_gene, gradient_value, color_selection):
    if color_selection == 0 and select_gene != gradient_value:
        df_data_table = pd.read_json(df_json[2])
        return dash_table.DataTable(
            id='datatable_div',
            columns=[{"name": i, "id": i} for i in df_data_table.columns],
            data=df_data_table.to_dict('records'),
            # row_selectable="single",
        ),
    else:
        return {}




@app.callback(
    Output('memory-rawdata', 'data'),
    [Input('color_selection', 'value'), Input('form_selection', 'value'), Input('data_selection', 'value'),
     Input('dropdown', 'value'), Input('upload-data-1', 'contents'), Input('dropdown_gene2', 'value'),
     Input('dropdown_geneset', 'value'),
     State('upload-data-1', 'filename'), State('upload-data-1', 'last_modified'),
     ])
def produce_raw_data(color_selection, form_selection, data_selection, index_selection, list_of_contents, colorgene,
                     cellgenes, list_of_names, list_of_dates):
    # data = None
    # filename = None
    # y_axis = None
    # global_type = None
    pond_length = 6
    index_list = []
    if type(index_selection) == list:
        index_list = index_selection
    else:
        index_list.append(index_selection)
    index_len = len(index_list)
    res_data = []
    if index_len is not None:
        for cur_index in index_list:
            if data_selection is not None and form_selection == 1:
                filename = df_data_file_list[data_selection]
                initial_rows = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                           header=None, nrows=pond_length)  # Adjust the number of rows as needed
                global_type = initial_rows[0][0].split('=')[1].replace(" ", "")
                df_col = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                     index_col=0,
                                     skiprows=pond_length, usecols=[0])
                lst = [x for x in df_col.index[2:] if str(x) != 'nan']

                # data = raw_data[[raw_data.columns[1], y_axis, raw_data.columns[2],raw_data.columns[0], colorgene]]
                if color_selection == 0 and colorgene is not None:
                    # load data from 2 genes
                    used_gene_lst = [6, 7, 8, lst.index(index_selection) + 9,
                                     lst.index(colorgene) + 9]  # position shifting
                    raw_data = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                           index_col=0,
                                           skiprows=lambda x: x not in used_gene_lst)

                    # firstrow as new header
                    y_axis = raw_data.index[2] if cur_index is None else cur_index

                    data = pd.DataFrame(
                        {raw_data.index[0]: raw_data.loc[raw_data.index[0]], y_axis: raw_data.loc[y_axis],
                         colorgene: raw_data.loc[colorgene],
                         raw_data.index[2]: raw_data.loc[raw_data.index[2]],
                         raw_data.index[1]: raw_data.loc[raw_data.index[1]],
                         })
                    # put the barcode back to the first column
                    # data.insert(0, 'Barcode', data.index)
                    data['Barcode'] = data.index
                    data = data.reset_index(drop=True)
                    # res_data.append(data.to_json())
                    # return [data.to_json(), filename, y_axis, global_type]
                else:
                    if isinstance(cellgenes, str):
                        cellgenes = [cellgenes]  # Convert string to list for uniform processing

                    cellgenes_indexes = [lst.index(item) + 9 if item in lst else None for item in cellgenes]
                    # load data from 2 genes
                    used_gene_lst = [6, 7, 8, lst.index(index_selection) + 9,
                                     lst.index(colorgene) + 9]  # position shifting
                    used_gene_lst = used_gene_lst + cellgenes_indexes
                    raw_data = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                           index_col=0,
                                           skiprows=lambda x: x not in used_gene_lst)

                    # firstrow as new header
                    y_axis = raw_data.index[2] if cur_index is None else cur_index

                    # Create the new DataFrame
                    data = pd.DataFrame({
                        raw_data.index[0]: raw_data.loc[raw_data.index[0]],
                        y_axis: raw_data.loc[y_axis],
                        **{gene: raw_data.loc[gene] for gene in cellgenes},
                        raw_data.index[2]: raw_data.loc[raw_data.index[2]],
                        raw_data.index[1]: raw_data.loc[raw_data.index[1]],
                    })
                    data['Barcode'] = data.index
                    data = data.reset_index(drop=True)
            elif list_of_contents is not None and colorgene is not None and form_selection == 0:
                filename = list_of_names[0]
                contents = parse_contents(list_of_contents[0], list_of_names, list_of_dates)
                data_dicts = contents[0]
                global_type = contents[1]
                x_axis = list(data_dicts.keys())[1]
                y_axis = list(data_dicts.keys())[3] if cur_index is None else cur_index
                datapoints_x = [float(item) for item in dict2List(data_dicts, x_axis)]
                datapoints_y = [float(item) for item in dict2List(data_dicts, y_axis)]
                datapoints_colorgene = [float(item) for item in dict2List(data_dicts, colorgene)]
                data = pd.DataFrame({x_axis: datapoints_x, y_axis: datapoints_y, colorgene: datapoints_colorgene})
                data['label'] = dict2List(data_dicts, 'label')
                data['Barcode'] = dict2List(data_dicts, 'Barcode')

                lst = list(data_dicts.keys())[3:]

            res_data.append(data.to_json())
        # return [res_data.to_json(), filename, y_axis, global_type]
        return [res_data, filename, y_axis, global_type, cellgenes, raw_data.to_json(), lst]


@app.callback(
    Output('memory-output', 'data'),
    [Input('threshold_YH', 'value'), Input('threshold_YL', 'value'),
     Input('threshold_X', 'value'), Input('memory-rawdata', 'data')
     ])
def produce_core_data(threshold_YH, threshold_YL, threshold_X, df_json):
    if df_json is not None and threshold_YH is not None and threshold_YL is not None and threshold_X is not None:
        data_list = df_json[0]
        file_type = df_json[3]
        filename = df_json[1]
        cellgenes = df_json[4]
        # color_axis = data.columns[2]
        # label = data['label']
        if file_type == 'AD':
            sub_name = ['HomeMG', 'DAM1', 'DAM2']
        elif file_type == 'AC':
            sub_name = ['SZ', 'MZ', 'DZ']

        res_data = []
        # display table for first graph only
        temp_index = 0
        for cur_data_list in data_list:
            raw_data = pd.read_json(cur_data_list)
            x_axis = raw_data.columns[0]
            y_axis = raw_data.columns[1]
            data, df_data_Final = \
                calculate_tables(x_axis, y_axis, raw_data, threshold_YL, threshold_YH, temp_index, sub_name)
        res_data.append(data.to_json())
        temp_index += 1

        if len(data.columns) > 5:
            raw_data = pd.read_json(data_list[0])
            color_axis = raw_data.columns[2]
            data, df_data_color_Final = calculate_tables(x_axis, color_axis, raw_data, threshold_YL, threshold_YH, -1, sub_name)
            return [res_data, df_data_Final.to_json(), df_data_color_Final.to_json(), cellgenes,
                    threshold_YH, threshold_YL, threshold_X, file_type, filename]
        else:
            return [res_data, df_data_Final.to_json(),
                    y_axis, cellgenes, threshold_YH, threshold_YL, threshold_X, file_type, filename]


@app.callback(
    Output('memory-visulize-output', 'data'),
    [Input('memory-output', 'data'), Input('color_selection', 'value') , Input('region_selection', 'value'), ])
def produce_visualize_data(df_json, color_selection, region_selection):
    if df_json is not None:
        data_list = df_json[0]
        # df_subset_temp = pd.read_json(data_list[0])
        res_data = []
        for cur_data in data_list:
            df_subset_temp = pd.read_json(cur_data)
            # df_subset_temp.iloc[:, 1]
            file_type = df_json[-2]
            file_name = df_json[-1]
            # flip the x and y axis
            threshold_YH = float(df_json[-5])
            threshold_YL = float(df_json[-4])
            threshold_X = float(df_json[-3])

            x_axis = df_subset_temp.columns[1]
            y_axis = df_subset_temp.columns[0]
            if file_type == 'AC':
                y_axis_name = '|                                        Deep-Zone             Mid-Zone          Sup-Zone'
            elif file_type == 'AD':
                y_axis_name = 'DAM-Stage 2                     DAM-Stage 1                   Homeostatic MG'

            # color_axis
            if df_subset_temp.columns[2] != 'label':
                color_axis = df_subset_temp.columns[2]
                df = pd.DataFrame(list(zip(df_subset_temp['Barcode'], df_subset_temp[x_axis], df_subset_temp[y_axis],
                                           df_subset_temp['label'], df_subset_temp[color_axis])),
                                  columns=['Barcode', x_axis, y_axis_name, 'label', color_axis])
                if color_selection == 1:
                    color_axis = df_json[-6]
                    x_mean = average_exclude_min(df_subset_temp[x_axis])
                    color_means = {col: average_exclude_min(df_subset_temp[col]) for col in color_axis}
                    df_subset_temp.reset_index(drop=True, inplace=True)
                    if region_selection == 0:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if min(df_subset_temp[x_axis]) < row[x_axis] < x_mean and all(
                                row[col] > color_means[col] for col in color_axis) else 'A', axis=1
                        )
                    elif region_selection == 1:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if row[x_axis] > x_mean and all(
                                row[col] > color_means[col] for col in color_axis) else 'A', axis=1
                        )
                    else:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if min(df_subset_temp[x_axis]) == row[x_axis] and all(
                                row[col] > color_means[col] for col in color_axis) else 'A', axis=1
                        )

            else:
                df = pd.DataFrame(list(zip(df_subset_temp['Barcode'], df_subset_temp[x_axis], df_subset_temp[y_axis],
                                           df_subset_temp['label'])),
                                  columns=['Barcode', x_axis, y_axis_name, 'label'])

                if color_selection == 1:
                    color_axis = df_json[-6]
                    x_mean = average_exclude_min(df_subset_temp[x_axis])
                    color_means = {col: average_exclude_min(df_subset_temp[col]) for col in color_axis}
                    df_subset_temp.reset_index(drop=True, inplace=True)
                    if region_selection == 0:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if min(df_subset_temp[x_axis]) < row[x_axis] < x_mean else 'A', axis=1
                        )
                    elif region_selection == 1:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if row[x_axis] > x_mean else 'A', axis=1
                        )
                    else:
                        df["cell_label"] = df_subset_temp.apply(
                            lambda row: 'P' if row[x_axis] ==  min(df_subset_temp[x_axis])  else 'A', axis=1
                        )


            if threshold_YH is not None and threshold_YL is not None:
                df.loc[df[y_axis_name] >= threshold_YH, 'label'] = '2'
                df.loc[df[y_axis_name] <= threshold_YL, 'label'] = '0'
                df.loc[(df[y_axis_name] < threshold_YH) & (df[y_axis_name] > threshold_YL), 'label'] = '1'
            res_data.append(df.to_json())
        return [res_data, threshold_X, file_name]


# @app.callback(
#     [Output('dropdown', 'options'), Output('dropdown', 'value')],
#     [Input('memory-rawdata', 'data')]
# )
# def update_date_dropdown(raw_data):
#     if raw_data is not None:
#         lst = raw_data[4]
#
#         return [[{'label': s[0], 'value': s[0]} for s in zip(lst, lst)], lst[0]]
#     else:
#         return [[{'label': s[0], 'value': str(s[0] + 2)}
#                 for s in zip(index_list, index_list)], ' ']
#
#
#
# @app.callback(
#     [Output('dropdown_gene2', 'options'), Output('dropdown_gene2', 'value')],
#     [Input('memory-rawdata', 'data')]
# )
# def update_date_dropdown_gene2(raw_data):
#     if raw_data is not None:
#         lst = raw_data[4]
#
#         return [[{'label': s[0], 'value': s[0]} for s in zip(lst, lst)], lst[0]]
#     else:
#         return [[{'label': s[0], 'value': str(s[0] + 2)}
#                 for s in zip(index_list, index_list)], ' ']

@app.callback(
    [Output('dropdown', 'options'), Output('dropdown', 'value')],
    [Input('dropdown', 'value'), Input('memory-rawdata', 'data'), ]
)
def update_data_dropdown(index_selection, df_json):
    lst = df_json[6]
    if index_selection is not None:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], index_selection]
    else:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], lst[0]]


@app.callback(
    [Output('dropdown_gene2', 'options'), Output('dropdown_gene2', 'value')],
    [Input('dropdown_gene2', 'value'), Input('memory-rawdata', 'data')]
)
def update_data_dropdown(colorgene, df_json):
    lst = df_json[6]
    if colorgene is not None:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], colorgene]
    else:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], lst[0]]


@app.callback(
    [Output('dropdown_geneset', 'options'), Output('dropdown_geneset', 'value')],
    [Input('dropdown_geneset', 'value'), Input('memory-rawdata', 'data'), ]
)
def update_data_dropdown(cellgenes, df_json):
    lst = df_json[6]
    if cellgenes is not None:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], cellgenes]
    else:
        return [[{'label': s[0], 'value': s[1]} for s in zip(lst, lst)], lst[0]]


@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def set_display_children(selected_value):
    return 'Selection: {}'.format(selected_value)


@app.callback(
    Output('display-selected-values-2', 'children'),
    [Input('dropdown_gene2', 'value'), Input('dropdown_geneset', 'value'), Input('color_selection', 'value')])
def set_display_children(selected_value, cellgenes, color_selection):
    if color_selection == 0:
        return 'Gradient Color: {}'.format(selected_value)
    else:
        return 'Cell Selection: {}'.format(cellgenes)


@app.callback(
    dash.dependencies.Output('display-selected-values-3', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def set_display_children(selected_value):
    return 'Distribution table: {}'.format(selected_value)



@app.callback(
    Output('display-selected-stat', 'children'),
    [Input('color_selection', 'value')])
def set_display_children(color_selection):
    if color_selection == 1:
        return 'Perform Statistical Test(Find Candidates):'
    else:
        return {}


@app.callback(
    Output('btn_stat_run', 'style'),
    [Input('color_selection', 'value'), ])
def update_btn_stat_run(form_selection):
    if form_selection == 1:
        return {'font-size': '25px', 'display': 'inline-block',
                'padding-right': '1vw'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('region_selection', 'style'),
    [Input('color_selection', 'value'), ])
def update_btn_stat_run(form_selection):
    if form_selection == 1:
        return { 'display': 'inline-block',}
    else:
        return {'display': 'none'}


@app.callback(
    Output('display-selected-values-3-1', 'children'),
    [Input('color_selection', 'value'), Input('stat_test_selection', 'value'), Input("btn_stat_run", "n_clicks"),
     Input('dropdown_geneset', 'value'), Input('dropdown', 'value'), Input('region_selection', 'value')])
def set_display_children(color_selection, stat_test_selection, n_clicks, cellgenes, selected_value, region_selection):
    if color_selection == 1:
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'btn_stat_run' in changed_id:
            # return 'Spearman Test Intra Selected Cells'
            if region_selection == 0:
                return 'Spearman Test Selected Cells ({}, Low {} High)'.format(selected_value, cellgenes) if selected_value != cellgenes else 'Spearman Test Selected Cells ({}, Low {} Low)'.format(selected_value, cellgenes)
            elif region_selection == 1:
                return 'Spearman Test Selected Cells ({}, High {} High)'.format(selected_value, cellgenes) if selected_value != cellgenes else 'Spearman Test Selected Cells ({}, High {} High)'.format(selected_value, cellgenes)
            else:
                return 'Spearman Test Selected Cells ({}, Absent {} High)'.format(selected_value, cellgenes) if selected_value != cellgenes else 'Spearman Test Selected Cells ({}, Absent {} Absent)'.format(selected_value, cellgenes)
        else:
            return {}
    else:
        return {}

@app.callback(
    Output('display-selected-values-4', 'children'),
    [Input('dropdown', 'value'), Input('dropdown_gene2', 'value'), Input('color_selection', 'value')])
def set_display_children(select_gene, gradient_value, color_selection):
    if color_selection == 0 and select_gene != gradient_value:
        return 'Distribution table: {}'.format(gradient_value)
    else:
        return {}



# @app.callback(
#     Output('text-output_pvalue', 'children'),
#     [Input('threshold_YH', 'value'), Input('threshold_YL', 'value'), Input('memory-output', 'data')])
# def update_output(threshold_YH, threshold_YL, df_json):
#     if df_json is not None and threshold_YH and threshold_YL:
#         df_subset_temp = pd.read_json(df_json[0])
#         # df_subset_temp.iloc[:, 1]
#         # flip the x and y axis
#         threshold_YH = float(threshold_YH)
#         threshold_YL = float(threshold_YL)
#
#         x_axis = df_subset_temp.columns[1]
#         if threshold_YH is not None and threshold_YL is not None:
#             df_left = df_subset_temp.loc[df_subset_temp[x_axis] <= threshold_YH]
#             df_right = df_subset_temp.loc[df_subset_temp[x_axis] >= threshold_YL]
#             from scipy import stats
#             _s, pvalue = stats.mannwhitneyu(df_left[df_subset_temp.columns[0]], df_right[df_subset_temp.columns[0]])
#             return "p value is: " + str(pvalue)
#         else:
#             return ""
#
#     return ""


@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"), Input('g1', 'selectedData'), Input('data_selection', 'value'),],
    prevent_initial_call=True,
)
def download(n_clicks, selectedData, data_selection):
    ## insert non-transosed files like (727)_MG_cell_group_stage2.csv
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn_csv' in changed_id:

        print("start")
        if selectedData is not None and data_selection is not None:
            df = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                   index_col=0, header=0,
                                   skiprows=6)
            sampleIDs = []
            # df = pd.read_json(df_json[0][0])
            for datapoint in selectedData['points']:
                # df_print = data_TSNE[data_TSNE['gene'].isin(sampleIDs)]
                sampleIDs.append(datapoint['customdata'][0])
            df_res = df[sampleIDs]
            print("finish getting the data")
            return dcc.send_data_frame(df_res.to_csv, "selecteddf.csv")
    else:
        return no_update


@app.callback(
    Output("download-dataframe-csv_2", "data"),
    [Input("btn_csv_2", "n_clicks"), Input('memory-visulize-output', 'data'), Input('data_selection', 'value')],
    prevent_initial_call=True,
)
def download(n_clicks, df_json, data_selection):
    ## insert non-transosed files like (727)_MG_cell_group_stage2.csv
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn_csv_2' in changed_id:

        print("download_2")
        if df_json is not None and data_selection is not None:
            df = pd.read_csv(input_csv_file_directory + df_data_file_list[data_selection], delimiter=',',
                                   index_col=0, header=0,
                                   skiprows=6)
            # data contains 2 nan lines and get the first data matrix
            df_cellselection = pd.read_json(df_json[0][0])
            df_res = df[df_cellselection[df_cellselection['cell_label'] == 'P']['Barcode']]
            print("finish getting the data")
            return dcc.send_data_frame(df_res.to_csv, "selecteddf_cell_selection.csv")
    else:
        return no_update


@app.callback(
    Output('display-selected-values-3-1', 'style'),
    [Input('color_selection', 'value'), ])
def update_localdata_panel(form_selection):
    if form_selection == 1:
        return {'font-size': '25px', 'display': 'inline-block','padding-right': '1vw', 'margin-right': 20, }
    else:
        return {'display': 'none'}


@app.callback(
    Output('stat_test_selection', 'style'),
    [Input('color_selection', 'value'), ])
def update_localdata_panel(form_selection):
    if form_selection == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('g1', 'style'),
    [Input('memory-rawdata', 'data'), Input('upload-data-1', 'contents'), State('upload-data-1', 'filename'),
     State('upload-data-1', 'last_modified'), ])
def update_graph1(df_json, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None and df_json is None:
        return {'display': 'none'}
    else:
        return {'display': 'inline-block'}


@app.callback(
    Output('viz_panel', 'style'),
    [Input('memory-rawdata', 'data'), Input('upload-data-1', 'contents'), State('upload-data-1', 'filename'),
     State('upload-data-1', 'last_modified'), ])
def update_viz_panel(df_json, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None or df_json is not None:
        return {'display': 'block', 'width': '95%', }
    else:
        return {'display': 'none'}


# @app.callback(
#     Output('g2', 'style'),
#     [Input('upload-data-1', 'contents'), State('upload-data-1', 'filename'), State('upload-data-1', 'last_modified'), ])
# def update_graph2(list_of_contents, list_of_names, list_of_dates):
#     # if list_of_contents is None:
#     #     return {'display': 'none'}
#     # else:
#     #     return {'display': 'inline-block'}
#     return {'display': 'none'}

# @app.callback(
#     Output('g0', 'figure'),
#     [Input('memory-rawdata', 'data')])
# def update_graph0(df_json):
#     fig = {}
#     if df_json is not None:
#         filename = df_json[1]
#         df_subset_temp = pd.DataFrame(pd.read_json(df_json[0]))
#         x_axis = df_subset_temp.columns[1]
#         y_axis = df_subset_temp.columns[0]
#         x = df_subset_temp[x_axis].astype(float)
#         y = df_subset_temp[y_axis].astype(float)
#         colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)', (1, 1, 0.2), (0.98, 0.98, 0.98)]
#
#         fig = ff.create_2d_density(
#             x, y,
#             colorscale=colorscale,
#             hist_color='rgb(255, 237, 222)', point_size=4, width=900, height= 1500
#         )
#     return fig

#
@app.callback(
    Output('g1', 'figure'),
    [Input('color_selection', 'value'), Input('dots_size', 'value'), Input('g_cluster', 'selectedData'),
     Input('threshold_YH', 'value'), Input('threshold_YL', 'value'),
     Input('threshold_X', 'value'), Input('threshold_X_DO', 'value'), Input('memory-visulize-output', 'data'),
     Input('upload-data-selection', 'contents'), State('upload-data-selection', 'filename'),
     State('upload-data-selection', 'last_modified')])
def update_graph1(color_selection, dots_size, g_cluster_selectedData, threshold_YH, threshold_YL, threshold_X,
                  threshold_X_DO, df_json, list_of_contents, list_of_names, list_of_dates):
    fig = {}
    if df_json is not None and threshold_YH is not None and threshold_YL is not None and threshold_X is not None and threshold_X_DO is not None:
        data_list = df_json[0]
        # data contains 2 nan lines and get the first data matrix
        df = pd.read_json(data_list[0])[:-2]
        # df_subset_temp.iloc[:, 1]
        file_name = df_json[-1]
        # file_type = df_json[-2]
        x_axis = df.columns[1]
        y_axis = df.columns[2]
        # mean_x_axis = df_json[-2]
        min_x_axis = min(df[x_axis])
        # calculate the avergae of z score data without zeros
        filter_list = list(filter(lambda a: a != min_x_axis, list(df[x_axis])))
        mean_x_axis = Average(filter_list) if len(filter_list) != 0 else 0
        # check if color is not correct
        df['label'] = df['label'].astype(str)
        color_axis = df.columns[-1]
        max_x = max(df[x_axis])
        max_y = max(df[y_axis])
        min_x = min(df[x_axis])
        min_y = min(df[y_axis])
        total_cells = len(df)
        DO_cells = len(filter_list)
        NDO_cells = len(df) - len(filter_list)
        cellNumber_text = 'Total # of cells: {}; Non-DO cells: {}; DO cells: {}'.format(total_cells, NDO_cells,
                                                                                        DO_cells)
        if color_axis == 'label':
            if list_of_contents is not None:
                df_subset_temp = [
                    parse_contents_df(c, n, d) for c, n, d in
                    zip(list_of_contents, list_of_names, list_of_dates)]
                # df_subset_temp = df_subset_temp[0].parse(0)

                df_subset_temp = df_subset_temp[0]
                list_selected = list(df_subset_temp['Barcode'])
                df["isSelected"] = np.where(df['Barcode'].isin(list_selected), "Y", "F")
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 color='isSelected',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 color_discrete_map={
                                     "Y": "red",
                                     "F": "#add8e6", },
                                 )

            elif g_cluster_selectedData is not None:
                sampleIDs = []
                for datapoint in g_cluster_selectedData['points']:
                    # df_print = data_TSNE[data_TSNE['gene'].isin(sampleIDs)]
                    sampleIDs.append(datapoint['customdata'][0])
                df["isSelected"] = np.where(df['Barcode'].isin(sampleIDs), "Y", "F")
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 color='isSelected',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 color_discrete_map={
                                     "Y": "red",
                                     "F": "#add8e6", },
                                 )
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 color='label',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 # color_discrete_map={'Home': '#faac01', 'Dam-like': '#c805f7', 'Trans': '#00c6ff'},
                                 color_discrete_map={'0': 'blue', '2': 'red', '1': 'grey'},
                                 )
        else:
            if color_selection == 0:
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 # color='label',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 # color_discrete_map={'2': 'blue', '0': 'red', '1': 'grey'},
                                 color=color_axis,
                                 )
            else:
                cellNumber_text = 'Total # of cells: {}; Selected cells (red): {}'.format(len(df), len(
                    df[df['cell_label'] == 'P']))
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 color='cell_label',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 color_discrete_map={
                                     "P": "red",
                                     "A": "#add8e6", },
                                 )
        fig.add_trace(go.Scatter(
            y=[max_y* 1.1],
            x=[min_x],
            # y=[max_y],
            mode="text",
            name="Text",
            text=[cellNumber_text],
            textposition="top right",
            textfont=dict(
                # family="sans serif",
                size=18,
                color="black"
            )
        ))
        # PC_r = cal_pearsonr(df['x_data'], df['y_data'])
        fig.update_traces(marker=dict(size=int(dots_size)),
                          selector=dict(mode='markers'))

        fig.update_xaxes(tickprefix="<b>", ticksuffix="</b><br>",
                         title_text=x_axis)
        fig.update_yaxes(tickprefix="<b>", ticksuffix="</b><br>",
                         title_text=y_axis)
        fig.update_layout(showlegend=False, dragmode='select')
        fig.add_shape(type="line",
                      x0=min_x, y0=threshold_YH, x1=max_x, y1=threshold_YH,
                      line=dict(color="Black", width=2)
                      )
        fig.add_shape(type="line",
                      x0=min_x, y0=threshold_YL, x1=max_x, y1=threshold_YL,
                      line=dict(color="Black", width=2)
                      )
        # vertical line for threshold_X with DO
        fig.add_shape(type="line",
                      x0=0, y0=min_y, x1=0, y1=max_y,
                      line=dict(color="Black", width=2)
                      )
        # vertical line for threshold_X_DO without DO
        fig.add_shape(type="line",
                      x0=mean_x_axis, y0=min_y, x1=mean_x_axis, y1=max_y,
                      line=dict(color="Black", width=2)
                      )
        MWDO_text = "MWDO=" + str(round(threshold_X_DO, 2))
        MWODO_text = "MWODO=" + str(round(threshold_X, 2))

        fig.add_trace(go.Scatter(
            x=[0],
            y=[max_y],
            mode="text",
            name="Text",
            text=[MWDO_text],
            textposition="top right",
            textfont=dict(
                # family="sans serif",
                size=16,
                # color="crimson"
                color="black"
            )
        ))

        fig.add_trace(go.Scatter(
            # x=[mean_x_axis-0.1],
            y=[max_y * 0.9],
            x=[mean_x_axis],
            # y=[max_y],
            mode="text",
            name="Text",
            text=[MWODO_text],
            textposition="top right",
            textfont=dict(
                # family="sans serif",
                size=16,
                color="black"
            )
        ))

        # fig.update_layout(dragmode='select')
        fig.update_layout({
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'width': 750, 'height': 900,
        })
        fig.update_xaxes(
            title_font={"size": 28},
            title_standoff=25)
    return fig


@app.callback(
    Output('g2', 'figure'),
    [Input('memory-visulize-output', 'data'),
     Input('upload-data-selection', 'contents'), State('upload-data-selection', 'filename'),
     State('upload-data-selection', 'last_modified')])
def update_graph2(df_json, list_of_contents, list_of_names, list_of_dates):
    fig = {}
    if df_json is not None:
        data_list = df_json[0]
        if len(data_list) != 1:
            # data contains 2 nan lines and get the first data matrix
            df = pd.read_json(data_list[1])[:-2]
            # df_subset_temp.iloc[:, 1]
            file_name = df_json[-1]
            file_type = df_json[-2]
            x_axis = df.columns[1]
            y_axis = df.columns[2]
            mean_x_axis = df_json[-2]
            # check if color is not correct
            df['label'] = df['label'].astype(str)
            color_axis = df.columns[-1]
            if color_axis == 'label':
                if list_of_contents is not None:
                    df_subset_temp = [
                        parse_contents_df(c, n, d) for c, n, d in
                        zip(list_of_contents, list_of_names, list_of_dates)]
                    # df_subset_temp = df_subset_temp[0].parse(0)

                    df_subset_temp = df_subset_temp[0]
                    list_selected = list(df_subset_temp['Barcode'])
                    df["isSelected"] = np.where(df['Barcode'].isin(list_selected), "Y", "F")
                    fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                     title=file_name,
                                     color='isSelected',
                                     # symbol = "label",
                                     hover_data={x_axis: True,  # remove species from hover data
                                                 y_axis: True,  # add other column, default formatting
                                                 'Barcode': True},
                                     color_discrete_map={
                                         "Y": "red",
                                         "F": "#add8e6", },
                                     )
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                     title=file_name,
                                     color='label',
                                     # symbol = "label",
                                     hover_data={x_axis: True,  # remove species from hover data
                                                 y_axis: True,  # add other column, default formatting
                                                 'Barcode': True},
                                     # color_discrete_map={'Home': '#faac01', 'Dam-like': '#c805f7', 'Trans': '#00c6ff'},
                                     color_discrete_map={'Home': 'blue', 'Dam-like': 'red', 'Trans': 'grey'},
                                     )
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 # color='label',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 # color_discrete_map={'2': 'blue', '0': 'red', '1': 'grey'},
                                 color=color_axis,
                                 )
            fig.update_layout({
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'width': 750, 'height': 800,
            })
    return fig


@app.callback(
    Output('g3', 'figure'),
    [Input('memory-visulize-output', 'data'),
     Input('upload-data-selection', 'contents'), State('upload-data-selection', 'filename'),
     State('upload-data-selection', 'last_modified')])
def update_graph2(df_json, list_of_contents, list_of_names, list_of_dates):
    fig = {}
    if df_json is not None:
        data_list = df_json[0]
        if len(data_list) != 1:
            # data contains 2 nan lines and get the first data matrix
            df = pd.read_json(data_list[2])[:-2]
            # df_subset_temp.iloc[:, 1]
            file_name = df_json[-1]
            file_type = df_json[-2]
            x_axis = df.columns[1]
            y_axis = df.columns[2]
            mean_x_axis = df_json[-2]
            # check if color is not correct
            df['label'] = df['label'].astype(str)
            color_axis = df.columns[-1]
            if color_axis == 'label':
                if list_of_contents is not None:
                    df_subset_temp = [
                        parse_contents_df(c, n, d) for c, n, d in
                        zip(list_of_contents, list_of_names, list_of_dates)]
                    # df_subset_temp = df_subset_temp[0].parse(0)

                    df_subset_temp = df_subset_temp[0]
                    list_selected = list(df_subset_temp['Barcode'])
                    df["isSelected"] = np.where(df['Barcode'].isin(list_selected), "Y", "F")
                    fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                     title=file_name,
                                     color='isSelected',
                                     # symbol = "label",
                                     hover_data={x_axis: True,  # remove species from hover data
                                                 y_axis: True,  # add other column, default formatting
                                                 'Barcode': True},
                                     color_discrete_map={
                                         "Y": "red",
                                         "F": "#add8e6", },
                                     )
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                     title=file_name,
                                     color='label',
                                     # symbol = "label",
                                     hover_data={x_axis: True,  # remove species from hover data
                                                 y_axis: True,  # add other column, default formatting
                                                 'Barcode': True},
                                     # color_discrete_map={'Home': 'blue', 'Dam-like': 'red', 'Trans': 'grey'},
                                     color_discrete_map={'Home': 'blue', 'Dam-like': 'red', 'Trans': 'grey'},
                                     )
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis,  # flip the x and y axis
                                 title=file_name,
                                 # color='label',
                                 # symbol = "label",
                                 hover_data={x_axis: True,  # remove species from hover data
                                             y_axis: True,  # add other column, default formatting
                                             'Barcode': True},
                                 # color_discrete_map={'2': 'blue', '0': 'red', '1': 'grey'},
                                 color=color_axis,
                                 )
            fig.update_layout({
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'width': 750, 'height': 800,
            })
    return fig


@app.callback(
    Output('g_cluster', 'figure'),
    [Input('g1', 'selectedData'), Input('upload-umap-data', 'contents'), Input('upload-data-selection', 'contents'),
     State('upload-data-selection', 'filename'), State('upload-data-selection', 'last_modified'),
     State('upload-umap-data', 'filename'), State('upload-umap-data', 'last_modified')])
def update_graph_cluster(g1_selectedData, list_of_contents, list_of_contents_selection, list_of_names_seelction,
                         list_of_dates_selection, list_of_names, list_of_dates):
    fig = {}
    if list_of_contents is not None:
        df_subset_temp = [
            parse_contents_df(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        df = df_subset_temp[0]
        file_name = list_of_names[0]
        df['label'] = df['label'].astype(str)
        if list_of_contents_selection is not None:
            df_subset_temp = [
                parse_contents_df(c, n, d) for c, n, d in
                zip(list_of_contents_selection, list_of_names_seelction, list_of_dates_selection)]
            # df_subset_temp = df_subset_temp[0].parse(0)

            df_subset_temp = df_subset_temp[0]
            list_selected = list(df_subset_temp['Barcode'])
            df["isSelected"] = np.where(df['Barcode'].isin(list_selected), "Y", "F")
            fig = px.scatter(df, x=df.columns[1], y=df.columns[2],  # flip the x and y axis
                             title=file_name,
                             color='isSelected',
                             # symbol = "label",
                             hover_data={df.columns[1]: True,
                                         df.columns[2]: True,
                                         'Barcode': True},
                             color_discrete_map={
                                 "Y": "red",
                                 "F": "#add8e6", },
                             )
        elif g1_selectedData is not None:
            sampleIDs = []
            for datapoint in g1_selectedData['points']:
                # df_print = data_TSNE[data_TSNE['gene'].isin(sampleIDs)]
                sampleIDs.append(datapoint['customdata'][0])
            df["isSelected"] = np.where(df['Barcode'].isin(sampleIDs), "Y", "F")
            fig = px.scatter(df, x=df.columns[1], y=df.columns[2],
                             title=file_name,
                             color='isSelected',
                             hover_data={df.columns[1]: True,
                                         df.columns[2]: True,
                                         'Barcode': True},
                             )
        else:
            # fig = px.scatter(df, x='X', y='Y',  # flip the x and y axis
            #                  # title=file_name,
            #                  color='label',
            #                  # symbol = "label",
            #                  hover_data={'X': True,  # remove species from hover data
            #                              'Y': True,  # add other column, default formatting
            #                              'Barcode': True},
            #                  # color_discrete_map={'Home': '#faac01', 'Dam-like': '#c805f7', 'Trans': '#00c6ff'},
            #                  )
            fig = px.scatter(df, x=df.columns[1], y=df.columns[2],
                             title=file_name,
                             color="label",
                             hover_data={df.columns[1]: True,
                                         df.columns[2]: True,
                                         'Barcode': True},
                             )
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'width': 750, 'height': 800,
        })
        fig.update_layout(dragmode='select')
    return fig


# @app.callback(
#     Output('g_histo', 'figure'),
#     [Input('threshold_YH', 'value'), Input('threshold_YL', 'value'),
#      Input('threshold_X', 'value'),
#      Input('g2', 'selectedData'), Input('memory-visulize-output', 'data')])
# def update_graph_histogram(threshold_YH, threshold_YL, threshold_X, selectedData, df_json):
#     fig = {}
#     if df_json is not None and threshold_YH is not None and threshold_YL is not None and threshold_X is not None:
#         df = pd.read_json(df_json[0])
#         # we flipped the data
#         y_data = df.columns[1]
#         df['label'] = df['label'].astype(int).astype(str)
#         fig = ff.create_distplot(
#             [df.loc[df['label'] == '0'][y_data].astype(float), df.loc[df['label'] == '2'][y_data].astype(float)],
#             ['0', '2'],
#             bin_size=.1, colors=['rgb(255, 0, 0)', 'rgb(0, 0, 255)'],
#             show_hist=False,
#             )
#         fig.update_layout({
#             'plot_bgcolor': 'rgba(0,0,0,0)',
#             'paper_bgcolor': 'rgba(0,0,0,0)',
#
#         })
#     return fig


# change these values
if __name__ == '__main__':
    app.run_server(port=8081, debug=True,
                   # host='0.0.0.0',
                   )
