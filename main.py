from agent.agent import get_employee_ids, analyze, save_analysis
from utils.logger import get_logger

logger = get_logger(__name__)


def analyze_llm():
    employee_ids = get_employee_ids()

    logger.info(f"Found {len(employee_ids)} employees")
    logger.info("=" * 60)

    for employee_id in employee_ids:
        logger.info(f"Analyzing {employee_id}...")

        result = analyze(employee_id)

        if result is not None:
            save_analysis(result)

            logger.info(f"{employee_id}: ")
            logger.info(f"{result.analysis.risk_level} ")
            logger.info(f"({result.analysis.risk_score})")

        else:
            logger.info(f"{employee_id}: FAILED")
            print()

        logger.info("-" * 60)


if __name__ == "__main__":
    analyze_llm()
