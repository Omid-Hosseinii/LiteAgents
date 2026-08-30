import json
from agent.analyzer import (
    analyze_employee,
    calculate_risk_score,
    get_risk_level,
)

from agent.models import (
    EmployeeRiskAnalysis,
    AgentResult,
    AIAnalysis,
)

from agent.prompts import build_employee_analysis_prompt
from agent.llm import generate_response


def analyze(employee_id):
    """
    Analyze one employee and generate AI analysis.
    """

    res = analyze_employee(employee_id)

    if res is None:
        return None

    risk_score = calculate_risk_score(res)
    risk_level = get_risk_level(risk_score)

    res["risk_score"] = risk_score
    res["risk_level"] = risk_level

    analysis = EmployeeRiskAnalysis(**res)

    prompt = build_employee_analysis_prompt(analysis)

    llm_response = generate_response(prompt)

    ai_data = json.loads(llm_response)

    ai_analysis = AIAnalysis(**ai_data)

    return AgentResult(
        analysis=analysis,
        ai_analysis=ai_analysis,
    )


def run_analysis_pipeline(employee_ids):
    """
    Run the complete analysis pipeline.

    Yields the result of each employee after analysis.
    """

    for employee_id in employee_ids:

        result = analyze(employee_id)

        if result is not None:
            yield result

