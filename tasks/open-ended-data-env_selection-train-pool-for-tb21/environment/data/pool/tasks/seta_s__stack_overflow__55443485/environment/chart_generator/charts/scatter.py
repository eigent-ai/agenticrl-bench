import altair as alt
from vega_datasets import data


def build_scatter():
    source = data.cars()

    chart = (
        alt.Chart(source)
        .mark_point()
        .encode(
            x=alt.X("Horsepower:Q", title="Horsepower"),
            y=alt.Y("Miles_per_Gallon:Q", title="Miles per Gallon"),
            color=alt.Color(
                "Name:N",
                legend=alt.Legend(title="Car Model", columns=1),
            ),
        )
        .properties(
            title="Car Performance by Model",
            width=250,
            height=150,
        )
        .configure_title(fontSize=8)
    )
    return chart
