# TEF Light Feature Roadmap

## Overview
This document captures major upcoming features for TEF Light, maintaining the "light" philosophy while adding key capabilities for real-world usage.

## Major Features in Priority Order

### 1. Stateless Plan Re-evaluation 🎯 **SIMPLIFIED APPROACH**

**Vision**: Pathfinder performs complete stateless re-evaluation of the entire plan each time, using natural language reasoning to decide what should change.

**Current Infrastructure**:
✅ `TaskNode.description` field supports any natural language  
✅ Pathfinder can return modified TaskNodes with refined descriptions  
✅ `_update_task_tree()` function exists for applying changes  

**The "Light" Philosophy**:
Instead of complex maturity tracking or proximity logic, leverage the LLM's natural language capabilities:
- **Stateless**: Each evaluation looks at EVERYTHING fresh
- **Full context**: Current task + entire tree + all observations 
- **Natural reasoning**: Let Pathfinder decide in natural language what needs updating
- **Progressive refinement**: Near-term tasks get more detail, distant ones stay as sketches

**Required Components**:
- [ ] **Enhanced Pathfinder prompt**: Add explicit guidance for stateless full re-evaluation
- [ ] **Task Specification Templates**: Standard format for task specifications (no maturity levels needed)
- [ ] **Simplified tree updates**: Replace entire tree with Pathfinder's output

**Success Criteria**:
- Pathfinder can take "Build a todo app" and elaborate it into a reasonable execution plan
- Each evaluation considers the full context and updates the plan accordingly
- Near-term tasks become detailed, distant tasks remain appropriately sketched

---

### 2. Simple Audit Trail System 📊 **KEEP IT SIMPLE**

**Vision**: Basic audit trail of what happened at each Act/Assess/Adapt step for debugging.

**Current Infrastructure**:
✅ `record()` function called after Act and Adapt phases  
✅ Git commits provide basic audit trail  
✅ Structured outputs from all agents  

**Simple MVP Approach**:
Instead of complex artifact directories, just extend `record()` with simple logging:
- **Act**: Log execution summary (what files changed, what was done)  
- **Assess**: Log the four perspective observations briefly
- **Adapt**: Log what Pathfinder decided to change (or "No changes")

**Implementation**:
```
runs/2025-01-24_15-30-45/
  task-001.log
    ACT: Created hello.py with main function, modified 1 file
    ASSESS: Build=feasible, Requirements=aligned, Integration=compatible, Quality=good
    ADAPT: No changes needed, task complete
```

**Required Changes**:
- [ ] **Extend record() function**: Accept optional Act/Assess/Adapt results
- [ ] **Simple log format**: Human-readable entries, not complex JSON
- [ ] **Timestamp-based run directories**: `runs/YYYY-MM-DD_HH-MM-SS/`

**Success Criteria**:
- Can trace through any execution to see what happened at each step
- Simple text format that's easy to read and debug
- Minimal overhead - just append to log files

---

### 3. Pathfinder's Plan Updates 🧭 **NATURAL LANGUAGE DRIVEN**

**Vision**: Let the Pathfinder use natural language reasoning to completely re-evaluate and update the entire plan.

**Current Understanding**: 
The Adapt step is NOT about merging trees programmatically - it's about the Pathfinder taking into account EVERY SINGLE THING and updating the plan based on its judgment.

**The "Light" Approach**:
- Pathfinder receives full context: current task + entire tree + all observations
- Uses natural language reasoning to decide what should change
- Refines near-term tasks with more detail
- Re-sketches distant tasks as needed
- Returns a complete updated plan

**Required Changes**:
- [ ] **Enhanced Pathfinder System Prompt**: 
  - "Take into account EVERYTHING: current task, entire task tree, all observations"
  - "Use natural language reasoning to decide what should change about the plan" 
  - "Refine near-term tasks, re-sketch distant ones per your judgment"
- [ ] **Simplified _update_task_tree()**: 
  - Just replace the entire tree with Pathfinder's output
  - No complex merging - Pathfinder already considered everything

**Success Criteria**:
- Pathfinder can intelligently update entire plans based on full context
- Natural language instructions can be almost directly embedded in the agent
- Plans evolve sensibly with detailed near-term tasks and sketched distant ones

---

### 4. Simple Failure Threshold Implementation ⚠️ **NICE TO HAVE**

**Vision**: Basic adaptive failure handling without complex retry logic.

**Current State**: 
✅ `failure_threshold` field exists in TaskNode (0.0-1.0)  
❌ No threshold manipulation logic  

**Simple Implementation**:
- [ ] **Threshold Increment**: Increase by 0.2 after each failure
- [ ] **Parent Escalation**: At 1.0, mark task failed and let parent adapt
- [ ] **Reset Mechanism**: Parent can reset child threshold with new approach

**Implementation Approach**:
1. Add threshold increment in main execution loop on failure
2. Add escalation logic when threshold reaches 1.0
3. Allow Pathfinder to reset thresholds during adaptation

**Success Criteria**:
- Tasks become more tolerant of failures over time
- Failed tasks escalate to parent for different approach
- Simple, predictable failure handling behavior

---

## Simplified Development Approach

### Immediate Focus
1. **Enhance Pathfinder System Prompt** - Add natural language guidance for full re-evaluation
2. **Implement Simple Audit Trail** - Extend record() function for basic logging  
3. **Fix Tree Updates** - Simple replacement, no complex merging

### Near-term
- Task Specification Templates (without maturity levels)
- Basic failure thresholds (when needed)

## Design Principles for All Features

1. **Maintain "Light" Philosophy**: Simple implementations over complex ones
2. **Preserve Existing Architecture**: Extend, don't replace current patterns
3. **Optional by Default**: New features don't break existing functionality
4. **Clear Abstractions**: Each feature has well-defined interfaces
5. **Testable Components**: Features can be validated independently

## Success Metrics

- **Progressive Elaboration**: Can start with 1-sentence project description and execute it
- **State Management**: Complete debugging capability for any execution
- **Tree Management**: Reliable complex plan modifications
- **Failure Handling**: Graceful degradation under various failure modes

---

*This roadmap reflects the current understanding of TEF Light's direction while maintaining flexibility for emerging requirements and insights.*