# Task Execution Framework - Overview

## Executive Summary

The Task Execution Framework (TEF) is a robust orchestration system that maximizes execution robustness through progressive elaboration and continuous reconciliation. Rather than requiring perfect upfront specifications, it adapts and refines plans during execution based on discovered reality, embodying the principle of "continuous course correction through comprehensive pre-planning."

### Core Philosophy
- **Maximize execution robustness** through progressive elaboration
- **Reconcile continuously** between intent and discovered reality
- **Adapt frequently** with small course corrections rather than major pivots
- **Single-entry recursive architecture** for all task complexity levels

## System Mental Model

```
    Project/Task Specification
           ↓
    ┌───────────────┐
    │ CodeTaskAgent │ ← Single entry point for ALL tasks
    └───────────────┘
           ↓
    ┌──────────────────────────────────────────────────────┐
    │  Execute → Verify → Navigate → Reconcile → Adapt     │ ← Core execution loop
    └──────────────────────────────────────────────────────┘
           ↓
    [Continue | Retry | Split | Refine Plan | Complete]
```

Every task, from simple edits to complex multi-step operations, flows through the same `CodeTaskAgent` function, ensuring uniform handling, logging, and control.

## Key Concepts

### 1. Single-Entry Recursive Orchestration
All agent calls go through `CodeTaskAgent(spec, environment)` - whether it's the initial project or a deeply nested subtask. This provides:
- Uniform error handling and recovery
- Consistent audit trails
- Predictable resource management
- Simplified debugging

### 2. Progressive Elaboration Architecture
Rather than requiring perfect specifications upfront, the system:
- Executes with initial reasonable assumptions
- Refines understanding through each attempt
- Uses the Navigator to reconcile intent with discovered reality
- Evolves task definitions as execution reveals new information

### 3. Information-Gathering Verifiers
Verifiers gather facts and observations rather than make decisions:
```json
{
  "verifier": "alignment",
  "observations": [...],
  "evidence": {...},
  "perspective": "product_requirements"
}
```
The Navigator uses these observations to make strategic decisions about task evolution.

### 4. Multi-Perspective Verification
Verifiers provide different lenses on the current state:
- **Build**: Compilation and technical feasibility
- **Requirements**: Alignment with acceptance criteria
- **Integration**: Compatibility with broader system context
- **Quality**: Code standards and maintainability

### 5. Navigator-Driven Flow Control
The Navigator makes strategic decisions based on reconciling all information:
- **Minor gaps** → Adjust current approach
- **Significant misalignment** → Refine task definition
- **Fundamental obstacles** → Decompose into subtasks
- **Goal completion** → Advance to next phase

## Key Architectural Decisions

### Decision 1: No Built-in Sub-agents
**Choice**: Custom verifier framework instead of Claude Code sub-agents  
**Rationale**: Provides finer control over verification logic and enables recursive verification patterns

### Decision 2: Python Implementation
**Choice**: Python with Claude Code SDK  
**Rationale**: 
- Native SDK support
- Minimal glue code
- ML/AI ecosystem compatibility
- Forces architectural simplicity

### Decision 3: No Testing Infrastructure (Initially)
**Choice**: No unit tests, integration tests, or test frameworks  
**Rationale**: Focus on verification of actual behavior rather than test proxies

### Decision 4: Commit Every Attempt
**Choice**: Git commit after each attempt with full artifacts  
**Rationale**: Complete traceability and ability to rewind/replay any step

### Decision 5: State-First, Not Code-First
**Choice**: Verifiers emit state; orchestrator decides  
**Rationale**: Separation of observation from decision-making enables policy evolution without verifier changes

## System Flow

### Core Execution Loop
1. **Load** task/project specification
2. **Execute** via Claude Code SDK
3. **Verify** through parallel verifiers (Build, Alignment, Integration, Quality)
4. **Navigate** - reconcile intent with current reality
5. **Adapt** - update task definition if needed
6. **Commit** execution results and plan changes

### Navigation Decisions
- **Continue**: Minor progress, stay on current path
- **Refine**: Update task definition based on discoveries
- **Decompose**: Split into parallel or sequential subtasks
- **Escalate**: Fundamental mismatch requiring higher-level guidance
- **Complete**: Goals achieved, advance to next phase

### Plan Evolution
- Navigator updates task specifications in real-time
- Changes tracked through separate git commits
- Original intent preserved as immutable reference
- Task tree modifications cascade through dependent tasks

## Core Components

