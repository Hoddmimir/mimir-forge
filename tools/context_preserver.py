"""
Context Preservation System for Mimir

This module provides functionality to save and restore conversation
context before and after LLM restarts on the Enigma server.

Usage:
    Before restart:  python3 -c "from tools.context_preserver import save_context; save_context()"
    After restart:   python3 -c "from tools.context_preserver import restore_context; restore_context()"
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ContextPreserver:
    """Handles saving and restoring conversation context."""
    
    def __init__(self, workspace: str | Path = "./mimir-forge") -> None:
        """Initialize the context preserver.
        
        Args:
            workspace: Path to the workspace directory.
        """
        self.workspace = Path(workspace)
        self.context_dir = self.workspace / ".context_backup"
        self.context_file = self.context_dir / "context_snapshot.json"
        self.sessions_dir = Path("/home/muninn/.openclaw/agents/main/sessions")
    
    def _ensure_dirs(self) -> None:
        """Ensure required directories exist."""
        self.context_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_timestamp(self) -> str:
        """Get ISO format timestamp with timezone."""
        return datetime.now(timezone.utc).isoformat()
    
    def _load_session_data(self, session_path: Path) -> dict[str, Any] | None:
        """Load session data from a .jsonl file.
        
        Args:
            session_path: Path to the session .jsonl file.
            
        Returns:
            Dictionary containing session data, or None if invalid.
        """
        try:
            if not session_path.exists():
                return None
                
            messages = []
            with open(session_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            messages.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            
            return {
                "path": str(session_path),
                "message_count": len(messages),
                "last_updated": session_path.stat().st_mtime,
                "messages": messages[-100:]  # Last 100 messages
            }
        except Exception as e:
            print(f"Warning: Could not load session {session_path}: {e}")
            return None
    
    def save_context(self, session_id: str | None = None) -> dict[str, Any]:
        """
        Save current conversation context to a backup file.
        
        This should be called BEFORE restarting the LLM server.
        
        Args:
            session_id: Optional specific session ID to save.
                       If None, saves all active sessions.
            
        Returns:
            Dictionary containing save summary.
        """
        self._ensure_dirs()
        
        print("=" * 60)
        print("  CONTEXT PRESERVATION - Saving Conversation State")
        print("=" * 60)
        print()
        
        timestamp = self._get_timestamp()
        
        context_data = {
            "version": "1.0",
            "saved_at": timestamp,
            "server": "Asgard",
            "model": "qwen-3.5-local",
            "sessions": [],
            "metadata": {}
        }
        
        # Find and save session data
        if session_id:
            # Save specific session
            session_path = self.sessions_dir / f"{session_id}.jsonl"
            if session_path.exists():
                session_data = self._load_session_data(session_path)
                if session_data:
                    context_data["sessions"].append({
                        "id": session_id,
                        "data": session_data
                    })
                    print(f"✓ Saved session: {session_id}")
                    print(f"  Messages preserved: {session_data['message_count']}")
            else:
                print(f"✗ Session not found: {session_id}")
        else:
            # Save all sessions
            session_files = list(self.sessions_dir.glob("*.jsonl"))
            for session_file in session_files:
                session_id = session_file.stem
                session_data = self._load_session_data(session_file)
                if session_data:
                    context_data["sessions"].append({
                        "id": session_id,
                        "data": session_data
                    })
                    print(f"✓ Saved session: {session_id}")
                    print(f"  Messages preserved: {session_data['message_count']}")
        
        # Save workspace state
        workspace_info = {
            "files": [],
            "last_modified": timestamp
        }
        
        # Track key workspace files
        key_dirs = ["memory", "knowledge", "projects"]
        for key_dir in key_dirs:
            dir_path = self.workspace / key_dir
            if dir_path.exists():
                for file_path in dir_path.rglob("*.md"):
                    rel_path = str(file_path.relative_to(self.workspace))
                    try:
                        mtime = datetime.fromtimestamp(
                            file_path.stat().st_mtime, timezone.utc
                        ).isoformat()
                        workspace_info["files"].append({
                            "path": rel_path,
                            "modified": mtime
                        })
                    except Exception:
                        pass
        
        context_data["metadata"]["workspace"] = workspace_info
        
        # Save to file
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2, default=str)
        
        print()
        print(f"✓ Context saved to: {self.context_file}")
        print(f"  Sessions preserved: {len(context_data['sessions'])}")
        print(f"  Timestamp: {timestamp}")
        print()
        print("=" * 60)
        print("  READY FOR RESTART")
        print("=" * 60)
        print()
        print("After restart, restore context with:")
        print(f'  python3 -c "from tools.context_preserver import restore_context; restore_context()"')
        print()
        
        return {
            "status": "success",
            "file": str(self.context_file),
            "sessions_saved": len(context_data["sessions"]),
            "timestamp": timestamp
        }
    
    def restore_context(self) -> dict[str, Any]:
        """
        Restore conversation context from backup file.
        
        This should be called AFTER the LLM server restarts.
        
        Returns:
            Dictionary containing restore summary.
        """
        if not self.context_file.exists():
            print("=" * 60)
            print("  NO CONTEXT BACKUP FOUND")
            print("=" * 60)
            print()
            print("No saved context found. You may need to save context first.")
            print()
            return {
                "status": "error",
                "message": "No context backup found",
                "file": str(self.context_file)
            }
        
        print("=" * 60)
        print("  CONTEXT RESTORATION - Loading Saved State")
        print("=" * 60)
        print()
        
        # Load context data
        with open(self.context_file, 'r', encoding='utf-8') as f:
            context_data = json.load(f)
        
        print(f"✓ Loaded context from: {self.context_file}")
        print(f"  Saved at: {context_data.get('saved_at', 'unknown')}")
        print(f"  Sessions to restore: {len(context_data.get('sessions', []))}")
        print()
        
        # Create a summary for the user
        restore_summary = {
            "status": "success",
            "sessions": [],
            "summary": ""
        }
        
        for session in context_data.get("sessions", []):
            session_id = session.get("id", "unknown")
            session_data = session.get("data", {})
            message_count = session_data.get("message_count", 0)
            
            # Get last few messages for summary
            messages = session_data.get("messages", [])
            last_messages = messages[-5:] if messages else []
            
            restore_summary["sessions"].append({
                "id": session_id,
                "message_count": message_count,
                "last_messages": last_messages
            })
            
            print(f"✓ Session: {session_id}")
            print(f"  Messages: {message_count}")
            if last_messages:
                last_msg = last_messages[-1]
                role = last_msg.get("role", "unknown")
                content = str(last_msg.get("content", ""))[:100]
                print(f"  Last from {role}: {content}...")
            print()
        
        print("=" * 60)
        print("  CONTEXT RESTORED")
        print("=" * 60)
        print()
        print("I have loaded the conversation context. You can now continue")
        print("the conversation where we left off.")
        print()
        
        return restore_summary


def save_context(session_id: str | None = None) -> dict[str, Any]:
    """
    Convenience function to save context.
    
    Args:
        session_id: Optional specific session ID to save.
        
    Returns:
        Save summary dictionary.
    """
    preserver = ContextPreserver()
    return preserver.save_context(session_id)


def restore_context() -> dict[str, Any]:
    """
    Convenience function to restore context.
    
    Returns:
        Restore summary dictionary.
    """
    preserver = ContextPreserver()
    return preserver.restore_context()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "save":
            save_context(sys.argv[2] if len(sys.argv) > 2 else None)
        elif command == "restore":
            restore_context()
        else:
            print(f"Usage: python3 {sys.argv[0]} [save|restore] [session_id]")
            sys.exit(1)
    else:
        print("Context Preserver - Save/Restore conversation state")
        print()
        print("Usage:")
        print(f"  python3 {sys.argv[0]} save          Save all sessions")
        print(f"  python3 {sys.argv[0]} save <id>      Save specific session")
        print(f"  python3 {sys.argv[0]} restore        Restore saved context")
