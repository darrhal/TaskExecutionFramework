#!/usr/bin/env python3
import os
import json
import subprocess
from typing import Any
import anthropic


def call_claude(prompt: str, model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 1024) -> str:
    """Simple wrapper for Claude API calls with sensible defaults"""
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract text from response content blocks
        response_text = ""
        for block in message.content:
            if block.type == "text":
                response_text += block.text
        
        return response_text
    except Exception as e:
        return f"Claude API Error: {str(e)}"


def execute_framework(environment_path: str, task_plan_path: str = "project_plan.json") -> None:
    # Load task tree from plan
    with open(task_plan_path, "r") as f:
        task_tree = json.load(f)

    execute_task(task_tree, environment_path)


def execute_task(task_tree: dict[str, Any], environment_path: str) -> None:
    while True:
        task = find_next_task(task_tree)
        if not task:
            break

        # Mark task as in progress
        task["status"] = "in_progress"
        
        # Act (atomic only)
        result = None
        if not task.get("children"):
            result = execute(task)
            record(f"ACT: {task['id']}")

        # Assess (all tasks)
        observations = assess(task, task_tree, result)

        # Adapt (all tasks)
        task_tree = adapt(task, observations, task_tree)
        
        # Mark task as completed
        task["status"] = "completed"
        record(f"ADAPT: {task['id']}")


# Task tree navigation
def find_next_task(tree: dict[str, Any]) -> dict[str, Any] | None:
    """Find the next atomic (leaf) task that's pending using depth-first traversal"""
    # If this task is atomic (no children) and pending, return it
    if not tree.get("children") and tree.get("status") == "pending":
        return tree
    
    # Otherwise, check children depth-first
    for child in tree.get("children", []):
        next_task = find_next_task(child)
        if next_task:
            return next_task
    
    return None


def execute(task: dict[str, Any]) -> dict[str, Any]:
    """Execute an atomic task and return comprehensive results"""
    print(f"Executing: {task.get('description')}")
    
    # Call Claude SDK to actually execute the task
    prompt = f"""
You are a software engineer implementing tasks in a codebase.

Task to complete: {task.get('description')}
Task ID: {task['id']}
Working directory: ./

Please implement this task by creating or modifying files as needed.
Respond with a brief summary of what you did.
"""
    
    sdk_response = call_claude(prompt)
    
    # Capture what changed in git
    try:
        git_diff = subprocess.run(['git', 'diff', 'HEAD'], 
                                 capture_output=True, text=True, check=True)
        diff_output = git_diff.stdout
    except subprocess.CalledProcessError:
        diff_output = "Error capturing git diff"
    
    return {
        "status": "success",
        "sdk_output": sdk_response,        # What the LLM said/did
        "git_diff": diff_output,           # Complete diff including new files  
        "environment_path": "./",          # For assessor exploration
        "errors": []
    }


def assess(task: dict[str, Any], tree: dict[str, Any], execution_result: dict[str, Any] | None) -> dict[str, Any]:
    """Assess from multiple perspectives and call SDK"""
    # Load assessment instructions
    with open("assessment_instructions.md", "r") as f:
        instructions = f.read()

    execution_info = ""
    if execution_result:
        execution_info = f"""
## Execution Result
Status: {execution_result.get('status')}
SDK Output: {execution_result.get('sdk_output')}
Environment Path: {execution_result.get('environment_path')}
Errors: {execution_result.get('errors', [])}

## Changes Made (Git Diff)
{execution_result.get('git_diff', 'No changes detected')}
"""

    prompt = f"""
{instructions}

## Current Task
Task: {task.get('description', 'Unknown task')}
Task ID: {task['id']}
{execution_info}

## Context
Full task tree: {json.dumps(tree, indent=2)}

Please assess this task according to the instructions above.
"""

    # Call Claude SDK with assessment prompt
    observations = call_claude(prompt)
    return {"observations": observations}


def adapt(task: dict[str, Any], obs: dict[str, Any], tree: dict[str, Any]) -> dict[str, Any]:
    """Navigate/adapt the plan based on observations"""
    prompt = f"""
You are a project navigator adapting plans based on observations.

Current Task: {task.get('description')}
Task ID: {task['id']}

Observations from assessment:
{obs.get('observations', 'No observations')}

Current Task Tree:
{json.dumps(tree, indent=2)}

Based on these observations, should the plan be modified?
Consider:
- Task decomposition if needed
- Plan refinement 
- Task status updates
- New tasks to insert
- Tasks to remove or reorder

Return the updated task tree as JSON, or the same tree if no changes needed.
"""
    
    adaptation = call_claude(prompt, max_tokens=2048)  # More tokens for tree modifications
    
    try:
        # Try to parse response as JSON (updated tree)
        updated_tree = json.loads(adaptation)
        return updated_tree
    except json.JSONDecodeError:
        # If not valid JSON, return original tree
        print(f"Adaptation not valid JSON: {adaptation}")
        return tree


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
    execute_framework(".")
