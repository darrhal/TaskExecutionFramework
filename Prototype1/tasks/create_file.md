---
id: create-file-001
title: Create simple Python file
type: atomic
source: user
constraints:
  - Must create a valid Python file
  - Should include basic error handling
  - File must be executable
acceptance:
  - File is created at specified location
  - Python syntax is valid
  - File contains the required functionality
  - File has appropriate comments
policy:
  max_attempts: 3
  max_depth: 1
---

# Create Simple Python File Task

This task demonstrates atomic task execution by creating a simple Python file with basic functionality.

## Objective

Create a Python file at `examples/hello_calculator.py` that:

1. **Implements a simple calculator** with add, subtract, multiply, divide functions
2. **Includes error handling** for division by zero
3. **Has a main function** that demonstrates the calculator
4. **Contains proper documentation** with docstrings
5. **Is executable** as a standalone script

## Technical Requirements

### File Location
- Path: `examples/hello_calculator.py`
- Must be created relative to the current working directory

### Functionality
```python
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract second number from first."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide first number by second, with error handling."""
    # Handle division by zero
    pass

def main():
    """Demonstrate calculator functionality."""
    # Show examples of each operation
    pass

if __name__ == "__main__":
    main()
```

### Code Quality Requirements
- Include docstrings for all functions
- Handle division by zero gracefully
- Use meaningful variable names
- Include comments explaining complex logic
- Follow PEP 8 style guidelines

## Success Criteria

The task is successful when:
- [x] File `examples/hello_calculator.py` exists
- [x] File contains all required functions (add, subtract, multiply, divide)
- [x] Division function handles zero-division error
- [x] Main function demonstrates all operations
- [x] All functions have docstrings
- [x] File is syntactically valid Python
- [x] File runs without errors when executed

## Expected Agent Behavior

The executor agent should:
1. **Read this task specification** from `state/current_task.json`
2. **Understand the requirements** and acceptance criteria
3. **Create the directory** if it doesn't exist
4. **Write the Python file** with all required functionality
5. **Test the file** to ensure it works correctly
6. **Document the execution** in the execution history

This task validates that the executor agent can:
- Handle file creation operations
- Generate syntactically correct code
- Follow detailed specifications
- Implement error handling
- Write comprehensive execution records