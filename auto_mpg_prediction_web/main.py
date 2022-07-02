import pickle
from flask import Flask, render_template, request, url_for
from model_files.ml_model import predict_mpg
import os

app = Flask("mpg_prediction_app")

@app.route('/', methods= ['GET', 'POST'])
def predict():
    if request.method == "POST":
        n_o_c = request.form.get('n_o_c')
        displacement = request.form.get('displacement')
        horsepower = request.form.get('horsepower')
        weight = request.form.get('weight')
        acceleration = request.form.get('acceleration')
        model_year = request.form.get('model_year')
        origin = request.form.get('origin')
        if int(origin) == 3:
            vehicle_config ={
            'Cylinders' : [int(n_o_c), 6, 8],
            'Displacement' : [float(displacement), 160.0, 165.0],
            'Horsepower' : [float(horsepower), 130.0, 98.0],
            'Weight' : [float(weight), 3150.0, 2600.0],
            'Acceleration' : [float(acceleration), 14.0, 16.0],
            'Model Year' : [int(model_year), 80, 78],
            'Origin' : [int(origin), 2, 1]
            }
        elif int(origin) == 2:
            vehicle_config ={
            'Cylinders' : [int(n_o_c), 6, 8],
            'Displacement' : [float(displacement), 160.0, 165.0],
            'Horsepower' : [float(horsepower), 130.0, 98.0],
            'Weight' : [float(weight), 3150.0, 2600.0],
            'Acceleration' : [float(acceleration), 14.0, 16.0],
            'Model Year' : [int(model_year), 80, 78],
            'Origin' : [int(origin), 3, 1]
            }
        elif int(origin) == 1:
            vehicle_config ={
            'Cylinders' : [int(n_o_c), 6, 8],
            'Displacement' : [float(displacement), 160.0, 165.0],
            'Horsepower' : [float(horsepower), 130.0, 98.0],
            'Weight' : [float(weight), 3150.0, 2600.0],
            'Acceleration' : [float(acceleration), 14.0, 16.0],
            'Model Year' : [int(model_year), 80, 78],
            'Origin' : [int(origin), 2, 3]
            }

        with open('./model_files/model.bin', 'rb') as f_in:
            model = pickle.load(f_in)
            f_in.close()

        predictions = predict_mpg(vehicle_config, model)

        return render_template('result.html', vehicle_config= vehicle_config, predictions= predictions)


    return render_template('home.html')

# @app.route('/favicon.ico')
# def favicon():
#     return url_for("static/favicon.ico")

if __name__ == '__main__':
    app.run(debug= True)