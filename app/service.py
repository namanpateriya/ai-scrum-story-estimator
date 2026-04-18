import logging
from crewai import Crew
from app.agents import get_agents
from app.tasks import get_tasks
from app.aggregator import normalize_output

logger = logging.getLogger(__name__)

def run_scrum_team(input_text: str):
    try:
        if not input_text.strip():
            raise ValueError("Empty input")

        po, dev, qa, sm = get_agents()
        tasks = get_tasks(input_text, po, dev, qa, sm)

        crew = Crew(
            agents=[po, dev, qa, sm],
            tasks=tasks,
            verbose=True
        )

        result = crew.kickoff()

        return normalize_output(result)

    except Exception as e:
        logger.error(f"Scrum execution failed: {str(e)}")
        raise
