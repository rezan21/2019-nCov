import json
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

animation_df = pd.read_csv("/tmp/myfolder/frame_animation_df.csv")
general_df = pd.read_csv("./app_data/general_df.csv")

def plot_animation(df=animation_df):
    fig = px.scatter_geo(df, locations="Country_Code",
                        hover_name="Country", size="Cases",
                        animation_frame="Time_Stamp",
                        projection="natural earth"
                        #,width=1100, height=700
                        )

    fig.update_layout(
            title = go.layout.Title(
            text = '<b>2019-nCoV</b>:Worldwide Periodic Confirmed Cases<br>Graph <i>Excludes</i> cases in China'),
            showlegend = True,

        )

    # convert to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON # return JSON

def plot_worldwide_graph(df=general_df):
    timestamp_grouped = df.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
    timestamp_grouped.reset_index(inplace=True)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["conf_cases"], name='Confirmed Cases',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["recov_cases"], name='Recovered Cases',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["death_cases"], name='Death Cases',
                            line=dict(width=3)))

    fig.update_layout(title='CoronaVirus Performance over Time (Worldwide)',
                    xaxis_title='Time',
                    yaxis_title='Number of Cases (Persons)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



def plot_china_world_graph(df=general_df):
    china = df[df["Country/Region"]=="Mainland China"].drop("Country/Region",axis=1)
    timestamp_grouped_exc_china = df.drop(china.index).reset_index(drop=True)
    timestamp_grouped_exc_china = timestamp_grouped_exc_china.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
    timestamp_grouped_exc_china.reset_index(inplace=True)

    china = df[df["Country/Region"]=="Mainland China"].drop("Country/Region",axis=1)
    china = china.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
    china.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["conf_cases"], name='Confirmed Cases (Excluding China)',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=china["timestamp"], y=china["conf_cases"], name="China's Confirmed Cases",
                            line=dict(width=3, dash="dash")))

    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["recov_cases"], name='Recovered Cases (Excluding China)',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=china["timestamp"], y=china["recov_cases"], name="China's Recovered Cases",
                            line=dict(width=3, dash="dash")))

    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["death_cases"], name='Death Cases (Excluding China)',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=china["timestamp"], y=china["death_cases"], name="China's Death Cases",
                            line=dict(width=3, dash="dash")))


    fig.update_layout(title='CoronaVirus: Global & China',
                    xaxis_title='Time',
                    yaxis_title='Number of Cases (Persons)')



    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_barchart(df=general_df):
    # latest stat of each country
    countries = df["Country/Region"].unique()
    country_grouped = df.groupby("Country/Region") # group by country
    countries_stat = []
    for country in countries:
        countries_stat.append(country_grouped.get_group(country).sort_values("timestamp", ascending=False).iloc[0]) # for each group get the latest stat

    countries_stat = pd.DataFrame(countries_stat).reset_index(drop=True)
    china = countries_stat[countries_stat["Country/Region"]=="Mainland China"].index
    countries_stat.drop(china,axis=0,inplace=True)
    other = countries_stat[countries_stat["Country/Region"]=="Others"].index
    countries_stat.drop(other,axis=0,inplace=True)



    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=countries_stat["Country/Region"],
        y=countries_stat["conf_cases"],
        name='Confirmed Cases',
    # marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=countries_stat["Country/Region"],
        y=countries_stat["recov_cases"],
        name='Recovered Cases',
        marker_color='lightgreen',


    ))
    fig.add_trace(go.Bar(
        x=countries_stat["Country/Region"],
        y=countries_stat["death_cases"],
        name='Death Cases',
        marker_color='red',


    ))

    fig.update_layout(title='CoronaVirus: Ratios<br><span style="font-size:80%">Excluding China</span>',
                    xaxis_title='Country',
                    yaxis_title='Number of Cases (Persons)')
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-55)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON