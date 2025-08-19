User: I've been doing some brainstorming on how to create a more reliable, robust framework/workflow/whatever, for defining and executing software development tasks. To some degree this involves iteration of the "plan" as defined by me, and the better that is, and/or the smaller the task I give a code agent (claude code, cursor, whatever) is always better. But more so, this is me searching for a way to minimize that up-front step, or just really condense it and make it concise, and use a much more explicitly programmed outer loop of agent/model calls to either allow a task to be executed with greater precision, or allow a bigger task to be executed without my input. At this point in time, I have actual intentions to implement something out here, to try it all out. I imagine this process initially involves programming some sort of command-line tool to read in an instruction set, like a .md file, and execute it until complete or some sort of other stop signal is received (I haven't brainstormed "give up" paths or limits to retries or anything like that yet). To start out I would almost certainly use the claude code sdk as my "agent call". (look documentation for this any anything else up in the web, as needed). But I could also see calling an LLM model directly as a potential option in some cases. My framework/language of comfort for the app itself is c#/.net, but I might lean more towards python or typescript since that's what claude code supports. I have some familiarity with typescript, and a little python. I might lean towards python just because it's so ubiquitous in ML/everything now. Part of me just wants to wrap the python calls in c#, but maybe I should just take the python plunge. I do feel I should just keep the actual app simple enough to start out, so maybe using python would force that. Here are my brainstorming notes. I'm looking for some help distilling this down into something more organized, such that I can continue to iterate and improve on the ideas, and get a more narrow definition of what I'm actually going to try to build.

