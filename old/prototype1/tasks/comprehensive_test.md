---
id: comprehensive-test-001
title: Comprehensive End-to-End Test
type: parent
source: user
constraints:
  - Must test all TEF components together
  - Should validate full Act→Assess→Adapt loop
  - Must exercise recursive ExecuteTask pattern
  - Should test error recovery mechanisms
  - Must validate Git integration
acceptance:
  - All phases execute correctly
  - Parent/child task hierarchy works
  - Error recovery activates when needed
  - Git commits track all changes
  - State management is consistent
policy:
  max_attempts: 2
  max_depth: 4
  timeout_seconds: 45
subtasks:
  - id: comprehensive-test-001-sub-1
    title: Basic Task Execution Test
    description: Test basic Act→Assess→Adapt cycle
    type: atomic
    constraints:
      - Must complete successfully
      - Should create proper state files
  - id: comprehensive-test-001-sub-2
    title: Error Recovery Test
    description: Test error recovery mechanisms
    type: atomic
    simulate_failure: true
    failure_type: simulated_test_failure
    constraints:
      - Must fail on first attempt
      - Should recover on second attempt
  - id: comprehensive-test-001-sub-3
    title: Nested Parent Task
    description: Test nested task hierarchies
    type: parent
    subtasks:
      - id: comprehensive-test-001-sub-3-sub-1
        title: Deep Atomic Task
        description: Test deep nesting
        type: atomic
      - id: comprehensive-test-001-sub-3-sub-2
        title: Deep Recovery Task
        description: Test recovery at depth
        type: atomic
        simulate_failure: true
---

# Comprehensive End-to-End Test

This task thoroughly tests all components of the Task Execution Framework working together.

## Purpose

Validate that all implemented features work correctly in combination:

1. **Recursive ExecuteTask Pattern**: Parent tasks with multiple levels of subtasks
2. **Act→Assess→Adapt Loop**: Full cycle execution with real Task tool integration
3. **Error Recovery**: Graceful failure handling and retry mechanisms
4. **Git Integration**: Dual commits (ACT and ADAPT phases) with proper attribution
5. **State Management**: Consistent state across all operations
6. **Checkpointing**: Recovery checkpoints at all levels

## Test Scenarios

### 1. Basic Execution (Sub-1)
- Simple atomic task execution
- Validates core Act→Assess→Adapt cycle
- Tests Git integration for successful completion

### 2. Error Recovery (Sub-2)
- Simulated failure on first attempt
- Recovery mechanisms activation
- Successful completion after retry
- Recovery checkpoint creation

### 3. Nested Hierarchy (Sub-3)
- Parent task containing atomic subtasks
- Multi-level task nesting (depth 2)
- One subtask with error recovery testing
- Validates recursive ExecuteTask pattern

## Expected Behavior

1. **Parent Task**: Orchestrates all subtasks recursively
2. **Basic Task**: Completes successfully in one attempt
3. **Recovery Task**: Fails first, succeeds after recovery
4. **Nested Parent**: Manages its own subtasks independently
5. **Deep Tasks**: Execute at depth=2 with proper context
6. **Git History**: Multiple commits showing all phases
7. **State Files**: Consistent throughout execution
8. **Recovery Files**: Checkpoints created at key points

## Success Criteria

- [x] All subtasks complete successfully
- [x] Error recovery works at multiple depths
- [x] Git commits track every phase
- [x] State remains consistent
- [x] Recovery checkpoints created
- [x] Recursive ExecuteTask pattern validated
- [x] Full loop integration confirmed