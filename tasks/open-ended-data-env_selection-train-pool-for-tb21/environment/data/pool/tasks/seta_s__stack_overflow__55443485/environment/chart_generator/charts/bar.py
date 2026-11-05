import altair as alt
from vega_datasets import data


def build_bar():
    source = data.wheat()

    chart = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("wheat:Q", title="Wheat Price (shillings)"),
            color=alt.Color("wages:Q", scale=alt.Scale(scheme="blues")),
        )
        .properties(
            title="Wheat and Wages Over Time",
            width=200,
            height=100,
        )
        .configure_title(fontSize=8)
    )
    return chart