- Generic, robust, software development task agential workflow
	- Planning and spec development, from a product perspective
	- Planning and spec development from an architectural perspective
	- Actual tasks to execute
	- What does this actually mean? What are we "searching" for? Existing examples to mimic? Yes, probably? What else?
	- We could create a prompt to help an LLM model drive the creation of this as it prompts a human for input
	- The output of this would somehow have to conform to the structure needed by the framework I've brainstormed below. In principal, that's all it would need to do. But the "bigger picture/surrounding context" concept is kind of unique. We sort of need to initialize this properly, but in principal, we could design this in such a way that the function "call" to the agent is homogenous, and simply differs by the parameters passed in to it, whether that's explicit/exact/symbolic parameters, or softer/natural language/neural "parameters".
	- Actual code changes (Agential "Do Task")
		- Agent call to execute the task.
		- Verification (This actually seems like the more critical piece, now that I think about it)
			- Build/test if possible
				- Test = product consistency, if product level testing. But I think to start, no testing. Even unit testing. Because if anything, I'd have it create the unit tests themselves, which wouldn't help what I'm going for here.
			- Softer evaluations
				- Basic task-level requirements evaluation (is what the agent did actually what it should have done?)
				- Architectural consistency
				- Security requirements
				- Style (architecture/design/actual code) consistency
				- "personality" consistency (if there was some means of defining a personality, like some softer/learned description of how the person initiating the task would have done it themselves. Obviously this bleeds in to/duplicates other areas very quickly)
				- Contextual relevancy
					- Is the next task in the process set up for success now?
					- Do the changes support the higher level goals? So maybe keeping it simple, "does this task support the successful completion of the parent task (if there is one?)". Maybe this is also say the same thing as "do the changes made in this diff support the higher-level product/architectural requirements", but does so at a more granular level.
				- Each of these steps potentially could provide feedback in the level of "error/warning/info" as a way of defining control flow for the next steps. I.e. if there are any errors, we need to try again, and if there are warnings, then maybe we try again but maybe we don't, based on configuration or some other softer/learned parameter passed in/directed by the previous functions in the workflow
				- Somehow the definitions of all of these things to evaluate have to be passed in or be available, at the beginning of the task.
				- Most of this could fall under the description of "code review" but from different "stakeholders" or something. Except for the Contextual relevancy parts, although, we could still model it in the same way.
				- I think the takeaway here after all of this brainstorming is that, at its core, a more robust agential coding task agent workflow revolves around more evaluation of success. More total quantity of evaluation, more diverse evaluation. I could even add things like security in. I could see a world where the different "stakeholder" evaluations could be configured explicitly for a run, or softly learned/passed through via "neurological" model outputs. Now I need to swing back below to the outer loop and expand on what I've started. How do I manage the signals from the evaluation step, to determine what step to take next?
		- If everything is good, or mostly good ("with comments") signal complete (but note the discoveries detailed about about errors/warning/info)
		- Commit changes (locally only) if success. Or maybe always? Probably not always, but maybe always write a log/.md file at this point in the process. Timestamp/task description/etc... But actually, if I didn't commit, I wouldn't have a great way of seeing the progress of the "inner retries" concept that I've ideated upon...hmm...
		- If improvements need to be made, loop. But how? State/environmental changes remain, with description of desired "diff". Yes, I think just a diff. I mean, to keep it simple at the start, we could just have every loop do an actual git diff. Then we need to pass in instructions for what to do. We are essentially creating a new task, which itself could need to be broken down into sub-tasks. In fact, I think that's key. I don't think I can try to constrain this to require a single one-shot agent call to try again, with whatever context I build up as the "feedback". I think I need to, at this step here, build up a list of tasks (potentially one is good enough), which modify the environment (make actual code changes). But that could get tricky. Would I call them to modify the "security" feedback sequentially, or in parallel with the "architectural consistency" feedback? Parallel would not work, and potentially there would be all sort of issues. Even if you did it sequentially, the feedback could be too specific to the state it was in when the feedback was created, and no longer perfectly relevant by the time the task is executed. So I think to start of, we do just loop back to another agent call, and trust/live with the one-shot of the agent handling the complete list of feedback, and of course, trust in the verification process that we will for sure have in place. I do wonder though, is this an iterative loop, or something more recursive, i.e. adds a layer of depth each time. What does this mean/how is this relevant? Well, it's all about context. If/when a sub-task/retry occurs, I think we want to go back and feed it through the same (exact same) evaluation process that it went through the first time (when it was determined another pass was needed), and do that exact same process over again. And I guess the key point I'm getting at here is that if the 2nd pass failed, for whatever reason, it would spawn a new "sub" task/agent call to attempt to address the problem. The key here though? It's that the context given to the 2nd pass would have to be constructed as a result of the evaluation of the 1st pass. Maybe literally we can just pass the results (errors/warnings/info) down to the next level. Somehow this has to know though, what "evaluators" to run. There's this concrete requirement here to figure out how to turn the softly evaluated (neural) functions into discrete, symbolic function calls/data. This appears to be do-able now, with a fairly high degree of precision/accuracy/confidence (tool calling/MCP's, structured output, etc), it's just a matter of how exactly to implement it.


Assistant: Awesome direction. Here’s a tight, buildable shape for what you described—an outer-loop harness that reads a task spec, drives an agent (start with Claude Code SDK), verifies results, and loops until success or stop.

1) Tech choices (pragmatic)

Language: Python (first) → smallest glue code with Claude Code SDK; TS also works; C# can shell the CLI later. SDKs: TS & Python; non-interactive “print mode” and flags are available via CLI/SDK (tools, permission modes, output formats).

Tooling: Use Claude Code tools + optional MCP servers for external systems (Jira, GitHub, Notion, etc.).

Stakeholders: Map to Claude Code Subagents (code-reviewer, debugger, security, etc.) with their own prompts/tools/contexts.

2) MVP architecture

Inputs

task.md (YAML front-matter + body), settings.yml, optional .mcp.json, subagents in .claude/agents/.

Core state machine

PLAN → EXECUTE → VERIFY → DECIDE → (RETRY | SPLIT | DONE | GIVE_UP)

Execution

Call Claude Code via Python SDK (ClaudeSDKClient.query) or CLI with --print / --output-format json, set --allowedTools, --permission-mode (e.g., plan, acceptEdits), and working directory.

Verification (gatekeepers)

Fast, deterministic first: build/lint/tests; then heuristic/symbolic checks (style, arch rules, security).

