
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="داشبورد وضعیت کارکنان",
    layout="wide",
)


# =========================
# Persian RTL CSS
# =========================

st.markdown(
    """
    <style>

    .rtl {
        direction: rtl;
        text-align: right;
    }

    .rtl h1,
    .rtl h2,
    .rtl h3,
    .rtl p,
    .rtl li {
        text-align: right;
    }

    .risk-high {
        color: #d32f2f;
        font-weight: bold;
    }

    .risk-medium {
        color: #f57c00;
        font-weight: bold;
    }

    .risk-low {
        color: #388e3c;
        font-weight: bold;
    }

    .section-box {
        direction: rtl;
        text-align: right;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Helper Functions
# =========================

def get_risk_class(risk_level):
    if risk_level == "HIGH":
        return "risk-high"

    if risk_level == "MEDIUM":
        return "risk-medium"

    return "risk-low"


def get_risk_text(risk_level):
    if risk_level == "HIGH":
        return "ریسک بالا"

    if risk_level == "MEDIUM":
        return "ریسک متوسط"

    return "ریسک پایین"


def render_employee(employee):
    risk_level = employee["risk_level"]
    risk_score = employee["risk_score"]

    risk_class = get_risk_class(risk_level)
    risk_text = get_risk_text(risk_level)

    st.markdown(
        f"""
        <div class="rtl">

        <h2>کارمند: {employee["employee_id"]}</h2>

        <p>
            سطح ریسک:
            <span class="{risk_class}">
                {risk_text}
            </span>
        </p>

        <p>
            امتیاز ریسک:
            <strong>{risk_score}</strong>
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analysis(employee):
    st.markdown(
        """
        <div class="rtl">
        <h3>توضیحات تحلیل</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    explanation = employee.get("explanation")

    if explanation:
        st.markdown(
            f"""
            <div class="section-box">
                {explanation}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="rtl">
        <h3>نشانه‌های هشدار</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    warning_signs = employee.get("warning_signs", [])

    if warning_signs:
        for warning in warning_signs:
            st.markdown(
                f"""
                <div class="rtl">
                • {warning}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="rtl">مورد هشدار خاصی ثبت نشده است.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="rtl">
        <h3>پیشنهادهای مدیریتی</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recommendations = employee.get("recommendations", [])

    if recommendations:
        for recommendation in recommendations:
            st.markdown(
                f"""
                <div class="rtl">
                • {recommendation}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="rtl">پیشنهادی ثبت نشده است.</div>',
            unsafe_allow_html=True,
        )


def render_employee_card(employee):
    render_employee(employee)

    render_analysis(employee)

    st.divider()


# =========================
# Get Employees
# =========================

response = requests.get(
    f"{API_URL}/employees",
    timeout=10,
)

response.raise_for_status()

employees = response.json()


# =========================
# Get Alerts
# =========================

alerts_response = requests.get(
    f"{API_URL}/alerts",
    timeout=10,
)

alerts_response.raise_for_status()

alerts = alerts_response.json()


# =========================
# Dashboard Header
# =========================

st.markdown(
    """
    <div class="rtl">
        <h1>داشبورد وضعیت کارکنان</h1>
        <p>تحلیل وضعیت کاری و سطح ریسک کارکنان</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# Alert Overview
# =========================

high_alerts = sum(
    1
    for alert in alerts
    if alert["risk_level"] == "HIGH"
)

medium_alerts = sum(
    1
    for alert in alerts
    if alert["risk_level"] == "MEDIUM"
)


st.markdown(
    """
    <div class="rtl">
        <h2>خلاصه هشدارها</h2>
    </div>
    """,
    unsafe_allow_html=True,
)


alert_col1, alert_col2 = st.columns(2)

with alert_col1:
    st.metric(
        "ریسک بالا",
        high_alerts,
    )

with alert_col2:
    st.metric(
        "ریسک متوسط",
        medium_alerts,
    )


# =========================
# Risk Summary
# =========================

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


st.markdown(
    """
    <div class="rtl">
        <h2>خلاصه وضعیت کارکنان</h2>
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "تعداد کل کارکنان",
        total_employees,
    )

with col2:
    st.metric(
        "ریسک بالا",
        high_risk,
    )

with col3:
    st.metric(
        "ریسک متوسط",
        medium_risk,
    )

with col4:
    st.metric(
        "ریسک پایین",
        low_risk,
    )


st.divider()


# =========================
# Employee Selection
# =========================

st.markdown(
    """
    <div class="rtl">
        <h2>جزئیات کارمند</h2>
    </div>
    """,
    unsafe_allow_html=True,
)


employee_ids = [
    employee["employee_id"]
    for employee in employees
]


selected_employee = st.selectbox(
    "انتخاب کارمند",
    ["همه کارکنان"] + employee_ids,
)


employee_id_input = st.text_input(
    "یا شناسه کارمند را وارد کنید",
    placeholder="مثال: P001",
)


search_button = st.button(
    "نمایش اطلاعات کارمند"
)


st.divider()


# =========================
# Direct Employee Search
# =========================

if search_button:

    employee_id = employee_id_input.strip()

    if not employee_id:

        st.warning(
            "لطفاً شناسه کارمند را وارد کنید."
        )

    else:

        employee_response = requests.get(
            f"{API_URL}/employees/{employee_id}",
            timeout=10,
        )

        if employee_response.status_code == 404:

            st.error(
                f"کارمندی با شناسه {employee_id} پیدا نشد."
            )

        else:

            employee_response.raise_for_status()

            selected = employee_response.json()

            render_employee_card(selected)


# =========================
# Dropdown
# =========================

elif selected_employee == "همه کارکنان":

    for employee in employees:
        render_employee_card(employee)


else:

    selected = next(
        employee
        for employee in employees
        if employee["employee_id"] == selected_employee
    )

    render_employee_card(selected)

