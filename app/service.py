import logging
import time
from crewai import Crew
from app.agents import get_agents
from app.tasks import get_tasks
from app.aggregator import normalize_output

# Optional Repo 1 integration
try:
    from app.service_repo1 import refine_jira_story
    REPO1_AVAILABLE = True
except:
    REPO1_AVAILABLE = False

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
TIMEOUT_SECONDS = 60


def run_scrum_team(input_text: str, use_refinement=False):
    if not input_text.strip():
        raise ValueError("Empty input")

    start_time = time.time()

    # Optional Repo 1 integration
    if use_refinement and REPO1_AVAILABLE:
        logger.info("Running refinement step (Repo 1)")
        input_text = refine_jira_story(input_text)

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

            elapsed = time.time() - start_time
            logger.info(f"Execution time: {elapsed:.2f}s")
            logger.info(f"Output size: {len(str(result))} chars")

            normalized = normalize_output(result)

            if "error" not in normalized:
                return normalized

            logger.warning("Validation failed, retrying...")

        except Exception as e:
            logger.error(f"Crew execution failed: {str(e)}")

        if time.time() - start_time > TIMEOUT_SECONDS:
            logger.error("Timeout reached")
            break

    return {
        "error": "Failed after retries/timeout",
        "raw_output": result if 'result' in locals() else None
    }
