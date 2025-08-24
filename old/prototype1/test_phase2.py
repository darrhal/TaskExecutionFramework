#!/usr/bin/env python3
"""
Phase 2 Test Script

Tests the Phase 2 implementation of the Task Execution Framework
by running through the orchestrator with an atomic task.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from tef_orchestrator import TEFOrchestrator

def test_phase2_implementation():
    """Test Phase 2 executor agent integration."""
    
    print("=" * 60)
    print("Phase 2 Test: Executor Agent Implementation")
    print("=" * 60)
    
    # Create test orchestrator
    orchestrator = TEFOrchestrator(state_dir="test_state", max_iterations=2)
    
    # Clear any previous state
    orchestrator.state_manager.clear_state()
    
    # Load the create_file.md task
    task_file = "tasks/create_file.md"
    print(f"\n1. Loading task: {task_file}")
    
    if not orchestrator.load_task_from_file(task_file):
        print(f"❌ Failed to load task file: {task_file}")
        return False
    
    print("✅ Task loaded successfully")
    
    # Check that task queue has the task
    print(f"\n2. Checking task queue...")
    if not orchestrator.task_queue.has_pending_tasks():
        print("❌ No pending tasks found in queue")
        return False
    
    print("✅ Task found in queue")
    
    # Get the task
    task = orchestrator.task_queue.get_next_task()
    if not task:
        print("❌ Could not retrieve task from queue")
        return False
    
    print(f"✅ Retrieved task: {task.get('id')} - {task.get('title')}")
    
    # Test agent invoker directly
    print(f"\n3. Testing AgentInvoker...")
    
    # Check if agent instructions exist
    agent_file = Path("agents/executor_agent.md")
    if not agent_file.exists():
        print(f"❌ Agent instructions not found: {agent_file}")
        return False
    
    print("✅ Executor agent instructions found")
    
    # Test instruction loading
    instructions = orchestrator.agent_invoker.load_agent_instructions("executor_agent")
    if not instructions:
        print("❌ Failed to load agent instructions")
        return False
    
    print(f"✅ Loaded agent instructions ({len(instructions)} characters)")
    
    # Test executor invocation
    print(f"\n4. Testing executor agent invocation...")
    execution_result = orchestrator.agent_invoker.invoke_executor(task)
    
    if not execution_result or execution_result.get("status") != "success":
        print("❌ Executor agent invocation failed")
        print(f"Result: {execution_result}")
        return False
    
    print("✅ Executor agent invocation successful")
    print(f"   - Execution type: {execution_result.get('execution_type')}")
    print(f"   - Status: {execution_result.get('status')}")
    print(f"   - Actions taken: {len(execution_result.get('actions_taken', []))}")
    
    # Test full orchestrator execution
    print(f"\n5. Testing full orchestrator loop...")
    
    try:
        success = orchestrator.run_main_loop()
        if not success:
            print("❌ Orchestrator loop failed")
            return False
        
        print("✅ Orchestrator loop completed successfully")
        
    except Exception as e:
        print(f"❌ Orchestrator loop threw exception: {e}")
        return False
    
    # Verify state files were created
    print(f"\n6. Verifying state files...")
    
    state_files = [
        "task_queue.json",
        "execution_history.json", 
        "current_task.json"
    ]
    
    for state_file in state_files:
        state_data = orchestrator.state_manager.read_state(state_file)
        if not state_data:
            print(f"❌ State file empty or missing: {state_file}")
            return False
        print(f"✅ State file exists and has data: {state_file}")
    
    # Check execution history specifically
    history = orchestrator.state_manager.read_state("execution_history.json")
    executions = history.get("executions", [])
    if not executions:
        print("❌ No executions found in history")
        return False
    
    latest_execution = executions[-1]
    print(f"✅ Latest execution recorded:")
    print(f"   - Task ID: {latest_execution.get('task_id')}")
    print(f"   - Status: {latest_execution.get('status')}")
    print(f"   - Type: {latest_execution.get('execution_type')}")
    print(f"   - Agent instructions used: {latest_execution.get('agent_instructions_used')}")
    
    print(f"\n{'=' * 60}")
    print("✅ Phase 2 Test PASSED - All components working correctly")
    print("✅ Executor agent integration successful")
    print("✅ State management functional")
    print("✅ AgentInvoker operational")
    print("✅ Ready for Phase 3 (Observer System)")
    print("=" * 60)
    
    return True

def print_test_summary():
    """Print what Phase 2 accomplishes."""
    print("\nPhase 2 Accomplishments:")
    print("- ✅ Executor Agent Instructions: Comprehensive natural language programming template")
    print("- ✅ AgentInvoker Class: Integration layer for Task tool (simulated)")
    print("- ✅ Agent Context Preparation: Proper state passing to agents")
    print("- ✅ Execution Result Processing: Enhanced result handling with metadata")
    print("- ✅ Atomic vs Parent Task Distinction: Proper branching logic")
    print("- ✅ State File Integration: Current task written for agent access")
    print("- ✅ Error Handling: Robust error management throughout")
    
    print(f"\nNext Steps (Phase 3):")
    print("- Create observer agent templates")
    print("- Implement parallel observer execution")
    print("- Add observation aggregation")
    print("- Test multi-perspective assessment")

if __name__ == "__main__":
    if test_phase2_implementation():
        print_test_summary()
        sys.exit(0)
    else:
        print("\n❌ Phase 2 Test FAILED")
        sys.exit(1)