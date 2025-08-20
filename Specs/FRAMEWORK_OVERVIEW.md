# Task Execution Framework - Overview

## Executive Summary

The Task Execution Framework (TEF) is a robust control system that maximizes execution robustness through progressive elaboration and continuous reconciliation. Rather than requiring perfect upfront specifications, it adapts and refines plans during execution based on discovered reality, embodying the principle of "continuous course correction through iterative assessment."

<details>
<summary>💡 <strong>What does this actually mean?</strong></summary>

**In simpler terms:** This framework is like a smart assistant that helps execute complex software tasks. Instead of needing a perfect plan upfront, it figures things out as it goes, making course corrections along the way.

**🚀 ELI5:** Imagine you're building a LEGO castle but don't have the exact instructions. This framework is like having a smart friend who helps you build it piece by piece, checking if it looks right and adjusting the plan as you discover new pieces or better ways to build it.
</details>

### Core Philosophy
- **Maximize execution robustness** through progressive elaboration
- **Reconcile continuously** between intent and discovered reality
- **Adapt frequently** with small course corrections rather than major pivots
- **Single-entry recursive architecture** for all task complexity levels

<details>
<summary>🎯 <strong>Understanding the Philosophy</strong></summary>

These are the core beliefs that drive how the framework operates. Think of them as the "personality traits" of the system.

**🎯 ELI5:** Like a GPS that recalculates your route when you take a wrong turn, this framework constantly adjusts its plan based on what it learns while working. It's better to adapt quickly than to plan perfectly from the start.
</details>

## System Mental Model

```
    Project/Task Specification
           ↓
    ┌──────────────┐
    │ ExecuteTask  │ ← Single entry point for ALL tasks
    └──────────────┘
           ↓
    ┌────────────────────────────┐
    │  Act → Assess → Adapt      │ ← Core control loop
    └────────────────────────────┘
           ↓
    [Continue | Retry | Split | Refine Plan | Complete]
```

Every task, from simple edits to complex multi-step operations, flows through the same `ExecuteTask` function, ensuring uniform handling, logging, and control.

<details>
<summary>🏭 <strong>How to Think About This System</strong></summary>

This diagram shows the high-level flow of how tasks move through the system. Everything flows through one central function, which ensures consistent handling.

**🏭 ELI5:** Think of this like a factory assembly line where every product (task) goes through the same stations in the same order, ensuring quality and consistency no matter how complex the product is.
</details>

## Key Concepts

### 1. Single-Entry Recursive Orchestration
All agent calls go through `ExecuteTask(spec, environment)` - whether it's the initial project or a deeply nested subtask. This provides:
- Uniform error handling and recovery
- Consistent audit trails
- Predictable resource management
- Simplified debugging

<details>
<summary>🚪 <strong>One Door In, Consistent Processing</strong></summary>

No matter what task you want to do, it all goes through the same entry point. This ensures every task gets the same quality of handling, logging, and error recovery.

**🚪 ELI5:** Like having one front door to a house - whether you're delivering mail, visiting friends, or coming home, everyone uses the same entrance. This way, security, logging, and house rules are applied consistently to everyone.
</details>

### 2. Progressive Elaboration Architecture
Rather than requiring perfect specifications upfront, the system:
- Executes with initial reasonable assumptions
- Refines understanding through each attempt
- Uses the Navigator to reconcile intent with discovered reality
- Evolves task definitions as execution reveals new information

<details>
<summary>🎨 <strong>Learning and Improving As You Go</strong></summary>

Instead of trying to plan everything perfectly from the start, the system starts with a reasonable guess and gets smarter with each attempt. It's like learning to cook a new recipe - you get better each time you make it.

**🎨 ELI5:** Like painting a picture where you start with a rough sketch and add more details as you go. You don't need to know exactly what the final painting will look like before you start - you figure it out as you paint.
</details>

### 3. Information-Gathering Observers
Observers gather facts and observations rather than make decisions:
```json
{
  "observer": "requirements",
  "observations": [...],
  "evidence": {...},
  "perspective": "product_requirements"
}
```
The Navigator uses these observations to make strategic decisions about task evolution.

<details>
<summary>👀 <strong>Observers, Not Judges</strong></summary>

Observers are like reporters - they observe and report what they see without making decisions. They gather facts from different perspectives, and then a separate component (the Navigator) makes decisions based on all the gathered information.

