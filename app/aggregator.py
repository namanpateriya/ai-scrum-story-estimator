import json
import logging

logger = logging.getLogger(__name__)

def normalize_output(raw_output: str):
    try:
        return json.loads(raw_output)
    except Exception as e:
        logger.error("JSON parsing failed")
        return {
            "error": "Invalid JSON output",
            "raw_output": raw_output
        }
