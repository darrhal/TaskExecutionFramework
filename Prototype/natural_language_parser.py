"""
Natural Language Task Specification Parser for TEF
Phase 6.4: Enable natural language task specifications
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TaskSpecification:
    """Structured task specification extracted from natural language."""
    id: str
    title: str
    description: str
    type: str  # 'atomic' or 'parent'
    requirements: List[str]
    acceptance_criteria: List[str]
    constraints: List[str]
    context: Dict[str, Any]
    priority: int
    estimated_effort: str
    dependencies: List[str]
    source: str = "natural_language"


class NaturalLanguageTaskParser:
    """Parse natural language task descriptions into structured specifications."""
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = Path(state_dir)
        self.parsing_patterns = self._load_parsing_patterns()
        self.context_keywords = self._load_context_keywords()
        
    def _load_parsing_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for extracting different task elements."""
        return {
            "goal_indicators": [
                r"(?:I want to|I need to|Please|Could you|Help me|Create|Build|Implement|Fix|Update|Add|Remove)",
                r"(?:The goal is to|The objective is|The purpose is|We need to|Let's|Should)",
                r"(?:Make sure|Ensure that|Verify that|Check that|Confirm that)"
            ],
            "requirement_indicators": [
                r"(?:must|should|shall|needs? to|has to|requires?|expects?)",
                r"(?:it is (?:important|crucial|essential|necessary) (?:that|to))",
                r"(?:the system (?:must|should|needs to))"
            ],
            "constraint_indicators": [
                r"(?:cannot|must not|should not|don't|avoid|exclude|without|except)",
                r"(?:within|before|after|by|deadline|timeout|limit)",
                r"(?:budget|cost|resource|memory|performance|security)"
            ],
            "acceptance_indicators": [
                r"(?:success (?:criteria|conditions?)|acceptance (?:criteria|conditions?))",
                r"(?:when (?:complete|done|finished)|should (?:result in|produce|generate))",
                r"(?:verify|test|check|confirm) (?:that|by|with)"
            ],
            "complexity_indicators": [
                r"(?:simple|basic|straightforward|easy|quick|fast)",
                r"(?:complex|complicated|advanced|sophisticated|comprehensive)",
                r"(?:step-by-step|multiple (?:steps|phases)|breakdown|decompose)"
            ],
            "priority_indicators": [
                r"(?:urgent|asap|immediately|right away|high priority|critical)",
                r"(?:when (?:you have time|convenient)|low priority|nice to have|optional)",
                r"(?:medium priority|normal|standard|regular)"
            ]
        }
    
    def _load_context_keywords(self) -> Dict[str, List[str]]:
        """Load keywords that provide context about task domain."""
        return {
            "development": ["code", "programming", "software", "application", "system", "build", "compile", "test", "debug"],
            "documentation": ["document", "docs", "readme", "guide", "manual", "instructions", "explain", "describe"],
            "data": ["data", "database", "csv", "json", "xml", "import", "export", "process", "analyze"],
            "deployment": ["deploy", "production", "server", "cloud", "kubernetes", "docker", "container"],
            "configuration": ["config", "settings", "environment", "variables", "parameters", "options"],
            "testing": ["test", "verify", "validate", "check", "ensure", "confirm", "quality"],
            "security": ["security", "authentication", "authorization", "permissions", "access", "encrypt"],
            "maintenance": ["fix", "bug", "error", "issue", "problem", "update", "upgrade", "patch"]
        }
    
    def parse_natural_language_task(self, text: str, task_id: Optional[str] = None) -> TaskSpecification:
        """Parse natural language text into a structured task specification."""
        
        # Generate task ID if not provided
        if not task_id:
            task_id = self._generate_task_id(text)
        
        # Extract basic information
        title = self._extract_title(text)
        description = self._clean_description(text)
        
        # Analyze task characteristics
        task_type = self._determine_task_type(text)
        requirements = self._extract_requirements(text)
        acceptance_criteria = self._extract_acceptance_criteria(text)
        constraints = self._extract_constraints(text)
        
        # Determine context and metadata
        context = self._extract_context(text)
        priority = self._determine_priority(text)
        estimated_effort = self._estimate_effort(text)
        dependencies = self._extract_dependencies(text)
        
        return TaskSpecification(
            id=task_id,
            title=title,
            description=description,
            type=task_type,
            requirements=requirements,
            acceptance_criteria=acceptance_criteria,
            constraints=constraints,
            context=context,
            priority=priority,
            estimated_effort=estimated_effort,
            dependencies=dependencies
        )
    
    def _generate_task_id(self, text: str) -> str:
        """Generate a task ID from the text content."""
        # Extract key words and create a meaningful ID
        words = re.findall(r'\w+', text.lower())
        key_words = [w for w in words[:5] if len(w) > 3]  # Take first 5 meaningful words
        
        if not key_words:
            key_words = ["task"]
        
        base_id = "-".join(key_words[:3])  # Use up to 3 words
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        
        return f"nl-{base_id}-{timestamp}"
    
    def _extract_title(self, text: str) -> str:
        """Extract a concise title from the task description."""
        # Try to find the main action/goal in the first sentence
        sentences = re.split(r'[.!?]+', text.strip())
        first_sentence = sentences[0].strip() if sentences else text.strip()
        
        # Clean up and truncate
        title = re.sub(r'^(?:I want to|I need to|Please|Could you|Help me)\s+', '', first_sentence, flags=re.IGNORECASE)
        title = title.strip().capitalize()
        
        # Truncate if too long
        if len(title) > 80:
            title = title[:77] + "..."
        
        return title or "Natural Language Task"
    
    def _clean_description(self, text: str) -> str:
        """Clean and format the task description."""
        # Remove extra whitespace and normalize
        description = re.sub(r'\s+', ' ', text.strip())
        
        # Ensure proper capitalization
        if description and not description[0].isupper():
            description = description[0].upper() + description[1:]
        
        return description
    
    def _determine_task_type(self, text: str) -> str:
        """Determine if this is an atomic or parent task."""
        text_lower = text.lower()
        
        # Indicators of parent tasks (complex, multi-step)
        parent_indicators = [
            "step-by-step", "multiple steps", "several parts", "phases",
            "breakdown", "decompose", "first.*then", "after.*before",
            "complex", "comprehensive", "system", "project", "workflow"
        ]
        
        for indicator in parent_indicators:
            if re.search(indicator, text_lower):
                return "parent"
        
        # Check for multiple verbs/actions
        action_words = re.findall(r'\b(?:create|build|implement|fix|update|add|remove|test|deploy|configure|setup|install)\b', text_lower)
        if len(action_words) > 2:
            return "parent"
        
        return "atomic"
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract requirements from the text."""
        requirements = []
        
        # Look for explicit requirement patterns
        for pattern in self.parsing_patterns["requirement_indicators"]:
            matches = re.finditer(pattern + r'[^.!?]*[.!?]?', text, re.IGNORECASE)
            for match in matches:
                req = match.group().strip()
                if req and len(req) > 10:  # Filter out very short matches
                    requirements.append(req)
        
        # Extract bullet points as requirements
        bullet_points = re.findall(r'[-*]\s+([^-*\n]+)', text)
        requirements.extend([point.strip() for point in bullet_points if len(point.strip()) > 5])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_requirements = []
        for req in requirements:
            if req.lower() not in seen:
                seen.add(req.lower())
                unique_requirements.append(req)
        
        return unique_requirements[:10]  # Limit to 10 requirements
    
    def _extract_acceptance_criteria(self, text: str) -> List[str]:
        """Extract acceptance criteria from the text."""
        criteria = []
        
        # Look for explicit acceptance criteria patterns
        for pattern in self.parsing_patterns["acceptance_indicators"]:
            matches = re.finditer(pattern + r'[^.!?]*[.!?]?', text, re.IGNORECASE)
            for match in matches:
                criterion = match.group().strip()
                if criterion and len(criterion) > 10:
                    criteria.append(criterion)
        
        # Look for "should" statements as criteria
        should_statements = re.findall(r'(?:should|will|can)\s+[^.!?]*[.!?]?', text, re.IGNORECASE)
        criteria.extend([stmt.strip() for stmt in should_statements if len(stmt.strip()) > 10])
        
        # If no explicit criteria found, infer from goal
        if not criteria:
            goal_match = re.search(r'(?:goal|objective|purpose) is to ([^.!?]*)', text, re.IGNORECASE)
            if goal_match:
                criteria.append(f"Successfully achieve: {goal_match.group(1).strip()}")
        
        # Remove duplicates
        seen = set()
        unique_criteria = []
        for criterion in criteria:
            if criterion.lower() not in seen:
                seen.add(criterion.lower())
                unique_criteria.append(criterion)
        
        return unique_criteria[:5]  # Limit to 5 criteria
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract constraints from the text."""
        constraints = []
        
        # Look for explicit constraint patterns
        for pattern in self.parsing_patterns["constraint_indicators"]:
            matches = re.finditer(pattern + r'[^.!?]*[.!?]?', text, re.IGNORECASE)
            for match in matches:
                constraint = match.group().strip()
                if constraint and len(constraint) > 5:
                    constraints.append(constraint)
        
        # Look for time constraints
        time_patterns = [
            r'(?:within|by|before)\s+\d+\s+(?:hours?|days?|weeks?|minutes?)',
            r'deadline\s+(?:is|of)\s+[^.!?]*',
            r'(?:asap|immediately|urgent|quickly)'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            constraints.extend(matches)
        
        return constraints[:5]  # Limit to 5 constraints
    
    def _extract_context(self, text: str) -> Dict[str, Any]:
        """Extract contextual information about the task."""
        context = {
            "domains": [],
            "technologies": [],
            "environments": [],
            "extracted_entities": []
        }
        
        text_lower = text.lower()
        
        # Identify domains
        for domain, keywords in self.context_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                context["domains"].append(domain)
        
        # Extract technology mentions
        tech_patterns = [
            r'\b(?:python|javascript|java|react|node|docker|kubernetes|aws|azure|gcp)\b',
            r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch)\b',
            r'\b(?:git|github|gitlab|jenkins|ci/cd)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text_lower)
            context["technologies"].extend(matches)
        
        # Extract file/path mentions
        file_mentions = re.findall(r'\b\w+\.(?:py|js|json|yaml|yml|md|txt|csv)\b', text)
        context["extracted_entities"].extend(file_mentions)
        
        # Remove duplicates
        for key in context:
            if isinstance(context[key], list):
                context[key] = list(set(context[key]))
        
        return context
    
    def _determine_priority(self, text: str) -> int:
        """Determine task priority from the text (1=highest, 10=lowest)."""
        text_lower = text.lower()
        
        # High priority indicators
        high_priority_words = ["urgent", "asap", "immediately", "critical", "important", "high priority"]
        if any(word in text_lower for word in high_priority_words):
            return 2
        
        # Low priority indicators
        low_priority_words = ["when convenient", "low priority", "nice to have", "optional", "eventually"]
        if any(word in text_lower for word in low_priority_words):
            return 8
        
        # Default to medium priority
        return 5
    
    def _estimate_effort(self, text: str) -> str:
        """Estimate effort required for the task."""
        text_lower = text.lower()
        
        # Simple/quick indicators
        simple_words = ["simple", "quick", "fast", "easy", "straightforward", "basic"]
        if any(word in text_lower for word in simple_words):
            return "low"
        
        # Complex indicators
        complex_words = ["complex", "comprehensive", "advanced", "sophisticated", "detailed", "thorough"]
        if any(word in text_lower for word in complex_words):
            return "high"
        
        # Multi-step indicators
        if re.search(r'(?:step|phase|part).*(?:step|phase|part)', text_lower):
            return "high"
        
        # Check text length as an indicator
        if len(text) > 500:
            return "medium"
        elif len(text) < 100:
            return "low"
        
        return "medium"
    
    def _extract_dependencies(self, text: str) -> List[str]:
        """Extract task dependencies from the text."""
        dependencies = []
        
        # Look for dependency patterns
        dependency_patterns = [
            r'(?:after|once|when)\s+([^,\.!?]+)(?:\s+(?:is|are)\s+(?:complete|done|finished))?',
            r'(?:depends on|requires|needs)\s+([^,\.!?]+)',
            r'(?:first|before)\s+([^,\.!?]+)'
        ]
        
        for pattern in dependency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                dep = match.strip()
                if len(dep) > 5 and len(dep) < 100:  # Reasonable length
                    dependencies.append(dep)
        
        return dependencies[:3]  # Limit to 3 dependencies
    
    def convert_to_yaml_format(self, task_spec: TaskSpecification) -> str:
        """Convert the task specification to YAML format for compatibility."""
        yaml_content = f"""---
id: {task_spec.id}
title: {task_spec.title}
type: {task_spec.type}
source: {task_spec.source}
"""
        
        if task_spec.constraints:
            yaml_content += "constraints:\n"
            for constraint in task_spec.constraints:
                yaml_content += f"  - {constraint}\n"
        
        if task_spec.acceptance_criteria:
            yaml_content += "acceptance:\n"
            for criterion in task_spec.acceptance_criteria:
                yaml_content += f"  - {criterion}\n"
        
        yaml_content += f"""policy:
  max_attempts: 3
  max_depth: 3
  timeout_seconds: 300
priority: {task_spec.priority}
estimated_effort: {task_spec.estimated_effort}
---

# {task_spec.title}

{task_spec.description}

## Requirements

"""
        
        for req in task_spec.requirements:
            yaml_content += f"- {req}\n"
        
        if task_spec.context.get("domains"):
            yaml_content += f"\n## Identified Domains\n\n"
            for domain in task_spec.context["domains"]:
                yaml_content += f"- {domain}\n"
        
        if task_spec.context.get("technologies"):
            yaml_content += f"\n## Technologies Mentioned\n\n"
            for tech in task_spec.context["technologies"]:
                yaml_content += f"- {tech}\n"
        
        if task_spec.dependencies:
            yaml_content += f"\n## Dependencies\n\n"
            for dep in task_spec.dependencies:
                yaml_content += f"- {dep}\n"
        
        return yaml_content
    
    def save_parsed_task(self, task_spec: TaskSpecification, tasks_dir: str = "tasks") -> str:
        """Save the parsed task specification to a file."""
        tasks_path = Path(tasks_dir)
        tasks_path.mkdir(exist_ok=True)
        
        # Generate filename
        filename = f"{task_spec.id}.md"
        file_path = tasks_path / filename
        
        # Convert to YAML format
        yaml_content = self.convert_to_yaml_format(task_spec)
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        return str(file_path)


class NaturalLanguageTaskEngine:
    """Engine for processing natural language task inputs."""
    
    def __init__(self, state_dir: str = "state", tasks_dir: str = "tasks"):
        self.parser = NaturalLanguageTaskParser(state_dir)
        self.state_dir = Path(state_dir)
        self.tasks_dir = Path(tasks_dir)
        self.tasks_dir.mkdir(exist_ok=True)
        
        # Initialize processing history
        self.processing_history_file = self.state_dir / "nl_processing_history.json"
        self._initialize_history()
    
    def _initialize_history(self):
        """Initialize the processing history file."""
        if not self.processing_history_file.exists():
            with open(self.processing_history_file, 'w') as f:
                json.dump({
                    "processed_tasks": [],
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
    
    def process_natural_language_input(self, text: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Process natural language input and create a task specification."""
        
        processing_result = {
            "input_text": text,
            "processing_timestamp": datetime.now().isoformat(),
            "status": "processing"
        }
        
        try:
            # Parse the natural language input
            task_spec = self.parser.parse_natural_language_task(text, task_id)
            
            # Save the task specification
            task_file_path = self.parser.save_parsed_task(task_spec, str(self.tasks_dir))
            
            # Update processing result
            processing_result.update({
                "status": "success",
                "task_specification": {
                    "id": task_spec.id,
                    "title": task_spec.title,
                    "type": task_spec.type,
                    "requirements_count": len(task_spec.requirements),
                    "acceptance_criteria_count": len(task_spec.acceptance_criteria),
                    "constraints_count": len(task_spec.constraints),
                    "priority": task_spec.priority,
                    "estimated_effort": task_spec.estimated_effort,
                    "identified_domains": task_spec.context.get("domains", []),
                    "technologies": task_spec.context.get("technologies", [])
                },
                "task_file_path": task_file_path,
                "parsing_insights": self._generate_parsing_insights(task_spec, text)
            })
            
            # Record in history
            self._record_processing(processing_result)
            
        except Exception as e:
            processing_result.update({
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            })
        
        return processing_result
    
    def _generate_parsing_insights(self, task_spec: TaskSpecification, original_text: str) -> Dict[str, Any]:
        """Generate insights about the parsing process."""
        return {
            "text_complexity": "high" if len(original_text) > 500 else "medium" if len(original_text) > 200 else "low",
            "ambiguity_indicators": self._detect_ambiguity(original_text),
            "confidence_score": self._calculate_confidence(task_spec, original_text),
            "suggested_clarifications": self._suggest_clarifications(task_spec, original_text)
        }
    
    def _detect_ambiguity(self, text: str) -> List[str]:
        """Detect potential ambiguities in the natural language input."""
        ambiguities = []
        
        # Check for vague language
        vague_words = ["somehow", "maybe", "perhaps", "probably", "something", "anything", "whatever"]
        if any(word in text.lower() for word in vague_words):
            ambiguities.append("Contains vague language that may need clarification")
        
        # Check for multiple interpretations
        if "or" in text.lower() and text.lower().count("or") > 2:
            ambiguities.append("Multiple options mentioned - may need prioritization")
        
        # Check for missing specifics
        if re.search(r'\b(?:some|many|few|several)\b', text, re.IGNORECASE):
            ambiguities.append("Quantitative details may need specification")
        
        return ambiguities
    
    def _calculate_confidence(self, task_spec: TaskSpecification, original_text: str) -> float:
        """Calculate confidence score for the parsing results."""
        score = 0.5  # Base score
        
        # Boost for clear requirements
        if len(task_spec.requirements) > 0:
            score += 0.2
        
        # Boost for acceptance criteria
        if len(task_spec.acceptance_criteria) > 0:
            score += 0.2
        
        # Boost for specific context
        if task_spec.context.get("domains") or task_spec.context.get("technologies"):
            score += 0.1
        
        # Penalty for very short or very long descriptions
        text_len = len(original_text)
        if text_len < 50:
            score -= 0.2
        elif text_len > 1000:
            score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    def _suggest_clarifications(self, task_spec: TaskSpecification, original_text: str) -> List[str]:
        """Suggest clarifications that might improve the task specification."""
        suggestions = []
        
        if not task_spec.acceptance_criteria:
            suggestions.append("Consider adding specific success criteria or expected outcomes")
        
        if task_spec.type == "parent" and not task_spec.requirements:
            suggestions.append("For complex tasks, consider breaking down into specific requirements")
        
        if not task_spec.constraints:
            suggestions.append("Consider specifying any time, resource, or technical constraints")
        
        if not task_spec.context.get("technologies") and "code" in original_text.lower():
            suggestions.append("Consider specifying programming languages or technologies to use")
        
        return suggestions
    
    def _record_processing(self, processing_result: Dict[str, Any]):
        """Record the processing result in history."""
        try:
            # Load existing history
            with open(self.processing_history_file, 'r') as f:
                history = json.load(f)
            
            # Add new processing record
            history["processed_tasks"].append(processing_result)
            history["last_updated"] = datetime.now().isoformat()
            
            # Keep only last 50 records
            if len(history["processed_tasks"]) > 50:
                history["processed_tasks"] = history["processed_tasks"][-50:]
            
            # Save updated history
            with open(self.processing_history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"[NL_PARSER] Error recording processing history: {e}")


# Integration functions
def process_natural_language_task(text: str, task_id: Optional[str] = None, 
                                tasks_dir: str = "tasks", state_dir: str = "state") -> Dict[str, Any]:
    """Process a natural language task description and create a task file."""
    engine = NaturalLanguageTaskEngine(state_dir, tasks_dir)
    return engine.process_natural_language_input(text, task_id)


def parse_and_save_nl_task(text: str, output_dir: str = "tasks") -> str:
    """Quick function to parse natural language and save as task file."""
    parser = NaturalLanguageTaskParser()
    task_spec = parser.parse_natural_language_task(text)
    return parser.save_parsed_task(task_spec, output_dir)


if __name__ == "__main__":
    # Example usage
    sample_text = """
    I need to create a web application that allows users to upload CSV files and visualize the data.
    The system should be able to handle files up to 10MB and support basic charts like bar graphs and line charts.
    Users must be able to filter and sort the data before creating visualizations.
    The application should be responsive and work on mobile devices.
    Please use React for the frontend and Python Flask for the backend.
    The project should be completed within 2 weeks.
    """
    
    result = process_natural_language_task(sample_text)
    print(f"Natural language processing result: {result.get('status')}")
    if result.get('task_file_path'):
        print(f"Task file created: {result['task_file_path']}")