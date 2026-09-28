"""Simple BMI (Body Mass Index) calculator built with Streamlit."""

import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

st.title("⚖️ BMI Calculator")
st.write("Enter your height and weight to calculate your Body Mass Index.")

unit = st.radio("Units", ["Metric (kg, cm)", "Imperial (lb, in)"], horizontal=True)

col1, col2 = st.columns(2)

if unit == "Metric (kg, cm)":
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=65.0, step=0.5)
    with col2:
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
    height_m = height_cm / 100
else:
    with col1:
        weight_lb = st.number_input("Weight (lb)", min_value=2.0, max_value=660.0, value=143.0, step=0.5)
    with col2:
        height_in = st.number_input("Height (in)", min_value=20.0, max_value=100.0, value=67.0, step=0.5)
    weight = weight_lb * 0.453592
    height_m = height_in * 0.0254

if st.button("Calculate BMI", type="primary"):
    if height_m <= 0:
        st.error("Height must be greater than zero.")
    else:
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            category, color = "Underweight", "🔵"
        elif bmi < 25:
            category, color = "Normal weight", "🟢"
        elif bmi < 30:
            category, color = "Overweight", "🟠"
        else:
            category, color = "Obese", "🔴"

        st.metric("Your BMI", f"{bmi:.1f}")
        st.subheader(f"{color} {category}")

        st.progress(min(bmi / 40, 1.0))

        st.markdown(
            """
            | Category | BMI range |
            |---|---|
            | Underweight | below 18.5 |
            | Normal weight | 18.5 – 24.9 |
            | Overweight | 25 – 29.9 |
            | Obese | 30 and above |
            """
        )

        st.caption("BMI is a general screening measure and does not account for muscle mass, age, or body composition. Consult a healthcare professional for a full assessment.")