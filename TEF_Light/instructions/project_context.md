# Project Context

## Technology Stack
- Python 3.10+
- Git for version control
- Command line interface

## Development Standards
- Use modern Python type hints (dict[str, Any] vs Dict[str, Any])
- Keep functions small and focused
- Write clear docstrings
- Handle errors gracefully

## Project Goals
- Build a minimal, working Task Execution Framework
- Demonstrate Act→Assess→Adapt cycle with real LLM agents
- Keep implementation under 250 lines of code
- Make the framework easily customizable

## Constraints
- No external databases or complex state management
- Everything stored in JSON task trees and git history
- Use only standard library + anthropic SDK
- Prioritize simplicity over features

## Domain Knowledge
This is a meta-programming project - we're building a framework that uses AI to build other software. The framework should be self-aware of this recursive nature and capable of improving itself if needed.