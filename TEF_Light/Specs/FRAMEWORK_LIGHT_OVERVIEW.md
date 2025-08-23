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

### Core Components

The framework consists of three main directories:
- **user_intent/**: Immutable, human-authored specifications
- **working_plan/**: Agent-modified, evolving task tree
- **environment/**: The actual repository being modified

### Task Tree Structure

A single JSON file represents the entire project as a hierarchical tree of tasks. Each task has:
- Unique ID and type (parent or atomic)
- Natural language description
- Failure threshold for adaptive retry handling
- Children tasks (for parent nodes)

## The Core Loop

The framework executes a continuous Act→Assess→Adapt cycle:

1. **Act Phase** (atomic tasks only): Execute changes to the environment
2. **Assess Phase** (all tasks): Gather observations from multiple perspectives
   - Build: compilation, technical feasibility
   - Requirements: alignment with acceptance criteria
   - Integration: compatibility with system context
   - Quality: code standards, maintainability
3. **Adapt Phase** (all tasks): Navigator searches for optimal path modifications

Each phase results in a git commit, providing complete traceability of both execution and planning evolution.

## Agent Architecture

Three pure functions orchestrate the framework:

- **Executor**: Performs actual environment changes (atomic tasks only)
- **Assessor**: Gathers facts from multiple perspectives without making decisions
- **Navigator**: Searches for optimal path forward, modifying the plan based on observations

All agents use structured I/O via the Claude SDK for reliable, deterministic behavior.

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

## Design Principles

- **Simplicity over complexity**: Minimal implementation (~200 lines)
- **Natural language specifications**: Tasks described in plain English
- **Everything in the tree**: No external state or databases
- **Continuous reconciliation**: Reality shapes the plan as much as the plan shapes reality
- **Complete observability**: Every decision and action tracked via git

## Benefits

- **Continuous reconciliation** between intent and reality
- **Deep understanding** through complete tree evaluation
- **Natural emergence** of complex behaviors from simple plan modifications
- **Complete traceability** through git history
- **Pause and amend** capability through immutable intent

The framework achieves sophisticated adaptation through simple, thorough re-evaluation rather than complex logic.