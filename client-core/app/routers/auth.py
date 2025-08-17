from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import Client
from app.schemas.client import ClientCreate
from app.core.security import create_access_token, generate_otp, get_password_hash, verify_password
from app.core.database import get_session  # Make sure to provide DB session dependency

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_create: ClientCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(Client).where(Client.client_email == user_create.client_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user_create.hashed_password)
    db_user = Client(
        client_email=user_create.client_email,
        client_name=user_create.client_name,
        client_username=user_create.client_username,
        hashed_password=hashed_pw,
        client_role="user",
        client_role_in_company=user_create.client_role_in_company,
        country=user_create.country,
        client_phone=user_create.client_phone,
        client_address=user_create.client_address,
        company_id=user_create.company_id,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(Client).where(Client.client_email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.client_email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/otp/request")
def request_otp(email: str, session: Session = Depends(get_session)):
    user = session.exec(select(Client).where(Client.client_email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    
    # Save OTP and expiry in DB or in-memory cache keyed by user (not shown)
    # Trigger email or SMS send with the OTP here
    
    return {"msg": "OTP sent"}

@router.post("/login/otp/verify")
def verify_otp(email: str, otp: str):
    # Verify OTP against stored value and expiry
    
    # If valid, create and return JWT token
    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
