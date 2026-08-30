from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from analyzer import analyze_user
from database import get_db, engine, Base
from models import SearchHistory
from auth import verify_api_key 

Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Github Profile Analyzer")

cache={}

@app.get("/analyze/{username}")
async def analyze(username: str, db:Session=Depends(get_db), _: None = Depends(verify_api_key)):
    if username in cache:
        return cache[username]

    result = await analyze_user(username)

    if result is None:
        raise HTTPException(status_code= 404, detail=f"Github user '{username}' not found")

    record = SearchHistory(
        username=username,
        followers=result["followers"],
        public_repos=result["public_repos"],
        top_languages=", ".join(result["top_languages"])
    )
    db.add(record)
    db.commit()

    cache[username] = result
    return result

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(SearchHistory)\
        .order_by(SearchHistory.searched_at.desc())\
        .limit(10)\
        .all()

    return[
        {
            "username": r.username,
            "followers": r.followers,
            "public_repos": r.public_repos,
            "top_languages": r.top_languages,
            "searched_at": r.searched_at
        }
        for r in records
    ]

@app.get("/stats")
def get_stats(db:Session=Depends(get_db)):
    from sqlalchemy import func

    results = db.query(
        SearchHistory.username,
        func.count(SearchHistory.id).label("search_count")
    ).group_by(SearchHistory.username)\
    .order_by(func.count(SearchHistory.id).desc())\
    .all()

    return{
        "most_searched":[
            {"username": r.username, "search_count": r.search_count}
            for r in results
        ],
        "total_searches": sum(r.search_count for r in results)
    }

@app.get("/")
async def root():
    return {"message": "Github Analyzer API - try/analyze/torvalds"}