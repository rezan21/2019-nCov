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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/confirmed-cases')
def confirmed_cases():
    cnfrmd_frame = plot_cnfrmd_frame()
    return render_template('confirmed_cases.html', figure=cnfrmd_frame)


if __name__ == '__main__':
    app.run(debug=True)