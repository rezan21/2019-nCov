from flask import Flask, render_template, url_for
from plots import plot_animation,plot_worldwide_graph,plot_china_world_graph,plot_barchart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/confirmed-cases')
def confirmed_cases():
    animation_frame = plot_animation()
    worldwide_graph = plot_worldwide_graph()
    china_world_graph = plot_china_world_graph()
    barchart = plot_barchart()
    return render_template('confirmed_cases.html',
                            animation_frame=animation_frame,
                            worldwide_graph=worldwide_graph,
                            china_world_graph=china_world_graph,
                            barchart=barchart
                        )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)