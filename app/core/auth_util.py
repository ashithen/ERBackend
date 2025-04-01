from fastapi import Header, status, HTTPException
import firebase_admin
from firebase_admin import credentials, auth
from typing_extensions import Annotated
from app.core.config import settings


def init_firebase():
    try:
        if settings.env == "local":
            cred = credentials.Certificate("app/core/lecturelift_serviceaccount.json")
        else:
            cred = credentials.ApplicationDefault() # For GCP
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase app: {e}")

async def verify_and_get_user(auth_token: Annotated[str, Header()]):
    if not auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing.")
    try:
        decoded_token = auth.verify_id_token(auth_token)
        return decoded_token["user_id"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token.")