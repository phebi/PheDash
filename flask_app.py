# A very simple Flask Hello World app for you to get started with...

# from flask import Flask

# flask_app = Flask(__name__)

# @flask_app.route('/')
# def index():
#     return 'Hello Flask app'

# with dash
import io
import base64
import json
import plotly.graph_objects as go
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import numpy as np
import pandas as pd

import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.config.suppress_callback_exceptions = True
index_page = html.Div([
    html.Title('Phebi数据分析'),
    html.Header(html.Meta(name="referrer", content="no-referrer")),
    html.Div(
        id='row_1',
        style={'display': 'flex'},
        children=[
            html.Div(id='上传数据',
                     className='left_bar',
                     children=[
                         html.Div(id='数据上传区域', className='columns',
                                  children=[
                                      html.H6('数据源'),
                                      # html.Div(
                                      #     className='twelve columns',
                                      #     children=[
                                      #         html.Div(
                                      #             children=[
                                      #                 '随机码：'
                                      #             ]),
                                      #         html.Div(id='id_store_check_res'),
                                      #         html.Div(id='id_store_str'),
                                      #     ]),
                                      html.Div(
                                          id='all_file_store',
                                          hidden=False,
                                          className='twelve columns',
                                          children=[
                                              dcc.Upload(
                                                  id='stock_file',
                                                  children=html.Div([
                                                      html.A('选择库存文件')]),
                                                  className='my_upload',
                                                  multiple=False),
                                              dcc.Upload(
                                                  id='daily_file',
                                                  children=html.Div([
                                                      html.A('选择日常数据文件')]),
                                                  className='my_upload',
                                                  multiple=False),
                                              dcc.Upload(
                                                  id='ad_file',
                                                  children=html.Div([
                                                      html.A('选择广告数据文件')]),
                                                  className='my_upload',
                                                  multiple=False
                                              ),
                                              dcc.Upload(
                                                  id='property_file',
                                                  children=html.Div([
                                                      html.A('选择产品属性文件')]),
                                                  className='my_upload',
                                                  multiple=False),
                                          ]
                                      ),
                                  ]),
                         html.Div(id='数据存储区域',
                                  children=[
                                      dcc.Store(id='daily_file_store', storage_type='session'),
                                      dcc.Store(id='daily_filename_store', storage_type='session'),
                                      dcc.Store(id='ad_file_store', storage_type='session'),
                                      dcc.Store(id='ad_filename_store', storage_type='session'),
                                      dcc.Store(id='output_store', storage_type='session'),
                                      html.Tbody([
                                          html.Th('文件内容'),
                                          html.Th('文件名'),
                                          html.Tr([
                                              html.Td(id='daily_file_td'),
                                              html.Td(id='daily_filename_td'),
                                          ]),
                                          html.Tr([
                                              html.Td(id='ad_file_td'),
                                              html.Td(id='ad_filename_td'),
                                          ])
                                      ],
                                ),

                                  ]),
                     ]),
            html.Div(id='聚合数据展示区域',
                     className='top_bar',
                     children=[
                         html.Div(id='daily_graph_ploy'),
                         html.H5('聚合数据区域'),
                         html.P('数据汇总、完成度等等')
                     ]),
        ]),
    html.Div(
        id='row_2',
        className='content_page',
        children=[
            html.Div(
                className='columns',
                children=[
                    html.Div(
                        draggable='true',
                        id='ASIN选择',
                        className='columns',
                        style={'position': 'fixed', 'left': '2.5%', 'top': '75%', 'width': '400px'},
                        children=[
                            html.Div(
                                className='four columns',
                                children=[
                                    dcc.Dropdown(id='select_cate_one',
                                                 style={'width': '120px'},
                                                 placeholder="一级类目", ),
                                    dcc.Dropdown(id='select_cate_two',
                                                 style={'width': '120px'},
                                                 placeholder="二级类目", ),
                                    dcc.Dropdown(id='select_fsku',
                                                 style={'width': '120px'},
                                                 placeholder="父sku", ),
                                    dcc.Dropdown(id='select_sku',
                                                 style={'width': '120px'},
                                                 placeholder="sku", ),
                                ],
                            ),
                            html.Div(
                                className='eight columns',
                                children=[
                                    dcc.Dropdown(id='select_ad_comb',
                                                 style={'width': '175px'},
                                                 placeholder='广告组合'),
                                    dcc.Dropdown(id='select_ad_action',
                                                 style={'width': '175px'},
                                                 placeholder="广告活动", ),
                                    dcc.Dropdown(id='select_ad_group',
                                                 style={'width': '175px'},
                                                 placeholder="广告组", ),
                                    dcc.Dropdown(id='select_ad_words',
                                                 style={'width': '175px'},
                                                 placeholder="广告投放", ),
                                ]
                            ),
                        ]),
                    html.Div(
                        id='pic_bar',
                        style={'position': 'fixed', 'left': '3%', 'top': '42%'},
                    ),
                    html.Div(
                        children=[
                            html.Div(id='asin_cate_one_fig'),
                            html.Div(id='asin_cate_two_fig'),
                            html.Div(id='asin_cate_fsku_fig')
                        ]
                    ),
                    html.Div(
                        id='父ASIN月度汇总',
                        children=[
                            html.Div(id='asin_sum_fig'),
                            html.Div(id='asin_time_fig'),
                            html.Div(id='sub_asin_sum_fig'),
                            html.Div(id='sub_asin_time_fig'),

                        ]),
                    html.Div(
                        id='广告组数据汇总',
                        children=[
                            html.Div(id='ad_comb_fig'),
                            html.Div(id='ad_action_sum_fig'),
                            html.Div(id='ad_group_sum_fig'),
                            html.Div(id='ad_keys_sum_fig'),
                            html.Div(id='ad_key_words_search')
                        ]),
                ]
            ),
        ]),
])

