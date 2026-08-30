from pydantic import BaseModel


class TrendAnalysis(BaseModel):
    overdue_increasing: bool
    actual_hours_increasing: bool


class EmployeeRiskAnalysis(BaseModel):
    employee_id: str
    periods: int
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    estimated_hours: float
    actual_hours: float
    email_count: int
    completion_rate: float
    trends: TrendAnalysis
    risk_score: int
    risk_level: str


class AIAnalysis(BaseModel):
    explanation: str
    warning_signs: list[str]
    recommendations: list[str]


class AgentResult(BaseModel):
    analysis: EmployeeRiskAnalysis
    ai_analysis: AIAnalysis
