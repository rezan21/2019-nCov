from flask import Flask, render_template, url_for
import json
import plotly
# import chart_studio.plotly as py
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


app = Flask(__name__)

def plot_cnfrmd_frame():
    # crate figure as usual
    df_cnfrmd = pd.read_csv("data/df_cnfrmd_proc.csv")
    fig = px.scatter_geo(df_cnfrmd, locations="Country_Code",
                        hover_name="Country", size="Cases",
                        animation_frame="Time_Stamp",
                        projection="natural earth"
                        #,width=1100, height=700
                        )

    fig.update_layout(
            title = go.layout.Title(
            text = '<b>2019-nCoV</b>: Coronavirus disease 2019-20<br>Study <i>Excludes</i> cases in China'),
            showlegend = True,

        )

    # convert to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON # return JSON

def plot_world_wide():
    df = pd.read_csv("data/visuals_02.csv")
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

def plot_exc_china():
    df = pd.read_csv("data/visuals_02.csv")
    china = df[df["Country/Region"]=="Mainland China"].drop("Country/Region",axis=1)
    timestamp_grouped_exc_china = df.drop(china.index).reset_index(drop=True)
    timestamp_grouped_exc_china = timestamp_grouped_exc_china.groupby("timestamp").sum().sort_values("timestamp", ascending=True)
    timestamp_grouped_exc_china.reset_index(inplace=True)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["conf_cases"], name='Confirmed Cases',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["recov_cases"], name='Recovered Cases',
                            line=dict(width=3)))
    fig.add_trace(go.Scatter(x=timestamp_grouped_exc_china["timestamp"], y=timestamp_grouped_exc_china["death_cases"], name='Death Cases',
                            line=dict(width=3)))

    fig.update_layout(title='CoronaVirus Performance over Time (Excluding China)',
                    xaxis_title='Time',
                    yaxis_title='Number of Cases (Persons)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_barchart():
    df = pd.read_csv("data/visuals_02.csv")
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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/confirmed-cases')
def confirmed_cases():
    cnfrmd_frame = plot_cnfrmd_frame()
    world_wide_plot= plot_world_wide()
    exc_china_plot = plot_exc_china()
    barchart_plot = plot_barchart()
    return render_template('confirmed_cases.html',
                            cnfrmd_frame=cnfrmd_frame,
                            world_wide_plot=world_wide_plot,
                            exc_china_plot=exc_china_plot,
                            barchart_plot=barchart_plot
                        )


if __name__ == '__main__':
    app.run(debug=True)