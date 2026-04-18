import json
import logging
from app.schemas import ScrumOutput

logger = logging.getLogger(__name__)

def normalize_output(raw_output: str):
    try:
        parsed = json.loads(raw_output)
        validated = ScrumOutput(**parsed)
        return validated.dict()

    except Exception as e:
        logger.warning(f"Validation failed: {str(e)}")

        return {
            "error": "Invalid structured output",
            "raw_output": raw_output
        }
