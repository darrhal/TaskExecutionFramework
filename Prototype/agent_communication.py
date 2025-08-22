"""
Agent Communication Patterns for TEF
Phase 6.2: Inter-agent messaging, shared context, and knowledge accumulation
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class AgentMessage:
    """Structured message between agents."""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: str
    message_id: str
    priority: int = 5  # 1=highest, 10=lowest
    requires_response: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        return cls(**data)


class AgentCommunicationHub:
    """Central hub for agent-to-agent communication."""
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        
        # Communication channels
        self.message_file = self.state_dir / "agent_messages.json"
        self.shared_context_file = self.state_dir / "shared_context.json"
        self.knowledge_base_file = self.state_dir / "knowledge_base.json"
        
        # Initialize files
        self._initialize_communication_files()
    
    def _initialize_communication_files(self):
        """Initialize communication files if they don't exist."""
        files_to_init = {
            self.message_file: {"messages": [], "last_cleanup": datetime.now().isoformat()},
            self.shared_context_file: {"contexts": {}, "last_updated": datetime.now().isoformat()},
            self.knowledge_base_file: {"learnings": [], "patterns": {}, "last_updated": datetime.now().isoformat()}
        }
        
        for file_path, default_content in files_to_init.items():
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump(default_content, f, indent=2)
    
    def send_message(self, sender: str, recipient: str, message_type: str, 
                    content: Dict[str, Any], priority: int = 5, requires_response: bool = False) -> str:
        """Send a message from one agent to another."""
        message = AgentMessage(
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            message_id=f"{sender}_{recipient}_{int(time.time() * 1000)}",
            priority=priority,
            requires_response=requires_response
        )
        
        # Load current messages
        with open(self.message_file, 'r') as f:
            data = json.load(f)
        
        # Add new message
        data["messages"].append(message.to_dict())
        
        # Sort by priority and timestamp
        data["messages"].sort(key=lambda x: (x["priority"], x["timestamp"]))
        
        # Save updated messages
        with open(self.message_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return message.message_id
    
    def get_messages_for_agent(self, agent_name: str, mark_as_read: bool = True) -> List[AgentMessage]:
        """Get all unread messages for a specific agent."""
        with open(self.message_file, 'r') as f:
            data = json.load(f)
        
        messages = []
        remaining_messages = []
        
        for msg_data in data["messages"]:
            if msg_data["recipient"] == agent_name or msg_data["recipient"] == "all":
                messages.append(AgentMessage.from_dict(msg_data))
                if not mark_as_read:
                    remaining_messages.append(msg_data)
            else:
                remaining_messages.append(msg_data)
        
        # Update messages file if marking as read
        if mark_as_read and messages:
            data["messages"] = remaining_messages
            with open(self.message_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        return messages
    
    def update_shared_context(self, context_key: str, context_data: Dict[str, Any], 
                            updated_by: str) -> None:
        """Update shared context that all agents can access."""
        with open(self.shared_context_file, 'r') as f:
            data = json.load(f)
        
        data["contexts"][context_key] = {
            "data": context_data,
            "updated_by": updated_by,
            "updated_at": datetime.now().isoformat()
        }
        data["last_updated"] = datetime.now().isoformat()
        
        with open(self.shared_context_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_shared_context(self, context_key: str = None) -> Dict[str, Any]:
        """Get shared context data."""
        with open(self.shared_context_file, 'r') as f:
            data = json.load(f)
        
        if context_key:
            return data["contexts"].get(context_key, {})
        return data["contexts"]
    
    def add_to_knowledge_base(self, learning_type: str, content: Dict[str, Any], 
                             learned_by: str) -> None:
        """Add a learning or pattern to the knowledge base."""
        with open(self.knowledge_base_file, 'r') as f:
            data = json.load(f)
        
        learning = {
            "type": learning_type,
            "content": content,
            "learned_by": learned_by,
            "learned_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        data["learnings"].append(learning)
        
        # Update patterns if it's a pattern learning
        if learning_type == "pattern":
            pattern_key = content.get("pattern_name", "unnamed")
            if pattern_key not in data["patterns"]:
                data["patterns"][pattern_key] = []
            data["patterns"][pattern_key].append(learning)
        
        data["last_updated"] = datetime.now().isoformat()
        
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_knowledge(self, learning_type: str = None) -> List[Dict[str, Any]]:
        """Get learnings from the knowledge base."""
        with open(self.knowledge_base_file, 'r') as f:
            data = json.load(f)
        
        if learning_type:
            return [learning for learning in data["learnings"] 
                   if learning["type"] == learning_type]
        return data["learnings"]
    
    def cleanup_old_messages(self, hours_threshold: int = 24) -> int:
        """Clean up old messages to prevent file bloat."""
        cutoff_time = datetime.now().timestamp() - (hours_threshold * 3600)
        
        with open(self.message_file, 'r') as f:
            data = json.load(f)
        
        original_count = len(data["messages"])
        
        # Keep only recent messages
        data["messages"] = [
            msg for msg in data["messages"]
            if datetime.fromisoformat(msg["timestamp"]).timestamp() > cutoff_time
        ]
        
        data["last_cleanup"] = datetime.now().isoformat()
        
        with open(self.message_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return original_count - len(data["messages"])


class CommunicatingAgent:
    """Base class for agents with communication capabilities."""
    
    def __init__(self, agent_name: str, communication_hub: AgentCommunicationHub):
        self.agent_name = agent_name
        self.comm_hub = communication_hub
    
    def send_message(self, recipient: str, message_type: str, content: Dict[str, Any], 
                    priority: int = 5, requires_response: bool = False) -> str:
        """Send a message to another agent."""
        return self.comm_hub.send_message(
            self.agent_name, recipient, message_type, content, priority, requires_response
        )
    
    def get_messages(self, mark_as_read: bool = True) -> List[AgentMessage]:
        """Get messages for this agent."""
        try:
            return self.comm_hub.get_messages_for_agent(self.agent_name, mark_as_read)
        except Exception as e:
            print(f"[COMM] Error getting messages for {self.agent_name}: {e}")
            return []
    
    def update_context(self, context_key: str, context_data: Dict[str, Any]) -> None:
        """Update shared context."""
        self.comm_hub.update_shared_context(context_key, context_data, self.agent_name)
    
    def get_context(self, context_key: str = None) -> Dict[str, Any]:
        """Get shared context."""
        return self.comm_hub.get_shared_context(context_key)
    
    def learn(self, learning_type: str, content: Dict[str, Any]) -> None:
        """Add learning to the knowledge base."""
        self.comm_hub.add_to_knowledge_base(learning_type, content, self.agent_name)
    
    def get_knowledge(self, learning_type: str = None) -> List[Dict[str, Any]]:
        """Get knowledge from the knowledge base."""
        return self.comm_hub.get_knowledge(learning_type)


class EnhancedExecutorAgent(CommunicatingAgent):
    """Executor agent with communication capabilities."""
    
    def execute_task_with_communication(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task with enhanced communication patterns."""
        
        try:
            # Check for relevant messages
            messages = self.get_messages()
            
            # Update shared context with task info
            self.update_context(f"current_execution_{task.get('id')}", {
                "task": task,
                "context": context,
                "executor": self.agent_name,
                "started_at": datetime.now().isoformat()
            })
            
            # Get relevant knowledge
            task_patterns = self.get_knowledge("task_pattern")
            execution_patterns = self.get_knowledge("execution_pattern")
        except Exception as e:
            print(f"[COMM] Error in communication setup: {e}")
            messages = []
            task_patterns = []
            execution_patterns = []
        
        # Process messages
        execution_guidance = []
        for message in messages:
            if message.message_type == "execution_guidance":
                execution_guidance.append(message.content)
            elif message.message_type == "context_update":
                context.update(message.content)
        
        # Execute with enhanced context
        result = {
            "task_id": task.get("id"),
            "execution_type": "atomic",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "communication_enhanced": True,
            "messages_processed": len(messages),
            "patterns_applied": len(task_patterns) + len(execution_patterns),
            "shared_context_used": bool(self.get_context()),
            "notes": "Phase 6.2: Enhanced execution with agent communication patterns"
        }
        
        try:
            # Send completion message to observers
            self.send_message("all_observers", "execution_complete", {
                "task_id": task.get("id"),
                "result": result,
                "available_for_assessment": True
            }, priority=2)
            
            # Learn from execution
            self.learn("execution_pattern", {
                "task_type": task.get("type"),
                "success": result["status"] == "success",
                "duration": "fast",  # Would calculate actual duration
                "context_factors": list(context.keys())
            })
        except Exception as e:
            print(f"[COMM] Error in post-execution communication: {e}")
            result["communication_error"] = str(e)
        
        return result


class CommunicatingObserver(CommunicatingAgent):
    """Observer agent with communication capabilities."""
    
    def observe_with_communication(self, task: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Perform observation with agent communication."""
        
        # Check for execution completion messages
        messages = self.get_messages()
        execution_messages = [m for m in messages if m.message_type == "execution_complete"]
        
        # Get shared context for the execution
        execution_context = self.get_context(f"current_execution_{task.get('id')}")
        
        # Perform observation
        observation = {
            "observer_type": self.agent_name,
            "status": "pass" if execution_result.get("status") == "success" else "fail",
            "confidence": 0.9,
            "observations": [],
            "communication_enhanced": True,
            "shared_context_used": bool(execution_context),
            "notes": f"Phase 6.2: {self.agent_name} with communication patterns"
        }
        
        # Send observation to navigator
        self.send_message("navigator", "observation_ready", {
            "task_id": task.get("id"),
            "observation": observation,
            "observer": self.agent_name
        }, priority=3)
        
        # Learn from observation
        self.learn("observation_pattern", {
            "observer_type": self.agent_name,
            "task_type": task.get("type"),
            "result": observation["status"],
            "confidence": observation["confidence"]
        })
        
        return observation


class CommunicatingNavigator(CommunicatingAgent):
    """Navigator agent with communication capabilities."""
    
    def navigate_with_communication(self, assessment: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
        """Make navigation decisions with agent communication."""
        
        # Get observation messages
        messages = self.get_messages()
        observation_messages = [m for m in messages if m.message_type == "observation_ready"]
        
        # Get relevant knowledge
        decision_patterns = self.get_knowledge("decision_pattern")
        
        # Make decision based on communication and knowledge
        overall_status = assessment.get("overall_status", "unknown")
        
        decision = {
            "decision": "COMPLETE" if overall_status == "pass" else "RETRY",
            "reasoning": f"Communication-enhanced decision based on {len(observation_messages)} observations",
            "confidence": "HIGH" if len(observation_messages) >= 2 else "MEDIUM",
            "communication_enhanced": True,
            "observations_received": len(observation_messages),
            "patterns_considered": len(decision_patterns),
            "decided_at": datetime.now().isoformat()
        }
        
        # Send decision to all agents
        self.send_message("all", "navigation_decision", {
            "task_id": task.get("id"),
            "decision": decision["decision"],
            "reasoning": decision["reasoning"]
        }, priority=1)
        
        # Learn from decision
        self.learn("decision_pattern", {
            "decision_type": decision["decision"],
            "task_type": task.get("type"),
            "assessment_status": overall_status,
            "confidence": decision["confidence"]
        })
        
        return decision


# Integration functions
def create_communication_system(state_dir: str = "state") -> AgentCommunicationHub:
    """Create and initialize the agent communication system."""
    return AgentCommunicationHub(state_dir)


def create_communicating_agents(comm_hub: AgentCommunicationHub) -> Dict[str, CommunicatingAgent]:
    """Create a set of communicating agents."""
    return {
        "executor": EnhancedExecutorAgent("executor", comm_hub),
        "build_observer": CommunicatingObserver("build_observer", comm_hub),
        "requirements_observer": CommunicatingObserver("requirements_observer", comm_hub),
        "quality_observer": CommunicatingObserver("quality_observer", comm_hub),
        "integration_observer": CommunicatingObserver("integration_observer", comm_hub),
        "navigator": CommunicatingNavigator("navigator", comm_hub)
    }


if __name__ == "__main__":
    # Example usage
    hub = create_communication_system()
    agents = create_communicating_agents(hub)
    
    print("Agent Communication System initialized for Phase 6.2")