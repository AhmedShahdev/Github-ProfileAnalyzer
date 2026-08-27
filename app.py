from fastapi import FastAPI, HTTPException
from analyzer import analyze_user

app = FastAPI(title= "Github Profile Analyzer")

cache={}

@app.get("/analyze/{username}")
async def analyze(username: str):
    if username in cache:
        return cache[username]

    result = await analyze_user(username)

    if result is None:
        raise HTTPException(status_code= 404, detail=f"Github user '{username}' not found")

    cache[username] = result

    return result


@app.get("/")
async def root():
    return {"message": "Github Analyzer API - try/analyze/torvalds"}