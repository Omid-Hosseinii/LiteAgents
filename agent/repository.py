
from database.connection import SessionLocal
from database.models import EmployeeRiskAnalysis


def get_employee_ids():
    """
    Get all employee IDs from the timeseries table.
    """

    from database.models import EmployeeTimeseries

    session = SessionLocal()

    try:

        employees = (
            session.query(
                EmployeeTimeseries.employee_id
            )
            .distinct()
            .order_by(
                EmployeeTimeseries.employee_id
            )
            .all()
        )

        return [
            employee_id
            for employee_id, in employees
        ]

    finally:
        session.close()


def save_analysis(result):
    """
    Save or update employee risk analysis.
    """

    session = SessionLocal()

    try:

        employee_id = result.analysis.employee_id

        employee = (
            session.query(EmployeeRiskAnalysis)
            .filter(
                EmployeeRiskAnalysis.employee_id
                == employee_id
            )
            .first()
        )

        if employee is None:

            employee = EmployeeRiskAnalysis(
                employee_id=employee_id,
            )

            session.add(employee)

        employee.risk_score = result.analysis.risk_score
        employee.risk_level = result.analysis.risk_level
        employee.explanation = result.ai_analysis.explanation
        employee.warning_signs = (
            result.ai_analysis.warning_signs
        )
        employee.recommendations = (
            result.ai_analysis.recommendations
        )

        session.commit()

    except Exception:

        session.rollback()
        raise

    finally:
        session.close()

