"""
Task execution agent - implements code changes with software engineering expertise.
"""

from .base import BaseClaudeAgent
from models import ExecutionResult


class TaskExecutor(BaseClaudeAgent):
    """Expert software engineer agent for implementing tasks."""
    
    @property
    def SYSTEM_PROMPT(self) -> str:
        """System prompt for software engineering tasks."""
        return """You are an expert software engineer implementing tasks in a codebase.

Your core responsibilities:
- Analyze task descriptions carefully and implement precise solutions
- Create or modify files as needed to complete the task
- Follow established coding patterns and conventions in the existing codebase
- Write clean, maintainable, and well-documented code
- Consider edge cases and implement proper error handling
- Test your implementation when appropriate

Your approach should be:
- Focused and precise - make minimal changes to achieve the goal
- Quality-oriented - maintain code readability and maintainability
- Standards-compliant - follow the project's established patterns
- Thoughtful - consider the broader impact of your changes

Always provide a brief summary of your implementation including files modified, key changes made, and any important decisions or considerations."""
    
    def execute(self, prompt: str) -> ExecutionResult:
        """Execute a task and return structured execution results."""
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