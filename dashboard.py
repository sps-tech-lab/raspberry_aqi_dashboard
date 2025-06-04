import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

app = Dash(__name__)
server = app.server

file_path = "~/dashboard/dust_log.csv"

def load_data(hours):
    df = pd.read_csv(file_path, sep='\t')
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    time_range = datetime.now() - timedelta(hours=hours)
    return df[df["Timestamp"] >= time_range]

app.layout = html.Div(
    style={
        'backgroundColor': '#1e1e1e',
        'padding': '20px',
        'color': '#ffffff',
        'fontFamily': 'Arial',
        'minHeight': '100vh'
    },
    children=[
        html.H1("Air Quality", style={'textAlign': 'center'}),
        html.Div(
            dcc.Dropdown(
                id='range-selector',
                options=[
                    {'label': '24h', 'value': 24},
                    {'label': '12h', 'value': 12},
                    {'label': '6h', 'value': 6},
                    {'label': '3h', 'value': 3},
                    {'label': '1h', 'value': 1},
                ],
                value=24,
                clearable=False,
                style={'width': '120px', 'margin': '0 auto', 'color': '#000'}
            ),
            style={'textAlign': 'center', 'marginBottom': '20px'}
        ),
        html.Div(id='latest-values', style={
            'textAlign': 'center',
            'fontSize': '20px',
            'marginBottom': '20px'
        }),
        dcc.Interval(id='interval', interval=60000, n_intervals=0),
        dcc.Graph(
            id='pm-graph',
            style={
                'backgroundColor': '#1e1e1e',
                'padding': '10px',
                'borderRadius': '8px'
            }
        ),
        html.Div(
            "SPS :: 2025 ",
            style={
                'textAlign': 'center',
                'fontSize': '8px',
                'marginTop': '40px',
                'color': '#888'
            }
        )
    ]
)

@app.callback(
    [Output('pm-graph', 'figure'),
     Output('latest-values', 'children')],
    [Input('interval', 'n_intervals'),
     Input('range-selector', 'value')]
)
def update_graph(n, selected_range):
    df = load_data(selected_range)
    if df.empty:
        return go.Figure(), "No data available"

    pm25 = df["PM2.5 (µg/m³)"]
    pm10 = df["PM10 (µg/m³)"]
    time = df["Timestamp"]

    last_pm25 = pm25.iloc[-1]
    last_pm10 = pm10.iloc[-1]
    last_time = time.iloc[-1].strftime("%Y-%m-%d %H:%M")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=pm25, name='PM2.5', line=dict(color='#00a2ff')))
    fig.add_trace(go.Scatter(x=time, y=pm10, name='PM10', line=dict(color='#ff9a00')))

    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Time',
        yaxis_title='µg/m³',
        xaxis=dict(showgrid=True, gridcolor='gray'),
        yaxis=dict(showgrid=True, gridcolor='gray'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            bgcolor='#1e1e1e'
        )
    )

    latest_info = f"PM2.5: {last_pm25:.1f} µg/m³ | PM10: {last_pm10:.1f} µg/m³"
    return fig, latest_info

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
