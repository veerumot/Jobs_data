#!/usr/bin/env python3

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import psycopg2
import plotly.express as px
from flask import Flask
import os


server = Flask(__name__)

load_figure_template("DARKLY")

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], server=server, url_base_pathname='/jobs-data/')

colors = {
    'background': '#111111',
    'text': 'lightgrey'
}



dash_app.layout = html.Div(children=[
    html.H1(children='Linkdein DevOps Job Data Analysis', style={
            'textAlign': 'center',
            'color': colors['text']
        }
        ),
    
    dcc.Interval(
        id="interval-component", interval=3600 * 1000, n_intervals=0
    ),

    dcc.Graph(
        id='line-chart'
    ),

    dcc.Graph(
        id='line-chart1'
    ),

    dcc.Graph(
        id='line-chart2'
    )
])
@dash_app.callback(
    Output('line-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def daily_data_postgres(Input):
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    print("Database connected successfully")
    cur = conn.cursor()
    query = """
                SELECT date, day_jobs
                FROM public.time_data
                ORDER BY DATE DESC
                LIMIT 7 ;
            """
    cur.execute(query)
    day_data = cur.fetchall()
    df = pd.DataFrame(day_data, columns= ['date', 'day_jobs'])
    # print(df)
    day_data = {
    'date': df['date'].tolist(),  # Convert 'date' column to list
    'value': df['day_jobs'].tolist()  # Convert 'day_jobs' column to list and rename to 'value'
    }
    print(day_data)
    cur.close()
    conn.close()
    fig = px.line(day_data, x='date', y='value', title= 'Data for daily posted jobs in Linkdein', markers=True, text='value')
    fig.update_traces(textposition='top center')
    fig.update_layout( 
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )
    return fig

@dash_app.callback(
    Output('line-chart1', 'figure'),
    Input('interval-component', 'n_intervals')
)
def weekly_data_postgres(Input):
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    print("Database connected successfully")
    cur = conn.cursor()
    query = """
                select current_week,round(avg(week_jobs))
                from time_data td 
                group by current_week
                ORDER BY current_week
                LIMIT 4 ;
            """
    cur.execute(query)
    week_data = cur.fetchall()
    df = pd.DataFrame(week_data, columns= ['current_week', 'week_jobs'])
    # print(df)
    week_data = {
    'week': df['current_week'].tolist(),  # Convert 'date' column to list
    'value': df['week_jobs'].tolist()  # Convert 'day_jobs' column to list and rename to 'value'
    }
    print(week_data)
    cur.close()
    conn.close()
    fig = px.line(week_data, x='week', y='value', title= 'Data for weekly posted jobs in Linkdein', markers=True, text='value')
    fig.update_traces(textposition='top center')
    fig.update_layout( 
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )
    return fig

@dash_app.callback(
    Output('line-chart2', 'figure'),
    Input('interval-component', 'n_intervals')
)
def montly_data_postgres(Input):
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    print("Database connected successfully")
    cur = conn.cursor()
    query = """
                select date_part('month', date::date) as month,
                round(avg(month_jobs))
                from time_data 
                group by date_part('month', date::date)
                order by month;
            """
    cur.execute(query)
    month_data = cur.fetchall()
    df = pd.DataFrame(month_data, columns= ['month', 'month_jobs'])
    # print(df)
    month_data = {
    'month': df['month'].tolist(),  # Convert 'date' column to list
    'value': df['month_jobs'].tolist()  # Convert 'day_jobs' column to list and rename to 'value'
    }
    print(month_data)
    cur.close()
    conn.close()
    fig = px.line(month_data, x='month', y='value', title= 'Data for Monthly posted jobs in Linkdein', markers=True, text='value')
    fig.update_traces(textposition='top center')
    fig.update_layout( 
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )
    return fig

if __name__ == "__main__":
    dash_app.run_server(debug=True, host="0.0.0.0")


