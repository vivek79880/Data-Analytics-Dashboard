import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(page_title='Data Analytics Dashboard', layout='wide')

st.title("📊 Data Analytics Dashboard")
st.write("Upload a CSV file to analyze and visualize the data.")

# File Upload
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.write(df.head())

    # Basic Data Information
    st.write("### Dataset Information")
    st.write(df.describe())
    
    # Data Visualization
    st.write("### Data Visualization")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.write("#### Distribution of Numeric Features")
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_col = st.selectbox("Select a column", num_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    
    # Filtering Data
    st.write("### Filter Data")
    filter_col = st.selectbox("Select a column to filter", df.columns)
    unique_values = df[filter_col].unique()
    selected_value = st.selectbox("Select a value", unique_values)
    filtered_df = df[df[filter_col] == selected_value]
    st.write(filtered_df)
else:
    st.write("Upload a CSV file to get started.")
