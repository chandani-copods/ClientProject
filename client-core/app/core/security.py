from datetime import datetime, timedelta, timezone
import secrets
from uuid import UUID
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
from pydantic import ValidationError
from app.core.config import settings

# Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    sub: str,
    client_id: UUID | None,
    role_id: UUID | None,
    jti: UUID,
    sid: UUID,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "jti": str(jti),
        "sid": str(sid),
        "sub": str(sub),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "iss": "client-core",  # TODO: Change to the actual issuer
        "aud": "client-web",  # TODO: Change to the actual audience
        # if None then don't serialize
        "role_id": str(role_id) if role_id else None,
        "client_id": str(client_id) if client_id else None,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    sub: str, jti: UUID, expiry: datetime, client_id: UUID | None, role_id: UUID | None
) -> str:
    to_encode = {
        "jti": str(jti),
        "sub": str(sub),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": expiry,
        "iss": "client-core",  # TODO: Change to the actual issuer
        "aud": "client-web",  # TODO: Change to the actual audience
        # if None then don't serialize
        "role_id": str(role_id) if role_id else None,
        "client_id": str(client_id) if client_id else None,
        
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        # TODO: Add issuer and audience validation
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="client-web",
            issuer="client-core",
        )
        return payload if payload.get("exp") >= datetime.now(timezone.utc).timestamp() else None
    
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except ValidationError as e:
        print(f"ValidationError: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def decode_refresh_token(token: str, allow_expired: bool = False):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="client-web",
            issuer="client-core",
            options={"verify_exp": not allow_expired},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.InvalidTokenError as e:
        print(f"InvalidTokenError: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


# Generate OTP
def generate_otp(length: int = 6) -> str:
    """Generates a cryptographically secure numeric OTP."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


# Hash OTP
def hash_otp(otp: str) -> str:
    return pwd_context.hash(otp)


# Verify OTP
def verify_otp(otp: str, hashed_otp: str) -> bool:
    return pwd_context.verify(otp, hashed_otp)

