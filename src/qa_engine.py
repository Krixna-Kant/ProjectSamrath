from typing import Dict, Any, Tuple, List
from src.data_processing import RainfallData, RAIN_DATASET_CITATION
import pandas as pd
from typing import Optional, Dict, Any


rain = RainfallData() 

def compare_avg_annual_rainfall(state_x: str, state_y: str, last_n_years: int) -> Dict[str, Any]:
    #get last n years for each
    s_x = rain.get_last_n_years_for_region(state_x, last_n_years)
    s_y = rain.get_last_n_years_for_region(state_y, last_n_years)
    #get overlapping years
    years_x = set(s_x['Year'].astype(int).tolist())
    years_y = set(s_y['Year'].astype(int).tolist())
    overlap = sorted(list(years_x.intersection(years_y)))
    if not overlap:
        # as fallback, use most recent min(length) contiguous years by intersection of available ranges
        overlap = sorted(list(years_x.union(years_y)))[-min(len(years_x), len(years_y)):]
    #filter series to overlap
    tx = s_x[s_x['Year'].isin(overlap)].sort_values('Year')
    ty = s_y[s_y['Year'].isin(overlap)].sort_values('Year')
    avg_x = float(tx['annual_rainfall_mm'].mean()) if not tx.empty else None
    avg_y = float(ty['annual_rainfall_mm'].mean()) if not ty.empty else None
    return {
        "state_x": state_x,
        "state_y": state_y,
        "years": [int(y) for y in overlap],
        "time_series_x": tx.to_dict(orient='records'),
        "time_series_y": ty.to_dict(orient='records'),
        "avg_x_mm": avg_x,
        "avg_y_mm": avg_y,
        "citation": RAIN_DATASET_CITATION
    }

def rainfall_trend(region: str, start_year: Optional[int] = None, end_year: Optional[int] = None) -> Dict[str, Any]:
    
    series = rain.get_annual_series_for_region(region, start_year, end_year)
    slope = rain.trend_slope_for_region(region, start_year, end_year)
    return {
        "region": region,
        "series": series.to_dict(orient='records'),
        "trend_slope_mm_per_year": float(slope) if slope is not None else None,
        "citation": RAIN_DATASET_CITATION
    }

def rainfall_time_series(region: str, start_year: Optional[int] = None, end_year: Optional[int] = None) -> Dict[str, Any]:
    
    series = rain.get_annual_series_for_region(region, start_year, end_year)
    return {
        "region": region,
        "series": series.to_dict(orient='records'),
        "citation": RAIN_DATASET_CITATION
    }
