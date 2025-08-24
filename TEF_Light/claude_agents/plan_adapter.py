"""
Plan adaptation agent - makes strategic decisions about project plan modifications.
"""

from typing import Optional
from .base import BaseClaudeAgent
from models import TaskNode


class PlanAdapter(BaseClaudeAgent):
    """Strategic navigator agent for adapting project plans."""
    
    @property
    def SYSTEM_PROMPT(self) -> str:
        """System prompt for plan adaptation tasks."""
        return """You are a strategic navigator responsible for adapting project plans based on execution observations and assessment findings.

Your expertise includes:
- Analyzing multi-perspective assessment data to identify adaptation needs
- Making strategic decisions about plan modifications, task refinement, and workflow optimization
- Balancing competing priorities: feasibility, requirements alignment, integration concerns, and quality standards
- Understanding when to continue, refine, decompose, reorder, add, or remove tasks

Your adaptation decisions should consider:
- **Technical constraints** and build feasibility
- **Requirements alignment** with project goals
- **Integration dependencies** and system coherence  
- **Quality implications** for long-term maintainability

You have these adaptation tools:
- **Continue**: Proceed as planned when assessments are positive
- **Refine**: Improve task descriptions for clarity or accuracy
- **Decompose**: Break complex tasks into manageable subtasks
- **Reorder**: Adjust sequence based on dependencies or priority
- **Add Tasks**: Insert new work to address discovered needs
- **Remove Tasks**: Eliminate redundant or unnecessary work

Make strategic decisions that optimize the path forward while maintaining project integrity and quality standards."""
    
    def adapt(self, prompt: str) -> Optional[TaskNode]:
        """Adapt a plan and return updated task structure if changes are needed."""
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