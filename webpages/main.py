import os
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import Graphrag class
# from graph import Graphrag 

from graph import graphrag

app = FastAPI()

# Initialize the Graphrag instance
graphrag = graphrag.Graphrag(local=True)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: str

@app.post("/query_similarity", response_model=QueryResponse)
async def query_similarity(query_request: QueryRequest):
    try:
        results = graphrag.query_similarity(query_request.query)
        return QueryResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
