import pandas as pd
from src.utils import normalize_text

class RainfallData:
    def __init__(self, csv_path="data/Sub_Division_IMD_2017.csv"):
        self.data = pd.read_csv(csv_path)
        self.data.columns = self.data.columns.str.strip()
        self.data["SUBDIVISION"] = self.data["SUBDIVISION"].apply(normalize_text)
    
    def get_available_regions(self):
        """Return list of available subdivisions."""
        return self.data["SUBDIVISION"].unique().tolist()
    
    def get_rainfall(self, query_state):
        """Find average annual rainfall for given state or subdivision."""
        query_norm = normalize_text(query_state)
        matched = self.data[self.data["SUBDIVISION"].str.contains(query_norm, case=False, na=False)]
        
        if matched.empty:
            return None
        
        avg_rainfall = matched["ANNUAL"].mean()
        return round(avg_rainfall, 2)
