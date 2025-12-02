# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
    'north': '#1AEDCF',
    'south': '#1AC6ED',
    'east': '#1AED87',
    'west': '#1AA4ED'
}

# Modern color scheme
colors = {
    'background': '#0F1419',
    'card': '#1A1F2E',
    'text': '#E8E9ED',
    'text_secondary': '#8B92A8',
    'accent': '#1AEDCF',
    'border': '#2A3142'
}

# App layout
app.layout = html.Div(style={
    'backgroundColor': colors['background'],
    'minHeight': '100vh',
    'padding': '20px',
    'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
}, children=[
    # Header
    html.Div(style={
        'maxWidth': '1400px',
        'margin': '0 auto',
        'marginBottom': '40px'
    }, children=[
        html.H1('Pink Morsel Sales Dashboard', 
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'marginBottom': '10px',
                    'fontSize': '42px',
                    'fontWeight': '700',
                    'letterSpacing': '-0.5px'
                }),
        html.P('Interactive visualization of pink morsel sales data across regions',
               style={
                   'textAlign': 'center',
                   'color': colors['text_secondary'],
                   'fontSize': '16px',
                   'marginBottom': '0'
               })
    ]),
    
    # Main Content Container
    html.Div(style={
        'maxWidth': '1400px',
        'margin': '0 auto'
    }, children=[
        # Filters Card
        html.Div(style={
            'backgroundColor': colors['card'],
            'borderRadius': '12px',
            'padding': '30px',
            'marginBottom': '30px',
            'border': f'1px solid {colors["border"]}',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
        }, children=[
            html.Div(style={'display': 'flex', 'gap': '40px', 'flexWrap': 'wrap'}, children=[
                # Date Range Picker
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.Label('Select Date Range', 
                              style={
                                  'color': colors['text'],
                                  'fontSize': '14px',
                                  'fontWeight': '600',
                                  'marginBottom': '12px',
                                  'display': 'block'
                              }),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=min_date,
                        end_date=max_date,
                        display_format='YYYY-MM-DD',
                        style={'width': '100%'}
                    ),
                ]),
                
                # Region Radio Buttons
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.Label('Filter by Region',
                              style={
                                  'color': colors['text'],
                                  'fontSize': '14px',
                                  'fontWeight': '600',
                                  'marginBottom': '12px',
                                  'display': 'block'
                              }),
                    dcc.RadioItems(
                        id='region-filter',
                        options=[
                            {'label': ' All Regions', 'value': 'all'},
                            {'label': ' North', 'value': 'north'},
                            {'label': ' East', 'value': 'east'},
                            {'label': ' South', 'value': 'south'},
                            {'label': ' West', 'value': 'west'}
                        ],
                        value='all',
                        inline=True,
                        style={'marginTop': '8px'},
                        labelStyle={
                            'display': 'inline-block',
                            'marginRight': '20px',
                            'color': colors['text_secondary'],
                            'fontSize': '14px',
                            'cursor': 'pointer'
                        },
                        inputStyle={
                            'marginRight': '6px',
                            'cursor': 'pointer'
                        }
                    ),
                ]),
            ])
        ]),
        
        # Charts Grid
        html.Div(style={'display': 'grid', 'gap': '30px'}, children=[
            # Time Series Chart Card
            html.Div(style={
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'padding': '30px',
                'border': f'1px solid {colors["border"]}',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            }, children=[
                html.H3('Sales Over Time', 
                       style={
                           'color': colors['text'],
                           'fontSize': '20px',
                           'fontWeight': '600',
                           'marginBottom': '20px',
                           'marginTop': '0'
                       }),
                dcc.Graph(id='time-series-chart', config={'displayModeBar': False})
            ]),
            
            # Regional Comparison Chart Card
            html.Div(style={
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'padding': '30px',
                'border': f'1px solid {colors["border"]}',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            }, children=[
                html.H3('Regional Sales Comparison',
                       style={
                           'color': colors['text'],
                           'fontSize': '20px',
                           'fontWeight': '600',
                           'marginBottom': '20px',
                           'marginTop': '0'
                       }),
                dcc.Graph(id='regional-chart', config={'displayModeBar': False})
            ]),
        ])
    ])
])


# Callback for updating charts based on filters
@app.callback(
    [Output('time-series-chart', 'figure'),
     Output('regional-chart', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('region-filter', 'value')]
)
def update_charts(start_date, end_date, selected_region):
    # Filter data based on selections
    filtered_df = df.copy()
    
    # Convert date strings to datetime if needed
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & 
                                  (filtered_df['date'] <= end_date)]
    
    # Filter by region if not 'all'
    if selected_region and selected_region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    # Time Series Chart - Sales over time by region
    time_series_data = filtered_df.groupby(['date', 'region'])['sales'].sum().reset_index()
    
    fig_time_series = px.line(time_series_data, 
                              x='date', 
                              y='sales', 
                              color='region',
                              color_discrete_map=region_colors,
                              labels={'sales': 'Total Sales ($)', 'date': 'Date', 'region': 'Region'})
    
    fig_time_series.update_layout(
        hovermode='x unified',
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font=dict(color=colors['text'], family="'Inter', sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor=colors['border'],
            color=colors['text'],
            title_font=dict(size=13, color=colors['text_secondary'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=colors['border'],
            color=colors['text'],
            title_font=dict(size=13, color=colors['text_secondary'])
        ),
        legend=dict(
            font=dict(color=colors['text']),
            bgcolor='rgba(0,0,0,0)',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=60, r=20, t=40, b=60)
    )
    
    # Regional Comparison Chart - Total sales by region
    regional_totals = filtered_df.groupby('region')['sales'].sum().reset_index()
    regional_totals = regional_totals.sort_values('sales', ascending=False)
    
    fig_regional = go.Figure(data=[
        go.Bar(
            x=regional_totals['region'],
            y=regional_totals['sales'],
            marker_color=[region_colors.get(r, '#808080') for r in regional_totals['region']],
            text=regional_totals['sales'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            textfont=dict(color=colors['text'], size=12),
            hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
        )
    ])
    
    fig_regional.update_layout(
        xaxis_title='Region',
        yaxis_title='Total Sales ($)',
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font=dict(color=colors['text'], family="'Inter', sans-serif"),
        xaxis=dict(
            showgrid=False,
            color=colors['text'],
            title_font=dict(size=13, color=colors['text_secondary'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=colors['border'],
            color=colors['text'],
            title_font=dict(size=13, color=colors['text_secondary'])
        ),
        margin=dict(l=60, r=20, t=20, b=60)
    )
    
    return fig_time_series, fig_regional


if __name__ == '__main__':
    app.run(debug=True)
