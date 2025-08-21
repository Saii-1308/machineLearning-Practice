import streamlit as st
import pandas as pd

st.title("streamlite text input")

name=st.text_input("enter your nsame:")
if name:
    st.write(f"hello, {name}")
#select age slider
age=st.slider("select your age: ",0,100,25)
st.write(f"your age:{age}")

#select option
option=["select","cpp","java","python","c","ml"]
choice=st.selectbox("choose your favrite languge: ",option)
st.write(f"You selected {choice}.")

data={
    "name":['sai','sayali','krushna','shlok'],
    "age":[20,21,18,11],
    "city":["korea","japan","tokiya","india"]
}
df=pd.DataFrame(data)
st.write(df)

uploded_file=st.file_uploader("choose a csv file",type="csv")

if uploded_file is not None:
    df=pd.read_csv(uploded_file)
    st.write(df)