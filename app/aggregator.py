import json
import logging
import os
from openai import OpenAI
from app.schemas import ScrumOutput

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def safe_parse(raw):
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        raw = str(raw)

    try:
        return json.loads(raw)
    except:
        return None


def repair_json(raw_output: str):
    try:
        prompt = f"""
Fix this into VALID JSON matching schema:

{raw_output}
"""

        res = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return safe_parse(res.choices[0].message.content)

    except Exception as e:
        logger.error(f"Repair failed: {e}")
        return None


def validate_partial(data: dict):
    """
    Partial validation — don't fail entire output
    """
    validated = {}

    for field in ScrumOutput.__fields__:
        validated[field] = data.get(field)

    # enforce defaults
    validated["story_points"] = validated.get("story_points") or 3
    validated["priority"] = validated.get("priority") or "Medium"

    return validated


def normalize_output(raw_output):
    parsed = safe_parse(raw_output)

    if not parsed:
        logger.warning("Parsing failed, attempting repair")
        parsed = repair_json(raw_output)

    if not parsed:
        return {"error": "Unrecoverable output", "raw_output": raw_output}

    return validate_partial(parsed)
