import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import os

path = "/home/ec2-user/ADV_Git_Project/"


app = dash.Dash(__name__)
app.title = "BTC Dashboard"

background_color = "#0d1117"
text_color = "#f5f5f5"
accent_color = "#00ffcc"

app.layout = html.Div([
<<<<<<< HEAD
    html.H1("Dashboard Bitcoin(ABC Bourse)", style={
=======
    html.H1("Dashboard Bitcoin (ABC Bourse)", style={
>>>>>>> 6c43c2c0d1c32f1efe9640a468bc7892f46abce7
        "textAlign": "center",
        "color": accent_color,
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "marginTop": "20px"
    }),

    dcc.Graph(id='btc-graph', config={"displayModeBar": False}, style={"margin": "20px"}),
    dcc.Graph(id='volatility-graph', config={"displayModeBar": False}, style={"margin": "20px"}),
    dcc.Graph(id='price-change-graph', config={"displayModeBar": False}, style={"margin": "20px"}),

    html.Div(id="last-update", style={
        "color": text_color,
        "fontSize": "12px",
        "textAlign": "center",
        "marginTop": "10px",
        "fontStyle": "italic"
    }),

    html.Div(id="daily-report", style={
        "padding": "20px",
        "color": text_color,
        "backgroundColor": "#1a1f2b",
        "borderRadius": "10px",
        "margin": "30px auto",
        "width": "85%",
        "boxShadow": "0px 0px 15px rgba(0,255,204,0.2)",
        "fontFamily": "'Courier New', Courier, monospace"
    }),

    dcc.Interval(
        id='interval-component',
        interval=150 * 1000,
        n_intervals=0
    )
], style={"backgroundColor": background_color, "minHeight": "100vh"})

@app.callback(
    [Output('btc-graph', 'figure'),
     Output('volatility-graph', 'figure'),
     Output('price-change-graph', 'figure'),
     Output('last-update', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    try:
        df = pd.read_csv(f'{path}data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price_eur'],
            mode='lines+markers',
            name='Prix BTC (€)',
            line=dict(color='lime')
        ))
        fig_price.update_layout(
            title="Prix du Bitcoin",
            xaxis_title='Heure',
            yaxis_title='Prix (€)',
            template='plotly_dark'
        )

        df['volatility_pct'] = df['price_eur'].pct_change().rolling(window=5).std() * 100
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['volatility_pct'],
            mode='lines',
            name='Volatilité (%)',
            line=dict(color='orange')
        ))
        fig_vol.update_layout(
            title="Volatilité (rolling std %)",
            xaxis_title='Heure',
            yaxis_title='Volatilité (%)',
            template='plotly_dark'
        )

        df['price_diff'] = df['price_eur'].diff()
        fig_diff = go.Figure()
        fig_diff.add_trace(go.Bar(
            x=df['timestamp'],
            y=df['price_diff'],
            name='Variation',
            marker_color='dodgerblue'
        ))
        fig_diff.update_layout(
<<<<<<< HEAD
            title=" Variation de prix",
=======
            title="Variation de prix",
>>>>>>> 6c43c2c0d1c32f1efe9640a468bc7892f46abce7
            xaxis_title='Heure',
            yaxis_title='Différence (€)',
            template='plotly_dark'
        )

        return fig_price, fig_vol, fig_diff, f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}"

    except Exception as e:
        empty_fig = go.Figure().add_annotation(
            text=f"Erreur : {e}",
            xref="paper", yref="paper", showarrow=False,
            font=dict(size=20, color="red")
        )
        return empty_fig, empty_fig, empty_fig, "Erreur"

@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_daily_report(n):
    if os.path.exists(f"{path}daily_report.csv"):
        try:
            report = pd.read_csv(f"{path}daily_report.csv")
            latest = report.iloc[-1]
            return html.Div([
                html.H3("Rapport quotidien (20h00)", style={"color": accent_color, "textAlign": "center"}),
                html.Div([
                    html.Div([
                        html.H4("Ouverture"),
                        html.P(f"{latest['open']:.2f} €")
                    ], style={"padding": "10px", "flex": "1"}),
                    html.Div([
                        html.H4("Clôture"),
                        html.P(f"{latest['close']:.2f} €")
                    ], style={"padding": "10px", "flex": "1"}),
                    html.Div([
                        html.H4("Variation"),
                        html.P(f"{latest['evolution_percent']:.2f}%")
                    ], style={"padding": "10px", "flex": "1"})
                ], style={"display": "flex", "justifyContent": "space-around", "marginTop": "20px"}),
                html.Hr(style={"borderTop": "1px solid #555"}),
                html.P(f"Min : {latest['min']:.2f} €"),
                html.P(f"Max : {latest['max']:.2f} €"),
                html.P(f"Moyenne : {latest['mean']:.2f} €"),
                html.P(f"Volatilité : {latest['volatility']:.4f}")
            ])
        except Exception as e:
            return html.P(f"Erreur dans le rapport : {e}", style={"color": "red"})
    else:
        return html.P("Aucun rapport disponible.", style={"color": "gray"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)