from flask import Flask, render_template, request, jsonify, abort
from nicotine_calculator.calculator import nicotine_calculation
from queries.vape_history import get_all_history_data, save_history


app = Flask(__name__)

@app.route('/')
def home():
    stored_data=get_all_history_data()
    return render_template('home.html', stored_data=stored_data)


@app.route("/add", methods=['POST'])
def add():

    r_data = request.get_json(silent=True)
    print(f'Got information: {r_data}' )

    required_keys = ['nicotine_concentration_mg_per_ml', 'vape_id', 'user_id', 'date', 'air_inhaled']

    # Check that the request has all the required information
    for key in required_keys:
        if r_data.get(key) is None:
            abort(400, description=f"Missing required parameter: {key}")

    air_inhaled = r_data.get('air_inhaled')
    user_id = r_data.get('user_id')
    vape_id = r_data.get('vape_id')
    nicotine_concentration_mg_per_ml = r_data.get('nicotine_concentration_mg_per_ml')
    date = r_data.get('date')

    # Calculate total nicotine inhaled
    total_nicotine_inhaled = nicotine_calculation(air_inhaled, nicotine_concentration_mg_per_ml)


    # Save the data to vape history
    save = save_history(
        user_id, vape_id,
        nicotine_concentration_mg_per_ml,
        float(total_nicotine_inhaled), air_inhaled, date
    )

    if save != 'success':
        abort(400, description=f"Failed saving data: {save}")

    return jsonify({
        "status": "success",
        "message": "History added"
    }), 201


 


if __name__=='__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
