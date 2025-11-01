# src/data_processing.py
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from src.utils import normalize_text

# Citation (static) for rainfall dataset
RAIN_DATASET_CITATION = "Sub-Divisional Monthly Rainfall (IMD) — source: data/Sub_Division_IMD_2017.csv"

class RainfallData:
    def __init__(self, csv_path: str = "data/Sub_Division_IMD_2017.csv"):
        # load CSV; expect columns like SUBDIVISION,YEAR,JAN,...,DEC,ANNUAL
        self.df = pd.read_csv(csv_path)
        # normalize column names
        self.df.columns = [c.strip() for c in self.df.columns]
        # ensure Year is int
        if 'YEAR' in self.df.columns:
            self.df.rename(columns={'YEAR': 'Year'}, inplace=True)
        if 'SUBDIVISION' in self.df.columns:
            self.df.rename(columns={'SUBDIVISION': 'Subdivision'}, inplace=True)
        if 'ANNUAL' not in self.df.columns and 'ANNUAL ' in self.df.columns:
            self.df.rename(columns={'ANNUAL ': 'ANNUAL'}, inplace=True)
        # Make sure types
        self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce').astype('Int64')
        # Ensure ANNUAL numeric
        if 'ANNUAL' in self.df.columns:
            self.df['ANNUAL'] = pd.to_numeric(self.df['ANNUAL'], errors='coerce')
        # normalized subdivision string column for matching
        self.df['subdivision_norm'] = self.df['Subdivision'].astype(str).apply(normalize_text)
        # precompute list of unique subdivisions
        self.subdivisions = self.df['Subdivision'].unique().tolist()

    def available_years(self) -> List[int]:
        yrs = sorted(self.df['Year'].dropna().unique().astype(int).tolist())
        return yrs

    def get_subdivisions_for_state(self, state_query: str) -> List[str]:

        q = normalize_text(state_query)
        # find subdivisions where normalized name contains the token or token contains subdivision
        mask = self.df['subdivision_norm'].str.contains(q, na=False)
        matches = self.df.loc[mask, 'Subdivision'].unique().tolist()
        # if none found, try token-by-token matching
        if not matches:
            tokens = q.split()
            for t in tokens:
                mask2 = self.df['subdivision_norm'].str.contains(t, na=False)
                m2 = self.df.loc[mask2, 'Subdivision'].unique().tolist()
                for x in m2:
                    if x not in matches:
                        matches.append(x)
        return matches

    def get_annual_series_for_region(self, region_query: str,
                                     start_year: Optional[int] = None,
                                     end_year: Optional[int] = None) -> pd.DataFrame:

        subs = self.get_subdivisions_for_state(region_query)
        if not subs:
            return pd.DataFrame(columns=['Year', 'ANNUAL'])
        df_sub = self.df[self.df['Subdivision'].isin(subs)].copy()
        #group by Year and compute mean annual rainfall across matched subdivisions
        series = df_sub.groupby('Year', as_index=False)['ANNUAL'].mean().rename(columns={'ANNUAL': 'annual_rainfall_mm'})
        #filter by years if requested
        if start_year is not None:
            series = series[series['Year'] >= start_year]
        if end_year is not None:
            series = series[series['Year'] <= end_year]
        series = series.dropna(subset=['annual_rainfall_mm']).sort_values('Year')
        return series

    def get_last_n_years_for_region(self, region_query: str, n: int) -> pd.DataFrame:
        s = self.get_annual_series_for_region(region_query)
        if s.empty:
            return s
        #take the last n available years
        s_sorted = s.sort_values('Year', ascending=False).head(n).sort_values('Year')
        return s_sorted

    def avg_over_period_for_region(self, region_query: str, start_year: int, end_year: int) -> Optional[float]:
        s = self.get_annual_series_for_region(region_query, start_year, end_year)
        if s.empty:
            return None
        return float(s['annual_rainfall_mm'].mean())

    def trend_slope_for_region(self, region_query: str, start_year: Optional[int] = None, end_year: Optional[int] = None) -> Optional[float]:

        s = self.get_annual_series_for_region(region_query, start_year, end_year)
        if s.shape[0] < 3:
            return None
        x = s['Year'].astype(float).to_numpy()
        y = s['annual_rainfall_mm'].to_numpy()
        # linear fit y = a*x + b -> slope=a
        a, b = np.polyfit(x, y, 1)
        return float(a)
