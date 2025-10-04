import streamlit as st
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

st.title("Data Cleaner & Visualizer Application")

#uplode csv file

uploded_files=st.file_uploader("Choose a CSV file",type="csv")
method=st.selectbox("select cleaning method",["mean","median","mode"])

if uploded_files:
    df=pd.read_csv(uploded_files)
    st.subheader("Original Data")
    st.write(df.head())
    
    #call backend api to clean data
    files={'file': uploded_files.getvalue()}
    
    #make post request to backend api
    response=requests.post("http://127.0.0.1:5000/clean",
                           files={'file': uploded_files},
                           data={'method': method})
    
    #convert json into dataframe
    cleaned_df=pd.DataFrame(response.json())
    st.subheader("clean data preview")
    st.write(cleaned_df.head())
    
    #visulization
    st.subheader("Data Visulization")

    st.subheader("missing values (before cleaning)")
    st.pyplot(sns.heatmap(df.isnull(),cbar=False))

    st.write("Missing values (after cleaning)")
    st.bar_chart(cleaned_df.select_dtypes(include=['float64','int64']))


    #download cleaned file

    csv=cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download cleaned data as CSV",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv')
