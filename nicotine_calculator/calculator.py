import pandas as pd
import joblib

# Load the model
model = joblib.load('nicotine_calculator/model.pkl')

def nicotine_calculation(air_inhaled, temperature_celsius, nicotine_concentration):
    # New data to predict (matching the training features)
    new_data = pd.DataFrame({
        'Air Inhaled': [air_inhaled],
        'Temperature Celsius': [temperature_celsius],
        'Nicotine Concentration': [nicotine_concentration],
    })

    # Get predictions
    score = model.predict(new_data)

    return round(float(score[0]), 0)

if __name__ == "__main__":
    nicotine_estimate = nicotine_calculation(0.5,28.9, 4)
    print(nicotine_estimate)