**👀 ELI5:** Imagine you have friends watching a soccer game from different seats in the stadium. Each friend sees the game from their angle and tells you what they observe. Then you (the Navigator) consult with your coaching staff (Strategists) to decide what to do based on all their different perspectives.
</details>

### 4. Multi-Perspective Assessment
Observers provide different lenses on the current state:
- **Build**: Compilation and technical feasibility
- **Requirements**: Alignment with acceptance criteria
- **Integration**: Compatibility with broader system context
- **Quality**: Code standards and maintainability

<details>
<summary>🔍 <strong>Looking at Problems from Different Angles</strong></summary>

Different verifiers check different aspects of the work, like having specialists examine different parts of a car - one checks the engine, another checks the brakes, another checks the electronics.

**🔍 ELI5:** Like having different doctors look at you during a checkup - an eye doctor checks your vision, a dentist checks your teeth, and a general doctor checks your overall health. Each one knows what to look for in their specialty.
</details>

### 5. Navigator-Driven Flow Control
The Navigator makes strategic decisions based on reconciling all information:
- **Minor gaps** → Adjust current approach
- **Significant misalignment** → Refine task definition
- **Fundamental obstacles** → Decompose into subtasks
- **Goal completion** → Advance to next phase

<details>
<summary>🧭 <strong>The Strategic Decision Maker</strong></summary>

The Navigator is like a ship's captain who takes in reports from all the crew members and decides what course to take. It doesn't just follow rigid rules - it makes intelligent decisions based on the current situation.

**🧭 ELI5:** Like a smart GPS that doesn't just say "recalculating" when you miss a turn, but actually thinks about whether there's a better route based on current traffic, road conditions, and your destination.
</details>

## Key Architectural Decisions

### Decision 1: No Built-in Sub-agents
**Choice**: Custom observer framework instead of Claude Code sub-agents  
**Rationale**: Provides finer control over assessment logic and enables recursive observation patterns

<details>
<summary>🔧 <strong>Custom Framework vs. Ready-Made Tools</strong></summary>

Instead of using Claude Code's built-in helper agents, this framework builds its own verification system. This gives more control over how verification works and allows for custom logic.

**🔧 ELI5:** Like choosing to build your own bicycle instead of buying one from the store. It takes more work, but you can customize it exactly how you want it to work.
</details>

### Decision 2: Python Implementation
**Choice**: Python with Claude Code SDK  
**Rationale**: 
- Native SDK support
- Minimal glue code
- ML/AI ecosystem compatibility
- Forces architectural simplicity

<details>
<summary>🐍 <strong>Why Python?</strong></summary>

Python was chosen because it has great support for AI/ML tools, the Claude SDK works well with it, and it keeps the code simple and readable.

**🐍 ELI5:** Like choosing English to write a book that will be read by people from many countries - Python is widely understood and has good tools for this type of work.
</details>

### Decision 3: No Testing Infrastructure (Initially)
**Choice**: No unit tests, integration tests, or test frameworks  
**Rationale**: Focus on assessment of actual behavior rather than test proxies

<details>
<summary>🚗 <strong>Real Behavior vs. Test Behavior</strong></summary>

Instead of writing traditional unit tests, this framework verifies that the actual code does what it's supposed to do in the real environment. It's like testing a car by driving it instead of just checking that all the parts are installed correctly.

**🚗 ELI5:** Instead of just checking if a cake recipe has the right ingredients listed, you actually bake the cake and taste it to see if it's good.
</details>

### Decision 4: Commit Every Attempt
**Choice**: Git commit after each attempt with full artifacts  
**Rationale**: Complete traceability and ability to rewind/replay any step

### Decision 6: Failure Handling is Local
**Choice**: Subtask failures don't cascade; parent tasks handle recovery  
**Rationale**: Enables resilient execution where each level can adapt to failures below it

### Decision 7: Simple Failure Counting
**Choice**: Count failures per observer type, not complex fingerprinting  
**Rationale**: Simplicity and predictability over sophisticated deduplication

<details>
<summary>📸 <strong>Complete History Tracking</strong></summary>

Every time the framework tries to do something, it saves a complete record of what happened. This means you can see exactly what was tried, when, and what the results were.

**📸 ELI5:** Like taking a photo after each move in a chess game. If something goes wrong, you can look back at any point and see exactly what the board looked like and what move was made.
</details>

### Decision 5: State-First, Not Code-First
**Choice**: Observers emit state; controller decides  
**Rationale**: Separation of observation from decision-making enables policy evolution without observer changes