Each verifier returns {severity: error|warning|info, messages:[…]}; aggregator decides next step.

Retry logic

If any error → one more single consolidated agent attempt (feed back all findings); on repeated failure, either SPLIT into sub-tasks or GIVE_UP per policy.

Persistence

Always emit a run log (runs/run-<timestamp>.md) and commit diffs when a verification boundary is passed (configurable), so you can see inner-loop progress.

3) Minimal task.md schema (copy/paste)
...

4) Controller skeleton (Python)
...

5) Mapping “stakeholders” → subagents & tools
...

6) Control-flow contract (outer-loop)

...

7) Milestones (one week of evenings)
...


If you want, I’ll turn this into a small repo scaffold (Python) with: task.md example, runner, verifier stubs, and two subagents (code-reviewer, debugger).

User: It's possible that would work. However, I want to back away from the approach of using sub-agents, and instead, try to explicitly program a little more of this outer loop myself. I want to be able to control this with a little more fidelity than the sub-agent spec provides, and notably, want to have the ability to have the "sub-agent" type calls be able to also call "sub-agents". I think what I'm going for is potentially a single top-level function (my main agent call) that is always the thing called for any agential function call, from the initial one defined by the user, to any function call within the sub-process. Also, I want to step back out and ideate on this more, before we dive into implementation details. Not sure on the format of that ideation, but sometimes code or pseod code can help, or maybe some n8n workflows, o mermaid diagrams, to help visualization. I'll let you decide.

Assistant: Got it. Let’s design a single-entry, recursive outer loop where every call goes through AgentCall(spec, context). Principles: one function, separation of concerns, recursion not parallelism, structured signals, deterministic gates. Provided contracts: TaskSpec YAML, AgentCall envelope, Verifier interface, pseudocode loop (Generate→Apply→Verify→Decide→Retry/Split), Mermaid flow and sequence diagrams. Prompts for generation and verification; emphasized stateful feedback and uniform logging. Offered next steps to turn into a small skeleton.

User: I wrote down my reactions and decisions: prefer global/inherited permissions (with future pass-down strategy), unsure on budgets (maybe high or none), like split-after-repeated-error, questions on building verifiers and how they tie to constraints/acceptance, want traceable commits (tags aren’t enough), prefer verifiers as model calls, want GeneratePlanAndEdits to be the Claude Code agent (returning edits), like Decide flow with shouldSplit based on retry count, remove tests for now, keep build step (possibly via Claude verifying build), ignore security, and want a big-picture evaluation about fit with parent/next tasks.

Assistant: Proposed a decision grid (1–15): call contract & inheritance; budgets; verification set; build policy; verifier implementation style; traceability; retry/split rules; child spec synthesis; task relationships for BigPicture; finding taxonomy; Claude Code usage; commit/logs; spec format; naming; shell scope. Asked for selections.

User: 1B, 2A, 3B, 4C, 5A. 6A. Still thinking. Just capturing.

Assistant: Confirmed those; requested numbers for budgets and thresholds; asked to pick the rest (7–15) with suggested defaults.

User: 7A, 8A, 9A. I don't understand 10.

Assistant: Explained “finding taxonomy”: small fixed codes to drive control flow; offered 10A default (BUILD_FAIL, SPEC_DIVERGENCE, CONTEXT_MISALIGN, STYLE_LINT) and requested remaining numbers.

User: I want them to emit whatever the state is.

Assistant: Shifted to state-first design (S2 open-state only or S3 open-state+tags). Defined JSON schemas for build/alignment/bigPicture/style; orchestrator rule table (thresholds, repeat detection via fingerprint), prompts for each verifier, and asked for picks on S2/S3, thresholds, fingerprint recipe, and the numbers for budgets/repeats/child budgets.

User: Let's swing back to this later. For the rest: 11A, 12A, 13A, 14A, 15B (no additional restrictions at all right now)

Assistant: Locked those; summarized open items (budgets, split trigger, child budgets, state model & thresholds, fingerprint). Provided a minimal spec skeleton and controller reminders.

