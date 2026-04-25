import datetime
import pandas as pd
from analysis import *
import streamlit as st
import plotly.graph_objects as go

df = pd.read_csv(r'.\data\Occupancy_Estimation_Prediction.csv')
df = df.iloc[:8084]
df[DATETIME] = df[DATETIME].map(lambda string: datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S'))
Y_LEGEND_POS = 1.3
X_LEGEND_POS = 1.22
st.set_page_config(layout="wide")
st.title("📊 Room Occupancy Signal Dashboard")
cols = st.columns(3)

for column_index, (measurement_columns, measurement_string) in enumerate(zip(MEASUREMENTS_COLUMNS_GROUPS, MEASUREMENTS_STRINGS)):
    data = list()
    for i, (sensor, color) in enumerate(zip(measurement_columns, SENSORS_COLORS)):
        sensor_scatter = go.Line(
            x=df[DATETIME],
            y=df[sensor],
            line=dict(color=color),
            name=f'Sensor {i+1}'
        )
        data.append(sensor_scatter)
    fig = go.Figure(data=data)
    # Label line (secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=df[DATETIME],
            y=np.int32(df[LABEL].values),
            mode="lines",
            name="#People",
            yaxis="y2",
            line=dict(color="green")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[DATETIME],
            y=np.int32(df[PREDICTION].values),
            mode="lines",
            name="Prediction",
            yaxis="y2",
            line=dict(dash="dot", color='orange')
        )
    )
    fig.update_layout(
        title=f'{measurement_string} Over Time',
        xaxis_title="Time",
        yaxis=dict(title="Sensor Measurement"),
        yaxis2=dict(
            title="#People",
            overlaying="y",
            side="right",
            tickvals=np.arange(4)
        ),
        height=350,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    fig.update_layout(legend=dict(
        yanchor="top",
        y=Y_LEGEND_POS,
        xanchor="right",
        x=X_LEGEND_POS
    ))
    time_min = df[DATETIME].min()
    time_min = time_min - datetime.timedelta(hours=time_min.hour, minutes=time_min.minute, seconds=time_min.second)
    ticks = pd.date_range(time_min, df[DATETIME].max(), freq="6H")
    fig.update_xaxes(
        tickmode="array",
        tickvals=ticks,
        ticktext=[t.strftime("%H:00\n%d-%m") for t in ticks],
        tickangle=45,
    )
    cols[column_index].plotly_chart(fig, use_container_width=True)
    fig.write_html(f"./data/{measurement_string}.html")
