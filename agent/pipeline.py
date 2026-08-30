
import time

from agent.agent import run_analysis_pipeline
from agent.repository import (
    get_employee_ids,
    save_analysis,
)


def execute_pipeline(progress_callback=None):

    start_time = time.perf_counter()

    employee_ids = get_employee_ids()

    total = len(employee_ids)
    completed = 0

    for result in run_analysis_pipeline(employee_ids):

        save_analysis(result)

        completed += 1

        if progress_callback:

            progress_callback(
                completed,
                total,
                result.analysis.employee_id,
                result.analysis.risk_level,
                result.analysis.risk_score,
            )

    elapsed_time = time.perf_counter() - start_time

    return {
        "total": total,
        "completed": completed,
        "elapsed_time": round(
            elapsed_time,
            2,
        ),
    }

