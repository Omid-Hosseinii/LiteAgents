
import requests
import streamlit as st

from dashboard.components.employee import render_employee
from dashboard.components.alerts import (
    render_alerts,
    render_alert_overview,
)


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Employee Health Dashboard",
    layout="wide",
)

st.title("Employee Health Dashboard")


# Get all employees
response = requests.get(
    f"{API_URL}/employees",
    timeout=10,
)

response.raise_for_status()

employees = response.json()


# Get active alerts
alerts_response = requests.get(
    f"{API_URL}/alerts",
    timeout=10,
)

alerts_response.raise_for_status()

alerts = alerts_response.json()


# Alert Overview
render_alert_overview(alerts)


# Risk Summary
total_employees = len(employees)

high_risk = sum(
    1
    for employee in employees
    if employee["risk_level"] == "HIGH"
)

medium_risk = sum(
    1
    for employee in employees
    if employee["risk_level"] == "MEDIUM"
)

low_risk = sum(
    1
    for employee in employees
    if employee["risk_level"] == "LOW"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", total_employees)

with col2:
    st.metric("High Risk", high_risk)

with col3:
    st.metric("Medium Risk", medium_risk)

with col4:
    st.metric("Low Risk", low_risk)


st.divider()


# Employee Selection
st.subheader("Employee Details")


# Dropdown
employee_ids = [
    employee["employee_id"]
    for employee in employees
]

selected_employee = st.selectbox(
    "Select Employee",
    ["All Employees"] + employee_ids,
)


# Direct Employee ID Search
employee_id_input = st.text_input(
    "Or enter Employee ID",
    placeholder="Example: E001",
)

search_button = st.button("Show Employee")


st.divider()


# Direct search has priority when button is clicked
if search_button:

    employee_id = employee_id_input.strip()

    if not employee_id:
        st.warning("Please enter an Employee ID.")

    else:
        employee_response = requests.get(
            f"{API_URL}/employees/{employee_id}",
            timeout=10,
        )

        if employee_response.status_code == 404:
            st.error(f"Employee '{employee_id}' not found.")

        else:
            employee_response.raise_for_status()

            selected = employee_response.json()

            render_employee(selected)
            render_alerts(selected)


# Otherwise use dropdown
elif selected_employee == "All Employees":

    for employee in employees:
        render_employee(employee)
        render_alerts(employee)
        st.divider()


else:

    selected = next(
        employee
        for employee in employees
        if employee["employee_id"] == selected_employee
    )

    render_employee(selected)
    render_alerts(selected)

