from flask import Flask, render_template, request, jsonify, abort, redirect
from queries.vape_history import get_all_history_data, save_history, update_total_nicotine
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

        # Save the data to vape history (total nicotine inhaled is filled in later per row)
        save_history(
            1, 1,
            nicotine_concentration_mg_per_ml,
            air_inhaled, temperature_celsius, date
        )

        return redirect('/')

    # GET request - display the page
    stored_data = get_all_history_data()
    return render_template('home.html', stored_data=stored_data)


@app.route('/update_total/<int:history_id>', methods=['POST'])
def update_total(history_id):
    # Total nicotine inhaled entered manually from the row's edit form
    total_nicotine_inhaled = request.form.get('total_nicotine_inhaled')
    if total_nicotine_inhaled in (None, ''):
        abort(400, description="Missing required parameter: total_nicotine_inhaled")

    try:
        total_nicotine_inhaled = float(total_nicotine_inhaled)
    except ValueError:
        abort(400, description="total_nicotine_inhaled must be a number")

    result = update_total_nicotine(history_id, total_nicotine_inhaled)
    if result != 'success':
        abort(400, description=f"Failed updating data: {result}")

    return redirect('/')


@app.route("/add", methods=['POST'])
def add():

    r_data = request.get_json(silent=True)
    print(f'Got information: {r_data}' )

    if r_data is None:
        abort(400, description="Request body must be JSON")

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


    # Save the data to vape history (no total nicotine calculation)
    save = save_history(
        user_id, vape_id,
        nicotine_concentration_mg_per_ml,
        air_inhaled, temperature_celsius, date
    )

    if save != 'success':
        abort(400, description=f"Failed saving data: {save}")

    return jsonify({
        "status": "success",
        "message": "History added"
    }), 201





if __name__=='__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
