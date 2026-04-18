from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.service import run_scrum_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Scrum Estimator")


class InputModel(BaseModel):
    input: str
    refine: bool = False


class BatchInput(BaseModel):
    inputs: list[str]
    refine: bool = False


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/estimate")
def estimate(data: InputModel):
    try:
        result = run_scrum_team(data.input, use_refinement=data.refine)
        return result
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, "Estimation failed")


@app.post("/estimate-batch")
def estimate_batch(data: BatchInput):
    results = []

    for inp in data.inputs:
        try:
            res = run_scrum_team(inp, use_refinement=data.refine)
            results.append(res)
        except Exception as e:
            results.append({"error": str(e)})

    return {"results": results}