<details>
<summary>👁️ <strong>Observe First, Decide Later</strong></summary>

The system separates "what happened" from "what to do about it". Verifiers just report what they observe, and a separate component makes decisions based on those observations.

**👁️ ELI5:** Like having weather reporters who just tell you "it's raining and 60 degrees" instead of "you should wear a raincoat". Someone else (you) decides what to wear based on the weather report.
</details>

## System Flow

### Core Execution Loop
1. **Load** task/project specification
2. **Act** - execute via Claude Code SDK (leaf tasks) or orchestrate subtasks (parent tasks)
3. **Assess** - gather observations through parallel observers
4. **Adapt** - reconcile intent with reality, handle failures locally, evolve plan as needed
5. **Commit** execution results and plan changes

**Key behaviors:**
- **Hierarchical orchestration**: Parent tasks coordinate subtasks, leaf tasks perform actual work
- **Local failure handling**: Subtask failures trigger parent's Adapt phase, not project failure
- **Continuous reconciliation**: Re-planning happens before each subtask and after failures
- **Failure counting**: Simple per-observer type counting with configurable retry limits

<details>
<summary>🔄 <strong>The Main Work Cycle</strong></summary>

This is the basic cycle that repeats for every task. Each step builds on the previous one, and the cycle continues until the task is complete or can't be completed.

**🔄 ELI5:** Like the process of learning to ride a bike: try to balance, see what happened, adjust your approach, try again. You keep doing this cycle until you can ride successfully.
</details>

### Navigation Decisions
- **Continue**: Minor progress, stay on current path
- **Refine**: Update task definition based on discoveries
- **Decompose**: Split into parallel or sequential subtasks
- **Escalate**: Fundamental mismatch requiring higher-level guidance
- **Complete**: Goals achieved, advance to next phase

<details>
<summary>🛣️ <strong>What the Navigator Can Decide</strong></summary>

Based on what it observes, the Navigator can choose from several different actions. Each action represents a different strategy for moving forward.

**🛣️ ELI5:** Like a driver who can choose to keep going straight, take a slight detour, make a U-turn, ask for help, or declare they've arrived at their destination.
</details>

### Plan Evolution
- Navigator updates task specifications in real-time
- Changes tracked through separate git commits
- Original intent preserved as immutable reference
- Task tree modifications cascade through dependent tasks

<details>
<summary>📋 <strong>How Plans Change Over Time</strong></summary>

The framework doesn't just execute a fixed plan - it actively improves and refines the plan as it learns more about what's needed. All changes are tracked so you can see how understanding evolved.

**📋 ELI5:** Like planning a vacation where you start with "visit Italy" but as you research, it becomes "visit Rome for 3 days, then Florence for 2 days, then take a day trip to Pisa." The plan gets more detailed and better as you learn more.
</details>

## Core Components

### 1. Controller (`controller.py`)
- Manages the Act→Assess→Adapt loop
- Coordinates all three phases mechanically
- Handles budgets and depth limits
- Manages git commits and artifacts

<details>
<summary>🎭 <strong>The Control Engine</strong></summary>

The Controller is like the engine of a car - it provides the mechanical power and coordination to move through the Act→Assess→Adapt cycle reliably and consistently.

**🎭 ELI5:** Like a teacher organizing a class project - they make sure everyone does their part at the right time, keep track of progress, and handle any problems that come up.
</details>

### 2. Navigator (`navigator.py`)
- **Multi-strategist architecture** for robust decision making
- **Strategic decision synthesis** based on observer reports and strategist perspectives
- **Task definition refinement** during the Adapt phase
- **Plan evolution tracking** with git commits for changes
- **Intent-reality reconciliation** to maintain alignment with goals

The Navigator employs multiple strategist functions:
- **Technical Strategist**: Evaluates decomposition and implementation approaches
- **Requirements Strategist**: Ensures alignment with user intent
- **Risk Strategist**: Identifies potential obstacles and failure modes
- **Efficiency Strategist**: Seeks simpler, more direct solutions

<details>
<summary>🧭 <strong>The Strategic Brain</strong></summary>

The Navigator is the strategic decision-maker that takes all the information gathered and decides what to do next. It employs multiple strategist perspectives to ensure robust decision-making. It's responsible for keeping the execution aligned with the original goals while adapting to reality.

**🧭 ELI5:** Like a ship's captain who listens to reports from the crew about weather, supplies, and navigation, then consults with different officers (navigation officer, safety officer, efficiency officer) before deciding whether to stay on course, change direction, or stop at a port.
</details>

