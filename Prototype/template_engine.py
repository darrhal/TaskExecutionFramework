"""
Natural Language Template Engine for TEF
Phase 6.1: Advanced template features with variable substitution, conditionals, and context injection
"""

import re
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class NaturalLanguageTemplateEngine:
    """Advanced templating system for natural language agent instructions."""
    
    def __init__(self, base_path: str = "agents"):
        self.base_path = Path(base_path)
        self.variable_pattern = re.compile(r'\{\{([^}]+)\}\}')
        self.conditional_pattern = re.compile(r'\{% if (.+?) %\}(.*?)\{% endif %\}', re.DOTALL)
        self.loop_pattern = re.compile(r'\{% for (.+?) in (.+?) %\}(.*?)\{% endfor %\}', re.DOTALL)
        self.include_pattern = re.compile(r'\{% include "([^"]+)" %\}')
        
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with advanced features."""
        try:
            # Load base template
            template_content = self._load_template(template_name)
            
            # Process template in stages
            rendered = self._process_includes(template_content, context)
            rendered = self._process_conditionals(rendered, context)
            rendered = self._process_loops(rendered, context)
            rendered = self._process_variables(rendered, context)
            rendered = self._process_context_injection(rendered, context)
            
            return rendered.strip()
            
        except Exception as e:
            return f"Template rendering error: {str(e)}"
    
    def _load_template(self, template_name: str) -> str:
        """Load template from file."""
        template_path = self.base_path / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _process_includes(self, content: str, context: Dict[str, Any]) -> str:
        """Process include statements."""
        def replace_include(match):
            include_name = match.group(1)
            try:
                included_content = self._load_template(include_name)
                # Recursively process includes
                return self._process_includes(included_content, context)
            except Exception as e:
                return f"<!-- Include error: {str(e)} -->"
        
        return self.include_pattern.sub(replace_include, content)
    
    def _process_conditionals(self, content: str, context: Dict[str, Any]) -> str:
        """Process conditional blocks."""
        def replace_conditional(match):
            condition = match.group(1).strip()
            block_content = match.group(2)
            
            try:
                # Evaluate condition
                if self._evaluate_condition(condition, context):
                    return block_content
                else:
                    return ""
            except Exception as e:
                return f"<!-- Conditional error: {str(e)} -->"
        
        return self.conditional_pattern.sub(replace_conditional, content)
    
    def _process_loops(self, content: str, context: Dict[str, Any]) -> str:
        """Process loop constructs."""
        def replace_loop(match):
            var_name = match.group(1).strip()
            iterable_name = match.group(2).strip()
            loop_content = match.group(3)
            
            try:
                iterable = self._get_context_value(iterable_name, context)
                if not isinstance(iterable, (list, tuple)):
                    return f"<!-- Loop error: {iterable_name} is not iterable -->"
                
                result_parts = []
                for item in iterable:
                    # Create loop context
                    loop_context = {**context, var_name: item}
                    # Process loop content recursively
                    processed_content = self._process_variables(loop_content, loop_context)
                    result_parts.append(processed_content)
                
                return "\n".join(result_parts)
                
            except Exception as e:
                return f"<!-- Loop error: {str(e)} -->"
        
        return self.loop_pattern.sub(replace_loop, content)
    
    def _process_variables(self, content: str, context: Dict[str, Any]) -> str:
        """Process variable substitutions."""
        def replace_variable(match):
            var_path = match.group(1).strip()
            try:
                value = self._get_context_value(var_path, context)
                if value is None:
                    return f"<!-- Variable not found: {var_path} -->"
                return str(value)
            except Exception as e:
                return f"<!-- Variable error: {str(e)} -->"
        
        return self.variable_pattern.sub(replace_variable, content)
    
    def _process_context_injection(self, content: str, context: Dict[str, Any]) -> str:
        """Inject additional context information."""
        # Add common context injections
        injections = {
            "{{TIMESTAMP}}": context.get("timestamp", "unknown"),
            "{{TASK_ID}}": context.get("task", {}).get("id", "unknown"),
            "{{DEPTH}}": str(context.get("depth", 0)),
            "{{ITERATION}}": str(context.get("iteration", 1))
        }
        
        for pattern, value in injections.items():
            content = content.replace(pattern, value)
        
        return content
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a conditional expression."""
        # Simple condition evaluation
        # Supports: var_name, var_name == "value", var_name > 0, etc.
        
        condition = condition.strip()
        
        # Handle simple existence checks
        if " " not in condition:
            value = self._get_context_value(condition, context)
            return bool(value)
        
        # Handle comparisons
        operators = ["==", "!=", ">=", "<=", ">", "<"]
        for op in operators:
            if op in condition:
                left, right = condition.split(op, 1)
                left_val = self._get_context_value(left.strip(), context)
                right_val = self._parse_value(right.strip())
                
                if op == "==":
                    return left_val == right_val
                elif op == "!=":
                    return left_val != right_val
                elif op == ">":
                    return left_val > right_val
                elif op == "<":
                    return left_val < right_val
                elif op == ">=":
                    return left_val >= right_val
                elif op == "<=":
                    return left_val <= right_val
        
        # Default to False for unknown conditions
        return False
    
    def _get_context_value(self, path: str, context: Dict[str, Any]) -> Any:
        """Get a value from context using dot notation."""
        parts = path.split('.')
        current = context
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
            
            if current is None:
                return None
        
        return current
    
    def _parse_value(self, value_str: str) -> Any:
        """Parse a string value to appropriate type."""
        value_str = value_str.strip()
        
        # Remove quotes if present
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # Try to parse as number
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass
        
        # Try to parse as boolean
        if value_str.lower() in ('true', 'false'):
            return value_str.lower() == 'true'
        
        # Return as string
        return value_str
    
    def create_enhanced_template(self, template_name: str, base_content: str, 
                                enhancements: Dict[str, Any]) -> None:
        """Create an enhanced template with advanced features."""
        enhanced_content = base_content
        
        # Add conditional sections
        if 'conditionals' in enhancements:
            for condition, content in enhancements['conditionals'].items():
                enhanced_content += f"\n\n{{% if {condition} %}}\n{content}\n{{% endif %}}"
        
        # Add loops
        if 'loops' in enhancements:
            for var, iterable, content in enhancements['loops']:
                enhanced_content += f"\n\n{{% for {var} in {iterable} %}}\n{content}\n{{% endfor %}}"
        
        # Add includes
        if 'includes' in enhancements:
            for include in enhancements['includes']:
                enhanced_content += f"\n\n{{% include \"{include}\" %}}"
        
        # Write enhanced template
        template_path = self.base_path / f"{template_name}.md"
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)


