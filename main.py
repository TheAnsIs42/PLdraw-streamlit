import streamlit as sl
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px
import plotly.io as pio
from scipy import signal


class dataEntry(dict):
    def __init__(self, file):
        super().__init__({"name": file.name, "data": read_data(file)})


def reloadEntry(filelist):
    sl.session_state.dataList = [dataEntry(file) for file in filelist]


def read_data(file) -> pd.DataFrame:

    h = 6.63e-34 / 1.6e-19  # eV energy
    c = 3e8
    data = pd.read_csv(file, sep=r"\s+", header=None, names=["wavelength", "count"])
    # normalize
    data["normalized"] = (data["count"] - data["count"].min()) / (
        data["count"].max() - data["count"].min()
    )
    data["energy"] = h * c / (data["wavelength"] * 1e-9)
    return data


def make_chart1(dataList):
    chart = (
        go.Figure()
        .update_xaxes(title_text="Wavelength(nm)")
        .update_yaxes(title_text="Intentsity(arb.u.)")
        .update_layout(legend=dict(x=0, y=0.5))  # legend position
    )
    colors = px.colors.qualitative.Plotly
    for idx, data in enumerate(dataList):
        # print(type(data["data"]))
        filter = signal.savgol_filter(data["data"]["normalized"], 150, 2)
        # print(data["data"]["wavelength"][filter.argmax()])
        chart.add_trace(
            go.Scatter(
                x=data["data"]["wavelength"],
                y=filter,
                name=data["name"],
                line_color=colors[idx],
            )
        )
        # chart.add_trace(
        #     go.Scatter(
        #         x=data["data"]["wavelength"],
        #         y=data["data"]["normalized"],
        #         name=data["name"],
        #         line_color=colors[idx],
        #     )
        # )
        chart.add_vline(
            x=data["data"]["wavelength"][filter.argmax()],
            line_color=colors[idx],
            annotation=dict(
                text=str(data["data"]["wavelength"][filter.argmax()]),
                textangle=90,
            ),
            annotation_position="bottom left",
        )
    # print(colors)
    chart.write_image("image/test.svg", format="svg")
    return chart


def chart2(dlist):
    chart = (
        go.Figure()
        .update_xaxes(title_text="Energy(eV)", autorange="reversed")
        .update_yaxes(title_text="Normalized Intentsity(arb.u.)")
    )
    for data in dlist:
        chart.add_trace(
            go.Scatter(x=data["data"]["energy"], y=data["data"]["normalized"])
        )
    return chart


def simpleChart(
    datas: list[dataEntry], eVplot: bool, normalize: bool, logY: bool = False
):
    chart = go.Figure().update_layout(legend=dict(x=0, y=0.5))  # legend position
    # print("redraw")
    if eVplot:
        dataX = "energy"
        chart.update_xaxes(title_text="Energy (eV)", autorange="reversed")
    else:
        dataX = "wavelength"
        chart.update_xaxes(title_text="Wavelength (nm)")
    if normalize:
        dataY = "normalized"
        chart.update_yaxes(title_text="Normalized intentsity (arb.u.)")
    else:
        dataY = "count"
        chart.update_yaxes(title_text="Intentsity (arb.u.)")
    if logY:
        chart.update_yaxes(type="log", minor=dict(ticks="inside", showgrid=True))
    for data in datas:
        chart.add_trace(
            go.Scatter(x=data["data"][dataX], y=data["data"][dataY], name=data["name"])
        )
    chart.write_image("image/simple.svg")
    return chart


# sl.session_state.upload_files = sl.file_uploader(
# "upload",
# accept_multiple_files=True,
# on_change=reloadEntry(sl.session_state.upload_files),
# )

pio.templates.default = "plotly_white"  # only control download chart theme
if "dataList" not in sl.session_state:
    sl.session_state.dataList = []
if "upload_files" not in sl.session_state:
    sl.session_state.upload_files = []
reloadEntry(sl.file_uploader("upload", accept_multiple_files=True))


# sl.dataframe(
#     sl.session_state.dataList,
#     column_config={"name": "name", "data": None},
#     hide_index=False,
# )
# print(sl.session_state.dataList)
tab1, tab2 = sl.tabs(["simple plot", "smooth & peak"])
with tab1:
    col1, col2, col3 = sl.columns(3)
    with col1:
        eVplot = sl.toggle("Energy plot")
    with col2:
        normalize = sl.toggle("Normalizing")
    with col3:
        logY = sl.toggle("Log Y axis")
    sl.plotly_chart(
        simpleChart(
            sl.session_state.dataList, eVplot=eVplot, normalize=normalize, logY=logY
        )
    )
    with open("image/simple.svg", "rb") as file:
        sl.download_button(
            "save figure", data=file, file_name="simple.svg", mime="image/svg"
        )

with tab2:
    # ...
    sl.toggle("placeholder")  # placeholder for the same height chart
    # sl.container(height=40) #other way for placeholder
    sl.plotly_chart(make_chart1(sl.session_state.dataList))
    with open("image/test.svg", "rb") as file:
        sl.download_button(
            "save figure", data=file, file_name="smooth.svg", mime="image/svg"
        )
