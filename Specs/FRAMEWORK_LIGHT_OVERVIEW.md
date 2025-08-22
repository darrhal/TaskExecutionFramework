# TEF Light v2 - Specification

## Overview

A simplified Task Execution Framework that treats the plan itself as a living specification, continuously refined through Act→Assess→Adapt cycles. The entire task tree is thoroughly reviewed from multiple perspectives on every iteration.

## Core Philosophy

### The Plan IS the Specification
- The task tree captures everything: goals, current state, history, and future plans
- No separate specification files - natural language descriptions are the spec
- Every cycle reviews the ENTIRE tree to maintain coherence and alignment

### Continuous Deep Re-evaluation
Not just "what failed" but "given everything we know, is this still the right plan?"

Every adaptation considers:
- Intent alignment with original goals
- Plan coherence across all tasks
- Next step optimization
- Task refinement opportunities

### Progressive Elaboration
- Tasks start as simple descriptions
- Get refined with detail as they approach execution
- "Attention proximity" - immediate tasks get the most refinement

### Task Execution Distinction
**Critical:** Only atomic tasks (leaves with no children) perform the Act phase:
- **Atomic tasks**: Execute changes to the environment, then Assess and Adapt
- **Parent tasks**: Skip Act, orchestrate children, still Assess and Adapt
- Both types participate in continuous re-evaluation

## Architecture

### Directory Structure
```
project/
  user_intent/           # Immutable, human-authored
    project.json         # Original task tree
    amendments/          # Clarifications added during execution
    
  working_plan/          # Agent-modified, evolving
    current.json         # The living task tree (entire project)
    
  environment/           # The actual repo being modified
    [project files]
```

### Task Tree Format
Single JSON file representing the entire project:

```json
{
  "id": "uuid-generated",
  "type": "parent",
  "description": "Build a REST API for user management",
  "failure_threshold": 0.0,
  "children": [
    {
      "id": "uuid-generated",
      "type": "atomic",
      "description": "Create user model with email and name fields",
      "failure_threshold": 0.3
    },
    {
      "id": "uuid-generated",
      "type": "parent",
      "description": "Implement CRUD endpoints",
      "failure_threshold": 0.0,
      "children": [...]
    }
  ]
}
```

## The Core Loop

```python
def execute_framework(task_tree_path, environment_path):
    tree = load_task_tree(task_tree_path)
    
    while has_pending_tasks(tree):
        task = find_next_task(tree)  # Depth-first traversal
        
        # Act (atomic tasks only)
        if task.type == "atomic":
            result = sdk_call("executor", task)
            git_commit(f"ACT: {task.id}")
        
        # Assess (all tasks, with full context)
        # Multiple perspectives gather facts, not decisions:
        # - Build: compilation, technical feasibility
        # - Requirements: alignment with acceptance criteria  
        # - Integration: compatibility with system context
        # - Quality: code standards, maintainability
        observations = sdk_call("assessor", {
            "task": task,
            "result": result if atomic else None,
            "entire_tree": tree,
            "perspectives": ["build", "requirements", "integration", "quality"]
        })
        
        # Adapt (can modify entire tree)
        # Navigator searches for optimal path modifications
        tree = sdk_call("navigator", {
            "task": task,
            "observations": observations,
            "entire_tree": tree,
            "user_intent": load_immutable_intent()
        })
        
        save_task_tree(tree)
        git_commit(f"ADAPT: {task.id}")
```

## SDK Agent Contracts

Three pure functions with structured I/O:

- **Executor**: `Task → ExecutionResult` - Performs actual environment changes
- **Assessor**: `(Task, Result, Tree) → Observations` - Gathers facts from multiple perspectives
- **Navigator**: `(Task, Observations, Tree, Intent) → ModifiedTree` - Searches for optimal path forward

All agents use the Claude SDK with JSON output format for reliable structured responses.

### Observer Philosophy
Assessors employ observers that emit state, not decisions:
- Observers gather objective facts and evidence
- Navigator interprets observations to make decisions
- This separation enables policy evolution without observer changes

## Key Design Decisions

### Failure Thresholds
Instead of retry counts, tasks have a `failure_threshold` (0.0 to 1.0):
- Starts at 0.0 (sensitive to issues)
- Increases after each failure
- At 1.0, escalates to parent
- Parent can reset with new approach

### Plan Modifications  
The Navigator searches for optimal path modifications:
- Insert new tasks anywhere
- Replace tasks with decompositions
- Refine descriptions in place
- Remove unnecessary tasks
- Reorder siblings
- Guided by strategist perspectives (technical, requirements, risk, efficiency)

### State Management
- **Immutable user intent**: Original plan preserved
- **Working plan**: Evolves through execution
- **Dual-purpose commits**: After every Act (execution) AND every Adapt (planning)
- **Complete traceability**: Git history shows both execution and plan evolution
- **No external state**: Everything is in the task tree

## Implementation Simplicity

Target: ~200 lines of Python
- Direct SDK calls (no complex agent templates)
- Single JSON file for entire project
- Natural language as specification
- No parallel execution complexity (emerges from siblings)
- No elaborate state management

## Benefits

- **Continuous reconciliation** between intent and reality
- **Deep understanding** through complete tree evaluation
- **Natural emergence** of complex behaviors from simple plan modifications
- **Complete traceability** through git history
- **Pause and amend** capability through immutable intent

The framework achieves sophisticated adaptation through simple, thorough re-evaluation rather than complex logic.