User: Just pick something for all those, as long as I can change them later. But we really need to dive into the details of the verifiers, how we make sure that they understand their criteria and access to the evaluation.

Assistant: Chose defaults: max_attempts=3, max_depth=3, repeat=2, child budgets (2, parent_depth-1), S2, thresholds (0.70/0.70, style warn >8), fingerprint F1. Deep-dove verifier design: common input pack (spec/context/workspace/relations/policy), strict state-only JSON outputs, parent build (must-pass, can run shell) vs child build (textual), alignment and big-picture schemas (coverage/risks), style diff-only heuristic, aggregation rules, feedback JSON back to ClaudeCode(mode="edit"), artifact storage per verifier, and run logging.

User: Summarize the most critical pieces of this conversation

Assistant: Here’s the tight core of what we decided and how it fits together.

Goal

A single-entry, recursive orchestrator that can execute any dev task end-to-end with explicit control (no built-in “sub-agents”). All calls—top-level and nested—go through the same function.

Architecture

Function: CodeTaskAgent(spec, ctx)

Loop: Generate (ClaudeCode edit) → Apply → Verify → Decide → (Retry | Split | Done)

Recursion: If a repeated issue persists, synthesize child specs and call CodeTaskAgent again with reduced budgets.

Traceability: Commit every attempt on agent/<task-id> and save artifacts under runs/<run-id>/attempt-<n>/.

Spec & Grants

Spec format: Markdown with YAML front-matter (id/title, constraints, acceptance, budgets, policy, relationships).

Grants: Global/inherited by default; a pass-down slot exists (inherit | restrict), currently inherit.

Neural backend

Claude Code only for now.

ClaudeCode(mode="edit") does the work (edits, commands).

ClaudeCode(mode="verify") runs verifiers and returns state-only JSON.

Shell allowed broadly during verify (per your 15B).

Verifiers (state-first; no fixed codes)

All return strict JSON; the orchestrator applies thresholds and rules.

Build

Parent depth: must actually build (dotnet build), return {attempted, exitCode, errors[], warnings, durationSec, executed[], logSample}.

Child depth: textual inference only (no shell); same schema.

TaskAlignment

Compares changes to this task’s acceptance/constraints.

Returns {score 0..1, coverage[{acceptance, met, why}], constraint_issues[], rationales[]}.

BigPictureFit

Judges fit with parent and next tasks (short snapshots provided).

Returns {score 0..1, supports_parent, supports_next[], risks[], rationales[]}.

Style/Lint (quick, diff-scoped)

Returns {issues[{rule, count, examples[]}], total}.

Aggregation defaults

Thresholds: alignment ≥ 0.70, bigPicture ≥ 0.70; style.total > 8 = warning.

Retry on parent build fail or below-threshold scores.

Split when the same issue fingerprint repeats ≥2 times (from attempt ≥2).

Fingerprint recipe: hash of top error/rationale strings (F1).

Defaults (editable)

Budgets: max_attempts=3, max_depth=3

Split trigger: repeat=2

Child budgets: child_attempts=2, child_depth = parent_depth-1

State model: S2 (open-state only)

Thresholds: as above

Logging: per-attempt plan.json, findings.json, raw transcript, verifier I/O; commit msg [{task-id}] attempt {n}: {decision}

Key design intents

Uniform entry point for every agentic call.

State-first verifiers: they “emit what they see”; the orchestrator decides.

Deterministic control via thresholds, fingerprints, and budgets.

Auditability through per-attempt commits and artifacts.

If you want, I can turn this into a verifiers.yml + minimal Python runner stub next.


User: 

You are now a facilitator who helps a capable user brainstorm options and make decisions. Volunteer expertise when it clearly helps. Be concise.

When I provide MY INPUT below, do this in one message:
1) Extract goals, constraints, and implicit criteria.
2) Build a short Decision Map (2–6 atomic decisions).
3) For each decision, list 2–4 options with tight trade-offs; mark your recommendation with ✔.
4) Give a concise Recommendations section (only essential rationale, ≤3 bullets total).
5) Provide a one-line Decision Snapshot (one per decision).
6) List Next Actions. If info is missing, start with ≤3 Need-to-Know questions, then proceed anyway using explicit assumptions.

