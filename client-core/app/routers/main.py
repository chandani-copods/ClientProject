from fastapi import APIRouter
from app.services.utils import common_error_responses
from app.routers import (
    auth,
    
)

api_router = APIRouter(responses=common_error_responses)
api_router.include_router(auth.router)
