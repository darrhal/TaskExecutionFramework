# TEF Light Manual Testing Instructions

## Overview
This guide helps you manually test and debug the TEF Light framework execution in VSCode, stepping through the Act→Assess→Adapt cycle to verify the enhanced logging and path management.

## Setup

### Prerequisites
1. VSCode with Python extension
2. Python environment with required dependencies
3. Git repository initialized in the test environment
4. Claude API key configured (for real testing) or mock mode (for deterministic testing)

### Test Environment Setup
```bash
# Create a clean test environment
mkdir tef_test_env
cd tef_test_env
git init
```

## Test Plans Available

### 1. Simple Calculator (`test_plans/simple_calculator.json`)
**Best for:** First-time testing, basic flow verification
- Creates a basic calculator with 4 math operations
- 1 parent task, 3 atomic subtasks
- Observable file creation and modifications
- Clear success criteria

### 2. Todo App (`test_plans/todo_app.json`)
**Best for:** Complex task hierarchy testing
- Multi-file application (model, views, main)
- Hierarchical task structure with dependencies
- Tests parent/child relationships

## VSCode Debugging Setup

### 1. Launch Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug TEF Light",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/test_runner.py",
            "args": ["--plan", "test_plans/simple_calculator.json", "--mock"],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

### 2. Key Breakpoint Locations

#### Core Loop (`tef_light.py`)
- **Line 74**: `execute_task()` entry - Observe task being processed
- **Line 80**: Task status change to "in_progress"
- **Line 85**: Before `execute()` call - Atomic task execution
- **Line 92**: Before `assess()` call - Assessment phase entry
- **Line 99**: Before `adapt()` call - Adaptation phase entry
- **Line 113**: Task completion - Status change to "completed"

#### Act Phase (`execute()` function)
- **Line 147**: Function entry - Task description logging
- **Line 159**: Claude agent execution
- **Line 170**: Return with results

#### Assess Phase (`assess()` function)
- **Line 173**: Function entry - Multi-perspective assessment
- **Line 200**: Return assessment results

#### Adapt Phase (`adapt()` function)
- **Line 203**: Function entry - Plan modification
- **Line 207**: Original intent loading
- **Line 242**: Pathfinder decision

#### Enhanced Logging
- **Line 277**: `_format_execution_report()` - ACT phase reporting
- **Line 288**: `_format_assessment_report()` - ASSESS phase reporting
- **Line 307**: `record()` function - Audit trail creation

## Step-by-Step Testing Procedure

### Phase 1: Setup and Initialization
1. **Start debugging session** with simple calculator test plan
2. **Set breakpoint** at `_init_project()` (line ~28)
3. **Step through** project directory creation
4. **Verify** global path variables are set correctly
5. **Check** directory structure creation:
   - `projects/{timestamp}/user_intent/`
   - `projects/{timestamp}/working_plan/`
   - `projects/{timestamp}/runs/`

### Phase 2: Task Tree Loading
1. **Break at** `execute_project()` (line 60)
2. **Step into** `TaskTree.load_from_file()`
3. **Verify** task tree structure loaded correctly
4. **Check** original intent preservation in `user_intent/original_plan.json`

### Phase 3: Core Loop Execution
For each task iteration:

#### 3.1 Act Phase (Atomic Tasks Only)
1. **Break at** line 85 (`execute()` call)
2. **Verify** `task.children` is None (atomic task)
3. **Step into** `execute()` function
4. **Observe** prompt generation and Claude agent call
5. **Check** `ExecutionResult` structure
6. **Step into** `_format_execution_report()`
7. **Verify** log formatting with status, files, changes
8. **Check** git diff capture

#### 3.2 Assess Phase (All Tasks)
1. **Break at** line 92 (`assess()` call)
2. **Step into** `assess()` function
3. **Observe** execution info formatting
4. **Check** prompt template rendering
5. **Verify** `AssessmentResult` with 4 perspectives
6. **Step into** `_format_assessment_report()`
7. **Check** pass/fail formatting for Build/Requirements/Integration/Quality

#### 3.3 Adapt Phase (All Tasks)
1. **Break at** line 99 (`adapt()` call)
2. **Step into** `adapt()` function
3. **Verify** original intent loading from `_original_intent_file`
4. **Check** observations formatting for template
5. **Observe** Pathfinder prompt construction
6. **Verify** TaskNode return or None

### Phase 4: Audit Trail Verification
1. **Check file creation** during execution:
   - `projects/{timestamp}/runs/{timestamp}.log` - Main execution log
   - `projects/{timestamp}/runs/{task-id}.log` - Task-specific logs
2. **Verify log format**:
   ```
   [2025-01-24 15:30:45] ACT: Executed task: Create calculator.py | Status: success | Files: 1 | Changes: Created basic calculator
   [2025-01-24 15:30:46] ASSESS: Assessment completed for task | Assessment: Build=pass, Requirements=pass, Integration=pass, Quality=pass
   [2025-01-24 15:30:47] ADAPT: No changes needed, proceeding as planned
   ```
3. **Check git commits**: Each ACT and ADAPT phase should create commits

### Phase 5: Path Management Verification
1. **Verify global path variables** remain consistent
2. **Check working plan updates** in `working_plan/current_plan.json`
3. **Verify original intent** remains immutable in `user_intent/original_plan.json`

## Mock Testing Mode

For deterministic testing without API calls, use mock mode:

```bash
python test_runner.py --plan test_plans/simple_calculator.json --mock
```

Mock mode provides:
- Predefined execution results
- Consistent assessment results
- Deterministic adaptation decisions
- Fast execution for debugging logic

## Expected Outputs

### Successful Run Indicators
1. **Console output** showing each phase
2. **Log files** created with structured entries
3. **Git commits** for each Act and Adapt phase
4. **Task status progression**: pending → in_progress → completed
5. **File creation** in test environment (calculator.py, etc.)

### Debug Watch Variables
Add these to your watch window:
- `task.id` - Current task identifier
- `task.status` - Task execution status
- `execution_result.status` - Act phase result
- `assessment.build.feasible` - Build assessment
- `_project_dir` - Current project directory
- `_original_intent_file.exists()` - Original intent preservation

## Common Issues and Solutions

### Issue: Path Not Found Errors
- **Cause**: Global path variables not initialized
- **Solution**: Ensure `_init_project()` runs first

### Issue: Git Commit Failures
- **Cause**: No changes to commit or git not initialized
- **Solution**: Initialize git in test environment

### Issue: Claude API Errors
- **Cause**: Missing API key or rate limits
- **Solution**: Use `--mock` mode for testing

### Issue: Missing Log Files
- **Cause**: Path creation or permission issues
- **Solution**: Check directory creation in `_init_project()`

## Advanced Testing

### Test Plan Modifications
Create custom test plans by modifying the JSON structure:
- Add more atomic tasks
- Create deeper hierarchies
- Test failure scenarios

### Logging Customization
Extend the format functions:
- Add more detail to execution reports
- Include timing information
- Add custom assessment criteria

### Integration Testing
Test with real Claude API:
1. Remove `--mock` flag
2. Set CLAUDE_API_KEY environment variable
3. Observe real agent responses and adaptations

This testing setup provides comprehensive debugging capabilities for verifying TEF Light's enhanced logging system and core execution flow.