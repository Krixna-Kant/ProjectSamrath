# app.py
import streamlit as st
import pandas as pd
from src.qa_engine import compare_avg_annual_rainfall, rainfall_trend, rainfall_time_series

st.set_page_config(page_title="Project Samarth - Rainfall", layout="wide")
st.title("Project Samarth — Rainfall Analysis (IMD)")

st.markdown("""
Use these tools to inspect IMD Sub-division annual rainfall aggregated to region queries.
Citations are provided for every numeric claim.
""")

mode = st.sidebar.selectbox("Choose an action", [
    "Compare rainfall (last N years)",
    "Region trend & timeseries",
    "Get timeseries for a region"
])

if mode == "Compare rainfall (last N years)":
    st.header("Compare average annual rainfall between two regions (last N years)")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.text_input("First region (state/subdivision)", "Maharashtra")
    with col2:
        s2 = st.text_input("Second region (state/subdivision)", "Gujarat")
    n = st.slider("Last N years (use available years)", min_value=1, max_value=30, value=5)
    if st.button("Compare"):
        out = compare_avg_annual_rainfall(s1, s2, n)
        st.subheader("Result")
        st.write(f"Over years: {out['years']}")
        left, right = st.columns(2)
        with left:
            st.write(f"**{out['state_x']}** — average: {out['avg_x_mm']} mm")
            if out['time_series_x']:
                df_x = pd.DataFrame(out['time_series_x'])
                df_x = df_x.rename(columns={'annual_rainfall_mm': 'rain_mm'})
                st.line_chart(df_x.set_index('Year')['rain_mm'])
                st.table(df_x)
        with right:
            st.write(f"**{out['state_y']}** — average: {out['avg_y_mm']} mm")
            if out['time_series_y']:
                df_y = pd.DataFrame(out['time_series_y'])
                df_y = df_y.rename(columns={'annual_rainfall_mm': 'rain_mm'})
                st.line_chart(df_y.set_index('Year')['rain_mm'])
                st.table(df_y)
        st.caption(out['citation'])

elif mode == "Region trend & timeseries":
    st.header("Region trend & timeseries")
    region = st.text_input("Region (state/subdivision)", "Maharashtra")
    start, end = st.slider("Year range", min_value=1901, max_value=2017, value=(2008, 2017))
    if st.button("Show trend"):
        out = rainfall_trend(region, start, end)
        st.write(f"Region: **{out['region']}**")
        st.write(f"Trend (slope): {out['trend_slope_mm_per_year']} mm/year")
        if out['series']:
            df = pd.DataFrame(out['series']).rename(columns={'annual_rainfall_mm':'rain_mm'})
            st.line_chart(df.set_index('Year')['rain_mm'])
            st.table(df)
        st.caption(out['citation'])

else:
    st.header("Get timeseries for a region")
    region = st.text_input("Region (state/subdivision)", "Maharashtra")
    start, end = st.slider("Year range", min_value=1901, max_value=2017, value=(2008, 2017))
    if st.button("Fetch"):
        out = rainfall_time_series(region, start, end)
        if out['series']:
            df = pd.DataFrame(out['series']).rename(columns={'annual_rainfall_mm':'rain_mm'})
            st.line_chart(df.set_index('Year')['rain_mm'])
            st.table(df)
        else:
            st.warning("No data for that region / years.")
        st.caption(out['citation'])
