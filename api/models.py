from pydantic import BaseModel


class EmployeeRiskResponse(BaseModel):
    employee_id: str
    risk_score: int
    risk_level: str
    explanation: str
    warning_signs: list[str]
    recommendations: list[str]