import pandas as pd
import streamlit as st


STUDENTS = {
    "1001": {
        "name": "Aisha Rahman",
        "class": "Grade 10",
        "marks": {"Mathematics": 92, "Science": 88, "English": 95, "History": 81, "Computing": 97},
    },
    "1002": {
        "name": "Aysha Khan",
        "class": "Grade 10",
        "marks": {"Mathematics": 84, "Science": 78, "English": 82, "History": 75, "Computing": 88},
    },
    "1003": {
        "name": "Mina Patel",
        "class": "Grade 10",
        "marks": {"Mathematics": 68, "Science": 73, "English": 59, "History": 71, "Computing": 64},
    },
    "1004": {
            "name": "Hasna",
            "class": "Grade 10",
            "marks": {"Mathematics": 96, "Science": 94, "English": 92, "History": 94, "Computing": 93},
    },
    "1005": {
            "name": "Jameela",
            "class": "Grade 10",
            "marks": {"Mathematics": 99, "Science": 98, "English": 96, "History": 97, "Computing": 96},
    },
    "1006": {
            "name": "Varnika",
            "class": "Grade 10",
            "marks": {"Mathematics": 98, "Science": 98, "English": 98, "History": 98, "Computing": 94},
    },
     "1007": {
             "name": "Zaina",
             "class": "Grade 10",
             "marks": {"Mathematics": 80, "Science": 64, "English": 52, "History": 64, "Computing": 73},
    },
    "1008": {
            "name": "Muneera",
            "class": "Grade 10",
            "marks": {"Mathematics": 80, "Science": 88, "English": 76, "History": 67, "Computing": 76},
    },
    "1009": {
            "name": "Zikra",
            "class": "Grade 10",
            "marks": {"Mathematics": 68, "Science": 78, "English": 88, "History": 78, "Computing": 74},
    },
}  


def grade_for(mark):
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


st.set_page_config(
    page_title="Student marksheet",
    page_icon=":material/school:",
    layout="centered",
)

st.title("Student marksheet", icon=":material/school:")
st.caption("Enter your roll number to view your subject marks and grades.")

st.session_state.setdefault("searched_roll", "")
st.session_state.setdefault("lookup_error", "")

with st.form("roll_number_form"):
    roll_number = st.text_input("Roll number", placeholder="e.g. 1001")
    submitted = st.form_submit_button("View marksheet", type="primary", width="stretch")

if submitted:
    roll_number = roll_number.strip()
    if not roll_number:
        st.session_state.searched_roll = ""
        st.session_state.lookup_error = "Enter your roll number to continue."
    elif roll_number not in STUDENTS:
        st.session_state.searched_roll = ""
        st.session_state.lookup_error = "No marksheet was found for that roll number."
    else:
        st.session_state.searched_roll = roll_number
        st.session_state.lookup_error = ""

if st.session_state.lookup_error:
    st.error(st.session_state.lookup_error)

if st.session_state.searched_roll:
    student = STUDENTS[st.session_state.searched_roll]
    average = sum(student["marks"].values()) / len(student["marks"])

    st.subheader(student["name"])
    st.caption(f"Roll number {st.session_state.searched_roll}  ·  {student['class']}")

    average_column, grade_column = st.columns(2)
    average_column.metric("Overall average", f"{average:.1f}%")
    grade_column.metric("Overall grade", grade_for(average))

    marksheet = pd.DataFrame([
        {"Subject": subject, "Marks": mark, "Grade": grade_for(mark)}
        for subject, mark in student["marks"].items()
    ])
    st.dataframe(marksheet, hide_index=True, width="stretch")

    with st.expander("Grade scale"):
        st.write("A: 90-100  ·  B: 80-89  ·  C: 70-79  ·  D: 60-69  ·  F: below 60")

st.caption("Demo roll numbers: 1001, 1002, 1003")