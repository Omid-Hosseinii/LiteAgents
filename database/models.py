
from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class EmployeeTimeseries(Base):

    __tablename__ = "employee_timeseries"

    employee_id = Column(
        String(50),
        primary_key=True,
    )

    date = Column(
        Date,
        primary_key=True,
    )

    total_tasks = Column(
        Integer,
        nullable=False,
    )

    completed_tasks = Column(
        Integer,
        nullable=False,
    )

    overdue_tasks = Column(
        Integer,
        nullable=False,
    )

    estimated_hours = Column(
        Float,
        nullable=False,
    )

    actual_hours = Column(
        Float,
        nullable=False,
    )

    email_count = Column(
        Integer,
        nullable=False,
    )


class EmployeeRiskAnalysis(Base):

    __tablename__ = "employee_risk_analysis"

    id = Column(
        Integer,
        primary_key=True,
    )

    employee_id = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    risk_score = Column(
        Integer,
        nullable=False,
    )

    risk_level = Column(
        String(20),
        nullable=False,
    )

    explanation = Column(
        String,
        nullable=False,
    )

    warning_signs = Column(
        JSONB,
        nullable=False,
    )

    recommendations = Column(
        JSONB,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

