from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class AgentState(BaseModel):
    # THE UNIVERSAL UNLOCK: Allow agents to add any field they want
    model_config = ConfigDict(extra='allow')

    topic: str
    platform: str
    
    # Core Fields
    research_data: Optional[List[Dict]] = None
    key_facts: Optional[List[str]] = None
    controversies: Optional[List[str]] = None 
    statistics: Optional[List[str]] = None
    
    # Writing Fields
    hook: Optional[str] = None
    cta: Optional[str] = None
    outline: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    
    # Output Fields
    score: int = Field(default=0)
    final_thread: Optional[List[str]] = None
    image_url: Optional[str] = None
    sources: Optional[List[str]] = None
    
    messages: List[Dict] = Field(default_factory=list)
