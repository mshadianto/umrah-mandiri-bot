"""
Budget optimization routes for Umrah Assistant API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.agents.budget_agent import budget_agent, KNOWLEDGE_BASE

router = APIRouter(prefix="/budget", tags=["Budget"])


class BudgetRequest(BaseModel):
    """Request model for budget optimization"""
    jamaah_count: int
    duration_days: int
    budget_max: int
    preferences: Optional[dict] = None


class PackageRecommendation(BaseModel):
    """Single package recommendation"""
    name: str
    total_price: int
    price_per_person: int
    hotel_makkah: str
    hotel_madinah: str
    airline: str
    breakdown: dict


class BudgetResponse(BaseModel):
    """Response model for budget optimization"""
    status: str
    packages: List[PackageRecommendation]


@router.post("/optimize", response_model=BudgetResponse)
async def optimize_budget(request: BudgetRequest):
    """
    Optimize budget and return 3 package recommendations using AI
    """
    try:
        result = await budget_agent.optimize_budget(
            jamaah_count=request.jamaah_count,
            duration=request.duration_days,
            budget_max=request.budget_max,
            preferences=request.preferences or {}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Budget optimization failed: {str(e)}")


@router.get("/knowledge-base")
async def get_knowledge_base():
    """
    Get the knowledge base for budget optimization
    """
    return {
        "status": "success",
        "knowledge_base": KNOWLEDGE_BASE
    }
