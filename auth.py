from fastapi import Header, HTTPException
from typing import Optional

API_KEYS = {
    "ahmed-user-123",
    "client-github"
}

def verify_api_key(x_api_key: Optional[str]= Header(None)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
