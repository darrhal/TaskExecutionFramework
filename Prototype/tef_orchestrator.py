#!/usr/bin/env python3
"""
Task Execution Framework (TEF) - Natural Language Prototype Orchestrator

This is the minimal orchestrator that implements the Act->Assess->Adapt loop
using natural language agents and persistent state files.

Usage:
    python tef_orchestrator.py --task tasks/hello_world.md
"""

import json
import os
import sys
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class StateManager:
    """Manages persistent state files for agent communication."""
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
    
    def read_state(self, filename: str) -> Dict[str, Any]:
        """Read state from JSON file."""
        try:
            state_file = self.state_dir / filename
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error reading state file {filename}: {e}")
            return {}
    
    def write_state(self, filename: str, data: Dict[str, Any]) -> bool:
        """Write state to JSON file."""
        try:
            state_file = self.state_dir / filename
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error writing state file {filename}: {e}")
            return False
    
    def clear_state(self) -> bool:
        """Clear all state files."""
        try:
            for state_file in self.state_dir.glob("*.json"):
                state_file.unlink()
            return True
        except Exception as e:
            print(f"Error clearing state: {e}")
            return False


class TaskQueue:
    """Manages task queue operations."""
    
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.queue_file = "task_queue.json"
    
    def add_task(self, task: Dict[str, Any]) -> bool:
        """Add task to queue."""
        try:
            queue_data = self.state_manager.read_state(self.queue_file)
            if "tasks" not in queue_data:
                queue_data["tasks"] = []
            
            # Generate task ID if not present
            if "id" not in task:
                task["id"] = str(uuid.uuid4())[:8]
            
            queue_data["tasks"].append(task)
            return self.state_manager.write_state(self.queue_file, queue_data)
        except Exception as e:
            print(f"Error adding task to queue: {e}")
            return False
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get next task from queue."""
        try:
            queue_data = self.state_manager.read_state(self.queue_file)
            tasks = queue_data.get("tasks", [])
            
            for task in tasks:
                if task.get("status") != "completed":
                    return task
            return None
        except Exception as e:
            print(f"Error getting next task: {e}")
            return None
    
    def mark_complete(self, task_id: str) -> bool:
        """Mark task as completed."""
        try:
            queue_data = self.state_manager.read_state(self.queue_file)
            tasks = queue_data.get("tasks", [])
            
            for task in tasks:
                if task.get("id") == task_id:
                    task["status"] = "completed"
                    task["completed_at"] = datetime.now().isoformat()
                    break
            
            return self.state_manager.write_state(self.queue_file, queue_data)
        except Exception as e:
            print(f"Error marking task complete: {e}")
            return False
    
    def has_pending_tasks(self) -> bool:
        """Check if there are pending tasks."""
        try:
            queue_data = self.state_manager.read_state(self.queue_file)
            tasks = queue_data.get("tasks", [])
            return any(task.get("status") != "completed" for task in tasks)
        except Exception as e:
            print(f"Error checking pending tasks: {e}")
            return False


class AgentInvoker:
    """Handles invocation of Claude Code Task tool agents."""
    
    def __init__(self, state_manager: StateManager, agents_dir: str = "agents"):
        self.state_manager = state_manager
        self.agents_dir = Path(agents_dir)
        
    def load_agent_instructions(self, agent_name: str) -> str:
        """Load agent instruction template from file."""
        try:
            agent_file = self.agents_dir / f"{agent_name}.md"
            if not agent_file.exists():
                raise FileNotFoundError(f"Agent instructions not found: {agent_file}")
            
            with open(agent_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading agent instructions for {agent_name}: {e}")
            return ""
    
    def prepare_agent_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for agent invocation."""
        return {
            "current_task": task,
            "execution_history": self.state_manager.read_state("execution_history.json"),
            "task_queue": self.state_manager.read_state("task_queue.json"),
            "working_directory": os.getcwd()
        }
    
    def invoke_executor(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke executor agent via Task tool (Phase 2 implementation)."""
        try:
            # For Phase 2, we'll simulate the Task tool invocation
            # In a real implementation, this would use the Claude Code SDK
            
            print(f"[AGENT] Invoking executor agent for task: {task.get('id')}")
            
            # Load agent instructions
            instructions = self.load_agent_instructions("executor_agent")
            if not instructions:
                return {
                    "status": "failure",
                    "error": "Could not load executor agent instructions"
                }
            
            # Prepare context
            context = self.prepare_agent_context(task)
            
            # Write current task to state for agent access
            self.state_manager.write_state("current_task.json", task)
            
            # Simulate agent execution (Phase 2 - will be replaced with actual Task tool call)
            execution_result = self._simulate_executor_agent(task, instructions, context)
            
            return execution_result
            
        except Exception as e:
            print(f"Error invoking executor agent: {e}")
            return {
                "status": "failure",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _simulate_executor_agent(self, task: Dict[str, Any], instructions: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate executor agent behavior for Phase 2 testing."""
        # Determine if task is atomic or parent
        has_subtasks = bool(task.get("subtasks") or task.get("children"))
        
        if has_subtasks:
            # Parent task - orchestrate subtasks
            return {
                "task_id": task.get("id"),
                "execution_type": "parent",
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "actions_taken": [
                    {
                        "action": "subtask_orchestration",
                        "description": "Analyzed parent task and prepared subtask execution plan"
                    }
                ],
                "results": {
                    "subtasks_created": 0,  # Would be populated by real agent
                    "orchestration_complete": True
                },
                "notes": "Phase 2 simulation: Parent task orchestration completed",
                "agent_instructions_used": bool(instructions)
            }
        else:
            # Atomic task - direct execution
            return {
                "task_id": task.get("id"),
                "execution_type": "atomic",
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "actions_taken": [
                    {
                        "action": "task_execution",
                        "target": "simulated_environment",
                        "description": "Executed atomic task according to acceptance criteria"
                    }
                ],
                "results": {
                    "files_created": [],
                    "files_modified": [],
                    "commands_executed": [],
                    "tests_passed": True
                },
                "notes": "Phase 2 simulation: Atomic task execution completed successfully",
                "agent_instructions_used": bool(instructions)
            }


class TEFOrchestrator:
    """Main orchestrator that implements the Act->Assess->Adapt loop."""
    
    def __init__(self, state_dir: str = "state", max_iterations: int = 10):
        self.state_manager = StateManager(state_dir)
        self.task_queue = TaskQueue(self.state_manager)
        self.agent_invoker = AgentInvoker(self.state_manager)
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create run directory
        self.run_dir = Path("runs") / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
    def load_task_from_file(self, task_file: str) -> bool:
        """Load task specification from markdown file."""
        try:
            task_path = Path(task_file)
            if not task_path.exists():
                print(f"Task file not found: {task_file}")
                return False
            
            with open(task_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter if present
            task_data = {
                "id": task_path.stem,
                "title": f"Task from {task_path.name}",
                "content": content,
                "source_file": str(task_path),
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            # Add to queue
            return self.task_queue.add_task(task_data)
            
        except Exception as e:
            print(f"Error loading task file: {e}")
            return False
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task (Act phase - enhanced for Phase 2)."""
        print(f"[ACT] Executing task: {task.get('title', 'Unknown')}")
        
        # Phase 2: Use agent invoker to execute via executor agent
        execution_result = self.agent_invoker.invoke_executor(task)
        
        # Process and enhance the result
        enhanced_result = {
            **execution_result,
            "orchestrator_metadata": {
                "run_id": self.run_id,
                "iteration": self.current_iteration,
                "phase": "Phase 2 - Executor Agent Implementation"
            }
        }
        
        # Write to execution history
        history = self.state_manager.read_state("execution_history.json")
        if "executions" not in history:
            history["executions"] = []
        history["executions"].append(enhanced_result)
        self.state_manager.write_state("execution_history.json", history)
        
        return enhanced_result
    
    def assess_execution(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess execution results (Assess phase - simplified for Phase 1)."""
        print(f"[ASSESS] Assessing execution result")
        
        # For Phase 1, we'll just simulate assessment
        # In Phase 3, this will invoke multiple observer agents
        assessment = {
            "execution_id": execution_result.get("task_id"),
            "overall_status": "pass",
            "observations": [
                {
                    "observer": "build_observer",
                    "status": "pass",
                    "message": "Task executed without errors",
                    "simulated": True
                }
            ],
            "assessed_at": datetime.now().isoformat()
        }
        
        # Write observations
        self.state_manager.write_state("observations.json", assessment)
        
        return assessment
    
    def adapt_plan(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt plan based on assessment (Adapt phase - simplified for Phase 1)."""
        print(f"[ADAPT] Adapting plan based on assessment")
        
        # For Phase 1, we'll just simulate adaptation
        # In Phase 4, this will invoke the navigator agent
        decision = {
            "assessment_id": assessment.get("execution_id"),
            "decision": "continue",
            "reasoning": "Task completed successfully, proceeding to next task",
            "plan_updates": [],
            "decided_at": datetime.now().isoformat(),
            "simulated": True
        }
        
        # Write decision
        self.state_manager.write_state("plan_updates.json", decision)
        
        return decision
    
    def run_main_loop(self) -> bool:
        """Run the main Act->Assess->Adapt loop."""
        print(f"Starting TEF Orchestrator (Run ID: {self.run_id})")
        print(f"Max iterations: {self.max_iterations}")
        
        try:
            while self.current_iteration < self.max_iterations:
                self.current_iteration += 1
                print(f"\n--- Iteration {self.current_iteration} ---")
                
                # Check if there are tasks to execute
                if not self.task_queue.has_pending_tasks():
                    print("No pending tasks found. Execution complete.")
                    break
                
                # Get next task
                current_task = self.task_queue.get_next_task()
                if not current_task:
                    print("No tasks available. Execution complete.")
                    break
                
                print(f"Processing task: {current_task.get('id')} - {current_task.get('title')}")
                
                # Act: Execute the task
                execution_result = self.execute_task(current_task)
                
                # Assess: Evaluate the execution
                assessment = self.assess_execution(execution_result)
                
                # Adapt: Decide next action
                decision = self.adapt_plan(assessment)
                
                # Mark task as completed if successful
                if decision.get("decision") == "continue":
                    self.task_queue.mark_complete(current_task.get("id"))
                    print(f"Task {current_task.get('id')} marked as completed")
                
                print(f"Iteration {self.current_iteration} completed")
            
            if self.current_iteration >= self.max_iterations:
                print(f"Reached maximum iterations ({self.max_iterations})")
            
            print(f"\nOrchestrator completed after {self.current_iteration} iterations")
            return True
            
        except KeyboardInterrupt:
            print("\nOrchestrator interrupted by user")
            return False
        except Exception as e:
            print(f"Error in main loop: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Task Execution Framework - Natural Language Prototype"
    )
    parser.add_argument(
        "--task", 
        required=True, 
        help="Path to task specification file"
    )
    parser.add_argument(
        "--state-dir", 
        default="state", 
        help="Directory for state files (default: state)"
    )
    parser.add_argument(
        "--max-iterations", 
        type=int, 
        default=10, 
        help="Maximum number of iterations (default: 10)"
    )
    parser.add_argument(
        "--clear-state", 
        action="store_true", 
        help="Clear all state files before starting"
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = TEFOrchestrator(
        state_dir=args.state_dir,
        max_iterations=args.max_iterations
    )
    
    # Clear state if requested
    if args.clear_state:
        print("Clearing previous state...")
        orchestrator.state_manager.clear_state()
    
    # Load task file
    if not orchestrator.load_task_from_file(args.task):
        print("Failed to load task file. Exiting.")
        sys.exit(1)
    
    print(f"Loaded task from: {args.task}")
    
    # Run orchestrator
    success = orchestrator.run_main_loop()
    
    if success:
        print("\nOrchestrator completed successfully!")
        sys.exit(0)
    else:
        print("\nOrchestrator failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()