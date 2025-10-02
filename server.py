# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "pandas",
# ]
# ///

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Load CSV once at startup
df = pd.read_csv("q-fastapi.csv")

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_methods=["*"],   # allow all methods
    allow_headers=["*"],   # allow all headers
)

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    """
    Return students from CSV.
    If ?class=... is provided, filter by one or more classes.
    """
    if class_:
        filtered = df[df["class"].isin(class_)]
    else:
        filtered = df

    students = [
        {"studentId": int(row.studentId), "class": row["class"]}
        for row in filtered.itertuples(index=False)
    ]
    return {"students": students}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
