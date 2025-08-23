#!/usr/bin/env python3
"""
TEF Light - Task Execution Framework (Simplified)

A minimal implementation of the Act→Assess→Adapt cycle using Claude SDK
with structured outputs for reliable task orchestration.
"""

import json
import subprocess

from claude_client import ClaudeClient
from models import ExecutionResult, AssessmentResult, TaskNode, TaskTree
from templates import template_manager


# Initialize Claude client globally
claude_client = ClaudeClient()


def execute_project_plan(environment_path: str,
                         task_plan_path: str = "sample_project_plan.json") -> None:
    """Execute the complete project plan using the task framework."""
    # Load and validate task tree from plan
    task_tree = TaskTree.load_from_file(task_plan_path)

    execute_task(task_tree.root, environment_path)


def execute_task(task_tree: TaskNode, environment_path: str) -> None:
    """Execute tasks using Act→Assess→Adapt cycle."""
    while True:
        task = find_next_task(task_tree)
        if not task:
            break

        # Mark task as in progress
        task.status = "in_progress"

        # Act (atomic only)
        execution_result = None
        if not task.children:
            execution_result = execute(task)
            record(f"ACT: {task.id}")

        # Assess (all tasks)
        assessment = assess(task, task_tree, execution_result)

        # Adapt (all tasks)
        updated_tree = adapt(task, assessment, task_tree)
        if updated_tree:
            # Update the tree with adapted changes
            _update_task_tree(task_tree, updated_tree)

        # Mark task as completed
        task.status = "completed"
        record(f"ADAPT: {task.id}")


# Task tree navigation
def find_next_task(tree: TaskNode) -> TaskNode | None:
    """Find the next atomic (leaf) task that's pending using depth-first traversal."""
    # If this task is atomic (no children) and pending, return it
    if not tree.children and tree.status == "pending":
        return tree

    # Otherwise, check children depth-first
    if tree.children:
        for child in tree.children:
            next_task = find_next_task(child)
            if next_task:
                return next_task

    return None


def _update_task_tree(original: TaskNode, updated: TaskNode) -> None:
    """Helper to update original task tree with adapted changes."""
    # For now, just update the root properties
    # In a more sophisticated implementation, we'd do a proper merge
    original.id = updated.id
    original.description = updated.description
    original.status = updated.status
    original.failure_threshold = updated.failure_threshold
    if updated.children:
        original.children = updated.children


def execute(task: TaskNode) -> ExecutionResult:
    """Execute an atomic task and return comprehensive results."""
    print(f"Executing: {task.description}")

    # Render prompt using template system
    prompt = template_manager.render(
        "task_execution",
        task_id=task.id,
        task_description=task.description,
        working_directory="./",
        additional_context=""  # Can be extended for future use
    )

    # Get structured execution result from Claude
    execution_result = claude_client.execute_task(prompt)

    # Ensure git_diff is captured if not provided by Claude
    if not execution_result.git_diff:
        try:
            git_diff = subprocess.run(['git', 'diff', 'HEAD'],
                                      capture_output=True, text=True, check=True)
            execution_result.git_diff = git_diff.stdout
        except subprocess.CalledProcessError:
            execution_result.git_diff = "Error capturing git diff"

    return execution_result


def assess(task: TaskNode, tree: TaskNode, execution_result: ExecutionResult | None) -> AssessmentResult:
    """Assess from multiple perspectives using Claude."""
    
    # Format execution info if available
    execution_info = ""
    if execution_result:
        execution_info = f"""
## Execution Result
Status: {execution_result.status}
Files Modified: {execution_result.files_modified}
Changes Made: {execution_result.changes_made}
Environment Path: {execution_result.environment_path}
Errors: {execution_result.errors}

## Changes Made (Git Diff)
{execution_result.git_diff or 'No changes detected'}
"""

    # Render prompt using template system
    prompt = template_manager.render(
        "task_assessment",
        task_id=task.id,
        task_description=task.description,
        execution_info=execution_info,
        task_tree_context=f"Full task tree: {json.dumps(tree.model_dump(), indent=2)}"
    )

    return claude_client.assess_task(prompt)


def adapt(task: TaskNode, obs: AssessmentResult, tree: TaskNode) -> TaskNode | None:
    """Navigate/adapt the plan based on observations."""
    
    # Format observations for template
    observations_text = f"""
Build Perspective:
- Feasible: {obs.build.feasible}
- Blockers: {obs.build.blockers}
- Observations: {obs.build.observations}

Requirements Perspective:
- Feasible: {obs.requirements.feasible}
- Blockers: {obs.requirements.blockers}
- Observations: {obs.requirements.observations}

Integration Perspective:
- Feasible: {obs.integration.feasible}
- Blockers: {obs.integration.blockers}
- Observations: {obs.integration.observations}

Quality Perspective:
- Feasible: {obs.quality.feasible}
- Blockers: {obs.quality.blockers}
- Observations: {obs.quality.observations}
"""

    # Render prompt using template system
    prompt = template_manager.render(
        "plan_adaptation",
        task_id=task.id,
        task_description=task.description,
        observations=observations_text,
        task_tree=json.dumps(tree.model_dump(), indent=2)
    )

    return claude_client.adapt_plan(prompt)


def record(msg: str) -> None:
    """Record progress with both logging and git commits"""
    print(msg)

    try:
        # Stage all changes
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
        # Commit with the message
        subprocess.run(['git', 'commit', '-m', msg], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")


if __name__ == "__main__":
    execute_project_plan(".")
