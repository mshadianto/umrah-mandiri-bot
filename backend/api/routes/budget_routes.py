# -*- coding: utf-8 -*-
"""
Budget API Routes with RAG Agent
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from app.agents.budget_agent import budget_agent

router = APIRouter(prefix="/api/v1/budget", tags=["budget"])

class BudgetRequest(BaseModel):
    jamaah: int
    duration: int
    budget_max: Optional[int] = None
    preferences: Optional[Dict] = None

class BudgetResponse(BaseModel):
    status: str
    data: Dict

@router.post("/optimize", response_model=BudgetResponse)
async def optimize_budget(request: BudgetRequest):
    """
    Get AI-powered budget recommendations
    """
    try:
        recommendations = await budget_agent.analyze_and_recommend(
            jamaah=request.jamaah,
            duration=request.duration,
            budget_max=request.budget_max,
            preferences=request.preferences
        )
        
        return BudgetResponse(
            status="success",
            data=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge-base")
async def get_knowledge_base():
    """Get available hotels and prices"""
    from app.agents.budget_agent import KNOWLEDGE_BASE
    return {
        "status": "success",
        "data": KNOWLEDGE_BASE
    }
```

---

## ✅ **Verification After Fix:**

Expected logs setelah fix dan redeploy:
```
✓ Users router loaded
✓ Umrah router loaded
✓ Chat router loaded
✓ Advanced router loaded
✓ Budget router loaded  ← HARUS MUNCUL!

Successfully loaded 5 routers: users, umrah, chat, advanced, budget
✅ API is ready to accept requests!
