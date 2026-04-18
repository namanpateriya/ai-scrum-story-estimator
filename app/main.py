from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.service import run_scrum_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Scrum Estimator")

class InputModel(BaseModel):
    input: str

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/estimate")
def estimate(data: InputModel):
    try:
        if not data.input.strip():
            raise HTTPException(400, "Empty input")

        logger.info("API request received")

        result = run_scrum_team(data.input)

        return result

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Estimation failed")
