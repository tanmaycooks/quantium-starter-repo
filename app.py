# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Initialize the app
app = Dash(__name__)

# Load the data
df = pd.read_csv('pink_morsel_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# Get unique regions and date range
regions = sorted(df['region'].unique())
min_date = df['date'].min()
max_date = df['date'].max()

# Define color scheme for regions
region_colors = {
    'north': '#1f77b4',
    'south': '#ff7f0e',
    'east': '#2ca02c',
    'west': '#d62728'
}

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Pink Morsel Sales Dashboard', 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P('Interactive visualization of pink morsel sales data across regions',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': 30})
    ]),
    
    # Filters Section
    html.Div([
        html.Div([
            html.Label('Select Date Range:', style={'fontWeight': 'bold', 'marginBottom': 5}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=min_date,
                end_date=max_date,
                display_format='YYYY-MM-DD',
                style={'marginBottom': 10}
            ),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label('Select Regions:', style={'fontWeight': 'bold', 'marginBottom': 5}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': region.title(), 'value': region} for region in regions],
                value=regions,  # All regions selected by default
                multi=True,
                style={'marginBottom': 10}
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'backgroundColor': '#ecf0f1', 
              'borderRadius': 5, 'marginBottom': 20}),
    
    # Charts Section
    html.Div([
        # Time Series Chart
        html.Div([
            html.H3('Sales Over Time', style={'textAlign': 'center', 'color': '#34495e'}),
            dcc.Graph(id='time-series-chart')
        ], style={'marginBottom': 30}),
        
        # Regional Comparison Chart
        html.Div([
            html.H3('Regional Sales Comparison', style={'textAlign': 'center', 'color': '#34495e'}),
            dcc.Graph(id='regional-chart')
        ], style={'marginBottom': 20}),
    ])
], style={'maxWidth': 1200, 'margin': '0 auto', 'padding': 20, 'fontFamily': 'Arial, sans-serif'})


# Callback for updating charts based on filters
@app.callback(
    [Output('time-series-chart', 'figure'),
     Output('regional-chart', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('region-filter', 'value')]
)
def update_charts(start_date, end_date, selected_regions):
    # Filter data based on selections
    filtered_df = df.copy()
    
    # Convert date strings to datetime if needed
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & 
                                  (filtered_df['date'] <= end_date)]
    
    # Filter by region if selections exist
    if selected_regions and len(selected_regions) > 0:
        filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
    
    # Time Series Chart - Sales over time by region
    time_series_data = filtered_df.groupby(['date', 'region'])['sales'].sum().reset_index()
    
    fig_time_series = px.line(time_series_data, 
                              x='date', 
                              y='sales', 
                              color='region',
                              color_discrete_map=region_colors,
                              labels={'sales': 'Total Sales ($)', 'date': 'Date', 'region': 'Region'},
                              title='')
    
    fig_time_series.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        legend=dict(title='Region', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    # Regional Comparison Chart - Total sales by region
    regional_totals = filtered_df.groupby('region')['sales'].sum().reset_index()
    regional_totals = regional_totals.sort_values('sales', ascending=False)
    
    fig_regional = go.Figure(data=[
        go.Bar(
            x=regional_totals['region'],
            y=regional_totals['sales'],
            marker_color=[region_colors[r] for r in regional_totals['region']],
            text=regional_totals['sales'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
        )
    ])
    
    fig_regional.update_layout(
        xaxis_title='Region',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
    )
    
    return fig_time_series, fig_regional


if __name__ == '__main__':
    app.run(debug=True)
