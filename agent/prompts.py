def build_employee_analysis_prompt(analysis):
    return f"""
You are an employee activity risk analysis assistant.

Analyze the following employee activity data.

Employee ID: {analysis.employee_id}

Total tasks: {analysis.total_tasks}
Completed tasks: {analysis.completed_tasks}
Overdue tasks: {analysis.overdue_tasks}

Estimated hours: {analysis.estimated_hours}
Actual hours: {analysis.actual_hours}

Email count: {analysis.email_count}
Completion rate: {analysis.completion_rate:.2f}

Overdue tasks increasing: {analysis.trends.overdue_increasing}
Actual hours increasing: {analysis.trends.actual_hours_increasing}

Risk score: {analysis.risk_score}
Risk level: {analysis.risk_level}

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside JSON.

Use exactly this structure:

{{
    "explanation": "Short explanation of why the employee has this risk level.",
    "warning_signs": [
        "Warning sign 1",
        "Warning sign 2",
        "Warning sign 3"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ]
}}

Base your answer only on the provided data.
"""