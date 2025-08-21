import sqlite3
import streamlit as st

connection=sqlite3.connect('student.db')
cursor=connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
id INTEGER primary key,
name text not null,
age interger not null,
grade text not null)
''')

connection.commit()

def get_connection():
    return sqlite3.connect('student.db')

def add_student(name,age,grade):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
    INSERT INTO students(name,age,grade) VALUES(?,?,?)''',(name,age,grade))

    conn.commit()
    conn.close()

def get_student():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows=cursor.fetchall()
    conn.close()

    return rows

st.title('Student Managnmnet System')

st.header('Add Student')

name=st.text_input('Enter student name')
age=st.number_input('Enter student age',min_value=1,max_value=100)
grade=st.text_input('Enter student grade')


if st.button('Add student'):
    if name and age and grade:
        add_student(name,age,grade)
        st.subheader('student added successfully')
    else:
        st.error('please fill all rhe fields')

st.header('Student List')
if st.button('Get student'):
    students=get_student()
    if students:
        for student in students:
            st.write(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
    else:
        st.error("No student found.")