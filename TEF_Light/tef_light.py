#!/usr/bin/env python3
"""
TEF Light - Task Execution Framework (Simplified)

A minimal implementation of the Act→Assess→Adapt cycle using Claude SDK
with structured outputs for reliable task orchestration.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from claude_agents import TaskExecutor, TaskAssessor, Pathfinder
from models import ExecutionResult, AssessmentResult, TaskNode, TaskTree
from templates import template_manager


# Initialize specialized agents
task_executor = TaskExecutor()
task_assessor = TaskAssessor()
pathfinder = Pathfinder()


def execute_project_plan(environment_path: str,
                         task_plan_path: str = "sample_project_plan.json") -> None:
    """Execute the complete project plan using the task framework."""
    # Create unique project directory structure
    from datetime import datetime
    project_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = Path(f"projects/{project_id}")
    
    # Create project directories
    (project_dir / "user_intent").mkdir(parents=True, exist_ok=True)
    (project_dir / "working_plan").mkdir(parents=True, exist_ok=True)
    (project_dir / "runs").mkdir(parents=True, exist_ok=True)
    
    # Store project directory and derived paths globally
    global _current_project_dir, _project_id, _main_log_path
    _current_project_dir = project_dir
    _project_id = project_id
    _main_log_path = project_dir / f"runs/{project_id}.log"
    
    # Initialize audit log
    _init_audit_log()
    
    # Load and validate task tree from plan
    task_tree = TaskTree.load_from_file(task_plan_path)
    
    # Preserve original user intent on first run (inline implementation)
    original_intent_path = project_dir / "user_intent/original_plan.json"
    if not original_intent_path.exists():
        task_tree.save_to_file(str(original_intent_path))
        print(f"Preserved original user intent: {original_intent_path}")

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
            # Record with detailed execution info
            act_details = f"Executed task: {task.description}"
            if execution_result:
                act_details += f" | Status: {execution_result.status} | Files: {len(execution_result.files_modified)} | Changes: {execution_result.changes_made}"
            record(f"ACT: {task.id}", phase="ACT", details=act_details)

        # Assess (all tasks)
        assessment = assess(task, task_tree, execution_result)
        
        # Record assessment summary
        assess_details = f"Build: {'pass' if assessment.build.feasible else 'fail'}, Requirements: {'pass' if assessment.requirements.feasible else 'fail'}, Integration: {'pass' if assessment.integration.feasible else 'fail'}, Quality: {'pass' if assessment.quality.feasible else 'fail'}"
        record(f"ASSESS: {task.id}", phase="ASSESS", details=assess_details)

        # Adapt (all tasks)
        updated_tree = adapt(task, assessment, task_tree)
        if updated_tree:
            # Update the tree with adapted changes
            _update_task_tree(task_tree, updated_tree)
            # Save evolving working plan
            _save_working_plan(task_tree)
            adapt_details = "Plan updated with modifications"
        else:
            adapt_details = "No changes needed, proceeding as planned"
        
        record(f"ADAPT: {task.id}", phase="ADAPT", details=adapt_details)

        # Mark task as completed
        task.status = "completed"


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

    # Get structured execution result from TaskExecutor
    execution_result = task_executor.execute(prompt)

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

    return task_assessor.assess(prompt)


def adapt(task: TaskNode, obs: AssessmentResult, tree: TaskNode) -> TaskNode | None:
    """Navigate/adapt the plan based on observations."""
    
    # Load original user intent for "north star" reference
    original_intent = _load_original_intent()
    
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
        original_user_intent=original_intent,
        observations=observations_text,
        task_tree=json.dumps(tree.model_dump(), indent=2)
    )

    return pathfinder.find_path(prompt)

# Global variables to track current project state
_current_project_dir: Optional[Path] = None
_project_id: Optional[str] = None
_main_log_path: Optional[Path] = None


def _load_original_intent() -> str:
    """Load original user intent as raw JSON data for template."""
    original_intent_path = _current_project_dir / "user_intent/original_plan.json"
    
    if not original_intent_path.exists():
        return "No original intent preserved (legacy execution)"
    
    try:
        # Just return the raw JSON content - no pretty formatting needed
        return original_intent_path.read_text()
    except Exception as e:
        return f"Error loading original intent: {e}"

def _save_working_plan(root_task: TaskNode) -> None:
    """Save current working plan to working_plan directory."""
    working_plan_path = _current_project_dir / "working_plan/current_plan.json"
    
    try:
        # Create a TaskTree wrapper for consistent saving
        current_tree = TaskTree(root=root_task)
        current_tree.save_to_file(str(working_plan_path))
        print(f"Saved working plan: {working_plan_path}")
    except Exception as e:
        print(f"Warning: Failed to save working plan: {e}")


def _init_audit_log() -> None:
    """Initialize audit log file for the current project."""
    from datetime import datetime
    
    with open(_main_log_path, 'w') as f:
        f.write(f"# TEF Light Execution Log - Project {_project_id}\n")
        f.write(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")


def record(msg: str, phase: Optional[str] = None, details: Optional[str] = None) -> None:
    """Record progress with both logging and git commits"""
    from datetime import datetime
    
    print(msg)
    
    # Write to audit log if we have a project directory
    if _main_log_path:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {phase}: {details}\n" if (phase and details) else f"[{timestamp}] {msg}\n"
        
        # Write to main execution log
        with open(_main_log_path, 'a') as f:
            f.write(log_entry)
        
        # Also write to task-specific log if we have a task ID
        if ':' in msg:  # Format: "PHASE: task-id" or "ACT: task-id", etc.
            parts = msg.split(': ', 1)
            if len(parts) == 2:
                task_id = parts[1]
                task_log_path = _current_project_dir / f"runs/{task_id}.log"
                with open(task_log_path, 'a') as f:
                    f.write(log_entry)

    try:
        # Stage all changes
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
        # Commit with the message
        subprocess.run(['git', 'commit', '-m', msg], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")


if __name__ == "__main__":
    execute_project_plan(".")
