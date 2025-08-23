"""
Clean interface for Claude API with structured outputs via schema validation.
"""

import anthropic
from anthropic.types import MessageParam, ToolParam, ToolUseBlock
from typing import Optional, Dict, Any, List

from models import ExecutionResult, AssessmentResult, TaskNode


class ClaudeClient:
    """Professional Claude API client with structured outputs via schema validation."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize the Claude client."""
        self.client = anthropic.Anthropic()
        self.model = model

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

            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                tools=schema_spec,
                tool_choice={"type": "tool", "name": validator_name}
            )

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
        result = self._call_with_schema(
            prompt=prompt,
            validator_name="execution_summary",
            validator_description=("Provides a structured summary of task execution "
                              "including status, files modified, changes made, "
                              "and any errors encountered."),
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
        result = self._call_with_schema(
            prompt=prompt,
            validator_name="assessment_summary",
            validator_description=("Provides structured assessment observations from Build, "
                              "Requirements, Integration, and Quality perspectives."),
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
        result = self._call_with_schema(
            prompt=prompt,
            validator_name="plan_update",
            validator_description=("Returns the updated task tree structure based on "
                              "assessment observations and adaptation decisions."),
            schema=TaskNode.model_json_schema(),
            max_tokens=2048
        )

        # Handle errors - return None to indicate no plan update
        if "error" in result:
            print(f"Plan adaptation failed: {result['error']}")
            return None

        # Pydantic will validate the structure
        return TaskNode.model_validate(result)