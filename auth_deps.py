from fastapi import HTTPException, Header
from firebase_admin import auth

async def get_uid(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split("Bearer ")[1]

    try:
        decoded = auth.verify_id_token(token)
        return decoded["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
