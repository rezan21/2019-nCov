import json
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

animation_df = pd.read_csv("app_data/frame_animation_df.csv")
general_df = pd.read_csv("app_data/general_df.csv")
df_death = pd.read_csv("app_data/df_death.csv")
df_recov = pd.read_csv("app_data/df_recov.csv")
df_grouped = pd.read_csv("app_data/df_grouped.csv")



def plot_animation(df=animation_df):
    fig = px.scatter_geo(df, locations="Country_Code",
                        hover_name="Country", size="Cases",
                        animation_frame="Time_Stamp",
                        projection="natural earth"
                        #,width=1100, height=700
                        )

    fig.update_layout(
            title = go.layout.Title(
            text = '<b>2019-nCoV</b>:Worldwide Periodic Confirmed Cases'),
            showlegend = True,

        )

    # convert to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON # return JSON

# def plot_worldwide_graph(df=general_df):
#     timestamp_grouped = df.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
#     timestamp_grouped.reset_index(inplace=True)


#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["conf_cases"], name='Confirmed Cases',
#                             line=dict(width=3)))
#     fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["recov_cases"], name='Recovered Cases',
#                             line=dict(width=3)))
#     fig.add_trace(go.Scatter(x=timestamp_grouped["timestamp"], y=timestamp_grouped["death_cases"], name='Death Cases',
#                             line=dict(width=3)))

#     fig.update_layout(title='CoronaVirus Performance over Time (Worldwide)',
#                     xaxis_title='Time',
#                     yaxis_title='Number of Cases (Persons)')

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON

def plot_china_world_graph(df=general_df):
    china = df[df["Country/Region"]=="China"].drop("Country/Region",axis=1)
    timestamp_grouped_exc_china = df.drop(china.index).reset_index(drop=True)
    timestamp_grouped_exc_china = timestamp_grouped_exc_china.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
    timestamp_grouped_exc_china.reset_index(inplace=True)

    china = df[df["Country/Region"]=="China"].drop("Country/Region",axis=1)
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

    fig.update_layout(title='CoronaVirus: Ratios',
                    xaxis_title='Country',
                   # yaxis_title='Number of Cases (Persons)'
                    showlegend=False)
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-55)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_death_rate(df_death=df_death):
    final_date = df_death["timestamp"].iloc[0]
    fig = px.bar(df_death, x='Country/Region', y='death_rate',hover_data=["death_cases", "conf_cases"])
    fig.update_layout(title_text='Death Rate By Country')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_recov_rate(df_recov=df_recov):
    fig = px.bar(df_recov, x='Country/Region', y='recover_rate', hover_data=["recov_cases", "conf_cases"] )
    fig.update_layout(title_text='Recover Rate By Country')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_recov_donut(df=df_grouped):
    labels1 = ['Recovered','Non-Recovered']
    values1 = [df["recov_cases"].sum(),df["conf_cases"].sum()-df["recov_cases"].sum()]

    fig = go.Figure(data=[go.Pie( labels=labels1,values=values1, hole=0.8)])
    fig.update_layout(title_text='Overall Recovery Ratio',showlegend=False)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_death_donut(df=df_grouped):
    labels2 = ['Dead','Alive']
    values2 = [df["death_cases"].sum(),df["conf_cases"].sum()-df["death_cases"].sum()]

    fig = go.Figure(data=[go.Pie( labels=labels2,values=values2, hole=0.8)])
    fig.update_layout(title_text='Overall Mortality Ratio',showlegend=False
    #width=330, height=330
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

