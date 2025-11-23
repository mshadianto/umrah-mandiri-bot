# -*- coding: utf-8 -*-
"""
Users API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current user (placeholder)"""
    return {
        "id": "1",
        "username": "test_user",
        "email": "test@example.com"
    }

@router.get("/health")
async def users_health():
    """Health check for users endpoint"""
    return {"status": "healthy", "service": "users"}
