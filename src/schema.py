from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class AgentState(BaseModel):
    # Universal Unlock
    model_config = ConfigDict(extra='allow')

    # Core Inputs
    topic: str
    platform: str
    
    # Research Data (Flexible: Accepts List or String)
    research: Optional[Any] = None
    research_data: Optional[Any] = None
    key_facts: Optional[Any] = None
    controversies: Optional[Any] = None
    statistics: Optional[Any] = None
    implications: Optional[Any] = None
    sources: Optional[Any] = None

    # Planner & Writer Outputs
    hook: Optional[Any] = None
    cta: Optional[Any] = None
    outline: Optional[Any] = None
    draft: Optional[Any] = None
    critique: Optional[Any] = None
    
    # Final Outputs
    score: int = Field(default=0)
    final_thread: Optional[Any] = None
    image_url: Optional[str] = None
    
    # History
    messages: List[Dict] = Field(default_factory=list)
def get(self, key, default=None):
        return getattr(self, key, default)
