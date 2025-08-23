"""
Clean interface for Claude API with structured outputs.

This module encapsulates all Claude API interactions and uses Pydantic models
for automatic schema generation and type safety.
"""

import anthropic
from typing import Optional

from models import ExecutionResult, AssessmentResult, TaskNode


class ClaudeClient:
    """Professional Claude API client with structured outputs."""
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize the Claude client."""
        self.client = anthropic.Anthropic()
        self.model = model
    
    def _call_with_tool(
        self, 
        prompt: str, 
        tool_name: str, 
        tool_description: str, 
        schema: dict,
        max_tokens: int = 1024
    ) -> dict:
        """Internal method to call Claude with tool use for structured output."""
        try:
            tools = [{
                "name": tool_name,
                "description": tool_description,
                "input_schema": schema
            }]
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                tools=tools,
                tool_choice={"type": "tool", "name": tool_name},
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract structured data from tool use
            for block in message.content:
                if block.type == "tool_use" and block.name == tool_name:
                    return block.input
            
            return {"error": "No structured output received"}
        except Exception as e:
            return {"error": f"Claude API Error: {str(e)}"}
    
    def call_text(self, prompt: str, max_tokens: int = 1024) -> str:
        """Call Claude for simple text output."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = ""
            for block in message.content:
                if block.type == "text":
                    response_text += block.text
            
            return response_text
        except Exception as e:
            return f"Claude API Error: {str(e)}"
    
    def execute_task(self, prompt: str) -> ExecutionResult:
        """Call Claude for task execution with structured ExecutionResult output."""
        result = self._call_with_tool(
            prompt=prompt,
            tool_name="execution_summary",
            tool_description="Provides a structured summary of task execution including status, files modified, changes made, and any errors encountered.",
            schema=ExecutionResult.model_json_schema()
        )
        
        # Handle errors gracefully with default ExecutionResult
        if "error" in result:
            return ExecutionResult(
                status="failure",
                files_modified=[],
                changes_made=f"Execution failed: {result['error']}",
                git_diff="",
                errors=[result["error"]],
                environment_path="./"
            )
        
        # Pydantic will validate the structure
        return ExecutionResult.model_validate(result)
    
    def assess_task(self, prompt: str) -> AssessmentResult:
        """Call Claude for task assessment with structured AssessmentResult output."""
        result = self._call_with_tool(
            prompt=prompt,
            tool_name="assessment_summary",
            tool_description="Provides structured assessment observations from Build, Requirements, Integration, and Quality perspectives.",
            schema=AssessmentResult.model_json_schema()
        )
        
        # Handle errors gracefully with default AssessmentResult
        if "error" in result:
            from models import PerspectiveAssessment
            default_perspective = PerspectiveAssessment(
                feasible=False,
                blockers=[result["error"]],
                observations="Assessment failed due to API error"
            )
            return AssessmentResult(
                build=default_perspective,
                requirements=default_perspective,
                integration=default_perspective,
                quality=default_perspective
            )
        
        # Pydantic will validate the structure
        return AssessmentResult.model_validate(result)
    
    def adapt_plan(self, prompt: str) -> Optional[TaskNode]:
        """Call Claude for plan adaptation with structured TaskNode output."""
        result = self._call_with_tool(
            prompt=prompt,
            tool_name="plan_update",
            tool_description="Returns the updated task tree structure based on assessment observations and adaptation decisions.",
            schema=TaskNode.model_json_schema(),
            max_tokens=2048
        )
        
        # Handle errors - return None to indicate no plan update
        if "error" in result:
            print(f"Plan adaptation failed: {result['error']}")
            return None
        
        # Pydantic will validate the structure
        return TaskNode.model_validate(result)