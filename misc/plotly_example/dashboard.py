from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

df = pd.read_csv('claims_sample_data.csv')
df['paid_month'] = pd.to_datetime(df['MONTH'], format="%Y%m", errors='coerce')
df['paid_month_year'] = df['paid_month'].dt.strftime('%m/%Y')
groupby_spec_df = df.groupby('CLAIM_SPECIALTY', as_index=False).PAID_AMOUNT.sum()
# leave top 9
groupby_spec_df['CLAIM_SPECIALTY'] = np.where(
    groupby_spec_df.PAID_AMOUNT >= groupby_spec_df.PAID_AMOUNT.sort_values(ascending=False).values[8], 
    groupby_spec_df.CLAIM_SPECIALTY,
    'Other')

app = Dash(__name__)

app.layout = html.Div([

    html.H1("Totals"),
    html.Div([
        html.Div(
            dcc.Graph(
                id='total_by_month',
                figure=px.line(df.groupby(['paid_month']).PAID_AMOUNT.sum(), title='Paids by month')),
            style={'width': '31%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(
                id='spec_pie',
                figure=px.pie(groupby_spec_df, values='PAID_AMOUNT', names='CLAIM_SPECIALTY', title='CLAIM_SPECIALTY')),
            style={'width': '27%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(
                id='payer_pie',
                figure=px.pie(df,
            values='PAID_AMOUNT', names='PAYER',
            title='PAYER')),
            style={'width': '19%', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(
                id='service_pie',
                figure=px.pie(df,
            values='PAID_AMOUNT', names='SERVICE_CATEGORY',
            title='SERVICE_CATEGORY')),
            style={'width': '23%', 'display': 'inline-block'}
        ),
        ]),
    
    html.H1("Filtered distribution and table"),
    html.Div([
        html.Div(
            dcc.Dropdown(
                df['SERVICE_CATEGORY'].unique(),
                'AncillaryFFS',
                id='SERVICE_CATEGORY',
            ), style={'width': '31%', 'display': 'inline-block'}),

        html.Div(
            dcc.Dropdown(
                df['PAYER'].unique(),
                'Payer F',
                id='PAYER',
            ), style={'width': '31%', 'display': 'inline-block'}),

        html.Div(
            dcc.Dropdown(
                df['paid_month_year'].unique(),
                '01/2018',
                id='year_month'
            ), style={'width': '31%', 'display': 'inline-block'}
        ),
    ]),

    html.Div([
        html.Div(dcc.Graph(id='paid_hist'), style={'width': '49%', 'display': 'inline-block'}),
        html.Div(
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns if c != 'paid_month' and c != 'MONTH'],
            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'}, id='table'), 
            style={'width': '49%', 'display': 'inline-block', 'margin-top': '70px'})
    ], style={'display': 'flex'}),

    html.H1("Total paids by date and category"),    
    html.Div([
        html.Div(
            dcc.RadioItems(
                ['SERVICE_CATEGORY', 'PAYER'],
                'SERVICE_CATEGORY',
                id='group_col',
            ), style={'width': '31%'}),

        html.Div(dcc.Graph(id='color_cat')),
    ]),

    html.H1("Pivot table"),
    html.Div([
        html.Div(
            dcc.RadioItems(
                ['SERVICE_CATEGORY', 'PAYER'],
                'SERVICE_CATEGORY',
                id='group_pivot_col',
            ), style={'width': '31%'}),
    html.Div(id='pivot_table', style={'width': '75%', 'display': 'inline-block', 'margin-top': '20px'})
    ])

])

@app.callback(
    Output('paid_hist', 'figure'),
    Input('SERVICE_CATEGORY', 'value'),
    Input('PAYER', 'value'),
    Input('year_month', 'value')
    )
def update_graph(SERVICE_CATEGORY, PAYER, year_month):
    fig = px.histogram(df[
        (df['SERVICE_CATEGORY'] == SERVICE_CATEGORY) & 
        (df['PAYER'] == PAYER) &
        (df['paid_month'] == year_month)], 'PAID_AMOUNT')
    return fig


@app.callback(
    Output('table', 'data'),
    Input('SERVICE_CATEGORY', 'value'),
    Input('PAYER', 'value'),
    Input('year_month', 'value'),
    )
def filter_table(SERVICE_CATEGORY, PAYER, year_month):
    return df[
        (df['SERVICE_CATEGORY'] == SERVICE_CATEGORY) & 
        (df['PAYER'] == PAYER) &
        (df['paid_month'] == year_month)].to_dict('records')


@app.callback(
    Output('color_cat', 'figure'),
    Input('group_col', 'value'),
    )
def filter_table(group_col):
    dff = df.groupby(['paid_month', group_col], as_index=False).PAID_AMOUNT.sum()
    fig = px.line(dff, x="paid_month", y="PAID_AMOUNT", color=group_col)
    return fig


@app.callback(
    Output('pivot_table', 'children'),
    Input('group_pivot_col', 'value'),
    )
def pivot_table(group_col):
    group2_col = 'PAYER'
    if group_col == 'PAYER':
        group2_col = 'SERVICE_CATEGORY'

    dff = df.groupby(group_col, as_index=False).agg({'CLAIM_SPECIALTY': 'nunique', group2_col: 'nunique', 'PAID_AMOUNT': 'sum', 'MONTH': 'nunique'})

    return dash_table.DataTable(
            data=dff.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in dff.columns],
            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'}, ), 


if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
