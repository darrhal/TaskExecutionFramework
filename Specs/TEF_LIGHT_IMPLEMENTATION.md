# TEF Light v2 - Implementation Details

## Technical Implementation

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

### Task Tree JSON Format
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

## Core Execution Loop

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

### Executor
`Task → ExecutionResult`

Performs actual environment changes for atomic tasks only.

### Assessor  
`(Task, Result, Tree) → Observations`

Gathers facts from multiple perspectives:
- **Build**: Compilation status, technical feasibility
- **Requirements**: Alignment with acceptance criteria
- **Integration**: Compatibility with system context
- **Quality**: Code standards, maintainability

Returns observations without making decisions.

### Navigator
`(Task, Observations, Tree, Intent) → ModifiedTree`

Searches for optimal path forward guided by strategist perspectives:
- **Technical**: Evaluates decomposition and implementation approaches
- **Requirements**: Ensures alignment with user intent
- **Risk**: Identifies potential obstacles and failure modes
- **Efficiency**: Seeks simpler, more direct solutions

All agents use the Claude SDK with JSON output format for reliable structured responses.

## Implementation Guidelines

### Target Simplicity
- ~200 lines of Python
- Direct SDK calls (no complex agent templates)
- Single JSON file for entire project
- Natural language as specification
- No parallel execution complexity (emerges from siblings)
- No elaborate state management

### Git Commit Strategy
- Commit after every Act phase (execution changes)
- Commit after every Adapt phase (plan modifications)
- Commit messages: `[task-id] ACT: <description>` and `[task-id] ADAPT: <reason>`

### Failure Threshold Mechanism
```python
# Instead of retry counts, use failure thresholds
if task.failure_threshold < 1.0:
    task.failure_threshold += 0.2  # Increment on failure
    # Retry with increased threshold
else:
    # Escalate to parent task
    parent.handle_child_failure(task)
```

### Plan Modification Patterns
The Navigator can apply these modifications:
```python
# Retry: Copy task with lessons learned
new_task = copy_task(failed_task)
new_task.failure_threshold += 0.2
tree.insert_at_front(new_task)

# Decompose: Replace with subtasks
subtasks = decompose_task(complex_task)
tree.replace_task(complex_task, subtasks)

# Refine: Update task description
task.description = refined_description

# Remove: Delete unnecessary task
tree.remove_task(redundant_task)
```

## State Management Details

### Immutable User Intent
- Original `user_intent/project.json` never modified
- Amendments directory for runtime clarifications
- Serves as north star for alignment checks

### Working Plan Evolution
- `working_plan/current.json` updated after each Adapt
- Contains entire task tree with current state
- Tracks failure thresholds and attempt history

### No External State
- All execution context in the task tree
- No separate databases or state files
- Git history provides complete audit trail