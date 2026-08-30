
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from database.models import EmployeeRiskAnalysis

from fastapi import BackgroundTasks
from agent.pipeline import execute_pipeline
import threading
import time



router = APIRouter()


@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db),
):
    employees = (
        db.query(EmployeeRiskAnalysis)
        .order_by(EmployeeRiskAnalysis.employee_id)
        .all()
    )

    return [
        {
            "employee_id": employee.employee_id,
            "risk_score": employee.risk_score,
            "risk_level": employee.risk_level,
            "explanation": employee.explanation,
            "warning_signs": employee.warning_signs,
            "recommendations": employee.recommendations,
            "created_at": employee.created_at,
        }
        for employee in employees
    ]


@router.get("/employees/{employee_id}")
def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
):
    employee = (
        db.query(EmployeeRiskAnalysis)
        .filter(
            EmployeeRiskAnalysis.employee_id == employee_id
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "employee_id": employee.employee_id,
        "risk_score": employee.risk_score,
        "risk_level": employee.risk_level,
        "explanation": employee.explanation,
        "warning_signs": employee.warning_signs,
        "recommendations": employee.recommendations,
        "created_at": employee.created_at,
    }


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db),
):
    employees = (
        db.query(EmployeeRiskAnalysis)
        .filter(
            EmployeeRiskAnalysis.risk_level.in_(
                ["HIGH", "MEDIUM"]
            )
        )
        .order_by(
            EmployeeRiskAnalysis.risk_score.desc()
        )
        .all()
    )

    return [
        {
            "employee_id": employee.employee_id,
            "risk_score": employee.risk_score,
            "risk_level": employee.risk_level,
            "explanation": employee.explanation,
            "warning_signs": employee.warning_signs,
            "recommendations": employee.recommendations,
        }
        for employee in employees
    ]






analysis_status = {
    "running": False,
    "total": 0,
    "completed": 0,
    "current_employee": None,
    "current_risk_level": None,
    "current_risk_score": None,
    "elapsed_time": 0,
    "error": None,
}


def update_analysis_status(
    completed,
    total,
    employee_id,
    risk_level,
    risk_score,
):
    analysis_status["completed"] = completed
    analysis_status["total"] = total
    analysis_status["current_employee"] = employee_id
    analysis_status["current_risk_level"] = risk_level
    analysis_status["current_risk_score"] = risk_score


def run_pipeline_background():

    analysis_status["running"] = True
    analysis_status["error"] = None
    analysis_status["completed"] = 0
    analysis_status["total"] = 0
    analysis_status["current_employee"] = None

    start_time = time.perf_counter()

    try:

        result = execute_pipeline(
            progress_callback=update_analysis_status
        )

        analysis_status["total"] = result["total"]
        analysis_status["completed"] = result["completed"]

    except Exception as exc:

        analysis_status["error"] = str(exc)

    finally:

        analysis_status["elapsed_time"] = round(
            time.perf_counter() - start_time,
            2,
        )

        analysis_status["running"] = False


@router.post("/analysis/run")
def start_analysis():

    if analysis_status["running"]:

        return {
            "status": "already_running",
        }

    thread = threading.Thread(
        target=run_pipeline_background,
        daemon=True,
    )

    thread.start()

    return {
        "status": "started",
    }


@router.get("/analysis/status")
def get_analysis_status():

    return analysis_status


