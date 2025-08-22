---
id: parent-task-001
title: Parent Task Test
type: parent
source: user
constraints:
  - Must demonstrate parent task orchestration
  - Should spawn and manage subtasks
acceptance:
  - All subtasks complete successfully
  - Parent task orchestrates properly
  - Recursive ExecuteTask pattern works
policy:
  max_attempts: 2
  max_depth: 3
subtasks:
  - id: parent-task-001-sub-1
    title: First Subtask
    description: Create a simple file
    type: atomic
  - id: parent-task-001-sub-2
    title: Second Subtask  
    description: Validate the created file
    type: atomic
---

# Parent Task Test

This task demonstrates the recursive ExecuteTask pattern by:

1. **Parent Task**: Orchestrates multiple subtasks
2. **Subtask 1**: Creates a simple test file
3. **Subtask 2**: Validates the created file

## Purpose

Test the framework's ability to:
- Handle parent tasks that contain subtasks
- Recursively invoke ExecuteTask for each subtask
- Maintain proper context between parent and child tasks
- Complete parent task only after all subtasks finish

## Expected Behavior

1. Parent task analyzes its subtasks
2. Each subtask is processed through the full Act→Assess→Adapt loop
3. Parent task monitors subtask completion
4. Parent task completes when all subtasks are done

## Success Criteria

- [x] Parent task loads and identifies subtasks
- [x] Subtasks are created and added to task queue
- [x] Each subtask executes through ExecuteTask recursively
- [x] Parent task completes after all subtasks finish
- [x] Proper hierarchy and context maintained throughout