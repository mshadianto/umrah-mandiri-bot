# -*- coding: utf-8 -*-
"""
Budget optimization routes for Umrah Assistant API
FIXED VERSION - No circular import (using lazy loading)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

# ✅ Create router with correct prefix
router = APIRouter(prefix="/api/v1/budget", tags=["Budget"])


class BudgetRequest(BaseModel):
    """Request model for budget optimization"""
    jamaah: int
    duration: int
    budget_max: Optional[int] = None
    preferences: Optional[Dict] = None


@router.get("/health")
async def budget_health():
    """
    Health check for budget service
    """
    import os
    
    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    
    return {
        "status": "healthy",
        "service": "budget_optimizer",
        "groq_api": "configured" if groq_configured else "not_configured",
        "endpoint": "/api/v1/budget/optimize"
    }


@router.get("/test")
async def budget_test():
    """
    Test endpoint to verify budget service is working
    """
    return {
        "status": "ok",
        "message": "Budget service is running",
        "endpoints": {
            "health": "/api/v1/budget/health",
            "optimize": "/api/v1/budget/optimize",
            "knowledge_base": "/api/v1/budget/knowledge-base"
        }
    }


@router.post("/optimize")
async def optimize_budget(request: BudgetRequest):
    """
    Optimize budget and return 3 package recommendations using AI
    
    Uses lazy import to avoid circular dependency
    """
    try:
        # ✅ LAZY IMPORT - Import only when function is called
        # This avoids circular import at module load time
        from app.agents.budget_agent import BudgetAgent
        
        # Create agent instance
        agent = BudgetAgent()
        
        logger.info(f"Budget optimization request: {request.jamaah} jamaah, {request.duration} days")
        
        # Call agent
        result = await agent.analyze_and_recommend(
            jamaah=request.jamaah,
            duration=request.duration,
            budget_max=request.budget_max,
            preferences=request.preferences or {}
        )
        
        # Check for errors in result
        if "error" in result:
            logger.warning(f"Agent returned error: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Validate packages exist
        if "packages" not in result or not result["packages"]:
            logger.error("No packages in result")
            raise HTTPException(status_code=500, detail="Failed to generate packages")
        
        logger.info(f"✅ Generated {len(result['packages'])} packages")
        
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except ImportError as e:
        logger.error(f"Import error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Budget agent not available: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Budget optimization failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Budget optimization failed: {str(e)}"
        )


@router.get("/knowledge-base")
async def get_knowledge_base():
    """
    Get the knowledge base for budget optimization
    Uses lazy import
    """
    try:
        # ✅ LAZY IMPORT
        from app.agents.budget_agent import KNOWLEDGE_BASE
        
        return {
            "status": "success",
            "knowledge_base": KNOWLEDGE_BASE
        }
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Knowledge base not available"
        )
