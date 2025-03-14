import uuid
from datetime import datetime
import json
from django.core.cache import cache


class SessionService :
    def __init__(self) :
        # We'll use Django's cache system instead of an in-memory dict for better persistence
        self.cache_timeout = 60 * 60 * 24  # 24 hours

    def create_session(self, user_id=None) :
        """Create a new session and return the session ID"""
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id" : user_id,
            "created_at" : datetime.now().isoformat(),
            "last_activity" : datetime.now().isoformat(),
            "context" : {},
            "history" : []
        }

        cache.set(f"voice_session_{session_id}", session_data, self.cache_timeout)
        return session_id

    def get_session(self, session_id) :
        """Get session data by ID"""
        return cache.get(f"voice_session_{session_id}")

    def update_session_activity(self, session_id) :
        """Update the last activity timestamp"""
        session_data = self.get_session(session_id)
        if session_data :
            session_data["last_activity"] = datetime.now().isoformat()
            cache.set(f"voice_session_{session_id}", session_data, self.cache_timeout)

    def add_to_history(self, session_id, user_input, bot_response) :
        """Add an interaction to the session history"""
        session_data = self.get_session(session_id)
        if session_data :
            if "history" not in session_data :
                session_data["history"] = []

            session_data["history"].append({
                "user" : user_input,
                "bot" : bot_response,
                "timestamp" : datetime.now().isoformat()
            })

            cache.set(f"voice_session_{session_id}", session_data, self.cache_timeout)
            self.update_session_activity(session_id)

    def get_history(self, session_id, limit=10) :
        """Get recent conversation history"""
        session_data = self.get_session(session_id)
        if session_data and "history" in session_data :
            history = session_data["history"]
            return history[-limit :] if limit else history
        return []