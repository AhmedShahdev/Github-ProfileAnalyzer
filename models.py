from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class SearchHistory(Base):
    __tablename__ = "github_search_history"

    id = Column(Integer, primary_key=True)
    username = Column(String , index=True)
    searched_at= Column(String, default=datetime.utcnow)
    followers = Column(Integer)
    public_repos = Column(Integer)
    top_languages = Column(String)