### 3. Observers
Parallel information-gathering modules that provide different perspectives during the Assess phase:

| Observer | Perspective | Information Gathered | Implementation | Max Retries |
|----------|-------------|---------------------|----------------|-------------|
| Build | Technical | Compilation status, errors | Shell commands or model analysis | 4 |
| Requirements | Acceptance | Criteria satisfaction progress | Model evaluation | 2 |
| Integration | System | Parent/child task compatibility | Model analysis | 2 |
| Quality | Standards | Code style, maintainability | Configurable (shell/model) | 3 |

**Implementation approach:**
- Start with hard-coded functions returning status and observations
- Clean interface: `observe(execution_result, environment) -> ObserverReport`
- Future evolution to support hybrid explicit/LLM-based observation
- Per-observer retry limits prevent infinite loops

<details>
<summary>🔬 <strong>The Observation Team</strong></summary>

Observers are like specialized sensors at different stations, each monitoring specific aspects of the work. They run in parallel to save time and provide comprehensive feedback.

**🔬 ELI5:** Like having different coaches for a sports team - one watches your form, another checks your strategy, another monitors your fitness. Each gives feedback from their expertise, and the head coach (Navigator) consults with assistant coaches (Strategists) to decide what to work on.
</details>

### 4. Task Specifications
Markdown files with YAML frontmatter, supporting both structured tasks and projects:

#### Project (Top-level)
```yaml
---
type: project
id: order-management-v2
title: Implement order management system
source: user  # or "generated"
original_preserved: true  # only if source=user
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

<details>
<summary>📝 <strong>The Work Instructions</strong></summary>

Task specifications are like detailed work orders that describe what needs to be done. They can be simple (a single task) or complex (a project with many subtasks). The YAML frontmatter acts like a cover sheet with all the important metadata.

**📝 ELI5:** Like a recipe card that has the ingredients list at the top (YAML) and the cooking instructions below (markdown). Some recipes are simple (scrambled eggs) while others have multiple parts (a three-course meal).
</details>

### 5. Artifacts & Logging
Every attempt produces organized artifacts following the Act→Assess→Adapt structure:
```
runs/<run-id>/
  attempt-001/
    act/
      execution.json
      stdout.log
    assess/
      build_observer.json
      requirements_observer.json
      integration_observer.json
      quality_observer.json
    adapt/
      strategist_perspectives.json
      navigator_decision.json
      plan_updates.json
```

Task organization:
- `tasks/original/` ← User-authored specifications only (immutable)
- `tasks/current/` ← All current specifications (evolved)
- Git commits: `[task-id] attempt n: <decision>` and `[task-id] ADAPT: <reason>`

<details>
<summary>📚 <strong>The Paper Trail</strong></summary>

The framework keeps detailed records of everything it does - like a scientist's lab notebook. This helps with debugging, learning from past runs, and understanding how decisions were made.

**📚 ELI5:** Like keeping a diary of a road trip - you write down where you went, what you saw, what decisions you made, and what happened. Later, you can look back and understand the whole journey.
</details>

## Configuration Philosophy

### Global Defaults (`observers.yml`)
Define stakeholders and default observer configurations centrally, including retry limits:
```yaml
observers:
  build:
    max_retries: 4
  requirements:
    max_retries: 2
  quality:
    max_retries: 3
  integration:
    max_retries: 2
```

### Per-Task Overrides
Tasks can override specific observer settings in their frontmatter.

### Runtime Flags
Manual overrides and operational controls via CLI arguments.

<details>
<summary>⚙️ <strong>Flexible Configuration System</strong></summary>

The framework uses a layered configuration approach - global defaults that apply to everything, task-specific overrides for special cases, and runtime flags for manual control. Each layer can override the previous one.

**⚙️ ELI5:** Like how your phone has default settings, but each app can have its own settings, and you can manually change things when needed. The most specific setting wins.
</details>

## Extension Points

### Adding New Observers
1. Define stakeholder and purpose
2. Implement observer function with standard interface
3. Register in `observers.yml` with retry limits
4. Set criticality level and retry behavior

Example observer implementation:
```python
def build_observer(execution_result, environment) -> ObserverReport:
    return {
        "status": "pass/fail",
        "observations": [...],
        "evidence": {...}
    }
