from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Annotated, Optional
from datetime import datetime, timezone

from db import get_session
from models import User, Session as SessionModel

router = APIRouter()

# Security Config
security = HTTPBearer()

# --- Models ---
class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

# --- Dependency ---
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_session)
) -> str:
    """
    Verify Better Auth session token by checking the database.

    Logic:
    1. Extract Bearer token from Authorization header
    2. Query session table for matching token
    3. Validate session exists and hasn't expired
    4. Return string user_id from Better Auth

    Returns:
        str: String user ID from Better Auth
    """
    token = credentials.credentials

    try:
        # 1. Query session table for this token
        statement = select(SessionModel).where(SessionModel.token == token)
        result = session.exec(statement).first()

        # 2. Check if session exists
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Check if session has expired (compare offset-aware datetimes)
        current_time = datetime.now(timezone.utc)
        if result.expires_at < current_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 4. Verify user still exists
        user = session.get(User, result.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 5. Return string user_id from Better Auth
        return user.id

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )