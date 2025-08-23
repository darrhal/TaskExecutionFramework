"""
Pydantic models for TEF Light structured outputs.

These models define the data structures used for communication with Claude
and automatic JSON schema generation for structured outputs.
"""

import json
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ExecutionResult(BaseModel):
    """Result of executing an atomic task."""
    
    status: Literal["success", "failure", "partial"] = Field(
        description="Status of the task execution"
    )
    files_modified: List[str] = Field(
        default_factory=list,
        description="List of file paths that were created or modified"
    )
    changes_made: str = Field(
        description="Brief summary of what was implemented"
    )
    git_diff: str = Field(
        default="",
        description="Complete git diff showing all changes made"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="Any errors encountered during execution"
    )
    environment_path: str = Field(
        default="./",
        description="Working directory path"
    )


class PerspectiveAssessment(BaseModel):
    """Assessment from a single perspective (Build, Requirements, Integration, or Quality)."""
    
    feasible: bool = Field(
        description="Whether this perspective considers the task feasible/successful"
    )
    blockers: List[str] = Field(
        default_factory=list,
        description="List of blockers or issues identified from this perspective"
    )
    observations: str = Field(
        description="Detailed observations from this perspective"
    )


class AssessmentResult(BaseModel):
    """Multi-perspective assessment of a completed task."""
    
    build: PerspectiveAssessment = Field(
        description="Technical feasibility and implementation assessment"
    )
    requirements: PerspectiveAssessment = Field(
        description="Alignment with project goals and acceptance criteria"
    )
    integration: PerspectiveAssessment = Field(
        description="Compatibility with system context and other tasks"
    )
    quality: PerspectiveAssessment = Field(
        description="Code quality, maintainability, and standards compliance"
    )


class TaskNode(BaseModel):
    """A task in the hierarchical task tree."""
    
    id: str = Field(
        description="Unique identifier for this task"
    )
    description: str = Field(
        description="Natural language description of what this task should accomplish"
    )
    status: Literal["pending", "in_progress", "completed", "failed"] = Field(
        default="pending",
        description="Current status of task execution"
    )
    failure_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Failure threshold (0.0 = sensitive to issues, 1.0 = escalate to parent)"
    )
    children: Optional[List['TaskNode']] = Field(
        default=None,
        description="Child tasks (None for atomic tasks, List for parent tasks)"
    )


class TaskTree(BaseModel):
    """Root task tree structure loaded from JSON files."""
    
    root: TaskNode = Field(
        description="Root task node containing the entire project hierarchy"
    )
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'TaskTree':
        """Load and validate task tree from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # If the JSON is just a task node, wrap it as root
        if isinstance(data, dict) and 'id' in data:
            return cls(root=TaskNode.model_validate(data))
        
        # Otherwise expect it to have a 'root' key
        return cls.model_validate(data)
    
    def save_to_file(self, file_path: str) -> None:
        """Save task tree to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)


# Enable forward references for recursive TaskNode model
TaskNode.model_rebuild()
TaskTree.model_rebuild()