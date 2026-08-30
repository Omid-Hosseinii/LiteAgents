import streamlit as st


def render_alerts(employee):
    st.write("### Warning Signs")

    for warning in employee["warning_signs"]:
        st.write(f"- {warning}")

    st.write("### Recommendations")

    for recommendation in employee["recommendations"]:
        st.write(f"- {recommendation}")


def render_alert_overview(alerts):
    st.subheader("⚠️ Active Alerts")

    if not alerts:
        st.success("No active alerts.")
        return

    for alert in alerts:
        st.warning(
            f"{alert['employee_id']} — "
            f"{alert['risk_level']} Risk "
            f"({alert['risk_score']})"
        )