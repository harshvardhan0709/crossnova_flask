from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://candidato:crossnova20@178.22.68.101:5434/auto'
db = SQLAlchemy(app)
# print(db.Table('auto',db.metadata))
auto_table = db.Table('auto', db.metadata, autoload = True, autoload_with=db.engine)

# class auto(db.Model):
#     __tablename__ = 'auto'
#     id  = db.Column( db.Integer, primary_key=True)
#     data = db.Column('data',db.Unicode)

# @app.route('/hello_world')
# def hello_world():
#     result = db.session.query(auto_table).all()
#     df = pd.DataFrame(result)
#     print(df['acceleration'])
#     # for r in result:
#     #     print(r)
#     return 'Hello, World!'
    

dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/'
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16],
                    mode='markers',
                    name='markers'))
#fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
fig.show()

colors = {
    'text': '#77777E'
}


dash_app.layout = html.Div(children=[
    html.H1(children='Crossnova Dashboard'),

    

    
    html.H1(children='Please Select any Two Options',
        style={
            'color': colors['text']
        }
    ),
    dcc.Checklist( id='inputs-box',
        options=[
            {'label': 'Acceleration', 'value': 'acceleration'},
            {'label': 'Cilinders', 'value': 'cilinders'},
            {'label': 'Displacement', 'value': 'displacement'},
            {'label': 'Horsepower', 'value': 'horsepower'},
            {'label': 'Model_year', 'value': 'model_year'},
            {'label': 'Weight', 'value': 'weight'},
            {'label': 'Mpg', 'value': 'mpg'}
        ],
        value=['acceleration','cilinders']
    ),
    html.Button('Load', id='button'),
    # html.Div(id='output-container-button',
    #          children='Enter a value and press submit')
    dcc.Graph(figure=fig, id='output-container-button',)
])

@dash_app.callback(
    dash.dependencies.Output('output-container-button', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('inputs-box', 'value')])
def update_output(n_clicks, value):
    result = db.session.query(auto_table).all()
    df = pd.DataFrame(result)
    x_out = df[value[0]]
    y_out = df[value[1]]
    return go.Figure(go.Scatter(x=x_out, y=y_out,
                    mode='markers',
                    name='markers'))

@app.route("/dash")
def my_dash_app():
    return dash_app.index()

# if __name__ == "__main__":
#     app.run()