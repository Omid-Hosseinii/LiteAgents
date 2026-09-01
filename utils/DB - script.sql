SELECT current_database(), current_user;

CREATE TABLE public.employee_activity (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50),
    timestamp TIMESTAMP,
    source VARCHAR(20),
    data JSONB
);

CREATE TABLE public.employee_timeseries (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50),
    date DATE,
    total_tasks INT DEFAULT 0,
    completed_tasks INT DEFAULT 0,
    overdue_tasks INT DEFAULT 0,
    estimated_hours NUMERIC DEFAULT 0,
    actual_hours NUMERIC DEFAULT 0,
    email_count INT DEFAULT 0
);

CREATE TABLE public.employee_risk_analysis (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50),
    risk_score INT,
    risk_level VARCHAR(20),
    explanation TEXT,
    warning_signs JSONB,
    recommendations JSONB,
    created_at TIMESTAMP,
    CONSTRAINT unique_employee_risk UNIQUE (employee_id)
);



TRUNCATE table employee_activity;
TRUNCATE TABLE employee_timeseries;
TRUNCATE table employee_risk_analysis;

select * from employee_activity;
select * from employee_timeseries;


SELECT
    id,
    employee_id,
    risk_score,
    risk_level,
    warning_signs,
    recommendations,
    created_at
FROM employee_risk_analysis;

