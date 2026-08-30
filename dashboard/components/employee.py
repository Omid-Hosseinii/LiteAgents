import streamlit as st


def render_employee(employee):
    st.subheader(f"Employee: {employee['employee_id']}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Risk Level",
            employee["risk_level"]
        )

    with col2:
        st.metric(
            "Risk Score",
            employee["risk_score"]
        )

    st.write("### Explanation")
    st.write(employee["explanation"])
