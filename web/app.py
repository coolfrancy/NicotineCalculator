from flask import Flask, render_template, request, jsonify, abort, redirect
from nicotine_calculator.calculator import nicotine_calculation
from queries.vape_history import get_all_history_data, save_history
from datetime import datetime


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extract form data
        air_inhaled = float(request.form.get('air_inhaled'))
        nicotine_concentration_mg_per_ml = float(request.form.get('nicotine_concentration_mg_per_ml'))
        temperature_celsius = float(request.form.get('temperature'))
        date = datetime.now()
        
        # Calculate total nicotine inhaled
        total_nicotine_inhaled = nicotine_calculation(air_inhaled, temperature_celsius, nicotine_concentration_mg_per_ml)


        # Save the data to vape history
        save_history(
            1, 1,
            nicotine_concentration_mg_per_ml,
            total_nicotine_inhaled, air_inhaled, temperature_celsius, date
        )
        
        return redirect('/')
    
    # GET request - display the page
    stored_data = stored_data=get_all_history_data()
    return render_template('home.html', stored_data=stored_data)

@app.route("/add", methods=['POST'])
def add():

    r_data = request.get_json(silent=True)
    print(f'Got information: {r_data}' )

    required_keys = ['nicotine_concentration_mg_per_ml', 'vape_id', 'user_id', 'date', 'air_inhaled', "temperature_celsius"]

    # Check that the request has all the required information
    for key in required_keys:
        if r_data.get(key) is None:
            abort(400, description=f"Missing required parameter: {key}")

    air_inhaled = r_data.get('air_inhaled')
    temperature_celsius = r_data.get('temperature_celsius')
    user_id = r_data.get('user_id')
    vape_id = r_data.get('vape_id')
    nicotine_concentration_mg_per_ml = r_data.get('nicotine_concentration_mg_per_ml')
    date = r_data.get('date')

    # Calculate total nicotine inhaled
    total_nicotine_inhaled = nicotine_calculation(air_inhaled, temperature_celsius, nicotine_concentration_mg_per_ml)


    # Save the data to vape history
    save = save_history(
        user_id, vape_id,
        nicotine_concentration_mg_per_ml,
        total_nicotine_inhaled, air_inhaled, date
    )

    if save != 'success':
        abort(400, description=f"Failed saving data: {save}")

    return jsonify({
        "status": "success",
        "message": "History added"
    }), 201


 


if __name__=='__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
