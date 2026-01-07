import base64
import io
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"margin": "40px"},
    children=[
        html.H1("Дашборд менеджмента товаров в розничной торговле"),

        html.P(
            "Дашборд предназначен для анализа ключевых показателей процесса "
            "управления ассортиментом, включая выручку, расходы, прибыль и складские показатели."
        ),

        dcc.Upload(
            id="upload-data",
            children=html.Div([
                "Drag and Drop or ",
                html.A("Select CSV File")
            ]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "marginBottom": "20px"
            },
            multiple=False
        ),

        html.Div(
            style={"display": "flex", "gap": "20px"},
            children=[
                dcc.Dropdown(
                    id="category-filter",
                    placeholder="Select category"
                ),
                dcc.Dropdown(
                    id="period-filter",
                    placeholder="Select period",
                    options=[
                        {"label": "Monthly", "value": "M"},
                        {"label": "Quarterly", "value": "Q"},
                        {"label": "Yearly", "value": "Y"}
                    ],
                    value="M"
                )
            ]
        ),

        dcc.Store(id="stored-data"),

        dcc.Graph(id="line-chart"),
        dcc.Graph(id="pie-chart"),
        dcc.Graph(id="hist-chart"),
        dcc.Graph(id="scatter-chart"),

        html.H3("Financial data table"),
        html.Div(id="data-table")
    ]
)

@app.callback(
    Output("stored-data", "data"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def load_csv(contents, filename):
    if contents is None:
        return None

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    df["date"] = pd.to_datetime(df["date"])
    return df.to_dict("records")

@app.callback(
    Output("category-filter", "options"),
    Input("stored-data", "data")
)
def update_category_options(data):
    if data is None:
        return []
    df = pd.DataFrame(data)
    categories = df["category"].unique()
    return [{"label": c, "value": c} for c in categories]


@app.callback(
    [
        Output("line-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("hist-chart", "figure"),
        Output("scatter-chart", "figure"),
        Output("data-table", "children")
    ],
    [
        Input("stored-data", "data"),
        Input("category-filter", "value"),
        Input("period-filter", "value")
    ]
)
def update_dashboard(data, category, period):
    if data is None:
        return {}, {}, {}, {}, "Upload CSV file to display data"

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    if category:
        df = df[df["category"] == category]

    df = (
        df
        .set_index("date")
        .resample(period)
        .sum(numeric_only=True)
        .reset_index()
    )

    line_fig = px.line(
        df,
        x="date",
        y=["revenue", "expenses"],
        title="Динамика доходов и расходов"
    )

    pie_fig = px.pie(
        df,
        values="expenses",
        names="date",
        title="Структура расходов"
    )

    hist_fig = px.histogram(
        df,
        x="profit",
        title="Распределение прибыли"
    )

    scatter_fig = px.scatter(
        df,
        x="sales_volume",
        y="profit",
        title="Корреляция прибыли и объема продаж"
    )

    table = html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(len(df))
            ])
        ],
        style={"width": "100%", "border": "1px solid black"}
    )

    return line_fig, pie_fig, hist_fig, scatter_fig, table


if __name__ == "__main__":
    app.run(debug=True)
