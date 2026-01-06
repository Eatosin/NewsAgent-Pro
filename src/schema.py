from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class AgentState(BaseModel):
    """
    The shared memory for the Multi-Agent System.
    Includes 'extra=allow' to prevent validation errors on new fields.
    """
    model_config = ConfigDict(extra='allow')

    # Input
    topic: str = ""
    platform: str = "twitter"
    
    # Research & Planning
    research_data: Optional[List[Dict]] = Field(default_factory=list)
    outline: Optional[str] = None
    hook: Optional[str] = None
    
    # Content
    draft: Optional[str] = None
    critique: Optional[str] = None
    score: float = 0.0
    revision_count: int = 0
    
    # Output
    final_thread: Optional[List[str]] = Field(default_factory=list)
    image_url: Optional[str] = None
    sources: Optional[List[str]] = Field(default_factory=list)

# 🛠️ UTILITY WRAPPER (Paste this here so it's available everywhere)
class HybridState:
    """
    Universal wrapper to allow both dot-notation (state.topic) 
    and dict-access (state['topic']).
    """
    def __init__(self, state):
        # Unwrap if it's already a HybridState
        if isinstance(state, HybridState):
            self.__dict__ = state.__dict__
        # Convert Pydantic to dict
        elif hasattr(state, 'model_dump'):
            self.__dict__.update(state.model_dump())
        # Use dict directly
        elif isinstance(state, dict):
            self.__dict__.update(state)
        else:
            raise ValueError(f"Unknown state type: {type(state)}")

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    def __getitem__(self, key):
        return self.__dict__.get(key)
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
