# Task Execution Framework - Overview

## Executive Summary

The Task Execution Framework (TEF) is a robust, verification-centric orchestration system for executing software development tasks with minimal upfront planning. It achieves reliability through comprehensive verification loops rather than perfect initial specifications, embodying the principle that "verification is the more critical piece."

### Core Philosophy
- **Minimize upfront planning** while maximizing execution robustness
- **Verify comprehensively** rather than specify perfectly
- **Fail fast and retry smart** with structured feedback loops
- **Single-entry recursive architecture** for all task complexity levels

## System Mental Model

```
    Task Specification
           ↓
    ┌───────────────┐
    │ CodeTaskAgent │ ← Single entry point for ALL tasks
    └───────────────┘
           ↓
    ┌─────────────────────────────────────┐
    │  Generate → Apply → Verify → Decide │ ← Core execution loop
    └─────────────────────────────────────┘
           ↓
    [Retry | Split | Done | Give Up]
```

Every task, from simple edits to complex multi-step operations, flows through the same `CodeTaskAgent` function, ensuring uniform handling, logging, and control.

## Key Concepts

### 1. Single-Entry Recursive Orchestration
All agent calls go through `CodeTaskAgent(spec, ctx)` - whether it's the initial user task or a deeply nested subtask. This provides:
- Uniform error handling and recovery
- Consistent audit trails
- Predictable resource management
- Simplified debugging

### 2. Verification-First Architecture
Rather than trying to specify everything upfront, the system:
- Executes with reasonable assumptions
- Verifies comprehensively after each attempt
- Uses verification feedback to guide retries
- Learns from failures through structured fingerprinting

### 3. State-First Verifiers
Verifiers "emit what they see" rather than make decisions:
```json
{
  "verifier": "alignment",
  "severity": "warning",
  "findings": [...],
  "evidence": {...}
}
```
The orchestrator applies deterministic rules to these states, ensuring consistent decision-making.

### 4. Stakeholder-Based Verification
Different aspects of code quality are owned by different "stakeholders":
- **Architecture**: Build integrity, structural consistency
- **Product**: Acceptance criteria, requirement alignment
- **Future**: Security (deferred), Performance (planned)

### 5. Deterministic Control Flow
"A fail is a fail" - control flow depends only on severity levels:
- **Error** → Retry (up to max_attempts)
- **Warning** → Retry if configured, otherwise continue
- **Info** → Continue
- **Repeated errors** → Split into child tasks or give up

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

### Happy Path
1. **Load** task specification (Markdown with YAML frontmatter)
2. **Execute** via Claude Code SDK (mode="edit")
3. **Verify** through staged verifiers (Build → Alignment → BigPicture)
4. **Decide** based on verification results
5. **Commit** and complete

### Retry Path
1. Same steps 1-3 as happy path
2. **Aggregate** errors/warnings from verifiers
3. **Feedback** structured findings to next attempt
4. **Loop** up to max_attempts

### Split Path
1. Same steps 1-3 as happy path
2. **Detect** repeated error fingerprints (≥2 occurrences)
3. **Generate** child task specifications
4. **Recurse** via CodeTaskAgent at depth+1
5. **Aggregate** child results

## Core Components

### 1. Orchestrator (`orchestrator.py`)
- Manages the execution loop
- Applies deterministic decision rules
- Handles budgets and depth limits
- Manages git commits and artifacts

### 2. Verifiers
Pluggable verification modules that assess different aspects:

| Verifier | Stakeholder | Purpose | Criticality |
|----------|-------------|---------|-------------|
| Build | Architecture | Ensures code compiles | Blocker |
| Alignment | Product | Validates acceptance criteria | Standard |
| BigPicture | Architecture | Checks parent/next task fit | Standard |
| Style | Architecture | Code quality (optional) | Advisory |

### 3. Task Specifications
Markdown files with YAML frontmatter:
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

### 4. Artifacts & Logging
Every attempt produces:
- `runs/<run-id>/attempt-<n>/verifier_outputs.json`
- `runs/<run-id>/attempt-<n>/decision.json`
- Git commit with message: `[task-id] attempt n: decision`

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

- **CodeTaskAgent**: The single-entry orchestration function
- **Verifier**: A module that assesses code changes from a specific perspective
- **Stakeholder**: An ownership role representing a verification perspective
- **Fingerprint**: A normalized hash identifying a specific error pattern
- **Split**: Creating child tasks when errors repeatedly occur
- **Severity**: Error/Warning/Info level determining control flow
- **Verdict**: Optional verifier veto (fail/pass/advisory)

## Next Steps

For detailed technical specifications, contracts, and implementation guidelines, see [`TECHNICAL_SPECIFICATION.md`](TECHNICAL_SPECIFICATION.md).

For hands-on examples and patterns, explore the `tasks/` directory and run the included examples.