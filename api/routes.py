from fastapi import APIRouter, HTTPException

from api.database import get_connection
from api.models import EmployeeRiskResponse


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/employees", response_model=list[EmployeeRiskResponse])
def get_employees():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    employee_id,
                    risk_score,
                    risk_level,
                    explanation,
                    warning_signs,
                    recommendations
                FROM employee_risk_analysis
                ORDER BY employee_id;
                """
            )

            rows = cursor.fetchall()

    return [
        EmployeeRiskResponse(
            employee_id=row[0],
            risk_score=row[1],
            risk_level=row[2],
            explanation=row[3],
            warning_signs=row[4],
            recommendations=row[5],
        )
        for row in rows
    ]


@router.get(
    "/employees/{employee_id}",
    response_model=EmployeeRiskResponse
)
def get_employee(employee_id: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    employee_id,
                    risk_score,
                    risk_level,
                    explanation,
                    warning_signs,
                    recommendations
                FROM employee_risk_analysis
                WHERE employee_id = %s;
                """,
                (employee_id,),
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return EmployeeRiskResponse(
        employee_id=row[0],
        risk_score=row[1],
        risk_level=row[2],
        explanation=row[3],
        warning_signs=row[4],
        recommendations=row[5],
    )


@router.get(
    "/alerts",
    response_model=list[EmployeeRiskResponse]
)
def get_alerts():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    employee_id,
                    risk_score,
                    risk_level,
                    explanation,
                    warning_signs,
                    recommendations
                FROM employee_risk_analysis
                WHERE risk_level IN ('HIGH', 'MEDIUM')
                ORDER BY risk_score DESC;
                """
            )

            rows = cursor.fetchall()

    return [
        EmployeeRiskResponse(
            employee_id=row[0],
            risk_score=row[1],
            risk_level=row[2],
            explanation=row[3],
            warning_signs=row[4],
            recommendations=row[5],
        )
        for row in rows
    ]