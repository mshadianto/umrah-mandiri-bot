# -*- coding: utf-8 -*-
"""
Budget Optimization Routes - FIXED VERSION
Endpoint sudah disesuaikan dengan yang dipanggil oleh bot: /api/v1/budget/*
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.agents.budget_agent import budget_agent

logger = logging.getLogger(__name__)

# FIX: Gunakan prefix lengkap yang sesuai dengan bot
# Bot calls: /api/v1/budget/optimize
router = APIRouter(prefix="/api/v1/budget", tags=["Budget"])


class BudgetOptimizeRequest(BaseModel):
    """Request model untuk optimisasi budget"""
    jamaah: int
    duration: int
    budget_max: Optional[int] = None
    preferences: Optional[Dict[str, Any]] = None


class BudgetOptimizeResponse(BaseModel):
    """Response model untuk optimisasi budget"""
    status: str
    data: Dict[str, Any]
    message: Optional[str] = None


@router.post("/optimize", response_model=BudgetOptimizeResponse)
async def optimize_budget(request: BudgetOptimizeRequest):
    """
    🤖 AI Budget Optimizer
    
    Endpoint ini menganalisis requirement user dan memberikan 3 rekomendasi
    paket umrah optimal menggunakan RAG + LLM (Groq).
    
    Args:
        request: BudgetOptimizeRequest dengan jamaah, duration, dll
    
    Returns:
        BudgetOptimizeResponse dengan 3 paket rekomendasi
    
    Example:
        POST /api/v1/budget/optimize
        {
            "jamaah": 2,
            "duration": 10,
            "budget_max": 50000000,
            "preferences": {"type": "all"}
        }
    """
    try:
        logger.info(f"📊 Budget optimization request: {request.jamaah} jamaah, {request.duration} days")
        
        # Call budget agent
        result = await budget_agent.analyze_and_recommend(
            jamaah=request.jamaah,
            duration=request.duration,
            budget_max=request.budget_max,
            preferences=request.preferences
        )
        
        # Check if result is valid
        if not result or "packages" not in result:
            logger.error("Budget agent returned invalid result")
            raise HTTPException(
                status_code=500,
                detail="AI analysis failed. Please check Groq API configuration."
            )
        
        # Check if we got packages
        if len(result.get('packages', [])) == 0:
            logger.warning("No packages generated")
            raise HTTPException(
                status_code=500,
                detail="Could not generate package recommendations. Please try again."
            )
        
        logger.info(f"✅ Generated {len(result.get('packages', []))} package recommendations")
        
        return BudgetOptimizeResponse(
            status="success",
            data=result,
            message="Budget optimization completed successfully"
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        logger.error(f"❌ Budget optimization error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Budget optimization failed: {str(e)}"
        )


@router.get("/health")
async def budget_health():
    """
    Health check untuk budget service
    Memeriksa status Groq API configuration
    """
    from app.config import settings
    
    groq_configured = bool(
        settings.GROQ_API_KEY and 
        settings.GROQ_API_KEY != "your-groq-key-here" and
        len(settings.GROQ_API_KEY) > 20
    )
    
    return {
        "status": "healthy" if groq_configured else "degraded",
        "service": "budget_optimizer",
        "groq_api": "configured" if groq_configured else "not_configured",
        "endpoint": "/api/v1/budget/optimize",
        "note": "Get free Groq API key from https://console.groq.com" if not groq_configured else None
    }


@router.get("/knowledge-base")
async def get_knowledge_base():
    """
    Get sample dari knowledge base
    Untuk debugging dan verification
    """
    from app.agents.budget_agent import KNOWLEDGE_BASE
    
    # Return preview
    lines = KNOWLEDGE_BASE.split('\n')
    preview_lines = lines[:50]  # First 50 lines
    
    return {
        "status": "success",
        "preview": '\n'.join(preview_lines),
        "total_lines": len(lines),
        "total_chars": len(KNOWLEDGE_BASE),
        "note": "This is a preview of the knowledge base used for budget optimization"
    }


@router.get("/test")
async def test_budget():
    """
    Test endpoint untuk memverifikasi budget service berjalan
    """
    return {
        "status": "ok",
        "message": "Budget service is running",
        "endpoints": {
            "optimize": "/api/v1/budget/optimize (POST)",
            "health": "/api/v1/budget/health (GET)",
            "knowledge_base": "/api/v1/budget/knowledge-base (GET)"
        }
    }
