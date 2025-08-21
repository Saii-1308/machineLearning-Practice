import streamlit as st
import pandas as pd
import numpy as np

#title
st.title("hello streamlit")
#simple text
st.write("this is simple text")

#creste simple dataframe
df=pd.DataFrame({
    "first column":[1,2,3,4],
    "second column":[10,20,30,40]
})

st.write("here is the dataframe")
st.write(df)

#create a line chart

chart_data=pd.DataFrame(
    np.random.randn(20,3),columns=['a','b','c']
)

st.line_chart(chart_data)