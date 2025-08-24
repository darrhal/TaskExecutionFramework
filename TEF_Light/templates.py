"""
Prompt template system for TEF Light.

Implements Anthropic's recommended template patterns with variables and XML tags
for structured, maintainable prompt generation.
"""

from string import Template
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class PromptTemplate:
    """A prompt template with variable substitution support."""
    
    template: str
    
    def render(self, **variables: Any) -> str:
        """
        Render template with variables using Anthropic's recommended patterns.
        
        Complex variables (dicts, lists, long strings) are wrapped in XML tags.
        Simple variables are substituted inline.
        """
        formatted_vars = {}
        
        for key, value in variables.items():
            if self._is_complex_variable(value):
                # Wrap complex variables in XML tags as recommended by Anthropic
                formatted_vars[key] = f"<{key}>\n{value}\n</{key}>"
            else:
                formatted_vars[key] = str(value)
        
        return Template(self.template).safe_substitute(**formatted_vars)
    
    def _is_complex_variable(self, value: Any) -> bool:
        """Determine if a variable should be wrapped in XML tags."""
        if isinstance(value, (dict, list)):
            return True
        
        str_value = str(value)
        # Consider strings longer than 50 chars or with newlines as complex
        return len(str_value) > 50 or '\n' in str_value


class TemplateManager:
    """Manages loading, caching, and rendering of prompt templates."""
    
    def __init__(self, template_dir: str = "prompt-templates"):
        self.template_dir = Path(template_dir)
        self._cache: Dict[str, PromptTemplate] = {}
    
    def load_template(self, name: str) -> PromptTemplate:
        """Load and cache template from file."""
        if name not in self._cache:
            template_path = self.template_dir / f"{name}.md"
            
            if not template_path.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                self._cache[name] = PromptTemplate(f.read())
        
        return self._cache[name]
    
    def render(self, template_name: str, **variables: Any) -> str:
        """Render a template with variables."""
        template = self.load_template(template_name)
        return template.render(**variables)
    
    def clear_cache(self) -> None:
        """Clear template cache (useful for development/testing)."""
        self._cache.clear()
    
    def template_exists(self, name: str) -> bool:
        """Check if a template file exists."""
        template_path = self.template_dir / f"{name}.md"
        return template_path.exists()


# Global template manager instance
template_manager = TemplateManager()