```

### Adding New Decision Rules
1. Add new strategist functions to Navigator
2. Modify synthesis logic in controller
3. Update fingerprinting if needed
4. Adjust thresholds in configuration

<details>
<summary>🔌 <strong>How to Extend the Framework</strong></summary>

The framework is designed to be extended with new capabilities. You can add new verifiers to check different things, or new decision rules to handle special situations. It's built to grow with your needs.

**🔌 ELI5:** Like adding new tools to a toolbox - you can add a new screwdriver (verifier) when you need to work with different screws, or create new rules about when to use which tool.
</details>

## Getting Started

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run a task
python controller.py --task tasks/task-001.md

# With parallel child execution
python controller.py --task tasks/task-001.md --parallel 3

# With manual override
python controller.py --task tasks/task-001.md --override DONE --why "Verified manually"
```

### Creating Your First Task
1. Copy `tasks/task-template.md`
2. Define acceptance criteria and constraints
3. Set appropriate budgets and policies
4. Run with controller

<details>
<summary>🚀 <strong>Getting Up and Running</strong></summary>

Starting with the framework is straightforward - install the dependencies, create a task file describing what you want to do, and run the orchestrator. The framework handles the complexity while you focus on defining what success looks like.

**🚀 ELI5:** Like using a microwave - you put in your food (task), set the timer (policies), press start (run orchestrator), and it handles the heating (execution) for you.
</details>

## Design Principles

1. **Explicit over Implicit**: All decisions are logged and traceable
2. **Assessment over Specification**: Comprehensive observation beats perfect planning
3. **Simplicity over Features**: Start minimal, add only proven needs
4. **Deterministic over Learned**: Predictable behavior for debugging
5. **State over Decisions**: Separate observation from judgment

<details>
<summary>🏛️ <strong>The Guiding Principles</strong></summary>

These principles guide every design decision in the framework. They prioritize clarity, reliability, and maintainability over complexity and cleverness. When in doubt, the framework chooses the simpler, more explicit approach.

**🏛️ ELI5:** Like the rules of good cooking - use fresh ingredients (explicit), taste as you go (verification), start with basic recipes (simplicity), follow proven techniques (deterministic), and check the food's state before deciding next steps (state over decisions).
</details>

## Future Roadmap

### Near Term
- Security observer (stakeholder model ready)
- Performance observer (metrics collection)
- Failure tracking implementation (per-observer counting)

### Medium Term
- Personality consistency via stakeholder prompts
- Learned advisory layers (never gating)
- Distributed execution support

### Long Term
- Multi-repository task coordination
- Cross-language support beyond Python
- IDE integrations

## Glossary

- **ExecuteTask**: The single-entry control function for all tasks (formerly CodeTaskAgent)
- **Controller**: The mechanical engine that runs the Act→Assess→Adapt loop
- **Navigator**: Strategic decision maker with multiple strategist perspectives that reconciles intent with reality
- **Observers**: Information-gathering modules providing different perspectives during assessment
- **Strategists**: Specialized decision-making functions within the Navigator providing diverse perspectives
- **Project**: Top-level task that preserves original user intent when user-authored
- **Environment**: Runtime context and state information
- **Reconciliation**: Process of aligning current reality with intended goals (part of Adapt phase)
- **Progressive Elaboration**: Refining plans through execution rather than upfront planning

## Next Steps

For hands-on examples and patterns, explore the `tasks/` directory and run the included examples. (TBD)

## Pending Design Decisions

The following topics require further discussion and decision-making:

### 1. Hierarchical Execution Flow
- How do parent tasks orchestrate vs leaf tasks that actually act?
- Where does continuous re-planning occur in the execution hierarchy?
- How do we balance local adaptation with global plan coherence?

### 2. Observer Implementation Details
- Plugin architecture for observers - how to make them truly configurable?
- Balance between explicit coded logic and LLM-based observation
- Standard interface for observer registration and configuration

### 3. Natural Language to Formal Spec Conversion
- How do users naturally describe tasks vs our internal structure?
- Automated conversion from informal descriptions to structured specs
- Preserving user intent through the formalization process

### 4. Task Ordering and Dependencies
- Handling parallel vs sequential execution declaratively
- Implicit vs explicit dependency management
- Dynamic reordering based on discovered dependencies

### 5. Navigator Naming and Scope
- Is "Navigator" the right term for the strategic decision maker?
- Should we split navigation from strategic planning?
- How do multiple strategists coordinate within the Navigator?

### 6. Technical Specification Updates
- Detailed contracts and interfaces
- Implementation guidelines
- To be completed after core design decisions are finalized