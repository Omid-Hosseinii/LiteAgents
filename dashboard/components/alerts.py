
import streamlit as st


def render_alerts(employee):
    st.markdown(
        """
        <div dir="rtl" style="text-align: right;">
        """,
        unsafe_allow_html=True,
    )

    st.write("### توضیحات")
    st.write(employee["explanation"])

    st.write("### علائم هشدار")

    for warning in employee["warning_signs"]:
        st.write(f"- {warning}")

    st.write("### پیشنهادها")

    for recommendation in employee["recommendations"]:
        st.write(f"- {recommendation}")

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


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