Constraints:
- Tone: concise & direct. Depth: balanced.
- Reasoning visibility: final answer; include ≤3 rationale bullets only if essential.
- Don’t browse or cite unless I explicitly ask or accuracy obviously depends on it.
- Avoid speculation; state assumptions if they matter.

Output sections (in order; skip any that aren’t needed):
- Need-to-Know (if any)
- Decision Map
- Options & Trade-offs
- Recommendations
- Decision Snapshot
- Next Actions
- Open Questions (only if needed)

Optional override (compact picks): If I include a line starting with “DECISIONS:” like DECISIONS: 1B, 2A(note), apply those choices directly.
I want to dive into the verifier design again. I want there to be somewhat of an abstract framework for this. Yes, to start I'll just have a build/TaskAlignment/BigPictureFit/style, but in principal the flow should be generic. I'm still not sure on the format. Should the verifier have control of pass/fail (control flow essentially, or your "#10 “Finding taxonomy”" thing), or should the be dumb and have the higher agent just take in. Or maybe the verifiers have the option to say fail/pass explicitly, or say it's in-between or just return the results and let the caller decide (however that happens). Also, FWIW, I think I'd rather push linting and really any code-level standardization to the primary Claude code agent call do "do", maybe via simple prompting. It's just not the critical part here. I could always run a neural/explicit code linter/cleaner later. But aside from that, again, just to reiterate, I want to be able to add "verifiers", which could also been seen as different personalities that review the changes, or reviewers with different roles, or stakeholders that review critically for how the changes affect their "stake" in the changes, e.g. maybe that's what we say they are "responsible for". I kind of like and am leaning towards the stakeholder language, maybe as a way to drive criticality and ownership of each item, through natural language. But maybe it doesn't matter. And I'm also still contemplating how to define the scope/definition/requirements for the verifier, because well, at the end of the day, the requirements are the test, so that's almost literally the key. Just not sure where to start on format, etc...
I'm also contemplating how to handle "configuring" each verifier to a particular level of "criticality", i.e., how critical of an assessment should it make? This would be sort of layered on top of (or below?) the actual structured levels of output (error, warning, info)...hopefully you get the picture.
ChatGPT said:
Thought for 29s
Need-to-Know

Do you want verifiers to have shell access (e.g., dotnet build) at all depths, or parent-only?

Where should verifier artifacts live? (e.g., runs/<run-id>/verifiers/<name>/…)

Any hard “must-block” classes besides build (e.g., license violations)?

Decision Map

Who controls pass/fail?

Output format from verifiers?

How to encode “criticality”?

Naming/model for review perspectives?

Verifier spec & registration format?

Lint/style scope (now)?

Options & Trade-offs

1) Pass/Fail control

A. Verifier decides (hard PASS/FAIL) — simple wiring; risks inconsistent policies.

B. Orchestrator-only — consistent; verifiers “dumb reporters”; some lost expertise.

C. Hybrid: verifier supplies decision_hint+confidence; orchestrator gates via policy ✔ — preserves expertise, keeps uniform control.

2) Output format

A. State JSON only (metrics/findings/rationales/artifacts) ✔ — minimal, robust to drift; orchestration applies rules.

B. Taxonomy-only (fixed codes) — compact, brittle early on.

C. State JSON + optional tags — richer, a bit heavier.

3) Criticality

A. Discrete levels (Blocker | Strict | Standard | Advisory) mapped to gating rules ✔ — clear mental model; easy to tune.

B. Weighted scores per verifier — flexible; harder to reason about.

C. Per-finding policy table — precise; verbose to maintain.

4) Perspective model

A. Stakeholders (Build, Product Fit, Architecture, Security, etc.) ✔ — matches your language; drives ownership.

B. Roles (reviewer, approver…) — generic, less meaningful.

C. Capabilities (lint, type-check…) — too low-level for “fit” verifiers.

