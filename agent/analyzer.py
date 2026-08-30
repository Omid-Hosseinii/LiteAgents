
from database.connection import SessionLocal
from database.models import EmployeeTimeseries


def get_employee_timeseries(employee_id):
    session = SessionLocal()

    try:
        return (
            session.query(EmployeeTimeseries)
            .filter(
                EmployeeTimeseries.employee_id == employee_id
            )
            .order_by(EmployeeTimeseries.date)
            .all()
        )

    finally:
        session.close()


def analyze_employee(employee_id):
    rows = get_employee_timeseries(employee_id)

    if not rows:
        return None

    total_tasks = sum(
        row.total_tasks
        for row in rows
    )

    completed_tasks = sum(
        row.completed_tasks
        for row in rows
    )

    overdue_tasks = sum(
        row.overdue_tasks
        for row in rows
    )

    estimated_hours = sum(
        row.estimated_hours
        for row in rows
    )

    actual_hours = sum(
        row.actual_hours
        for row in rows
    )

    email_count = sum(
        row.email_count
        for row in rows
    )

    completion_rate = (
        completed_tasks / total_tasks
        if total_tasks > 0
        else 0
    )

    # Trend data

    overdue_trend = [
        row.overdue_tasks
        for row in rows
    ]

    actual_hours_trend = [
        float(row.actual_hours)
        for row in rows
    ]

    overdue_increasing = (
        len(overdue_trend) >= 2
        and overdue_trend[-1] > overdue_trend[0]
    )

    actual_hours_increasing = (
        len(actual_hours_trend) >= 2
        and actual_hours_trend[-1]
        > actual_hours_trend[0]
    )

    return {
        "employee_id": employee_id,
        "periods": len(rows),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "estimated_hours": float(estimated_hours),
        "actual_hours": float(actual_hours),
        "email_count": email_count,
        "completion_rate": completion_rate,
        "trends": {
            "overdue_increasing": overdue_increasing,
            "actual_hours_increasing": actual_hours_increasing,
        },
    }


def calculate_risk_score(analysis):
    score = 0

    if analysis["trends"]["overdue_increasing"]:
        score += 40

    if analysis["completion_rate"] < 0.8:
        score += 30

    if analysis["actual_hours"] > analysis["estimated_hours"]:
        score += 20

    return min(score, 100)


def get_risk_level(risk_score):
    if risk_score >= 70:
        return "HIGH"

    elif risk_score >= 40:
        return "MEDIUM"

    else:
        return "LOW"

