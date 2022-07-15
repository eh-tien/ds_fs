import os
import pathlib
from flask import Flask, render_template, request, redirect
import pickle
import numpy as np
import sklearn

app = Flask(__name__, template_folder='templates')

@app.route('/')
def route_page():
    return redirect('/api/get_woz_value')

@app.route('/api/get_woz_value')
def hello_world():
    return render_template(template_name_or_list='home.html')

def predictor(list_to_predict):
    to_predict = np.array(list_to_predict).reshape(1,7)
    loaded_model = pickle.load(open('model.pkl', 'rb'))
    result = loaded_model.predict(to_predict)

    return round(result[0],2)

result=100
@app.route('/api/get_woz_value', methods=['POST', 'GET'])
def output():
    if request.method == "POST":
        list_to_predict = request.form.to_dict()
        list_to_predict = list(list_to_predict.values())
        list_to_predict = list(map(float, list_to_predict))

        result = predictor(list_to_predict)
        result = f'Average WOZ value: €{result}'

        print(request.form.to_dict())

        return render_template("home.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