df_pro = pd.read_excel('产品属性表20200117.xlsx')


# 上传数据
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # 上传csv文件
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return df.to_json(), filename
        elif 'xls' in filename:
            # 上传xlsx文件
            df = pd.read_excel(io.BytesIO(decoded))
            return df.to_json(), filename
    except Exception as e:
        print(e)
        return None, None
# 上传日常运营数据文件


@app.callback([Output('daily_file_store', 'data'),
               Output('daily_filename_store', 'data')],
              [Input('daily_file', 'contents')],
              [State('daily_file', 'filename'),
               State('daily_file', 'last_modified'),
               State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def update_output(list_of_contents, list_of_names, list_of_dates, file, filename):
    if list_of_contents is not None:
        # children = [
        #     parse_contents(c, n, d) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        df_row, filename = parse_contents(list_of_contents, list_of_names, list_of_dates)

        # 解决Excel毫秒时间戳问题
        df = pd.read_json(df_row, convert_dates='date', date_unit='ms')
        # 数据预处理
        df_match = pd.merge(df, df_pro, left_on='sub_asin', right_on='ASIN', how='left')
        df_match['一级类目'].fillna('其他一级类目', inplace=True)
        df_match['二级类目'].fillna('其他二级类目', inplace=True)
        df_json = df_match.to_json()

        return df_json, filename

    else:
        return file, filename


# 上传广告数据文件
@app.callback([Output('ad_file_store', 'data'),
               Output('ad_filename_store', 'data')],
              [Input('ad_file', 'contents')],
              [State('ad_file', 'filename'),
               State('ad_file', 'last_modified'),
               State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def update_output(list_of_contents, list_of_names, list_of_dates, file, fname):
    if list_of_contents is not None:
        # children = [
        #     parse_contents(c, n, d) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        df_json, filename = parse_contents(list_of_contents, list_of_names, list_of_dates)

        # 解决毫秒时间戳问题
        df = pd.read_json(df_json, convert_dates='date', date_unit='ms')
        # df = pd.read_json(df_json)
        df['销量'] = df['7天总销售量(#)']
        df['销售额'] = df['7天总销售额(￥)']
        data_info = df[['广告组合名称', '广告活动名称', '广告组名称', '投放', '客户搜索词', '展现量', '点击量', '销量', '销售额', '花费']]
        return data_info.to_json(), filename
    else:
        return file, fname


# 数据表格提示
def get_td(mt, file_data, file_name):
    if not (mt and file_data and file_name):
        return 'file_data...', 'file_name...'
    else:
        return file_data[:10], file_name


@app.callback([Output('daily_file_td', 'children'),
               Output('daily_filename_td', 'children')],
              [Input('daily_file_store', 'modified_timestamp')],
              [State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def get_daily_td(mt, daily_file_data, daily_file_name, ):
    return get_td(mt, daily_file_data, daily_file_name)


@app.callback([Output('ad_file_td', 'children'),
               Output('ad_filename_td', 'children')],
              [Input('ad_file_store', 'modified_timestamp')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_ad_td(mt, ad_file_data, ad_file_name):
    return get_td(mt, ad_file_data, ad_file_name)


# 选择一级类目-下拉菜单
@app.callback(Output('select_cate_one', 'options'),
              [Input('daily_file_store', 'modified_timestamp')],
              [State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def get_cate_one(mt, file_data, filename):
    if not (mt and file_data and filename):
        return [{'label': 'none', 'value': 'none'}]
    else:
        if file_data:
            df = pd.DataFrame(json.loads(file_data))
            cate_list = df['一级类目'].unique()
            result = [{'label': i, 'value': i} for i in cate_list]
            return result


# 选择二级类目-菜单
@app.callback(Output('select_cate_two', 'options'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_cate_one', 'value')],
              [State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def get_cate_two(mt, cate_one, file_data, file_name):
    if not all([mt, cate_one, file_data, file_name]):
        return [{'label': 'none', 'value': 'none'}]
    else:
        if file_data:
            df = pd.DataFrame(json.loads(file_data))
            sub_asin_list = list(df[df['一级类目'] == cate_one]['二级类目'].unique())
            result = [{'label': i, 'value': i} for i in sub_asin_list]
            return result


# 选择-父SKU下拉菜单
@app.callback(Output('select_fsku', 'options'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_cate_one', 'value'),
               Input('select_cate_two', 'value')],
              [State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def get_fsku(mt, cate_one, cate_two, file_data, file_name):
    if not (mt and file_data and file_name):
        return [{'label': 'none', 'value': 'none'}]
    else:
        if file_data:
            df = pd.DataFrame(json.loads(file_data))
            df = df[(df['一级类目'] == cate_one) & (df['二级类目'] == cate_two)]
            if cate_two == '其他二级类目':
                value_list = df['asin'].unique()
                result = [{'label': i, 'value': i} for i in value_list]
                return result
            else:
                value_list = df['父SKU'].unique()
                if any(value_list):
                    result = [{'label': i, 'value': i} for i in value_list]
                    return result
                else:
                    return [{'label': 'none', 'value': 'none'}]


# 选择子sku-下拉菜单
@app.callback(Output('select_sku', 'options'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_cate_one', 'value'),
               Input('select_cate_two', 'value'),
               Input('select_fsku', 'value')],
              [State('daily_file_store', 'data'),
               State('daily_filename_store', 'data')])
def get_sub_asin(mt, cate_one, cate_two, fsku, file_data, file_name):
    if not all([mt, fsku, file_data, file_name]):
        return [{'label': 'none', 'value': 'none'}]
    else:
        if file_data:
            df = pd.DataFrame(json.loads(file_data))
            df = df[(df['一级类目'] == cate_one) & (df['二级类目'] == cate_two)]

            if cate_two == '其他二级类目':
                value_list = df[df['asin'] == fsku]['sub_asin'].unique()

            else:
                value_list = df[df['父SKU'] == fsku]['SKU'].unique()

            if any(value_list):
                result = [{'label': i, 'value': i} for i in value_list]
                return result
            else:
                return [{'label': 'none', 'value': 'none'}]


# 商品信息展示区域
@app.callback(Output('pic_bar', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_sku', 'value')],
              [State('daily_file_store', 'data')])
def get_pic_bar(mt, sku, data):
    if not all([mt, (sku != 'none'), data, sku]):
        return []
    else:
        res_df = df_pro[df_pro['SKU'] == sku]
        res_df .fillna('未注明', inplace=True)
        asin_dict = res_df.to_dict('list')

        if not any(asin_dict.values()):
            return []
        empty_list = ['未注明']
        goods_name = asin_dict.get('名称', empty_list)[0]
        pic_url = asin_dict.get('图片链接', empty_list)[0]
        if pic_url:
            pic_url = pic_url.replace('.jpg', '._SL160.jpg')
        asin = asin_dict.get('ASIN', empty_list)[0]
        color = asin_dict.get('颜色', empty_list)[0]
        size = asin_dict.get('SIZE', empty_list)[0]
        on_shelf_time = asin_dict.get('上架时间', empty_list)[0]
        if on_shelf_time and on_shelf_time != '未注明':
            try:
                on_shelf_time = datetime.datetime.strftime(on_shelf_time, '%Y-%m-%d')
            except:
                pass
        seller = asin_dict.get('店铺', empty_list)[0]

        if seller in ['SK', 'HA']:
            row_url = 'https://www.amazon.co.jp/dp/'
        else:
            row_url = 'https://www.amazon.com/'
        goods_url = row_url + asin
        children = html.Div([
            html.Div(
                className='columns',
                children=[
                    html.Div(html.Img(src=pic_url, width=160, height=160, style={"referrer": "no-referrer"})),
                    html.Div(
                        children=[
                            html.Ul(
                                className='my_ul',
                                children=[
                                    html.Li(html.A('商品链接', href=goods_url, target='blank')),
                                    html.Li('名称：' + str(goods_name)),
                                    html.Li('颜色：' + str(color)),
                                    html.Li('尺寸：' + str(size)),
                                    html.Li('上架时间：' + str(on_shelf_time))
                                ]
                            )
                        ]
                    )
                ])
        ])
        return children


# 一级类目展示
@app.callback(Output('asin_cate_one_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp')],
              [State('daily_file_store', 'data')])
def get_asin_cate_one_fig(mt, data):
    if not (mt and data):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        df_sum_asin = df.groupby(by=['一级类目']).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum, '已订购商品销售额': np.sum}).reset_index()
        df_sum_asin['转化率'] = df_sum_asin['已订购商品数量'] / df_sum_asin['买家访问次数']
        df_sum_asin['转化率'] = df_sum_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        df_sum_asin.sort_values(by=['买家访问次数'], inplace=True, ascending=False)
        fig = get_daily_sum_fig(df_sum_asin, mode='一级类目', title='各一级类目')
        fig2 = get_daily_table_fig(df_sum_asin, mode='一级类目')
        children = html.Div(
            className='four columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )
        return children


# 二级类目展示
@app.callback(Output('asin_cate_two_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_cate_one', 'value')],
              [State('daily_file_store', 'data')])
def get_asin_cate_two_fig(mt, cate_one, data):
    if not all([mt, cate_one, data]):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        df = df[df['一级类目'] == cate_one]
        df_sum_asin = df.groupby(by=['二级类目']).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum, '已订购商品销售额': np.sum}).reset_index()
        df_sum_asin['转化率'] = df_sum_asin['已订购商品数量'] / df_sum_asin['买家访问次数']
        df_sum_asin['转化率'] = df_sum_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        df_sum_asin.sort_values(by=['买家访问次数'], inplace=True, ascending=False)
        fig = get_daily_sum_fig(df_sum_asin, mode='二级类目', title=cate_one + '-各二级类目-')
        fig2 = get_daily_table_fig(df_sum_asin, mode='二级类目')
        children = html.Div(
            className='four columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 二级类目下的父sku
@app.callback(Output('asin_cate_fsku_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_cate_one', 'value'),
               Input('select_cate_two', 'value')],
              [State('daily_file_store', 'data')])
def get_asin_cate_two_fig(mt, cate_one, cate_two, data):
    if not all([mt, cate_one, cate_two, (cate_one != 'none'), (cate_two != 'none'), data]):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        df = df[(df['一级类目'] == cate_one) & (df['二级类目'] == cate_two)]
        if cate_two == '其他二级类目':
            mode = 'asin'
        else:
            mode = '父SKU'
        df_sum_asin = df.groupby(by=[mode]).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum, '已订购商品销售额': np.sum}).reset_index()
        df_sum_asin['转化率'] = df_sum_asin['已订购商品数量'] / df_sum_asin['买家访问次数']
        df_sum_asin['转化率'] = df_sum_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        df_sum_asin.sort_values(by=['买家访问次数'], inplace=True, ascending=False)
        fig = get_daily_sum_fig(df_sum_asin, mode=mode, title=cate_two + '-各父sku-')
        fig2 = get_daily_table_fig(df_sum_asin, mode=mode)
        children = html.Div(
            className='four columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 所有父级sku月度汇总
@app.callback(Output('asin_sum_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp')],
              [State('daily_file_store', 'data')])
def get_asin_sum_fig(mt, data):
    if not (mt and data):
        return []
    else:
        df = pd.read_json(data, convert_dates='date', date_unit='ms')

        df_sum_asin = df.groupby(by=['父SKU']).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum, '已订购商品销售额': np.sum}).reset_index()
        df_sum_asin['转化率'] = df_sum_asin['已订购商品数量'] / df_sum_asin['买家访问次数']
        df_sum_asin['转化率'] = df_sum_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        df_sum_asin.sort_values(by=['买家访问次数'], inplace=True, ascending=False)
        fig = get_daily_sum_fig(df_sum_asin, mode='父SKU', title='所有父级sku')
        fig2 = get_daily_table_fig(df_sum_asin, mode='父SKU')
        children = html.Div(
            className='twelve columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 父级SKU月度时域
@app.callback(Output('asin_time_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_fsku', 'value')],
              [State('daily_file_store', 'data')])
def get_asin_time_fig(mt, fsku, data):
    if not all([mt, fsku, data]):
        return []
    else:
        df = pd.read_json(data, convert_dates='date', date_unit='ms')
        df = df[df['父SKU'] == fsku]
        df_asin = df.groupby(by=['date']).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum}).reset_index()
        df_asin['转化率'] = df_asin['已订购商品数量'] / df_asin['买家访问次数']
        df_asin['转化率'] = df_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        fig = get_daily_time_fig(df_asin, title=fsku)
        fig2 = get_daily_table_fig(df_asin, mode='date')
        children = html.Div(
            className='twelve columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 子SKU月度汇总
@app.callback(Output('sub_asin_sum_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_fsku', 'value')],
              [State('daily_file_store', 'data')])
def get_sub_asin_sum(mt, fsku, data):
    if not (mt and fsku and data):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        df = df[df['父SKU'] == fsku]
        df_sum_asin = df.groupby(by=['SKU']).agg(
            {'买家访问次数': np.sum, '已订购商品数量': np.sum, '已订购商品销售额': np.sum}).reset_index()
        df_sum_asin['转化率'] = df_sum_asin['已订购商品数量'] / df_sum_asin['买家访问次数']
        df_sum_asin['转化率'] = df_sum_asin['转化率'].apply(lambda x: '{:.2%}'.format(x))
        df_sum_asin.sort_values(by=['买家访问次数'], inplace=True, ascending=False)
        fig = get_daily_sum_fig(df_sum_asin, mode='SKU', title=fsku)
        fig2 = get_daily_table_fig(df_sum_asin, mode='SKU')
        children = html.Div(
            className='twelve columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 子ASIN月度时域图示
@app.callback(Output('sub_asin_time_fig', 'children'),
              [Input('daily_file_store', 'modified_timestamp'),
               Input('select_sku', 'value')],
              [State('daily_file_store', 'data')])
def get_sub_asin_time(mt, sku, data):
    if not (mt and sku and data):
        return []
    else:
        df = pd.read_json(data, convert_dates='date', date_unit='ms')
        # try:
        #     df['date'] = df['date'].apply(lambda x: datetime.datetime.strftime(x, '%m-%d'))
        # except:
        #     pass
        df_one_asin = df[df['SKU'] == sku]
        df_one_asin['转化率'] = df_one_asin['订单商品数量转化率'].apply(lambda x: '{:.2%}'.format(x))
        fig = get_daily_time_fig(df_one_asin, title=sku)
        fig2 = get_daily_table_fig(df_one_asin, mode='date')
        children = html.Div(
            className='twelve columns',
            children=[
                dcc.Graph(figure=fig, className='twelve columns'),
                dcc.Graph(figure=fig2, className='twelve columns',
                          style={'height': 100},
                          )
            ]
        )

        return children


# 选择广告组合名称-菜单
@app.callback(Output('select_ad_comb', 'options'),
              [Input('ad_file_store', 'modified_timestamp')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_action(mt, file_data, file_name):
    if not (mt and file_data and file_name):
        return [{'label': 'none', 'value': 'none'}]
    else:
        df = pd.DataFrame(json.loads(file_data))
        asin_list = df['广告组合名称'].unique()
        result = [{'label': i, 'value': i} for i in asin_list]
        return result


# 根据广告组合选择广告活动名称-菜单
@app.callback(Output('select_ad_action', 'options'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb','value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_action(mt, ad_comb, file_data, file_name):
    if not all([mt, ad_comb, file_data, file_name]):
        return [{'label': 'none', 'value': 'none'}]
    else:
        df = pd.DataFrame(json.loads(file_data))
        df = df[df['广告组合名称'] == ad_comb]
        asin_list = df['广告活动名称'].unique()
        result = [{'label': i, 'value': i} for i in asin_list]
        return result


# 根据广告组合、广告活动， 选择广告组名称-菜单
@app.callback(Output('select_ad_group', 'options'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb','value'),
               Input('select_ad_action', 'value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_group(mt, ad_comb, ad_action, file_data, file_name):
    if not all([mt, ad_comb, file_data, file_name]):
        return [{'label': 'none', 'value': 'none'}]
    else:
        df = pd.DataFrame(json.loads(file_data))
        df = df[(df['广告组合名称'] == ad_comb) &
                (df['广告活动名称'] == ad_action)]
        sub_asin_list = list(df['广告组名称'].unique())
        result = [{'label': i, 'value': i} for i in sub_asin_list]
        return result


# 选择广告投放名称-菜单
@app.callback(Output('select_ad_words', 'options'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb', 'value'),
               Input('select_ad_action', 'value'),
               Input('select_ad_group', 'value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_ad_group(mt, ad_comb, ad_action, ad_group, file_data, file_name):
    if not all([mt, ad_comb, ad_action, ad_group, file_data, file_name]):
        return [{'label': 'none', 'value': 'none'}]
    else:
        df = pd.DataFrame(json.loads(file_data))
        df = df[(df['广告组合名称'] == ad_comb) &
                (df['广告活动名称'] == ad_action) &
                (df['广告组名称'] == ad_group)]
        sub_asin_list = list(df['投放'].unique())

        result = [{'label': i, 'value': i} for i in sub_asin_list]
        return result


# 定义绘图辅助函数
def get_ploy_fig(df, title):
    fig = go.Figure()
    df_result = pd.DataFrame()

    df_result.loc[0, '总展现量'] = df['展现量'].sum()
    df_result.loc[0, '总花费'] = df['花费'].sum()
    df_result.loc[0, '总销售额'] = df['销售额'].sum()
    df_result.loc[0, '平均点击率'] = df['点击量'].sum() / df['展现量'].sum()
    df_result.loc[0, '平均acos'] = df['花费'].sum() / df['销售额'].sum()

    for i in ['总花费', '总销售额']:
        try:
            df_result[i] = df_result[i].apply(lambda x: "{:.2f}".format(x))
        except:
            pass
    for i in ['平均点击率', '平均acos']:
        try:
            df_result[i] = df_result[i].apply(lambda x: '{:.2%}'.format(x))
        except:
            pass
    fig.add_trace(go.Table(
        header={'values': list(df_result.columns)},
        cells=dict(
            values=[df_result[k].tolist() for k in df_result.columns[:]],
            align="center")
    ))
    fig.update_layout(dict(
        margin={'l': 0, 't': 0, 'r': 0, 'b': 0},
        height=120,
        title=title + '-广告汇总数据'
    )
    )
    return fig


# 绘制聚合曲线
def get_daily_sum_fig(df_sum_asin, mode, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=df_sum_asin[mode],
               y=df_sum_asin['买家访问次数'],
               yaxis='y',
               name='访问量',
               text=df_sum_asin['买家访问次数'],
               textposition='auto',
               hovertemplate='%{y}'))
    fig.add_trace(
        go.Scatter(x=df_sum_asin[mode],
                   y=df_sum_asin['已订购商品数量'],
                   yaxis='y2',
                   name='销量',
                   mode='lines+markers', ),
    )
    fig.add_trace(
        go.Scatter(x=df_sum_asin[mode],
                   y=df_sum_asin['转化率'],
                   yaxis='y3',
                   name='转化率',
                   mode='lines+markers',
                   hovertemplate='%{y}%')
    )

    fig.update_layout(
        xaxis=dict(
            domain=[0, 1]
        ),
        yaxis=dict(
            title="访问量",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="销量",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.00725,
        ),
        yaxis3=dict(
            title="转化率",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        hovermode='x',
        title=title + '聚合曲线'
    )

    return fig


# 绘制日常数据表格
def get_daily_table_fig(df, mode):
    if 'date' in df.columns:
        try:
            df['date'] = df['date'].apply(lambda x: datetime.datetime.strftime(x, '%m-%d'))
        except:
            pass
    fig = go.Figure()
    fig.add_trace(
        go.Table(
            # columnorder=[i+1 for i in range(len(df[mode]))],
            # columnwidth=[30 for each in range(len(df[mode]))],
            header=dict(values=list(df[mode]),
                        fill_color='paleturquoise',
                        align='center'),
            cells=dict(values=df[['买家访问次数', '已订购商品数量', '转化率']].values.tolist(),
                       fill_color='lavender',
                       align='center'),

        )
    )
    fig.update_layout(

        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4,
        )
    )
    return fig


def get_daily_html_table(df, mode):
    html.Tbody(
        [html.Th(each) for each in (list(df[mode]))],
        html.Tr(
            [html.Td(each) for each in df['卖家访问次数'].values.tolist()]
        ),
        html.Tr(
            html.Td(df['已订购商品数量'].values.tolist())
        ),
        html.Tr(
            html.Td(df['转化率'].values.tolist())
        ),
    )

    pass


# 绘制时域曲线
def get_daily_time_fig(df, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['买家访问次数'],
            name='访问量',
            yaxis='y',
            text=df['买家访问次数'],
            textposition='auto',
            hovertemplate='%{y}',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['已订购商品数量'],
            name='销量',
            yaxis='y2',
            mode='lines+markers',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['转化率'],
            name='转化率',
            yaxis='y3',
            mode='lines+markers',
            hovertemplate='%{y}%'
        )
    )

    fig.update_layout(
        xaxis=dict(
            domain=[0, 1]
        ),
        # xaxis_tickformat='%m-%d (.%a)',
        xaxis_tickformat='%m-%d',
        yaxis=dict(
            title="访问量",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="销量",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.00725
        ),
        yaxis3=dict(
            title="转化率",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        hovermode='x',
        title=title + '时域曲线'
    )

    return fig


# 绘制广告曲线
def get_ad_fig(df, mode, title):
    fig = go.Figure()
    fig_bar = go.Bar(x=df[mode], y=df['展现量'], yaxis='y', name='展现量', text=df['展现量'], textposition='auto',
                     hovertemplate='%{text}')
    fig_line = go.Scatter(x=df[mode], y=df['acos'], yaxis='y2', name='acos', mode='lines+markers',
                          hovertemplate='%{y}%')
    df['acos_目标'] = 30
    fig_line_half = go.Scatter(x=df[mode], y=df['acos_目标'], yaxis='y2', name='30%acos线', mode='lines',
                               hovertemplate='%{y}%')
    fig_line2 = go.Scatter(x=df[mode], y=df['转化率'], yaxis='y3', name='转化率', mode='lines+markers',
                           hovertemplate='%{y}%')
    fig_line3 = go.Scatter(x=df[mode], y=df['花费'], yaxis='y4', name='花费', mode='lines+markers')
    fig_line4 = go.Scatter(x=df[mode], y=df['点击率'], yaxis='y5', name='点击', mode='lines+markers',
                           hovertemplate='%{y}%')
    fig.add_trace(fig_bar)
    fig.add_trace(fig_line)
    fig.add_trace(fig_line2)
    fig.add_trace(fig_line_half)
    fig.add_trace(fig_line3)
    fig.add_trace(fig_line4)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        xaxis=dict(
            domain=[0, 1]
        ),
        yaxis=dict(
            title="展现量",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="acos",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.015,
        ),
        yaxis3=dict(
            title="转化率",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.95,
        ),
        yaxis4=dict(
            title="花费",
            titlefont=dict(
                color="#993333"
            ),
            tickfont=dict(
                color="#993333"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.975,
        ),
        yaxis5=dict(
            title="点击率",
            titlefont=dict(
                color="#339999"
            ),
            tickfont=dict(
                color="#339999"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.995,
        ),
        hovermode='x',
        title=title + '广告数据',
    )
    return fig


# 广告数据汇总图示-广告组合图示
@app.callback(Output('ad_comb_fig', 'children'),
              [Input('ad_file_store', 'modified_timestamp')],
              [State('ad_file_store', 'data')])
def get_ad_action_sum_fig(mt, data):
    if not (mt and data):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        data_group = df.groupby('广告组合名称').agg(
            {'展现量': np.sum, '点击量': np.sum, '销量': np.sum, '销售额': np.sum, '花费': np.sum}).reset_index()
        data_group['acos'] = (data_group['花费'] / data_group['销售额']).apply(lambda x: '{:.2%}'.format(x))
        data_group['点击率'] = (data_group['点击量'] / data_group['展现量']).apply(lambda x: '{:.2%}'.format(x))
        data_group['转化率'] = (data_group['销量'] / data_group['点击量']).apply(lambda x: '{:.2%}'.format(x))
        data_group.sort_values(['展现量'], inplace=True, ascending=False)
        data_group.reset_index(drop=True, inplace=True)
        fig = get_ad_fig(data_group, mode='广告组合名称', title='全部')
        children = html.Div([
            dcc.Graph(figure=fig,
                      className='twelve columns',
                      style={'height': 450})
        ])
        return children


# 广告活动图示
@app.callback(Output('ad_action_sum_fig', 'children'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb', 'value')],
              [State('ad_file_store', 'data')])
def get_ad_action_sum_fig(mt, ad_comb, data):
    if not all([mt, ad_comb, data]):
        return []
    else:
        df = pd.DataFrame(json.loads(data))
        df = df[df['广告组合名称'] == ad_comb]
        data_group = df.groupby('广告活动名称').agg(
            {'展现量': np.sum, '点击量': np.sum, '销量': np.sum, '销售额': np.sum, '花费': np.sum}).reset_index()
        data_group['acos'] = (data_group['花费'] / data_group['销售额']).apply(lambda x: '{:.2%}'.format(x))
        data_group['点击率'] = (data_group['点击量'] / data_group['展现量']).apply(lambda x: '{:.2%}'.format(x))
        data_group['转化率'] = (data_group['销量'] / data_group['点击量']).apply(lambda x: '{:.2%}'.format(x))
        data_group.sort_values(['展现量'], inplace=True, ascending=False)
        data_group.reset_index(drop=True, inplace=True)
        fig = get_ad_fig(data_group, mode='广告活动名称', title=ad_comb)
        children = html.Div([
            dcc.Graph(figure=fig,
                      className='six columns',
                      style={'height': 450})
        ])
        return children


# 广告组具体图示
@app.callback(Output('ad_group_sum_fig', 'children'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb', 'value'),
               Input('select_ad_action', 'value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_ad_group_fig(mt, ad_comb, ad_action, data, filename):
    if not all([mt, ad_comb, ad_action, data]):
        return []
    else:
        df_row = pd.DataFrame(json.loads(data))
        data_action = df_row[(df_row['广告组合名称'] == ad_comb)&
                             (df_row['广告活动名称'] == ad_action)]
        data_group = data_action.groupby('广告组名称').agg(
            {'展现量': np.sum, '点击量': np.sum, '销量': np.sum, '销售额': np.sum, '花费': np.sum}).reset_index()

        data_group['acos'] = (data_group['花费'] / data_group['销售额']).apply(lambda x: '{:.2%}'.format(x))
        data_group['点击率'] = (data_group['点击量'] / data_group['展现量']).apply(lambda x: '{:.2%}'.format(x))
        data_group['转化率'] = (data_group['销量'] / data_group['点击量']).apply(lambda x: '{:.2%}'.format(x))
        data_group.sort_values(['展现量'], inplace=True, ascending=False)
        data_group.reset_index(drop=True, inplace=True)
        fig = get_ad_fig(data_group, mode='广告组名称', title=ad_comb + '/' + ad_action)
        children = html.Div([
            dcc.Graph(figure=fig,
                      className='six columns'),
        ])
        return children


# 广告投放具体图示
@app.callback(Output('ad_keys_sum_fig', 'children'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb', 'value'),
               Input('select_ad_action', 'value'),
               Input('select_ad_group', 'value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_ad_group_fig(mt, ad_comb, ad_action, ad_group, data, filename):
    if not all([mt, ad_comb, ad_action, ad_group, data]):
        return []
    else:
        df_row = pd.DataFrame(json.loads(data))
        data_action = df_row[(df_row['广告组合名称'] == ad_comb) &
                             (df_row['广告活动名称'] == ad_action) &
                             (df_row['广告组名称'] == ad_group)]
        data_group = data_action.groupby('投放').agg(
            {'展现量': np.sum, '点击量': np.sum, '销量': np.sum, '销售额': np.sum, '花费': np.sum}).reset_index()
        data_group['acos'] = (data_group['花费'] / data_group['销售额']).apply(lambda x: '{:.2%}'.format(x))
        data_group['点击率'] = (data_group['点击量'] / data_group['展现量']).apply(lambda x: '{:.2%}'.format(x))
        data_group['转化率'] = (data_group['销量'] / data_group['点击量']).apply(lambda x: '{:.2%}'.format(x))
        data_group.sort_values(['展现量'], inplace=True, ascending=False)
        data_group.reset_index(drop=True, inplace=True)
        fig = get_ad_fig(data_group, mode='投放', title=ad_comb + "/" + ad_action + "/" +  ad_group)
        children = html.Div([
            dcc.Graph(figure=fig, className='twelve columns'),
        ])
        return children


# 广告搜索词具体图示
@app.callback(Output('ad_key_words_search', 'children'),
              [Input('ad_file_store', 'modified_timestamp'),
               Input('select_ad_comb', 'value'),
               Input('select_ad_action', 'value'),
               Input('select_ad_group', 'value'),
               Input('select_ad_words', 'value')],
              [State('ad_file_store', 'data'),
               State('ad_filename_store', 'data')])
def get_ad_words_fig(mt, ad_comb, ad_action, ad_group, ad_words, data, filename):
    if not all([mt,ad_comb, ad_action, ad_group, ad_words, data]):
        return []
    else:
        df_row = pd.DataFrame(json.loads(data))
        data_action = df_row[(df_row['广告组合名称'] == ad_comb) &
                             (df_row['广告活动名称'] == ad_action) &
                             (df_row['广告组名称'] == ad_group) &
                             (df_row['投放'] == ad_words)]
        data_group = data_action.groupby('客户搜索词').agg(
            {'展现量': np.sum, '点击量': np.sum, '销量': np.sum, '销售额': np.sum, '花费': np.sum}).reset_index()

        data_group['acos'] = (data_group['花费'] / data_group['销售额']).apply(lambda x: '{:.2%}'.format(x))
        data_group['点击率'] = (data_group['点击量'] / data_group['展现量']).apply(lambda x: '{:.2%}'.format(x))
        data_group['转化率'] = (data_group['销量'] / data_group['点击量']).apply(lambda x: '{:.2%}'.format(x))
        data_group.sort_values(['展现量'], inplace=True, ascending=False)
        data_group.reset_index(drop=True, inplace=True)
        fig = get_ad_fig(data_group, mode='客户搜索词', title=ad_words)
        children = html.Div([
            dcc.Graph(figure=fig, className='twelve columns'),
        ])
        return children


#  新增功能，生成独立的文件夹，可下载文件，

# @server.route("/download/<path>/<path2>/<file_name>", methods=['GET'])
# def download_file(path, path2, file_name):
#     directory = os.getcwd() + "/" + path + "/" + path2 + "/"
#     try:
#         response = flask.make_response(flask.send_from_directory(directory, file_name, as_attachment=True))
#         response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
#         return response
#     except Exception as e:
#         raise e


# 类似文件下载的页面
# page_table = html.Div([
#     # html.Link('返回主页'),
#     html.Div(id='show_data'),
# ])

#
# @app.callback(Output('show_data', 'children'),
#               [Input('choose_store', 'value'),
#                Input('output_store', 'modified_timestamp')],
#               [State('output_store', 'data')])
# def choose_store(mt, value, data):
#     if all([mt, value, data]):
#         return data


# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/table':
#         return page_table
#     else:
#         return index_page
app.layout = index_page

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])
if __name__ == '__main__':
    app.run_server(debug=True)