from flask import Flask, render_template, url_for
from plots import plot_animation, plot_china_world_graph, plot_barchart, plot_death_rate,\
plot_recov_rate, plot_recov_donut, plot_death_donut
# from plots import plot_worldwide_graph
import os
app = Flask(__name__)

@app.route('/')
def visuals():
    animation_frame = plot_animation()
    #worldwide_graph = plot_worldwide_graph()
    china_world_graph = plot_china_world_graph()
    barchart = plot_barchart()
    death_rate_chart = plot_death_rate()
    recov_rate_chart = plot_recov_rate()
    recov_donut = plot_recov_donut()
    death_donut = plot_death_donut()
    return render_template('visuals.html',
                            animation_frame=animation_frame,
                            #worldwide_graph=worldwide_graph,
                            china_world_graph=china_world_graph,
                            barchart=barchart,
                            death_rate_chart=death_rate_chart,
                            recov_rate_chart=recov_rate_chart,
                            recov_donut=recov_donut,
                            death_donut=death_donut

                        )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)