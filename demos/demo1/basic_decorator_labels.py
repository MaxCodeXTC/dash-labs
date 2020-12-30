import dash
import dash_express as dx
import numpy as np
import dash_core_components as dcc
import plotly.express as px

app = dash.Dash(__name__)


@dx.parameterize(
    app,
    inputs=dict(
        fun=["sin", "cos", "exp"], figure_title="Initial Title",
        phase=(1, 10), amplitude=(1, 10),
    ),
    labels=dict(
        fun="Function",
        figure_title="Figure Title",
        phase="Phase: {:.2f}",
        amplitude="Amplitude: {:.2f}"
    )
)
def greet(fun, figure_title, phase, amplitude):
    xs = np.linspace(-10, 10, 100)
    return dcc.Graph(figure=px.line(
        x=xs, y=getattr(np, fun)(xs + phase) * amplitude
    ).update_layout(title_text=figure_title))

app.layout = greet.layout(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=9102)