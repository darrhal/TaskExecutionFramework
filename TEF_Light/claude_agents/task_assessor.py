"""
Task assessment agent - provides objective observations from multiple perspectives.
"""

from .base import BaseClaudeAgent
from models import AssessmentResult, PerspectiveAssessment


class TaskAssessor(BaseClaudeAgent):
    """Technical assessor agent for multi-perspective task evaluation."""
    
    @property
    def SYSTEM_PROMPT(self) -> str:
        """System prompt for technical assessment tasks."""
        return """You are a technical assessor providing objective observations about software development tasks.

Your role is to assess tasks from four critical perspectives:

**Build Perspective**: Evaluate technical implementation feasibility, dependencies, and potential blockers.

**Requirements Perspective**: Analyze alignment with project goals, clarity of acceptance criteria, and outcome relevance.

**Integration Perspective**: Examine how tasks fit within the broader system context, dependencies, and potential conflicts.

**Quality Perspective**: Review maintainability concerns, adherence to standards, and potential technical debt.

Your observations must be:
- Objective and factual, not prescriptive
- Focused on what you observe, not what should be done
- Comprehensive across all four perspectives
- Evidence-based and specific

Provide structured observations that inform decision-making without making the decisions yourself."""
    
    def assess(self, prompt: str) -> AssessmentResult:
        """Assess a task and return structured assessment results."""
        result = self._call_with_schema(
            prompt=prompt,
            validator_name="assessment_summary",
            validator_description=("Provides structured assessment observations from Build, "
                              "Requirements, Integration, and Quality perspectives."),
            schema=AssessmentResult.model_json_schema()
        )

        # Handle errors gracefully with default AssessmentResult
        if "error" in result:
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