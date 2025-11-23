# -*- coding: utf-8 -*-
"""
Umrah API endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ManasikResponse(BaseModel):
    title: str
    description: str
    steps: List[str]

@router.get("/manasik", response_model=ManasikResponse)
async def get_manasik():
    """Get manasik umrah overview"""
    return {
        "title": "Manasik Umrah",
        "description": "Panduan lengkap umrah",
        "steps": [
            "Ihram dari miqat",
            "Thawaf 7 putaran",
            "Sa'i 7 kali",
            "Tahalul"
        ]
    }

@router.get("/health")
async def umrah_health():
    """Health check"""
    return {"status": "healthy", "service": "umrah"}
