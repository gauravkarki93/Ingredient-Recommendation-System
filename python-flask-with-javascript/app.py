from __future__ import print_function
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for

import io
import os
import uuid
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from recipe_api import RecipeApi
import json
#import recipe_api as ra

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True
app._static_folder = os.path.abspath("templates/static/")
apiObj = RecipeApi()
training_set = apiObj.recreateTrainingSet("data/pickledGroundTruth005gtsch.pkl")
print(len(training_set))

@app.route('/', methods=['GET'])
def index():
    title = 'Create these input'
    return render_template('layouts/index.html',
                           title=title)

@app.route('/results/<uuid>', methods=['GET'])
def results(uuid):
    title = 'Result'
    data = get_file_content(uuid)
    return render_template('layouts/results.html',
                           title=title,
                           data=data)

@app.route('/getIngredients', methods=['GET'])
def getIngredients():
    title = 'Get Ingredients'
    path = 'data/pickledIDX005gtsch.pkl'
    ingrList = apiObj.getListofIngredients(path)
    jsonResp = {'data': ingrList}
    print(jsonify(jsonResp))
    return jsonify(jsonResp)

@app.route('/recommendTopIngr', methods = ['POST'])
def post_javascript_data():
    str = request.form['list_ingr']
    myList = json.loads(str)
    print("input list =", myList)
    print("type input =",type(myList))
    arhr, topKFinding = apiObj.predict(myList, "data/pickledRules005gtsch.pkl", training_set, "data/pickledGroundTruth005gtsch.pkl")
    recommend = []
    for tuple in topKFinding:
        if len(tuple[0]) == 1:
            recommend.append(tuple[0])
    print("Arhr =", arhr)
    print("top k ingr=", recommend)
    data = {}
    data[arhr] = recommend
    json_data = json.dumps(data)
    return json_data

@app.route('/plot/<imgdata>')
def plot(imgdata):
    data = [float(i) for i in imgdata.strip('[]').split(',')]
    data = np.reshape(data, (200, 200))
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.axis('off')
    axis.imshow(data, interpolation='nearest')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open('images/'+unique_id+'.csv', 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

def get_file_content(uuid):
    with open('images/'+uuid+'.csv', 'r') as file:
        return file.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
