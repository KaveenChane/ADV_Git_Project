import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import os

app = dash.Dash(__name__)
app.title = "BTC Dashboard"

app.layout = html.Div([
    html.H1("Prix du Bitcoin (ABC Bourse)", style={"textAlign": "center"}),

    dcc.Graph(id='btc-graph'),
    dcc.Graph(id='volatility-graph'),
    dcc.Graph(id='price-change-graph'),

    html.Div(id="last-update", style={"color": "gray", "fontSize": "12px", "textAlign": "center", "marginTop": "10px"}),

    html.Div(id="daily-report", style={"padding": "20px", "color": "white", "backgroundColor": "#1e1e1e"}),

    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # ⏱ rafraîchit toutes les 10 secondes
        n_intervals=0
    )
])

@app.callback(
    [Output('btc-graph', 'figure'),
     Output('volatility-graph', 'figure'),
     Output('price-change-graph', 'figure'),
     Output('last-update', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    try:
        df = pd.read_csv('data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Graph prix
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price_eur'],
            mode='lines+markers',
            name='Prix BTC (€)',
            line=dict(color='orange')
        ))
        fig_price.update_layout(
            title="Prix du Bitcoin",
            xaxis_title='Heure',
            yaxis_title='Prix (€)',
            template='plotly_dark'
        )

        # Volatilité en pourcentage
        df['volatility_pct'] = df['price_eur'].pct_change().rolling(window=5).std() * 100
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['volatility_pct'],
            mode='lines',
            name='Volatilité (%)',
            line=dict(color='purple')
        ))
        fig_vol.update_layout(
            title="Volatilité (rolling std %)",
            xaxis_title='Heure',
            yaxis_title='Volatilité (%)',
            template='plotly_dark'
        )

        # Variation de prix
        df['price_diff'] = df['price_eur'].diff()
        fig_diff = go.Figure()
        fig_diff.add_trace(go.Bar(
            x=df['timestamp'],
            y=df['price_diff'],
            name='Variation',
            marker_color='lightblue'
        ))
        fig_diff.update_layout(
            title="Variation de prix (vs. précédent)",
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
    if os.path.exists("daily_report.csv"):
        try:
            report = pd.read_csv("daily_report.csv")
            latest = report.iloc[-1]
            return html.Div([
                html.H3("Rapport quotidien (20h)", style={"color": "#00ffcc", "textAlign": "center"}),
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
                ], style={"display": "flex", "justifyContent": "space-around"}),
                html.Hr(),
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
    app.run(debug=True)
