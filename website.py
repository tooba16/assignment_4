# Project 9: Build a Python Website in 15 Minutes With Streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simple Data Dashboard")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Summary")
        st.write(df.describe())

        if not df.empty:
            st.subheader("Filter Data")
            columns = df.columns.tolist()

            # Select column for filtering
            selected_column = st.selectbox("Select column to filter by", columns)
            unique_values = df[selected_column].dropna().unique()

            # Ensure there are values to select
            if len(unique_values) > 0:
                selected_value = st.selectbox("Select value", unique_values)
                filtered_df = df[df[selected_column] == selected_value]
                st.write(filtered_df)
            else:
                st.warning("No unique values found for filtering.")

            # Plotting section
            st.subheader("Plot Data")
            x_column = st.selectbox("Select x-axis column", columns)
            y_column = st.selectbox("Select y-axis column", columns)

            if st.button("Generate Plot"):
                try:
                    # Drop missing values from selected columns
                    chart_data = filtered_df[[x_column, y_column]].dropna()

                    # Ensure selected columns are numeric for plotting
                    if pd.api.types.is_numeric_dtype(chart_data[y_column]):
                        st.line_chart(chart_data.set_index(x_column))
                    else:
                        st.warning("Selected y-axis column must be numeric.")
                except Exception as e:
                    st.error(f"Error generating plot: {e}")
        else:
            st.warning("Uploaded file is empty.")
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
else:
    st.info("Please upload a CSV file to begin.")
