import streamlit as st

# Input Fields
name = st.text_input("Enter your Name")
age = st.number_input("Enter your Age", min_value=0)
address = st.text_input("Enter your Address")
img = st.camera_input("Capture your Image")

choice = ['Male', 'Female', 'Other']
gender = st.selectbox("Select your Gender", choice)

education_option = ['Select', 'Middle school', 'High school', 'B.E/B.Tech', 'MBA']
education = st.selectbox("Select your Education", education_option)

option = st.radio('Choose Stream', ['Computer', 'IT', 'AI&DS'])

upload_file = st.file_uploader("Upload your Resume", type='pdf')

level = st.select_slider('Level of Experience', options=['Beginner', 'Intermediate', 'Professional'])

# Display Output
st.title("Your Details")

st.text(f"Your Name: {name}")

if age < 18:
    st.warning(f"You're not eligible. Age: {age}")
else:
    st.success(f"You're eligible. Age: {age}")

st.text(f"Your Address: {address}")

if img is not None:
    st.image(img, caption="Captured Image")

st.text(f"Your Selected Gender: {gender}")
st.text(f"Your Education Level: {education}")
st.text(f"Your Selected Stream: {option}")

if upload_file is not None:
    st.success("Resume uploaded successfully!!")
    st.text(f"File Name: {upload_file.name}")
else:
    st.warning("File not uploaded. Try again!")

st.text(f"Your Experience Level: {level}")
