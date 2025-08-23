# TEF Light Structured Output Refactoring - Change Review

## 1) Quick Orientation

**Purpose**: Refactor TEF Light from unstructured Claude API calls returning plain text/JSON to guaranteed structured outputs using Pydantic models and Claude's tool-use feature.

**Main areas touched**: Split monolithic `tef_light.py` into three modules - `models.py` (Pydantic data models), `claude_client.py` (Claude API wrapper), and a cleaned `tef_light.py` (orchestration only).

**High-level flow**: JSON file → Pydantic TaskTree validation → Execute/Assess/Adapt cycle with typed models → Claude returns structured data via tool-use schemas → No more JSON parsing errors.

**Public contracts changed**: All functions now use typed Pydantic models (ExecutionResult, AssessmentResult, TaskNode) instead of dicts. Task tree loading validates structure on load.

**What to watch for**: Notice how Claude responses are now guaranteed to match expected schemas - no more try/except for JSON parsing.

## 2) Guided Reading Order

- [ ] **models.py** (new file, ~125 lines)
  - Defines Pydantic models for all data structures (ExecutionResult, AssessmentResult, TaskNode, TaskTree)
  - Models auto-generate JSON schemas for Claude's tool-use feature
  - Replaces TypedDict/raw dicts with validated, typed objects
  - Connects to: Used by both claude_client.py and tef_light.py for type safety
  - Example: `TaskTree.load_from_file("plan.json")` returns validated TaskTree object

- [ ] **claude_client.py** (new file, ~139 lines)  
  - Encapsulates all Claude API interactions with structured output guarantees
  - Uses Pydantic's `.model_json_schema()` to generate tool schemas automatically
  - Three typed methods: `execute_task()`, `assess_task()`, `adapt_plan()`
  - Connects to: Called by tef_light.py agent functions, uses models.py schemas
  - Example: `client.execute_task(prompt)` returns typed ExecutionResult, never raw text

- [ ] **tef_light.py:1-30** (imports and setup)
  - Now imports from new modules instead of defining everything inline
  - Creates global `claude_client` instance for all agent functions
  - `execute_framework()` now uses `TaskTree.load_from_file()` with validation
  - Connects to: Entry point that orchestrates everything using typed models

- [ ] **tef_light.py:31-87** (core execution loop)
  - `execute_task()` uses TaskNode properties (`.status`, `.children`) not dict access
  - New `find_next_task()` traverses typed TaskNode tree
  - Added `_update_task_tree()` helper to merge adapted changes
  - Connects to: Calls agent functions (execute/assess/adapt) with typed models

- [ ] **tef_light.py:89-121** (execute function)
  - Returns typed `ExecutionResult` instead of dict
  - Calls `claude_client.execute_task()` for structured output
  - Accesses properties like `execution_result.git_diff` with type safety
  - Previous: Built dict manually, called raw `call_claude()` returning text

- [ ] **tef_light.py:124-158** (assess function)
  - Returns typed `AssessmentResult` with four perspective sub-objects
  - Uses `execution_result.status` not `execution_result.get('status')`
  - Calls `claude_client.assess_task()` for guaranteed structure
  - Previous: Returned dict with single "observations" text field

- [ ] **tef_light.py:161-205** (adapt function)
  - Returns typed `TaskNode` or None (no more JSON parsing)
  - Formats structured observations from `obs.build.feasible` etc
  - Calls `claude_client.adapt_plan()` - no try/except needed
  - Previous: Called raw Claude, tried to parse JSON, often failed

## 3) Before vs After Map

**Old Path**:
```
json.load() → dict
call_claude(prompt) → text string  
json.loads(response) → maybe dict, maybe error
task["status"] = "pending" → runtime KeyError possible
```

**New Path**:
```
TaskTree.load_from_file() → validated TaskTree
claude_client.execute_task() → guaranteed ExecutionResult
task.status = "pending" → IDE autocomplete, type-safe
No JSON parsing needed → tool-use returns structured data
```

**Why**: Claude's tool-use feature guarantees structured outputs matching our schemas, eliminating JSON parse errors and providing full type safety throughout the framework.

## 4) Key Concepts & Data Shapes

**Terms introduced**:
- **Pydantic models**: Python classes that validate and serialize data with type hints
- **Tool-use**: Claude API feature forcing responses into defined JSON schemas
- **model_json_schema()**: Pydantic method generating JSON schemas from models

**Changed interfaces**:
- `execute()`: `dict → ExecutionResult`
- `assess()`: `dict → AssessmentResult` 
- `adapt()`: `dict → TaskNode | None`
- Task access: `task["id"] → task.id`
- Tree loading: `json.load(f) → TaskTree.load_from_file(path)`

## 5) Mental Model Cheat Sheet

- All data flows through Pydantic models - no raw dicts anywhere
- Claude can't return malformed JSON - tool-use enforces schemas
- Type hints actually work now - IDE knows all properties
- Three-layer architecture: models (data), claude_client (API), tef_light (logic)
- Validation happens on load - bad JSON fails fast with clear errors
- No more defensive `get()` calls - properties are guaranteed to exist

## 6) Short-on-time Route

**Quick skim path**:
1. Look at `models.py:71-94` for TaskNode definition - this is what everything operates on
2. Check `claude_client.py:68-83` for execute_task() - shows structured output pattern
3. See `tef_light.py:25` - TaskTree.load_from_file() replaces json.load()
4. Note `tef_light.py:38` - task.status not task["status"]

**Minimal test**:
```bash
py -c "from models import TaskTree; t = TaskTree.load_from_file('test_task.json'); print(t.root.id)"
```