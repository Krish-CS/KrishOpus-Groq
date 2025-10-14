"""
Session Manager - FIXED VERSION
✅ Properly updates sections when chat modifies content
✅ Stores chat history
✅ Auto-cleanup of expired sessions
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional


class SessionManager:
    """Manages user sessions for document generation"""
    
    def __init__(self, session_timeout_hours: int = 24):
        """
        Initialize session manager
        
        Args:
            session_timeout_hours: Hours before session expires (default: 24)
        """
        self.sessions = {}
        self.session_timeout = timedelta(hours=session_timeout_hours)
        print(f"✅ SessionManager initialized (timeout: {session_timeout_hours}h)")
    
    
    def create_session(
        self,
        topic: str,
        subject: str,
        sections: Dict[str, str],
        template_path: str
    ) -> str:
        """
        Create a new session
        
        Args:
            topic: Assignment topic
            subject: Subject name
            sections: Generated content sections
            template_path: Path to template file
        
        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "topic": topic,
            "subject": subject,
            "sections": sections,
            "template_path": template_path,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "chat_history": []
        }
        
        print(f"✅ Session created: {session_id}")
        return session_id
    
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session by ID
        
        Args:
            session_id: Session identifier
        
        Returns:
            Session data or None if not found/expired
        """
        if session_id not in self.sessions:
            print(f"⚠ Session not found: {session_id}")
            return None
        
        session = self.sessions[session_id]
        
        # Check if expired
        created_at = datetime.fromisoformat(session["created_at"])
        if datetime.now() - created_at > self.session_timeout:
            print(f"⚠ Session expired: {session_id}")
            del self.sessions[session_id]
            return None
        
        # Update last accessed time
        session["last_accessed"] = datetime.now().isoformat()
        
        return session
    
    
    def update_sections(self, session_id: str, updated_sections: Dict[str, str]):
        """
        CRITICAL FIX: Update specific sections in session
        This is called when chat refinement modifies content
        
        Args:
            session_id: Session identifier
            updated_sections: Dictionary of section_name: new_content
        """
        if session_id not in self.sessions:
            print(f"⚠ Session {session_id} not found for update")
            return
        
        # Update each section with new content
        for section_name, new_content in updated_sections.items():
            self.sessions[session_id]["sections"][section_name] = new_content
        
        # Update last accessed time
        self.sessions[session_id]["last_accessed"] = datetime.now().isoformat()
        
        print(f"✅ Session {session_id} updated with {len(updated_sections)} section(s)")
    
    
    def add_chat_message(
        self,
        session_id: str,
        role: str,
        message: str
    ):
        """
        Add a message to chat history
        
        Args:
            session_id: Session identifier
            role: 'user' or 'assistant'
            message: Message content
        """
        if session_id not in self.sessions:
            print(f"⚠ Session {session_id} not found for chat message")
            return
        
        self.sessions[session_id]["chat_history"].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update last accessed
        self.sessions[session_id]["last_accessed"] = datetime.now().isoformat()
    
    
    def get_chat_history(self, session_id: str) -> list:
        """
        Get chat history for a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of chat messages
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get("chat_history", [])
    
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"✅ Session deleted: {session_id}")
            return True
        
        print(f"⚠ Session not found: {session_id}")
        return False
    
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        now = datetime.now()
        expired = []
        
        for session_id, session in self.sessions.items():
            created_at = datetime.fromisoformat(session["created_at"])
            if now - created_at > self.session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            print(f"✅ Cleaned up {len(expired)} expired session(s)")
    
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)
    
    
    def list_sessions(self) -> list:
        """
        List all active sessions
        
        Returns:
            List of session summaries
        """
        summaries = []
        
        for session_id, session in self.sessions.items():
            summaries.append({
                "session_id": session_id,
                "topic": session["topic"],
                "subject": session["subject"],
                "created_at": session["created_at"],
                "last_accessed": session["last_accessed"],
                "section_count": len(session["sections"]),
                "chat_message_count": len(session.get("chat_history", []))
            })
        
        return summaries
