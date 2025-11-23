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

## ✅ **Checklist Update:**

Pastikan 3 file ini sudah benar:

### **1. `backend/api/routes/budget_routes.py`**
- ✅ Line 8: `from app.agents.budget_agent import budget_agent`
- ✅ Line 47: `from app.agents.budget_agent import KNOWLEDGE_BASE`

### **2. `backend/app/main.py`**
- ✅ Line ~190: Import budget router
- ✅ Version 3.0.0

### **3. `backend/app/agents/budget_agent.py`**
- ✅ Already exists (from screenshot)
- ✅ Has `budget_agent = BudgetAgent()` at bottom

---

## 🚀 **Deployment Steps:**

1. **Update `backend/api/routes/budget_routes.py`** - Fix import path
2. **Update `backend/app/main.py`** - Add budget router (versi 3.0.0)
3. **Commit & Push ke GitHub**
4. **Wait Railway auto-deploy** (~2 min)
5. **Check Railway logs** - Harusnya muncul "✓ Budget router loaded"
6. **Test bot lagi** - Klik Budget button

---

## 📊 **Expected Railway Logs After Fix:**
```
✓ Users router loaded
✓ Umrah router loaded  
✓ Chat router loaded
✓ Advanced router loaded
✓ Budget router loaded  ← HARUS ADA INI!

Successfully loaded 5 routers: users, umrah, chat, advanced, budget
