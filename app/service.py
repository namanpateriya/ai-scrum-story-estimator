import logging
from crewai import Crew
from app.agents import get_agents
from app.tasks import get_tasks
from app.aggregator import normalize_output

logger = logging.getLogger(__name__)

MAX_RETRIES = 2

def run_scrum_team(input_text: str):
    if not input_text.strip():
        raise ValueError("Empty input")

    po, dev, qa, sm = get_agents()
    tasks = get_tasks(input_text, po, dev, qa, sm)

    crew = Crew(
        agents=[po, dev, qa, sm],
        tasks=tasks,
        verbose=True
    )

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Running CrewAI (attempt {attempt+1})")

            result = crew.kickoff()

            logger.info("Raw Output Received")
            logger.info(result)

            normalized = normalize_output(result)

            if "error" not in normalized:
                return normalized

            logger.warning("Invalid output, retrying...")

        except Exception as e:
            logger.error(f"Crew execution failed: {str(e)}")

    return {
        "error": "Failed after retries",
        "raw_output": result if 'result' in locals() else None
    }
