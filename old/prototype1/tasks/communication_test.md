---
id: communication-test-001
title: Agent Communication Test
type: atomic
source: user
constraints:
  - Must test inter-agent messaging
  - Should demonstrate shared context
  - Must validate knowledge accumulation
acceptance:
  - Agents communicate via message passing
  - Shared context is updated and accessed
  - Knowledge base accumulates learnings
  - Communication enhances execution quality
policy:
  max_attempts: 2
  max_depth: 2
  timeout_seconds: 45
---

# Agent Communication Test

This task tests the Phase 6.2 agent communication patterns and knowledge sharing.

## Purpose

Validate that the agent communication system provides:

1. **Inter-agent Messaging**: Structured message passing between agents
2. **Shared Context Files**: Common context accessible to all agents
3. **Knowledge Accumulation**: Learning storage and retrieval
4. **Communication Patterns**: Established communication workflows

## Test Scenarios

### Message Passing
- Executor sends completion messages to observers
- Observers send observations to navigator
- Navigator broadcasts decisions to all agents
- Messages are prioritized and processed correctly

### Shared Context
- Execution context shared between agents
- Context updates propagated to all agents
- Historical context accessible for learning
- Context-aware decision making

### Knowledge Base
- Execution patterns are learned and stored
- Decision patterns are accumulated
- Observation patterns are recorded
- Knowledge is retrieved and applied

## Expected Behavior

The communication system should:
1. Initialize message, context, and knowledge files
2. Enable agents to send and receive structured messages
3. Maintain shared context across agent interactions
4. Accumulate knowledge from each execution
5. Apply learned patterns to improve future executions

## Success Criteria

- [x] Communication files are created and managed
- [x] Agents send messages to each other
- [x] Shared context is updated and accessed
- [x] Knowledge base accumulates learnings
- [x] Communication patterns enhance execution
- [x] Inter-agent coordination is observable