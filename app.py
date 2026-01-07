import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

data = {
    "date": pd.date_range(start="2024-01-01", periods=10, freq="M"),
    "revenue": [120000, 135000, 128000, 150000, 160000, 158000, 170000, 175000, 180000, 190000],
    "expenses": [90000, 95000, 92000, 100000, 105000, 103000, 110000, 112000, 115000, 118000],
    "profit": [30000, 40000, 36000, 50000, 55000, 55000, 60000, 63000, 65000, 72000],
    "sales_volume": [800, 820, 790, 860, 900, 890, 920, 940, 960, 1000],
    "stock_level": [500, 480, 470, 450, 430, 420, 400, 390, 380, 360]
}

df = pd.DataFrame(data)

expense_structure = pd.DataFrame({
    "category": ["Закупка товара", "Логистика", "Хранение", "Маркетинг", "Прочее"],
    "value": [55, 15, 10, 12, 8]
})

# Линейный график: доходы и расходы
line_fig = px.line(
    df,
    x="date",
    y=["revenue", "expenses"],
    title="Динамика доходов и расходов"
)

# Круговая диаграмма: структура расходов
pie_fig = px.pie(
    expense_structure,
    names="category",
    values="value",
    title="Структура расходов"
)

# Гистограмма прибыли
hist_fig = px.histogram(
    df,
    x="profit",
    nbins=5,
    title="Распределение прибыли"
)

# График рассеяния: прибыль vs объем продаж
scatter_fig = px.scatter(
    df,
    x="sales_volume",
    y="profit",
    title="Корреляция прибыли и объема продаж"
)

table = html.Table(
    [
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody(
            [
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(len(df))
            ]
        )
    ],
    style={"width": "100%", "border": "1px solid black"}
)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Дашборд менеджмента товаров в розничной торговле"),

        html.P(
            "Дашборд предназначен для анализа ключевых показателей процесса "
            "управления ассортиментом, включая выручку, расходы, прибыль и складские показатели."
        ),

        dcc.Graph(figure=line_fig),
        dcc.Graph(figure=pie_fig),
        dcc.Graph(figure=hist_fig),
        dcc.Graph(figure=scatter_fig),

        html.H3("Ключевые показатели по периодам"),
        table
    ],
    style={"margin": "40px"}
)

if __name__ == "__main__":
    app.run(debug=True)
