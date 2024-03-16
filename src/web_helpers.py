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

