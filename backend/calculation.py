def nicotine_calculation(air_inhaled: float, nicotine_concentration_mg_per_ml : float) -> float:
    """
    this function calculates nicontine inhaled and return a float
    """
    try:
        calculation = nicotine_concentration_mg_per_ml  * air_inhaled #add vyr culculating model

        return calculation

    except Exception as e:
        return f'failed doing nicotine calculation: {e}' 