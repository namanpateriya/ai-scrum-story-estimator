import logging
import time
from crewai import Crew
from app.agents import get_agents
from app.tasks import get_tasks
from app.aggregator import normalize_output

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
TIMEOUT_SECONDS = 60


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
            start = time.time()

            result = crew.kickoff()

            if not isinstance(result, str):
                result = str(result)

            output = normalize_output(result)

            if "error" not in output:
                return output

            logger.warning("Retrying due to invalid output")

            if time.time() - start > TIMEOUT_SECONDS:
                break

        except Exception as e:
            logger.error(f"Execution failed: {e}")

    return {"error": "Failed after retries"}
