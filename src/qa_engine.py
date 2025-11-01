from src.data_processing import RainfallData

def get_rainfall_response(state_name):
    rainfall = RainfallData()
    result = rainfall.get_rainfall(state_name)
    
    if result is None:
        return f"No rainfall data found for '{state_name}'. Please check the name or try a nearby subdivision."
    
    return f"Average Annual Rainfall for {state_name.title()}: {result} mm"
