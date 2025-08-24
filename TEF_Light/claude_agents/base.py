"""
Base class for Claude agents with shared functionality.
"""

import anthropic
from abc import ABC, abstractmethod
from anthropic.types import ToolParam, ToolUseBlock, TextBlock
from typing import Dict, Any, List


class BaseClaudeAgent(ABC):
    """Base class for specialized Claude agents."""
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize the Claude agent."""
        self.client = anthropic.Anthropic()
        self.model = model
    
    @property
    @abstractmethod
    def SYSTEM_PROMPT(self) -> str:
        """Each agent must define its own system prompt."""
        pass
    
    def _call_with_schema(
        self,
        prompt: str,
        validator_name: str,
        validator_description: str,
        schema: Dict[str, Any],
        max_tokens: int = 1024
    ) -> Dict[str, Any]:
        """Call Claude with schema validation for structured output."""
        try:
            schema_spec: List[ToolParam] = [{
                "name": validator_name,
                "description": validator_description,
                "input_schema": schema
            }]

            # Build the create parameters
            create_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "tools": schema_spec,
                "tool_choice": {"type": "tool", "name": validator_name}
            }
            
            # Add system prompt only if provided and not empty
            if self.SYSTEM_PROMPT:
                create_params["system"] = self.SYSTEM_PROMPT
                
            message = self.client.messages.create(**create_params)

            # Extract structured data from response
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name == validator_name:
                    if isinstance(block.input, dict):
                        return block.input
                    return {"error": f"Unexpected input type: {type(block.input)}"}

            return {"error": "No structured output received"}
        except Exception as e:
            return {"error": f"Claude API Error: {str(e)}"}
    
    def call_text(self, prompt: str, max_tokens: int = 1024) -> str:
        """Call Claude for simple text output."""
        try:
            # Build the create parameters
            create_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            # Add system prompt only if provided and not empty
            if self.SYSTEM_PROMPT:
                create_params["system"] = self.SYSTEM_PROMPT
                
            message = self.client.messages.create(**create_params)

            response_text = ""
            for block in message.content:
                if isinstance(block, TextBlock):
                    response_text += block.text

            return response_text
        except Exception as e:
            return f"Claude API Error: {str(e)}"