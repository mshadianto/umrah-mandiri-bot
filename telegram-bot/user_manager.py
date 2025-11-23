# -*- coding: utf-8 -*-
"""
User Data Manager - Stores user preferences and state
"""
from tinydb import TinyDB, Query
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserManager:
    """Manage user data and preferences"""
    
    def __init__(self, db_path: str = 'user_data.json'):
        self.db = TinyDB(db_path)
        self.users = self.db.table('users')
        self.conversations = self.db.table('conversations')
        self.progress = self.db.table('progress')
        
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data"""
        User = Query()
        result = self.users.get(User.user_id == user_id)
        return result
    
    def create_or_update_user(self, user_id: int, data: Dict[str, Any]):
        """Create or update user"""
        User = Query()
        
        # Merge with existing data
        existing = self.get_user(user_id)
        if existing:
            data = {**existing, **data, 'updated_at': datetime.now().isoformat()}
            self.users.update(data, User.user_id == user_id)
        else:
            data['user_id'] = user_id
            data['created_at'] = datetime.now().isoformat()
            data['updated_at'] = datetime.now().isoformat()
            self.users.insert(data)
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        user = self.get_user(user_id)
        return user.get('language', 'id') if user else 'id'
    
    def set_user_language(self, user_id: int, language: str):
        """Set user's language preference"""
        self.create_or_update_user(user_id, {'language': language})
    
    def get_user_location(self, user_id: int) -> Optional[str]:
        """Get user's location"""
        user = self.get_user(user_id)
        return user.get('location') if user else None
    
    def set_user_location(self, user_id: int, location: str):
        """Set user's location"""
        self.create_or_update_user(user_id, {'location': location})
    
    def add_conversation(self, user_id: int, message: str, response: str, agent: str = "unknown"):
        """Add conversation to history"""
        self.conversations.insert({
            'user_id': user_id,
            'message': message,
            'response': response[:500],  # Store summary
            'agent': agent,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_conversation_history(self, user_id: int, limit: int = 10):
        """Get recent conversation history"""
        User = Query()
        results = self.conversations.search(User.user_id == user_id)
        return sorted(results, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def update_progress(self, user_id: int, step: str, completed: bool = True):
        """Update umrah progress"""
        User = Query()
        existing = self.progress.get(User.user_id == user_id)
        
        if existing:
            progress_data = existing.get('steps', {})
            progress_data[step] = {
                'completed': completed,
                'timestamp': datetime.now().isoformat()
            }
            self.progress.update({'steps': progress_data}, User.user_id == user_id)
        else:
            self.progress.insert({
                'user_id': user_id,
                'steps': {
                    step: {
                        'completed': completed,
                        'timestamp': datetime.now().isoformat()
                    }
                }
            })
    
    def get_progress(self, user_id: int) -> Dict[str, Any]:
        """Get user's umrah progress"""
        User = Query()
        result = self.progress.get(User.user_id == user_id)
        return result.get('steps', {}) if result else {}
    
    def get_progress_percentage(self, user_id: int) -> int:
        """Calculate progress percentage"""
        steps = ['ihram', 'thawaf', 'sai', 'tahalul']
        progress = self.get_progress(user_id)
        
        completed = sum(1 for step in steps if progress.get(step, {}).get('completed', False))
        return int((completed / len(steps)) * 100)
    
    def close(self):
        """Close database connection"""
        self.db.close()

# Global instance
user_manager = UserManager()