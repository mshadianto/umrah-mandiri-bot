# -*- coding: utf-8 -*-
"""
Agent Orchestrator - Routes queries to specialized agents
"""
from typing import Dict, Any, List
from app.agents.guide_agent import GuideAgent
from app.agents.doa_agent import DoaAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.location_agent import LocationAgent
import logging

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrates multiple specialized agents"""
    
    def __init__(self):
        self.agents = {
            "guide": GuideAgent(),
            "doa": DoaAgent(),
            "budget": BudgetAgent(),
            "location": LocationAgent()
        }
    
    async def route_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route query to appropriate agent"""
        # Determine which agent should handle the query
        agent_name = self._classify_query(query)
        
        logger.info(f"Routing query to {agent_name} agent: {query}")
        
        # Execute agent
        agent = self.agents.get(agent_name)
        if agent:
            result = await agent.execute({
                "query": query,
                "context": context or {}
            })
            return result
        else:
            # Fallback to guide agent
            return await self.agents["guide"].execute({
                "query": query,
                "context": context or {}
            })
    
    def _classify_query(self, query: str) -> str:
        """Classify query to determine which agent to use"""
        query_lower = query.lower()
        
        # Doa keywords
        if any(word in query_lower for word in ['doa', 'dzikir', 'bacaan', 'wirid']):
            return "doa"
        
        # Budget keywords
        if any(word in query_lower for word in ['biaya', 'harga', 'budget', 'murah', 'mahal', 'berapa']):
            return "budget"
        
        # Location keywords
        if any(word in query_lower for word in ['lokasi', 'tempat', 'dimana', 'di mana', 'hotel', 'pintu', 'jarak']):
            return "location"
        
        # Default to guide agent
        return "guide"