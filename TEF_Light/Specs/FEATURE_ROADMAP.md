# TEF Light Feature Roadmap

## Overview
This document captures major upcoming features for TEF Light, maintaining the "light" philosophy while adding key capabilities for real-world usage.

## Major Features in Priority Order

### 1. Stateless Plan Re-evaluation 🎯 **SIMPLIFIED APPROACH**

**Vision**: Pathfinder performs complete stateless re-evaluation using natural language reasoning, considering ALL available context to decide what should change.

**Current Infrastructure**:
✅ `TaskNode.description` field supports any natural language  
✅ Pathfinder can return modified TaskNodes with refined descriptions  
✅ `_update_task_tree()` function exists for applying changes  

**Complete Context for Pathfinder** (The missing pieces!):
- **Current task** being executed
- **Entire task tree** (working plan)  
- **Original user intent** (immutable reference - the "north star")
- **Assessment observations** (from Build/Requirements/Integration/Quality perspectives)
- **Execution results** (if from Act phase)

**The Four Adapt Phase Evaluators**:
Pathfinder should employ these perspectives (NOT the Assess observers):
- **Next Step Evaluator**: "What's the immediate next action needed?"
- **Plan Coherence Evaluator**: "Do all tasks maintain consistency as a whole?"
- **Task Refinement Evaluator**: "Which upcoming tasks need more detail?"
- **Intent Alignment Evaluator**: "How well does the current plan align with original goals?"

**Multiple Strategist Synthesis**:
- **Technical Strategist**: Evaluates decomposition and implementation approaches
- **Requirements Strategist**: Ensures alignment with user intent
- **Risk Strategist**: Identifies potential obstacles and failure modes  
- **Efficiency Strategist**: Seeks simpler, more direct solutions

**Directory Structure Needed**:
```
user_intent/           # Immutable, human-authored specifications
working_plan/          # Agent-modified, evolving task tree  
environment/           # The actual repository being modified
```

**Required Components**:
- [ ] **Enhanced Pathfinder prompt**: Include the four Adapt evaluators and strategist perspectives
- [ ] **Original intent preservation**: Separate user_intent from working_plan
- [ ] **Intent-reality reconciliation**: Always check alignment with original goals
- [ ] **Task Specification Templates**: Standard format for consistency

**Success Criteria**:
- Pathfinder considers original user intent in all decisions
- Each evaluation uses the four Adapt evaluator perspectives
- Plans evolve while maintaining alignment with original goals
- "Pause and amend" capability through immutable intent reference

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

**Vision**: Let the Pathfinder use natural language reasoning to completely re-evaluate and update the entire plan using proper Adapt phase perspectives.

**Corrected Understanding**: 
The Adapt step uses DIFFERENT evaluators than the Assess step! Pathfinder should employ the four Adapt evaluators, not mix in the Assess observer perspectives.

**Complete Pathfinder Context**:
- Current task + entire tree + **original user intent** + assessment observations + execution results

**Proper Adapt Phase Process**:
1. **Intent Alignment Evaluation**: Check against original user goals
2. **Plan Coherence Evaluation**: Ensure all tasks work together consistently  
3. **Next Step Evaluation**: Identify immediate actions needed
4. **Task Refinement Evaluation**: Determine which tasks need more detail
5. **Strategist Synthesis**: Combine Technical/Requirements/Risk/Efficiency perspectives

**Required Changes**:
- [ ] **Enhanced Pathfinder System Prompt**: 
  - Include the four Adapt evaluators (not Assess observers)
  - Always reference original user intent as the "north star"
  - Incorporate multiple strategist perspectives for decision synthesis
  - Emphasize intent-reality reconciliation
- [ ] **Template Updates**: 
  - Pass original user intent to Pathfinder
  - Separate assessment observations from adaptation evaluation

**Success Criteria**:
- Pathfinder uses correct Adapt evaluators, not Assess observers
- All decisions reference original user intent for alignment
- Plans evolve while maintaining coherence and intent alignment
- Multiple strategist perspectives inform robust decision-making

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