5) Spec & registration

A. YAML manifest + Python plugin (prompt+runner) ✔ — declarative wiring + testable code.

B. Code-only plugin registration — fast, less portable.

C. Prompt-only verifiers — lowest friction, weak reproducibility.

6) Lint/style now

A. Advisory-only (default off; can enable) ✔ — aligns with “let Claude clean during Do”.

B. Strict gate — noisy early.

C. Skip entirely — lose signal for drift.

Recommendations

Go Hybrid control (1C), State JSON (2A), and Criticality levels (3A) to keep verifiers pluggable while centralizing policy.

Model perspectives as Stakeholders (4A) and register with YAML+plugin (5A) for clarity and evolvability.

Keep lint/style advisory-only and disabled by default (6A).

Decision Snapshot

1C — Verifier returns decision_hint+confidence; orchestrator makes the final gate.
2A — Verifier outputs State JSON (metrics, findings, rationales, artifacts).
3A — Criticality levels map to gating: Blocker/Strict/Standard/Advisory.
4A — Use “Stakeholder” naming to define responsibility.
5A — YAML manifest + Python plugin per verifier.
6A — Lint/style advisory-only, off by default.

Next Actions

Define VerifierContract v0.1 (JSON Schema):

{
  "verifier_id": "string",
  "stakeholder": "Build|TaskAlignment|BigPicture|Security|…",
  "decision_hint": "pass|fail|review|none",
  "confidence": 0.0,
  "severity_counts": {"error":0,"warning":0,"info":0},
  "metrics": {"alignment_score":0.0,"big_picture_score":0.0,"build_exit_code":0, "...": null},
  "findings": [
    {"id":"SPEC_DIVERGENCE","severity":"error","message":"...","evidence":"...","fingerprint":"..."}
  ],
  "rationales": ["..."],
  "artifacts": [{"path":"runs/...","purpose":"log|trace|diff"}],
  "duration_sec": 0
}


Policy & Criticality YAML (gates + thresholds):

criticality:
  Blocker: {block_on: ["decision_hint=fail","severity.error>0","build_exit_code!=0"]}
  Strict:  {min_scores: {alignment: 0.80, big_picture: 0.80}, block_on: ["severity.error>0"]}
  Standard:{min_scores: {alignment: 0.70, big_picture: 0.70}}
  Advisory:{never_block: true}

defaults:
  repeat_to_split: 2
  fingerprint_fields: ["findings[].id","findings[].message|first128"]

verifiers:
  - id: build
    stakeholder: Build
    criticality: Blocker
    exec: shell   # parent-only (assume); child: neural
    cmd: ["dotnet","build","-nologo"]
  - id: align
    stakeholder: TaskAlignment
    criticality: Standard
    exec: neural
    thresholds: {alignment: 0.70}
  - id: bigpic
    stakeholder: BigPicture
    criticality: Standard
    exec: neural
    thresholds: {big_picture: 0.70}
  - id: style
    stakeholder: Style
    criticality: Advisory
    enabled: false


Plugin interface (Python)

class Verifier:
    id: str
    stakeholder: str
    def prepare(self, spec, ctx, ws) -> dict: ...
    def run(self, inputs: dict) -> dict:  # returns VerifierContract JSON
        ...


Aggregator (pseudocode)

def gate(outputs, policy):
    # normalize + compute fingerprints
    decision = "pass"
    reasons = []
    for out in outputs:
        crit = policy.criticality[out.meta.criticality]
        if blocks(out, crit): decision = "retry"; reasons.append(out)
    if is_repeat(reasons, policy.repeat_to_split): return "split"
    return decision


Implement first three verifiers (build, align, bigpic) with minimal prompts and produce fingerprints.

Wire artifacts + commits per attempt; store each verifier’s JSON and raw input snapshot.

Open Questions

Do you want parent-only shell builds, with child-depth neural builds (fast heuristic), as previously sketched?

Any verifier that should start at Blocker besides Build (e.g., Security when enabled)?

Should decision_hint=review ever block at Standard, or only add warnings?