# Integration with existing TEF system
class EnhancedAgentInvoker:
    """Enhanced agent invoker with advanced templating."""
    
    def __init__(self, state_manager, template_engine: NaturalLanguageTemplateEngine = None):
        self.state_manager = state_manager
        self.template_engine = template_engine or NaturalLanguageTemplateEngine()
    
    def invoke_enhanced_executor(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Invoke executor with enhanced templating."""
        try:
            # Prepare enhanced context
            enhanced_context = {
                "task": task,
                "timestamp": context.get("timestamp") if context else None,
                "depth": context.get("depth", 0) if context else 0,
                "iteration": context.get("iteration", 1) if context else 1,
                "state": {
                    "queue": self.state_manager.read_state("task_queue.json"),
                    "history": self.state_manager.read_state("execution_history.json")
                },
                "has_subtasks": bool(task.get("subtasks")),
                "is_parent": task.get("type") == "parent",
                "failure_simulation": task.get("simulate_failure", False)
            }
            
            # Render enhanced template
            instructions = self.template_engine.render_template("executor_agent_enhanced", enhanced_context)
            
            # For Phase 6, we would integrate with actual Task tool here
            # For now, simulate the enhanced execution
            return self._simulate_enhanced_execution(task, instructions, enhanced_context)
            
        except Exception as e:
            return {
                "status": "failure",
                "error": str(e),
                "timestamp": enhanced_context.get("timestamp", "unknown")
            }
    
    def _simulate_enhanced_execution(self, task: Dict[str, Any], instructions: str, 
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate enhanced execution with better context awareness."""
        task_id = task.get("id", "unknown")
        
        # Enhanced execution logic based on context
        if context.get("has_subtasks"):
            return {
                "task_id": task_id,
                "execution_type": "parent",
                "status": "success",
                "template_enhanced": True,
                "context_used": {
                    "depth": context.get("depth", 0),
                    "subtask_count": len(task.get("subtasks", [])),
                    "template_features": ["conditionals", "variables", "context_injection"]
                },
                "notes": f"Phase 6.1: Enhanced templating used for parent task orchestration",
                "timestamp": context.get("timestamp", "unknown")
            }
        else:
            return {
                "task_id": task_id,
                "execution_type": "atomic",
                "status": "success",
                "template_enhanced": True,
                "context_used": {
                    "depth": context.get("depth", 0),
                    "template_features": ["variables", "context_injection"]
                },
                "notes": f"Phase 6.1: Enhanced templating used for atomic task execution",
                "timestamp": context.get("timestamp", "unknown")
            }


if __name__ == "__main__":
    # Example usage
    engine = NaturalLanguageTemplateEngine()
    
    # Example context
    context = {
        "task": {
            "id": "example-task",
            "title": "Example Task",
            "type": "atomic"
        },
        "depth": 0,
        "iteration": 1,
        "has_subtasks": False
    }
    
    print("Natural Language Template Engine initialized for Phase 6.1")