### 1. Orchestrator (`orchestrator.py`)
- Manages the execution loop
- Coordinates execution, verification, and navigation phases
- Handles budgets and depth limits
- Manages git commits and artifacts

### 2. Navigator (`navigator.py`)
- **Strategic decision making** based on verifier observations
- **Task definition refinement** during execution
- **Plan evolution tracking** with git commits for changes
- **Intent-reality reconciliation** to maintain alignment with goals

### 3. Verifiers
Parallel information-gathering modules that provide different perspectives:

| Verifier | Perspective | Information Gathered | Implementation |
|----------|-------------|---------------------|----------------|
| Build | Technical | Compilation status, errors | Shell commands or model analysis |
| Alignment | Requirements | Acceptance criteria progress | Model evaluation |
| Integration | System | Parent/child task compatibility | Model analysis |
| Quality | Standards | Code style, maintainability | Configurable (shell/model) |

### 4. Task Specifications
Markdown files with YAML frontmatter, supporting both structured tasks and projects:

#### Project (Top-level)
```yaml
---
type: project
id: order-management-v2
title: Implement order management system
original_intent: preserved_separately  # Immutable reference
subtasks:
  - parallel:
    - tasks/order-api.md
    - tasks/order-validation.md
  - tasks/integration-tests.md
---
Project description and context...
```

#### Task (Recursive)
```yaml
---
id: task-001
title: Add order cancellation endpoint
constraints: [...]
acceptance: [...]
policy:
  max_attempts: 3
  max_depth: 3
---
Implementation details...
```

### 5. Artifacts & Logging
Every attempt produces:
- `runs/<run-id>/attempt-<n>/verifier_outputs.json`
- `runs/<run-id>/attempt-<n>/navigator_decision.json`
- `tasks/original/` ← Immutable original specifications
- `tasks/current/` ← Evolved specifications
- Git commits: `[task-id] attempt n: decision` and `[task-id] PLAN UPDATE: reason`

## Configuration Philosophy

### Global Defaults (`verifiers.yml`)
Define stakeholders and default verifier configurations centrally.

### Per-Task Overrides
Tasks can override specific verifier settings in their frontmatter.

### Runtime Flags
Manual overrides and operational controls via CLI arguments.

## Extension Points

### Adding New Verifiers
1. Define stakeholder and purpose
2. Implement verifier returning state JSON
3. Register in `verifiers.yml`
4. Set criticality level and retry behavior

### Adding New Decision Rules
1. Modify aggregator logic in orchestrator
2. Update fingerprinting if needed
3. Adjust thresholds in configuration

## Getting Started

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run a task
python orchestrator.py --task tasks/task-001.md

# With parallel child execution
python orchestrator.py --task tasks/task-001.md --parallel 3

# With manual override
python orchestrator.py --task tasks/task-001.md --override DONE --why "Verified manually"
```

### Creating Your First Task
1. Copy `tasks/task-template.md`
2. Define acceptance criteria and constraints
3. Set appropriate budgets and policies
4. Run with orchestrator

## Design Principles

1. **Explicit over Implicit**: All decisions are logged and traceable
2. **Verification over Specification**: Comprehensive checking beats perfect planning
3. **Simplicity over Features**: Start minimal, add only proven needs
4. **Deterministic over Learned**: Predictable behavior for debugging
5. **State over Decisions**: Separate observation from judgment

## Future Roadmap

### Near Term
- Security verifier (stakeholder model ready)
- Performance verifier (metrics collection)
- Enhanced fingerprinting algorithms

### Medium Term
- Personality consistency via stakeholder prompts
- Learned advisory layers (never gating)
- Distributed execution support

### Long Term
- Multi-repository task coordination
- Cross-language support beyond Python
- IDE integrations

## Glossary

- **CodeTaskAgent**: The single-entry orchestration function for all tasks
- **Navigator**: Strategic decision maker that reconciles intent with reality
- **Project**: Top-level task that preserves original immutable intent
- **Verifier**: Information-gathering module providing different perspectives
- **Environment**: Runtime context and state information
- **Reconciliation**: Process of aligning current reality with intended goals
- **Progressive Elaboration**: Refining plans through execution rather than upfront planning

## Next Steps

For detailed technical specifications, contracts, and implementation guidelines, see [`TECHNICAL_SPECIFICATION.md`](TECHNICAL_SPECIFICATION.md).

For hands-on examples and patterns, explore the `tasks/` directory and run the included examples.