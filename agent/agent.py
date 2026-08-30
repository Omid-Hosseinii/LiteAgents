import json
import psycopg2

from analyzer import analyze_employee, calculate_risk_score, get_risk_level
from models import EmployeeRiskAnalysis, AgentResult, AIAnalysis
from prompts import build_employee_analysis_prompt
from llm import generate_response


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "ai_user",
    "password": "ai_password", }


def analyze(employee_id_):
    res = analyze_employee(employee_id_)

    if res is None:
        return None

    risk_score = calculate_risk_score(res)
    risk_level = get_risk_level(risk_score)

    res["risk_score"] = risk_score
    res["risk_level"] = risk_level

    analysis = EmployeeRiskAnalysis(**res)

    prompt = build_employee_analysis_prompt(analysis)

    llm_response = generate_response(prompt)

    print("\n========== LLM RESPONSE ==========")
    print(llm_response)
    print("==================================\n")

    try:
        ai_data = json.loads(llm_response)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from LLM for {employee_id_}")
        print(f"JSON error: {e}")
        return None

    try:
        ai_analysis = AIAnalysis(**ai_data)
    except Exception as e:
        print(f"ERROR: Invalid AI analysis for {employee_id_}")
        print(f"Validation error: {e}")
        return None

    return AgentResult(
        analysis=analysis,
        ai_analysis=ai_analysis,
    )




def get_employee_ids():
    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT employee_id
                FROM employee_timeseries
                ORDER BY employee_id;
                """
            )

            return [row[0] for row in cursor.fetchall()]

    finally:
        connection.close()


def save_analysis(res):
    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO employee_risk_analysis (
                    employee_id,
                    risk_score,
                    risk_level,
                    explanation,
                    warning_signs,
                    recommendations
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (employee_id)
                DO UPDATE SET
                    risk_score = EXCLUDED.risk_score,
                    risk_level = EXCLUDED.risk_level,
                    explanation = EXCLUDED.explanation,
                    warning_signs = EXCLUDED.warning_signs,
                    recommendations = EXCLUDED.recommendations,
                    created_at = CURRENT_TIMESTAMP;
                """,
                (
                    res.analysis.employee_id,
                    res.analysis.risk_score,
                    res.analysis.risk_level,
                    res.ai_analysis.explanation,
                    json.dumps(res.ai_analysis.warning_signs),
                    json.dumps(res.ai_analysis.recommendations),
                ),
            )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    employee_ids = get_employee_ids()

    print(f"Found {len(employee_ids)} employees")
    print("=" * 60)

    for employee_id in employee_ids:
        print(f"Analyzing {employee_id}...")

        result = analyze(employee_id)

        if result is not None:
            save_analysis(result)

            print(
                f"{employee_id}: "
                f"{result.analysis.risk_level} "
                f"({result.analysis.risk_score})"
            )
        else:
            print(f"{employee_id}: FAILED")

        print("-" * 60)
