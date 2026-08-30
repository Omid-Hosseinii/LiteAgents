from utils.n8n import trigger_workflow

from agent.agent import (
    get_employee_ids,
    analyze,
    save_analysis,
)


def run_pipeline():

    # 1. Run n8n and wait until it finishes
    trigger_workflow()

    # 2. Get employees from PostgreSQL
    employee_ids = get_employee_ids()

    results = []

    # 3. Run AI analysis for every employee
    for employee_id in employee_ids:

        result = analyze(employee_id)

        if result is not None:
            save_analysis(result)

            results.append(
                {
                    "employee_id": employee_id,
                    "risk_level": result.analysis.risk_level,
                    "risk_score": result.analysis.risk_score,
                }
            )

    return {
        "total_employees": len(employee_ids),
        "processed_employees": len(results),
        "results": results,
    }
