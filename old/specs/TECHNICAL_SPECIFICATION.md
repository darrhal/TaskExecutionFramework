# Task Execution Framework - Technical Specification

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Data Models & Contracts](#data-models--contracts)
4. [Execution Flow](#execution-flow)
5. [Verifier Specifications](#verifier-specifications)
6. [Configuration System](#configuration-system)
7. [Error Handling & Recovery](#error-handling--recovery)
8. [Artifacts & Logging](#artifacts--logging)
9. [API Reference](#api-reference)
10. [Implementation Guidelines](#implementation-guidelines)
11. [Performance & Limits](#performance--limits)
12. [Extension Guide](#extension-guide)

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Layer                           │
│  task.md files │ verifiers.yml │ CLI interface │ Overrides  │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                     Orchestration Layer                      │
│   CodeTaskAgent │ Aggregator │ Decision Engine │ Registry   │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                      Execution Layer                         │
│  Claude Code SDK │ Verifiers │ Git Operations │ File I/O    │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                      Persistence Layer                       │
│   Git Commits │ Run Artifacts │ JSON Logs │ Child Specs     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Component Interactions

```python
# Simplified interaction flow
def CodeTaskAgent(spec: TaskSpec, ctx: Context) -> Result:
    for attempt in range(1, spec.policy.max_attempts + 1):
        # 1. Execute
        do_agent_result = ClaudeCode.edit(spec, ctx)
        
        # 2. Verify
        verifier_outputs = []
        for verifier in get_staged_verifiers():
            output = verifier.run(ctx)
            verifier_outputs.append(output)
            if should_short_circuit(output):
                break
        
        # 3. Decide
        decision = aggregate(verifier_outputs, policy, fingerprints)
        
        # 4. Act
        if decision.kind == "DONE":
            return Success(decision)
        elif decision.kind == "SPLIT":
            return spawn_children(decision.fingerprints)
        elif decision.kind == "RETRY":
            continue
    
    return GiveUp(reason="budgets_exhausted")
```

## 2. Core Components

### 2.1 Orchestrator

**File**: `orchestrator.py`  
**Class**: `CodeTaskAgent`  
**Responsibility**: Main execution loop and control flow

#### Key Methods

```python
def orchestrate(task_md: Path, verifiers_yaml: Path, repo_dir: Path) -> None:
    """
    Main orchestration entry point.
    
    Args:
        task_md: Path to task specification file
        verifiers_yaml: Path to verifier registry
        repo_dir: Repository root directory
    
    Side Effects:
        - Creates git commits for each attempt
        - Writes artifacts to runs/<run-id>/
        - May spawn child tasks recursively
    """

def aggregate(
    outputs: List[VerifierOutput], 
    reg: Registry, 
    attempt: int, 
    policy: Policy, 
    fp_counts: Dict[str,int]
) -> Decision:
    """
    Deterministic aggregation of verifier outputs.
    
    Returns:
        Decision with kind in [DONE, RETRY, FAIL, SPLIT, GIVE_UP]
    """

def spawn_child_specs(
    repeated_fps: List[str], 
    findings: List[Finding], 
    parent_spec: Dict,
    depth: int
) -> List[Path]:
    """
    Generate child task specifications for repeated errors.
    
    Returns:
        List of paths to generated child spec files
    """
```

### 2.2 Verifier Framework

#### Base Verifier Interface

```python
class Verifier:
    """Base class for all verifiers."""
    
    id: str
    cfg: VerifierConfig
    
    def __init__(self, cfg: VerifierConfig):
        self.cfg = cfg
        self.id = cfg.id
    
    def run(self, ctx: Dict) -> VerifierOutput:
        """
        Execute verification logic.
        
        Args:
            ctx: Context dictionary containing:
                - spec: Task specification
                - diff_summary: Current git diff
                - repo: Repository path
                - workspace: File tree and changes
                - relations: Parent/next task snapshots
        
        Returns:
            VerifierOutput with severity, findings, evidence
        """
        raise NotImplementedError
```

#### Context Structure

```python
{
    "spec": {
        "id": "task-001",
        "title": "...",
        "acceptance": ["..."],
        "constraints": {...},
        "relationships": {
            "parent_id": "task-000",
            "next_ids": ["task-002"]
        }
    },
    "context": {
        "depth": 0,
        "attempt": 1,
        "run_id": "20240119-143022",
        "budgets": {
            "max_attempts": 3,
            "max_depth": 3
        }
    },
    "workspace": {
        "root": "./",
        "tree": ["src/...", "tests/..."],
        "changed_files": ["src/Foo.cs"],
        "diff_unified": "...",
        "summaries": [...]
    },
    "relations": {
        "parent_excerpt": {...},
        "next_excerpts": [...]
    },
    "policy": {
        "build": {"mode": "must-pass"},
        "thresholds": {...}
    }
}
```

### 2.3 Claude Code Integration

**SDK**: `claude-code-sdk` (Python)  
**Modes**: 
- `edit`: Primary task execution
- `verify`: Verification assessments (future)

#### Do-Agent Configuration

```python
async def run_do_agent(ctx: Dict) -> None:
    """Execute primary task via Claude Code SDK."""
    
    options = ClaudeCodeOptions(
        permission_mode="acceptEdits",  # Non-interactive editing
        allowed_tools=["Write", "Read", "Grep"],  # Default safe set
        max_turns=3,
        cwd=ctx["repo"],
        system_prompt=build_system_prompt(ctx["spec"])
    )
    
    # Optional: Enable Bash for specific tasks
    if ctx["spec"].get("do_agent", {}).get("allowed_tools"):
        options.allowed_tools = ctx["spec"]["do_agent"]["allowed_tools"]
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query(build_task_prompt(ctx))
        # Stream handling and artifact logging...
```

## 3. Data Models & Contracts

### 3.1 Core Types

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Severity = str  # "error" | "warning" | "info"
Verdict = Optional[str]  # None | "fail" | "pass" | "advisory"
DecisionKind = str  # "DONE" | "RETRY" | "FAIL" | "SPLIT" | "GIVE_UP"

@dataclass
class Evidence:
    """Supporting evidence for a finding."""
    file: Optional[str] = None
    lines: Optional[Tuple[int, int]] = None
    log_sample: Optional[str] = None
    command: Optional[str] = None

@dataclass
class Finding:
    """Individual issue identified by a verifier."""
    type: str  # e.g., "BUILD_FAIL", "SPEC_DIVERGENCE"
    msg: str
    evidence: Evidence = field(default_factory=Evidence)
    fingerprint: str = ""  # Normalized hash for repeat detection

@dataclass
class VerifierOutput:
    """Complete output from a single verifier."""
    verifier: str
    severity: Severity
    summary: str
    findings: List[Finding] = field(default_factory=list)
    verdict: Verdict = None  # Optional veto
    rationale: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class Policy:
    """Execution policy and budgets."""
    max_attempts: int = 3
    max_depth: int = 3
    split_on_repeat_errors: int = 2

@dataclass
class Decision:
    """Aggregated decision from all verifiers."""
    kind: DecisionKind
    reason: str
    repeat_fps: List[str] = field(default_factory=list)
```

### 3.2 Task Specification Schema

```yaml
# task.md frontmatter
---
id: string  # Unique identifier (required)
title: string  # Human-readable title (required)
constraints:
  language: string  # e.g., "C#/.NET"
  style: [string]  # Style requirements
  architecture: [string]  # Architectural constraints
acceptance: [string]  # List of acceptance criteria (required)
policy:
  max_attempts: integer  # Default: 3
  max_depth: integer  # Default: 3
  split_on_repeat_errors: integer  # Default: 2
verifier_overrides:
  <verifier_id>:
    warn_triggers_retry: boolean
    required: boolean
    config: object
relationships:
  parent_id: string  # Parent task ID
  parent_snapshot: string  # Brief parent description
  next_ids: [string]  # Potential next tasks
  next_tasks: [string]  # Brief next task descriptions
do_agent:
  allowed_tools: [string]  # Override allowed tools
  permission_mode: string  # Override permission mode
  max_turns: integer  # Override max turns
git:
  branch: string  # Branch to work on
  commit_on_success: boolean  # Auto-commit on success
---
# Task body (markdown)
Implementation details, context, examples...
```

### 3.3 Verifier Registry Schema

```yaml
# verifiers.yml
stakeholders:
  - id: string  # Unique ID
    description: string  # Role description

verifiers:
  - id: string  # Unique ID (required)
    stakeholder: string  # Reference to stakeholder (required)
    mode: string  # "shell" | "model"
    required: boolean  # Is this verifier mandatory?
    warn_triggers_retry: boolean  # Do warnings cause retry?
    config:
      # Verifier-specific configuration
      command: string  # For shell verifiers
      timeout_sec: integer
      acceptance_window: integer  # For model verifiers
      consider_next_tasks: boolean
```

## 4. Execution Flow

### 4.1 Main Execution Loop

```
START
  │
  ├─→ Load task.md
  ├─→ Parse frontmatter & body
  ├─→ Load verifiers.yml
  ├─→ Apply task overrides
  │
  ├─→ ATTEMPT LOOP (1 to max_attempts)
  │     │
  │     ├─→ Create attempt directory
  │     ├─→ Execute do_agent (Claude Code)
  │     ├─→ Capture git diff
  │     │
  │     ├─→ VERIFICATION STAGE
  │     │     ├─→ Run Build verifier
  │     │     ├─→ If fail/error: short-circuit
  │     │     ├─→ Run Alignment verifier
  │     │     ├─→ If fail: short-circuit
  │     │     ├─→ Run BigPicture verifier
  │     │     └─→ If fail: short-circuit
  │     │
  │     ├─→ AGGREGATION
  │     │     ├─→ Check for vetos
  │     │     ├─→ Count error severities
  │     │     ├─→ Update fingerprint counts
  │     │     ├─→ Check repeat thresholds
  │     │     └─→ Apply warning policies
  │     │
  │     ├─→ DECISION
  │     │     ├─→ DONE: Success, exit
  │     │     ├─→ FAIL: Veto, exit
  │     │     ├─→ SPLIT: Generate children
  │     │     ├─→ RETRY: Continue loop
  │     │     └─→ GIVE_UP: Budgets exhausted
  │     │
  │     └─→ Log artifacts & commit
  │
  └─→ END
```

### 4.2 Child Task Spawning

```python
def handle_split(decision: Decision, parent_spec: Dict, depth: int):
    """Handle SPLIT decision by generating and executing child tasks."""
    
    # 1. Generate child specifications
    child_specs = []
    for fp in decision.repeat_fps:
        child_spec = {
            "id": f"{parent_spec['id']}-child-{fp[:8]}",
            "title": f"Resolve {finding.type} in {finding.evidence.file}",
            "parent_snapshot": parent_spec["title"],
            "constraints": parent_spec.get("constraints", {}),
            "acceptance": [f"Resolve {finding.msg}"],
            "policy": {
                "max_attempts": 2,  # Reduced for children
                "max_depth": depth - 1,
                "split_on_repeat_errors": 2
            },
            "origin": {
                "parent_id": parent_spec["id"],
                "fingerprint": fp,
                "attempt": attempt,
                "reason": finding.msg
            }
        }
        child_specs.append(child_spec)
    
    # 2. Execute children (parallel if configured)
    if parallel_workers > 1:
        with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
            futures = [
                executor.submit(orchestrate, child_path, verifiers_yaml, repo_dir)
                for child_path in child_paths
            ]
            results = [f.result() for f in futures]
    else:
        for child_path in child_paths:
            orchestrate(child_path, verifiers_yaml, repo_dir)
```

## 5. Verifier Specifications

### 5.1 Build Verifier

**Purpose**: Ensure code compiles/builds successfully  
**Stakeholder**: Architecture  
**Mode**: Shell (parent) / Model (child)  
**Criticality**: Blocker

#### Implementation (Parent Depth)

```python
class BuildVerifier(Verifier):
    def run(self, ctx: Dict) -> VerifierOutput:
        cmd = self.cfg.config.get("command", "dotnet build")
        timeout = int(self.cfg.config.get("timeout_sec", 600))
        
        proc = subprocess.run(cmd, shell=True, capture_output=True, 
                            text=True, timeout=timeout)
        
        if proc.returncode == 0:
            return VerifierOutput(
                verifier=self.id,
                severity="info",
                summary="Build succeeded",
                findings=[],
                metadata={"exitCode": 0}
            )
        else:
            fp = structured_fingerprint("BUILD_FAIL", None, None, 
                                       proc.stderr[-300:])
            return VerifierOutput(
                verifier=self.id,
                severity="error",
                summary="Build failed",
                findings=[Finding(
                    type="BUILD_FAIL",
                    msg="Build failed",
                    evidence=Evidence(
                        log_sample=proc.stderr[-2000:],
                        command=cmd
                    ),
                    fingerprint=fp
                )],
                verdict="fail",  # Veto on build failure
                metadata={"exitCode": proc.returncode}
            )
```

#### Implementation (Child Depth)

At child depth, use textual analysis instead of actual build:

```python
def run_textual_build_check(ctx: Dict) -> VerifierOutput:
    """Infer build status from diff without running build."""
    diff = ctx.get("diff_summary", "")
    
    # Check for obvious syntax errors
    syntax_issues = check_syntax_patterns(diff)
    
    # Check for missing imports/dependencies
    dependency_issues = check_dependency_patterns(diff)
    
    if syntax_issues or dependency_issues:
        return VerifierOutput(
            verifier="build",
            severity="warning",
            summary="Potential build issues detected",
            findings=syntax_issues + dependency_issues
        )
    
    return VerifierOutput(
        verifier="build",
        severity="info",
        summary="No obvious build issues detected"
    )
```

### 5.2 Alignment Verifier

**Purpose**: Validate acceptance criteria are met  
**Stakeholder**: Product  
**Mode**: Model  
**Criticality**: Standard

```python
class AlignmentVerifier(Verifier):
    def run(self, ctx: Dict) -> VerifierOutput:
        acceptance = ctx["spec"].get("acceptance", [])
        diff_summary = ctx.get("diff_summary", "")
        
        # Limited to acceptance_window items
        window = self.cfg.config.get("acceptance_window", 5)
        acceptance = acceptance[:window]
        
        # Check each acceptance criterion
        missing = []
        for criterion in acceptance:
            if not appears_addressed(criterion, diff_summary):
                fp = structured_fingerprint("SPEC_DIVERGENCE", 
                                          None, None, criterion)
                missing.append(Finding(
                    type="SPEC_DIVERGENCE",
                    msg=f"Acceptance not addressed: {criterion}",
                    fingerprint=fp
                ))
        
        if not missing:
            return VerifierOutput(
                verifier=self.id,
                severity="info",
                summary="All acceptance criteria addressed"
            )
        else:
            return VerifierOutput(
                verifier=self.id,
                severity="warning",
                summary=f"{len(missing)} acceptance items missing",
                findings=missing
            )
```

### 5.3 BigPicture Verifier

**Purpose**: Ensure changes fit with parent/next tasks  
**Stakeholder**: Architecture  
**Mode**: Model  
**Criticality**: Standard

```python
class BigPictureVerifier(Verifier):
    def run(self, ctx: Dict) -> VerifierOutput:
        parent = ctx["relations"].get("parent_excerpt", {})
        next_tasks = ctx["relations"].get("next_excerpts", [])
        diff = ctx.get("diff_summary", "")
        
        risks = []
        
        # Check parent compatibility
        if parent and breaks_parent_assumptions(diff, parent):
            risks.append(Finding(
                type="CONTEXT_RISK",
                msg="Changes may violate parent constraints",
                fingerprint=structured_fingerprint(
                    "CONTEXT_RISK", None, None, 
                    "parent_violation"
                )
            ))
        
        # Check next task setup
        for next_task in next_tasks:
            if not enables_next_task(diff, next_task):
                risks.append(Finding(
                    type="CONTEXT_RISK",
                    msg=f"Doesn't enable: {next_task['id']}",
                    fingerprint=structured_fingerprint(
                        "CONTEXT_RISK", None, None,
                        next_task['id']
                    )
                ))
        
        severity = "info" if not risks else "warning"
        return VerifierOutput(
            verifier=self.id,
            severity=severity,
            summary="Big-picture fit ok" if not risks 
                    else "Potential context risks",
            findings=risks
        )
```

### 5.4 Style Verifier (Optional/Disabled)

**Purpose**: Code style and linting  
**Stakeholder**: Architecture  
**Mode**: Model  
**Criticality**: Advisory

```python
class StyleVerifier(Verifier):
    def run(self, ctx: Dict) -> VerifierOutput:
        # Quick diff-based style check
        diff = ctx.get("diff_summary", "")
        
        issues = []
        # Check for common style violations
        # This is intentionally minimal since style
        # is handled by the Do-agent prompting
        
        return VerifierOutput(
            verifier=self.id,
            severity="info",
            summary=f"{len(issues)} style suggestions",
            findings=issues
        )
```

## 6. Configuration System

### 6.1 Configuration Hierarchy

```
1. Default values (in code)
    ↓
2. Global registry (verifiers.yml)
    ↓
3. Task overrides (task.md frontmatter)
    ↓
4. Runtime flags (CLI arguments)
    ↓
5. Manual overrides (--override flag)
```

### 6.2 Configuration Loading

```python
def load_registry(path: Path, task_overrides: Dict) -> Registry:
    """Load and merge verifier configurations."""
    
    # Load base registry
    data = load_yaml(path)
    stakeholders = {s["id"]: s for s in data.get("stakeholders", [])}
    
    # Apply task-specific overrides
    verifier_configs = {}
    for v in data.get("verifiers", []):
        # Get task override if exists
        override = task_overrides.get("verifier_overrides", {}).get(v["id"], {})
        
        # Merge configurations
        merged = {**v, **override}
        
        verifier_configs[v["id"]] = VerifierConfig(
            id=v["id"],
            stakeholder=v["stakeholder"],
            required=merged.get("required", True),
            warn_triggers_retry=merged.get("warn_triggers_retry", True),
            config=merged.get("config", {})
        )
    
    return Registry(stakeholders=stakeholders, verifiers=verifier_configs)
```

### 6.3 Runtime Configuration

```python
# CLI arguments
parser.add_argument("--task", required=True, help="Path to task.md")
parser.add_argument("--verifiers", default="verifiers.yml")
parser.add_argument("--repo", default=".")
parser.add_argument("--parallel", type=int, default=1)
parser.add_argument("--depth", type=int, default=0)
parser.add_argument("--strict", action="store_true")
parser.add_argument("--override", choices=["DONE", "RETRY", "SPLIT", "FAIL"])
parser.add_argument("--why", help="Justification for override")

# Environment variables
DO_AGENT_ALLOW_BASH = os.getenv("DO_AGENT_ALLOW_BASH", "0") == "1"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

## 7. Error Handling & Recovery

### 7.1 Error Categories

| Category | Handling | Recovery |
|----------|----------|----------|
| Build failures | Retry with feedback | Up to max_attempts |
| Spec divergence | Retry with specifics | Highlight missing items |
| Context risks | Warning or retry | Depends on config |
| Repeated errors | Split to children | Recursive resolution |
| API failures | Exponential backoff | Retry with delay |
| Timeout | Log and continue | Mark as error |
| Resource limits | Give up gracefully | Log final state |

### 7.2 Fingerprinting Strategy

```python
def structured_fingerprint(
    kind: str, 
    file: Optional[str], 
    symbol: Optional[str], 
    text: str
) -> str:
    """
    Generate stable fingerprint for error detection.
    
    Components:
    - kind: Error type (BUILD_FAIL, SPEC_DIVERGENCE, etc.)
    - file: Affected file path (normalized)
    - symbol: Affected symbol/function (if applicable)
    - text: Normalized error text (first 200 chars)
    
    Returns:
        16-character hex hash
    """
    components = [
        kind,
        normalize_path(file) if file else "",
        symbol or "",
        normalize_text(text)[:200]
    ]
    
    fingerprint_str = "|".join(components)
    return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
```

### 7.3 Feedback Construction

```python
def build_feedback(outputs: List[VerifierOutput]) -> Dict:
    """Build structured feedback for retry attempts."""
    
    feedback = {
        "attempt": attempt,
        "errors": [],
        "warnings": [],
        "focus_areas": []
    }
    
    for output in outputs:
        if output.severity == "error":
            feedback["errors"].extend([
                {
                    "verifier": output.verifier,
                    "finding": f.msg,
                    "evidence": f.evidence.__dict__
                }
                for f in output.findings
            ])
        elif output.severity == "warning":
            feedback["warnings"].extend([
                {
                    "verifier": output.verifier,
                    "finding": f.msg
                }
                for f in output.findings
            ])
    
    # Identify focus areas
    if "BUILD_FAIL" in [f.type for o in outputs for f in o.findings]:
        feedback["focus_areas"].append("Fix compilation errors first")
    
    if "SPEC_DIVERGENCE" in [f.type for o in outputs for f in o.findings]:
        feedback["focus_areas"].append("Address missing acceptance criteria")
    
    return feedback
```

## 8. Artifacts & Logging

### 8.1 Directory Structure

```
runs/
├── run-20240119-143022/
│   ├── attempt-1/
│   │   ├── verifier_outputs.json
│   │   ├── decision.json
│   │   ├── do_agent_stream.ndjson
│   │   └── do_agent_result.json
│   ├── attempt-2/
│   │   └── ...
│   ├── child-specs/
│   │   ├── child-001.md
│   │   └── child-002.md
│   └── children-runs/
│       ├── child-001/
│       └── child-002/
```

### 8.2 Artifact Schemas

#### verifier_outputs.json
```json
[
  {
    "verifier": "build",
    "severity": "error",
    "summary": "Build failed",
    "findings": [...],
    "verdict": "fail",
    "metadata": {"exitCode": 1, "durationSec": 18.4}
  },
  ...
]
```

#### decision.json
```json
{
  "kind": "RETRY",
  "reason": "Error findings present",
  "repeat_fps": [],
  "attempt": 1,
  "timestamp": "2024-01-19T14:30:22Z",
  "override": null
}
```

#### do_agent_result.json
```json
{
  "session_id": "...",
  "cost": {
    "input_tokens": 1234,
    "output_tokens": 567,
    "total_cost_usd": 0.023
  },
  "duration_sec": 45.2,
  "tools_used": ["Write", "Read", "Grep"],
  "files_modified": ["src/Orders.cs", "src/OrderService.cs"]
}
```

### 8.3 Git Commit Format

```
[{task-id}] attempt {n}: {decision}

Severity counts:
- Errors: {error_count}
- Warnings: {warning_count}
- Info: {info_count}

Decision: {DONE|RETRY|SPLIT|FAIL|GIVE_UP}
Reason: {decision_reason}

Run ID: {run_id}
Attempt: {attempt}/{max_attempts}
Depth: {depth}/{max_depth}
```

## 9. API Reference

### 9.1 Main Entry Points

```python
def orchestrate(
    task_md: Path,
    verifiers_yaml: Path = Path("verifiers.yml"),
    repo_dir: Path = Path("."),
    depth: int = 0,
    parallel_workers: int = 1,
    override: Optional[str] = None,
    override_reason: Optional[str] = None
) -> None:
    """
    Execute a task with verification loop.
    
    Args:
        task_md: Task specification file
        verifiers_yaml: Verifier registry file
        repo_dir: Repository root
        depth: Current recursion depth
        parallel_workers: Max parallel children
        override: Manual decision override
        override_reason: Justification for override
    
    Raises:
        ValueError: Invalid task specification
        RuntimeError: Execution failure
    """
```

### 9.2 Verifier API

```python
class Verifier(ABC):
    """Abstract base class for verifiers."""
    
    @abstractmethod
    def run(self, ctx: Dict) -> VerifierOutput:
        """Execute verification logic."""
        pass
    
    def prepare(self, spec: Dict, ctx: Dict, ws: Dict) -> Dict:
        """Prepare context for verification."""
        return {
            "spec": spec,
            "context": ctx,
            "workspace": ws,
            "relations": self.load_relations(spec),
            "policy": self.load_policy(spec)
        }
```

### 9.3 Extension Points

```python
# Custom verifier registration
def register_verifier(verifier_class: Type[Verifier], config: VerifierConfig):
    """Register a custom verifier."""
    VERIFIER_REGISTRY[config.id] = verifier_class(config)

# Custom aggregation rules
def add_aggregation_rule(rule: Callable[[List[VerifierOutput]], Decision]):
    """Add custom aggregation rule."""
    AGGREGATION_RULES.append(rule)

# Custom fingerprinting
def register_fingerprinter(
    error_type: str, 
    fingerprinter: Callable[[Finding], str]
):
    """Register custom fingerprinting logic."""
    FINGERPRINTERS[error_type] = fingerprinter
```

## 10. Implementation Guidelines

### 10.1 Adding a New Verifier

1. **Define the stakeholder** in `verifiers.yml`:
```yaml
stakeholders:
  - id: performance
    description: Performance and efficiency concerns
```

2. **Create verifier class**:
```python
class PerformanceVerifier(Verifier):
    def run(self, ctx: Dict) -> VerifierOutput:
        # Analyze performance implications
        # Return structured findings
        pass
```

3. **Register in verifiers.yml**:
```yaml
verifiers:
  - id: performance
    stakeholder: performance
    mode: model
    required: false
    warn_triggers_retry: false
    config:
      thresholds:
        max_complexity: 10
        max_file_size: 10000
```

4. **Add to staged execution** if needed:
```python
VERIFICATION_STAGE = ["build", "alignment", "big_picture", "performance"]
```

### 10.2 Customizing Decision Logic

```python
def custom_aggregator(outputs: List[VerifierOutput], policy: Policy) -> Decision:
    """Example custom aggregation logic."""
    
    # Check for critical performance issues
    perf_issues = [
        f for o in outputs 
        if o.verifier == "performance" 
        for f in o.findings 
        if "CRITICAL" in f.type
    ]
    
    if perf_issues:
        return Decision(
            kind="FAIL",
            reason="Critical performance regression detected"
        )
    
    # Fallback to default aggregation
    return default_aggregate(outputs, policy)
```

### 10.3 Best Practices

#### Verifier Development
- Keep verifiers stateless and idempotent
- Always include evidence in findings
- Use structured fingerprints for repeatability
- Emit state, don't make decisions
- Include timing metadata for performance tracking

#### Error Handling
- Never let verifiers crash the orchestrator
- Wrap all external calls in try/except
- Log failures but continue execution
- Provide actionable error messages

#### Performance
- Cache expensive computations in metadata
- Use async/await for I/O operations (future)
- Implement timeouts for all external calls
- Batch file operations when possible

## 11. Performance & Limits

### 11.1 Default Limits

| Parameter | Default | Maximum | Notes |
|-----------|---------|---------|-------|
| max_attempts | 3 | 10 | Per task |
| max_depth | 3 | 5 | Recursion limit |
| split_threshold | 2 | 5 | Repeat count |
| verifier_timeout | 120s | 600s | Per verifier |
| do_agent_timeout | 300s | 900s | Claude Code |
| parallel_children | 1 | 10 | Concurrent |
| max_file_size | 1MB | 10MB | For diff |
| max_findings | 100 | 1000 | Per verifier |

### 11.2 Performance Characteristics

#### Time Complexity
- Single attempt: O(V) where V = number of verifiers
- Full execution: O(A × V) where A = attempts
- With splits: O(A × V × C^D) where C = children, D = depth

#### Space Complexity
- Artifacts: O(A × V × S) where S = average output size
- Git commits: O(A) commits per task
- Memory: O(F) where F = file count in repo

### 11.3 Optimization Strategies

```python
# 1. Early termination on critical failures
if output.verdict == "fail":
    return  # Skip remaining verifiers

# 2. Parallel verifier execution (future)
async def run_verifiers_parallel(verifiers, ctx):
    tasks = [v.run(ctx) for v in verifiers]
    return await asyncio.gather(*tasks)

# 3. Incremental diff analysis
def get_incremental_diff(last_attempt, current_attempt):
    # Only analyze changes since last attempt
    return git_diff(f"attempt-{last_attempt}", f"attempt-{current_attempt}")

# 4. Fingerprint caching
@lru_cache(maxsize=1000)
def cached_fingerprint(kind, file, symbol, text):
    return structured_fingerprint(kind, file, symbol, text)
```

## 12. Extension Guide

### 12.1 Plugin Architecture (Future)

```python
class VerifierPlugin:
    """Base class for verifier plugins."""
    
    @property
    @abstractmethod
    def metadata(self) -> Dict:
        """Plugin metadata."""
        return {
            "name": "...",
            "version": "...",
            "author": "...",
            "requires": ["..."]
        }
    
    @abstractmethod
    def register(self, registry: Registry):
        """Register plugin components."""
        pass
```

### 12.2 MCP Integration (Future)

```python
class MCPVerifier(Verifier):
    """Verifier using Model Context Protocol."""
    
    def __init__(self, cfg: VerifierConfig, mcp_server: str):
        super().__init__(cfg)
        self.mcp_client = MCPClient(mcp_server)
    
    async def run(self, ctx: Dict) -> VerifierOutput:
        # Query MCP server for verification
        response = await self.mcp_client.verify(ctx)
        return self.parse_mcp_response(response)
```

### 12.3 Distributed Execution (Future)

```python
class DistributedOrchestrator:
    """Orchestrator with distributed child execution."""
    
    def __init__(self, worker_pool: List[str]):
        self.workers = worker_pool
        self.scheduler = TaskScheduler(self.workers)
    
    async def execute_children(self, child_specs: List[Dict]):
        """Distribute children across workers."""
        tasks = []
        for spec, worker in zip(child_specs, self.scheduler.assign()):
            task = self.execute_remote(spec, worker)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
```

## Appendix A: Complete Configuration Examples

### A.1 Simple Task

```yaml
---
id: fix-001
title: Fix compilation error in OrderService
acceptance:
  - "OrderService.cs compiles without errors"
  - "All existing tests pass"
---
The OrderService.cs file has a syntax error on line 42. Fix it.
```

### A.2 Complex Task with Overrides

```yaml
---
id: feature-001
title: Implement order cancellation API
constraints:
  language: "C#/.NET"
  style: ["async/await only", "RESTful conventions"]
  architecture: ["maintain layer separation", "use existing services"]
acceptance:
  - "POST /api/orders/{id}/cancel endpoint exists"
  - "Returns 200 when order can be cancelled"
  - "Returns 409 when order cannot be cancelled"
  - "Emits OrderCancelled domain event"
  - "Updates order status to 'Cancelled'"
policy:
  max_attempts: 5
  max_depth: 4
  split_on_repeat_errors: 3
verifier_overrides:
  alignment:
    warn_triggers_retry: true
    config:
      acceptance_window: 10
  big_picture:
    required: true
    config:
      consider_next_tasks: true
relationships:
  parent_id: "epic-001"
  parent_snapshot: "Order management system overhaul"
  next_ids: ["feature-002", "feature-003"]
  next_tasks: ["Add cancellation UI", "Implement refund processing"]
do_agent:
  allowed_tools: ["Write", "Read", "Grep", "Bash"]
  max_turns: 5
git:
  branch: "feature/order-cancellation"
  commit_on_success: true
---

## Context

We need to add order cancellation capability to our e-commerce platform. Orders can only be cancelled if they haven't been shipped yet.

## Technical Notes

- Use the existing OrderService and OrderRepository
- Follow the established CQRS pattern
- Ensure idempotency - multiple cancel requests should be safe
- Add appropriate logging and telemetry

## Examples

Similar endpoints: 
- `/api/orders/{id}/ship` - for shipping orders
- `/api/orders/{id}/complete` - for completing orders

## Testing Considerations

- Unit test the business logic
- Integration test the API endpoint
- Verify event emission
- Test concurrent cancellation attempts
```

### A.3 Minimal verifiers.yml

```yaml
stakeholders:
  - id: architecture
    description: System structure and build integrity
  - id: product
    description: Feature requirements and acceptance

verifiers:
  - id: build
    stakeholder: architecture
    mode: shell
    required: true
    warn_triggers_retry: true
    config:
      command: "dotnet build --no-restore"
      timeout_sec: 300
      
  - id: alignment
    stakeholder: product
    mode: model
    required: true
    warn_triggers_retry: true
    config:
      acceptance_window: 5
```

## Appendix B: Troubleshooting Guide

### B.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Build keeps failing | Syntax errors | Check build verifier logs |
| Infinite retry loop | Deterministic error | Add to split threshold |
| Child tasks not running | Depth limit reached | Increase max_depth |
| Slow execution | Large diffs | Increase timeouts |
| API rate limits | Too many calls | Add backoff/caching |

### B.2 Debug Mode

```bash
# Enable verbose logging
export TEF_LOG_LEVEL=DEBUG

# Dry run without changes
python orchestrator.py --task task.md --dry-run

# Skip specific verifiers
python orchestrator.py --task task.md --skip-verifiers style,security

# Force specific decision
python orchestrator.py --task task.md --override DONE --why "Manual verification"
```

### B.3 Recovery Procedures

```bash
# Resume from specific attempt
git checkout attempt-2-branch
python orchestrator.py --task task.md --resume

# Replay with modified policy
python orchestrator.py --task task.md --replay \
  --override-policy max_attempts=10

# Clean up failed runs
python cleanup.py --before "2024-01-19" --status failed
```

## Appendix C: Security Considerations

### C.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| Malicious task specs | Validate YAML schema |
| Command injection | Use subprocess with arrays |
| API key exposure | Environment variables only |
| Infinite recursion | Depth limits enforced |
| Resource exhaustion | Timeouts and quotas |

### C.2 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Validate all inputs** - Schema validation on task specs
3. **Limit permissions** - Default to read-only tools
4. **Audit all actions** - Comprehensive logging
5. **Isolate execution** - Consider containers (future)

## Appendix D: Future Enhancements

### D.1 Planned Features

1. **Security Verifier** (Q2 2024)
   - Static analysis integration
   - Secret scanning
   - Dependency vulnerability checks

2. **Performance Verifier** (Q3 2024)
   - Complexity analysis
   - Performance regression detection
   - Resource usage tracking

3. **Personality Consistency** (Q4 2024)
   - Coding style learning
   - Pattern matching from history
   - Developer preference modeling

### D.2 Research Areas

1. **Learned Policies**
   - Success pattern recognition
   - Optimal retry strategies
   - Adaptive thresholds

2. **Distributed Execution**
   - Worker pool management
   - Task scheduling
   - Result aggregation

3. **Advanced Fingerprinting**
   - Semantic similarity
   - Root cause clustering
   - Predictive failure detection

---

*This specification represents version 1.0 of the Task Execution Framework. For updates and contributions, see the project repository.*