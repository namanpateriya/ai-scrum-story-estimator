import json
import logging
import os
from openai import OpenAI
from app.schemas import ScrumOutput

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def repair_json(raw_output: str):
    """
    Attempt to repair invalid JSON using LLM
    """
    try:
        prompt = f"""
Fix the following into STRICT valid JSON only.

Return ONLY JSON.

INPUT:
{raw_output}
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"JSON repair failed: {str(e)}")
        return None


def consistency_check(output: dict):
    """
    Basic cross-field consistency checks
    """
    try:
        if "technical_approach" in output and "story_points" in output:
            if "complex" in output["technical_approach"].lower() and output["story_points"] < 5:
                output["story_points"] = 5  # bump up

        if len(output.get("risks", [])) > 3 and output["story_points"] < 5:
            output["story_points"] = 5

        return output

    except Exception:
        return output


def normalize_output(raw_output: str):
    """
    Full pipeline:
    Parse → Validate → Repair → Enforce → Return
    """

    # Step 1: Try parse
    try:
        parsed = json.loads(raw_output)
    except Exception:
        logger.warning("Initial JSON parsing failed. Attempting repair...")
        repaired = repair_json(raw_output)

        if not repaired:
            return {"error": "Unrecoverable JSON", "raw_output": raw_output}

        try:
            parsed = json.loads(repaired)
        except Exception:
            return {"error": "Repair failed", "raw_output": raw_output}

    # Step 2: Validate schema
    try:
        validated = ScrumOutput(**parsed).dict()
    except Exception as e:
        logger.warning(f"Schema validation failed: {str(e)}")
        return {"error": "Schema validation failed", "raw_output": parsed}

    # Step 3: Consistency check
    validated = consistency_check(validated)

    return validated
