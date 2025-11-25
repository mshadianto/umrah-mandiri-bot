# -*- coding: utf-8 -*-
"""
Budget optimization routes for Umrah Assistant API
FIXED VERSION - Correct endpoint prefix
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.agents.budget_agent import budget_agent

logger = logging.getLogger(__name__)

# ✅ FIXED: Correct prefix with /api/v1
router = APIRouter(prefix="/api/v1/budget", tags=["Budget"])


class BudgetOptimizeRequest(BaseModel):
    """Request model for budget optimization"""
    jamaah: int
    duration: int
    budget_max: Optional[int] = None
    preferences: Optional[Dict[str, Any]] = None


@router.post("/optimize")
async def optimize_budget(request: BudgetOptimizeRequest):
    """
    AI-powered budget optimization
    Returns 3 package recommendations (Ekonomis, Standar, Premium)
    """
    try:
        logger.info(f"Budget optimization request: {request.jamaah} jamaah, {request.duration} days")
        
        # Call budget agent
        result = await budget_agent.analyze_and_recommend(
            jamaah=request.jamaah,
            duration=request.duration,
            budget_max=request.budget_max,
            preferences=request.preferences
        )
        
        # Validate result
        if not result or "packages" not in result:
            logger.error("Budget agent returned invalid result")
            raise HTTPException(
                status_code=500,
                detail="Budget optimization failed - invalid response from AI"
            )
        
        logger.info(f"✅ Successfully generated {len(result['packages'])} packages")
        
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Budget optimization error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Budget optimization failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check for budget service"""
    try:
        # Check if Groq API key is configured
        groq_configured = budget_agent.groq_client is not None
        
        return {
            "status": "healthy",
            "service": "budget_optimizer",
            "groq_api": "configured" if groq_configured else "not_configured",
            "endpoint": "/api/v1/budget/optimize"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify routing works"""
    return {
        "message": "Budget service is reachable!",
        "endpoint": "/api/v1/budget/test",
        "status": "ok"
    }
