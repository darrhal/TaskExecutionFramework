I've been doing some brainstorming on how to create a more reliable, robust framework/workflow/whatever, for defining and executing software development tasks. To some degree this involves iteration of the "plan" as defined by me, and the better that is, and/or the smaller the task I give a code agent (claude code, cursor, whatever) is always better. But more so, this is me searching for a way to minimize that up-front step, or just really condense it and make it concise, and use a much more explicitly programmed outer loop of agent/model calls to either allow a task to be executed with greater precision, or allow a bigger task to be executed without my input. At this point in time, I have actual intentions to implement something out here, to try it all out. I imagine this process initially involves programming some sort of command-line tool to read in an instruction set, like a .md file, and execute it until complete or some sort of other stop signal is received (I haven't brainstormed "give up" paths or limits to retries or anything like that yet). To start out I would almost certainly use the claude code sdk as my "agent call". (look documentation for this any anything else up in the web, as needed). But I could also see calling an LLM model directly as a potential option in some cases. My framework/language of comfort for the app itself is c#/.net, but I might lean more towards python or typescript since that's what claude code supports. I have some familiarity with typescript, and a little python. I might lean towards python just because it's so ubiquitous in ML/everything now. Part of me just wants to wrap the python calls in c#, but maybe I should just take the python plunge. I do feel I should just keep the actual app simple enough to start out, so maybe using python would force that. Here are my brainstorming notes. I'm looking for some help distilling this down into something more organized, such that I can continue to iterate and improve on the ideas, and get a more narrow definition of what I'm actually going to try to build.



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


ChatGPT said:
Thought for 1m 3s

Awesome direction. Here’s a tight, buildable shape for what you described—an outer-loop harness that reads a task spec, drives an agent (start with Claude Code SDK), verifies results, and loops until success or stop.

1) Tech choices (pragmatic)

Language: Python (first) → smallest glue code with Claude Code SDK; TS also works; C# can shell the CLI later. SDKs: TS & Python; non-interactive “print mode” and flags are available via CLI/SDK (tools, permission modes, output formats). 
Anthropic
+1

Tooling: Use Claude Code tools + optional MCP servers for external systems (Jira, GitHub, Notion, etc.). 
Anthropic
+1

Stakeholders: Map to Claude Code Subagents (code-reviewer, debugger, security, etc.) with their own prompts/tools/contexts. 
Anthropic

2) MVP architecture

Inputs

task.md (YAML front-matter + body), settings.yml, optional .mcp.json, subagents in .claude/agents/.

Core state machine

PLAN → EXECUTE → VERIFY → DECIDE → (RETRY | SPLIT | DONE | GIVE_UP)

Execution

Call Claude Code via Python SDK (ClaudeSDKClient.query) or CLI with --print / --output-format json, set --allowedTools, --permission-mode (e.g., plan, acceptEdits), and working directory. 
Anthropic
+1

Verification (gatekeepers)

Fast, deterministic first: build/lint/tests; then heuristic/symbolic checks (style, arch rules, security).

Each verifier returns {severity: error|warning|info, messages:[…]}; aggregator decides next step.

Retry logic

If any error → one more single consolidated agent attempt (feed back all findings); on repeated failure, either SPLIT into sub-tasks or GIVE_UP per policy.

Persistence

Always emit a run log (runs/run-<timestamp>.md) and commit diffs when a verification boundary is passed (configurable), so you can see inner-loop progress.

3) Minimal task.md schema (copy/paste)
---
id: "TDX-42"
title: "Add filtered index to Tickets; remove key lookup"
repo: "./"
entrypoint: "Explain & implement changes"
context:
  goals:
    - "Eliminate key lookups on query X"
    - "Keep EF model consistent"
constraints:
  lang: "C#/.NET"
  style: ["FxCop/IDE analyzers clean", "Async only"]
  security: ["No secrets", "No PII logging"]
tools:
  allowed: ["Bash", "Read", "Edit", "WebSearch"]
  mcp_config: ".mcp.json"   # optional
subagents:
  - "code-reviewer"
  - "debugger"
acceptance:
  - "EF migration compiles"
  - "SELECT plan shows no Key Lookup"
  - "All unit tests green"
retry_policy:
  max_attempts: 3
  on_warning_retry: false
git:
  commit_on_success_gate: true
  branch: "agent/TDX-42"
---
Rationale / links / notes below the front-matter…


(Subagents format & storage mirror Claude Code’s agent files. 
Anthropic
)

4) Controller skeleton (Python)
import asyncio, subprocess, json, time, pathlib, yaml
from typing import List, Dict
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions  # pip install claude-code-sdk

def run(cmd, cwd="."):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

def load_task(path="task.md"):
    # parse YAML front-matter; keep body as context attachment
    import re
    t = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)$", t, re.S)
    meta = yaml.safe_load(m.group(1)); body = m.group(2)
    return meta, body

async def call_agent(prompt: str, meta: Dict, body: str):
    opts = ClaudeCodeOptions(
        system_prompt=f"You are a precise coding agent. Follow constraints: {meta.get('constraints',{})}",
        allowed_tools=meta.get("tools",{}).get("allowed", []),
        max_turns=5,  # tune
        permission_mode="acceptEdits",  # or "plan" for dry-run
        cwd=meta.get("repo","./"),
    )
    async with ClaudeSDKClient(options=opts) as client:
        await client.query(f"""{prompt}

<task-frontmatter>
{yaml.safe_dump(meta)}
</task-frontmatter>

<task-body>
{body}
</task-body>

Respond with a concise plan, the exact edits to apply, and commands to run for verification.""")
        # You can also stream; here we just wait for the result:
        out = []
        async for msg in client.receive_response():
            if hasattr(msg, "content"):
                for block in msg.content:
                    if hasattr(block, "text"): out.append(block.text)
        return "".join(out)

def verify(meta: Dict) -> List[Dict]:
    findings = []
    # Fast checks first (examples):
    if run(["git","diff","--quiet"]).returncode != 0:
        pass
    b = run(["dotnet","build","-warnaserror"]); 
    if b.returncode != 0: findings.append({"severity":"error", "msg":"Build failed", "detail": b.stderr[:1000]})
    t = run(["dotnet","test","-l:trx;LogFileName=test.trx"])
    if t.returncode != 0: findings.append({"severity":"error","msg":"Tests failed"})
    # Add linters/security (e.g., run(["pwsh","-c","Invoke-Semgrep ..."]))
    return findings

def decide(findings: List[Dict], policy) -> str:
    if any(f["severity"]=="error" for f in findings): return "RETRY"
    if any(f["severity"]=="warning" for f in findings) and policy.get("on_warning_retry"): return "RETRY"
    return "DONE"

async def main():
    meta, body = load_task()
    run(["git","switch","-c",meta["git"]["branch"]], cwd=meta["repo"])
    attempts = 0
    while attempts < meta["retry_policy"]["max_attempts"]:
        attempts += 1
        log = pathlib.Path(f"runs/run-{int(time.time())}.md"); log.write_text("starting…")
        result = await call_agent(meta["entrypoint"], meta, body)
        log.write_text(result)
        findings = verify(meta)
        decision = decide(findings, meta.get("retry_policy",{}))
        if decision == "DONE":
            if meta["git"].get("commit_on_success_gate"):
                run(["git","add","-A"]); run(["git","commit","-m", f"{meta['id']} pass {attempts}"])
            break
    else:
        print("GIVE_UP")

if __name__ == "__main__":
    asyncio.run(main())


(Using Claude Code Python SDK and options mirrors docs; permission_mode, allowed_tools, cwd, and CLI parity come from SDK/CLI references. 
Anthropic
+1
)

5) Mapping “stakeholders” → subagents & tools

Create .claude/agents/ files for code-reviewer, security, arch-review, etc., each with its own tool grants (e.g., Read,Grep,Edit,Bash) and concise checklists. Claude will delegate automatically or on request. 
Anthropic

Attach MCP servers (Jira, GitHub, Notion, Sentry…) via claude mcp add … and check in project-scoped .mcp.json when it’s safe. 
Anthropic

6) Control-flow contract (outer-loop)

Signals in → actions out

errors>0 → single consolidated retry (feed all findings; don’t “parallel-fix”).

warnings>0 & on_warning_retry=true → retry; else continue with “comments”.

attempts == max → GIVE_UP.

Optional SPLIT rule: if the same error class repeats twice, create child tasks (new task.md) for the agent.

7) Milestones (one week of evenings)

Bootstrap: Python project; task.md loader; run Claude Code in plan mode; write logs.

Edit + Gate: switch to acceptEdits; add build/test linters; basic retry logic; commit-on-gate.

Stakeholders: add subagents + security/arch checklists; MCP for Jira/GitHub if desired.

Task splitting: failure taxonomer → spawn child tasks; simple dashboard of runs.

8) Practical notes

Use --output-format json (or SDK result types) when you want structured steps/edits for auditing. 
Anthropic

Permission modes: plan for read-only planning, acceptEdits to apply changes without pausing. 
Anthropic

If you expect heavy usage, be aware of Claude Code weekly usage limits on Pro/Max as of late Aug 2025. 
Tom's Guide

If you want, I’ll turn this into a small repo scaffold (Python) with: task.md example, runner, verifier stubs, and two subagents (code-reviewer, debugger).

You said:
It's possible that would work. However, I want to back away from the approach of using sub-agents, and instead, try to explicitly program a little more of this outer loop myself. I want to be able to control this with a little more fidelity than the sub-agent spec provides, and notably, want to have the ability to have the "sub-agent" type calls be able to also call "sub-agents". I think what I'm going for is potentially a single top-level function (my main agent call) that is always the thing called for any agential function call, from the initial one defined by the user, to any function call within the sub-process. Also, I want to step back out and ideate on this more, before we dive into implementation details. Not sure on the format of that ideation, but sometimes code or pseod code can help, or maybe some n8n workflows, o mermaid diagrams, to help visualization. I'll let you decide.
ChatGPT said:
Thought for 34s

Got it. Let’s design a single-entry, recursive outer loop where every agentic call (top-level or nested) goes through the same function. No sub-agent feature dependency—just your orchestrator.

Principles (what you’re optimizing for)

One function to rule them all: AgentCall(spec, context) -> result. Every “sub-call” invokes this same function → uniform logs, budgets, and controls.

Separation of concerns: Generate → Apply → Verify → Decide. Each step is explicit and programmable.

Recursion, not parallelism: Child tasks are spawned only when policy says so; each child runs the same loop.

Signals, not vibes: Verifiers return structured error|warning|info findings with machine-actionable codes.

Deterministic boundaries: Commit or checkpoint at gates so retries are auditable.

Core contracts
TaskSpec (YAML front-matter + body)
id: "TDX-42"
title: "Remove key lookups on query X"
repo: "./"
constraints:
  language: "C#/.NET"
  style: ["IDExxx analyzers clean"]
  security: ["no secrets in config"]
acceptance:
  - "dotnet build passes"
  - "tests:green"
  - "plan:no KeyLookup"
tools:
  allowed: ["Read","Edit","Shell","WebSearch"]
budgets:
  max_attempts: 3
  max_depth: 3
  time_minutes: 20
policy:
  retry_on_warning: false
  split_after_repeated_error: 2   # same error code twice ⇒ spawn child TaskSpecs

AgentCall envelope (always the same)
{
  "spec": { /* TaskSpec parsed */ },
  "context": {
    "depth": 0,
    "parent_id": null,
    "run_id": "2025-08-17T17-53-11Z",
    "workspace": "./",
    "grants": ["Read","Edit","Shell"],
    "budgets": {"attempt": 1, "attempts_used": 0, "time_left": 1200},
    "snapshot": {"git_head": "abc123"}
  }
}

Verifier interface
type Finding = { severity:"error"|"warning"|"info", code:string, msg:string, detail?:string };
type Verifier = (ctx) => Promise<Finding[]>;

Outer-loop algorithm (single entry for all calls)
function AgentCall(spec, ctx):
  ensure ctx.depth <= spec.budgets.max_depth

  attempt = 0
  while attempt < spec.budgets.max_attempts and time_left(spec) > 0:
    attempt += 1
    save_checkpoint("pre-exec")  # git tag/commit or fs snapshot

    # 1) PLAN + GENERATE (LLM or tool call; your only “model step”)
    proposal = GeneratePlanAndEdits(spec, ctx) 
      # returns: {plan[], edits[], commands[], notes[]}

    # 2) APPLY
    apply(edits)                 # file edits; keep patch file
    run(commands.pre_verify?)    # optional prep

    # 3) VERIFY (sequence of verifiers you choose)
    findings = []
    findings += BuildVerifier()
    findings += TestVerifier()
    findings += StyleVerifier()
    findings += SecurityVerifier()
    findings += ArchVerifier()
    findings = normalize(findings)  # unique by code, sorted by severity

    record_log({attempt, proposal, findings})

    # 4) DECIDE
    if hasError(findings):
       if shouldSplit(findings, history, spec.policy):
         children = makeChildSpecs(spec, findings)   # each child narrower
         for child in children:
            AgentCall(child, ctx.with(depth+1, parent=spec.id))
         # after children, re-run verification at this level
         continue
       else:
         # RETRY once with consolidated feedback
         spec = specWithFeedback(spec, findings)     # inject structured issues
         revert_or_keep_partial(spec.policy)         # configurable
         continue

    if hasWarnings(findings) and spec.policy.retry_on_warning:
       spec = specWithFeedback(spec, findings)
       continue

    # SUCCESS GATE
    checkpoint("success")        # commit, tag, write run summary
    return {status:"ok", findings, location: current_commit()}

  # OUT OF BUDGET
  checkpoint("give_up")
  return {status:"give_up", findings: last_findings, attempts: attempt}

What the single “Generate” step does

Takes TaskSpec, prior feedback, and the current workspace state.

Produces exact edits (patches), shell commands to run, and a short plan.

You can implement this using any LLM or SDK, but your orchestrator treats it as a black box that returns structured outputs.

Findings taxonomy (keep it tiny and useful)

Build: BUILD_FAIL, MISSING_DEP

Test: TEST_FAIL, COVERAGE_DROP

Style: STYLE_LINT, ANALYZER_RULE_<ID>

Security: SECRET_LEAK, VULN_LIB, DANGEROUS_API

Arch: LAYER_VIOLATION, BOUNDARY_CROSS

Product: ACCEPTANCE_NOT_MET, SPEC_DIVERGENCE

These make policy programmable (e.g., “split if LAYER_VIOLATION repeats twice”).

Recursion & splitting (how nested calls stay sane)

Split trigger: same error code recurs ≥ N → synthesize child TaskSpec(s) with scoped goals (e.g., “extract DAL boundary”).

Child call: AgentCall(child, depth+1).

Backpressure: children inherit or reduce budgets; results are verified again at the parent level (no parallel mutation).

Mermaid visuals
Flow (outer loop)
flowchart TD
  A[AgentCall(spec,ctx)] --> B[Generate plan+edits]
  B --> C[Apply edits]
  C --> D[Run verifiers]
  D -->|errors| E{Split?}
  E -->|yes| F[Create child specs]
  F --> G[AgentCall(child,...)] --> D
  E -->|no| H[Retry with feedback] --> B
  D -->|warnings & retry_on_warning| H
  D -->|clean| I[Success gate -> commit/log]
  H --> B

Sequence (nested call)
sequenceDiagram
  participant Parent as AgentCall(parent)
  participant Gen as Generate()
  participant Verify as Verifiers[]
  participant Child as AgentCall(child)

  Parent->>Gen: spec + feedback
  Gen-->>Parent: edits + commands
  Parent->>Parent: apply edits
  Parent->>Verify: run all verifiers
  Verify-->>Parent: findings(error: LAYER_VIOLATION)
  Parent->>Parent: error repeats ⇒ split
  Parent->>Child: AgentCall(child-spec)
  Child-->>Parent: ok
  Parent->>Verify: re-verify parent
  Verify-->>Parent: clean → success gate

Minimal prompts (model-agnostic)

Generation prompt (single entry everywhere):

You are a precise coding agent. 
Constraints: <yaml constraints>
Goal: <title + acceptance>
Workspace: <path + brief tree>
Prior findings (structured): <JSON list of {code,msg,detail}>
Produce:
1) A short plan (≤5 steps).
2) Exact file edits as unified diffs.
3) Shell commands to run (if any).
Only return valid JSON with fields: plan[], edits[], commands[].


Verifier prompts (only if you choose LLM-based checks): keep them separate and stateless; return {severity, code, msg}.

n8n-style node view (optional)

ReadSpec → Generate → ApplyPatch → Verify(Build/Test/Style/Sec/Arch) → Decide

Decide branches to RetryWithFeedback or SpawnChildSpecs (loop to Generate), or SuccessGate.

Why this hits your goals

A single top-level function handles all calls and nested retries.

You get fine-grained control (budgets, split rules, gates).

It’s model-agnostic: swap Claude Code / OpenAI / local LLM without touching the loop.

Reproducible runs via checkpoints and structured logs.

Tight next steps (design-level)

Finalize Finding codes and Policy rules (that’s your control lever).

Decide gate commits (on success only vs. after each attempt).

Draft child-spec synthesis rules (how to carve errors into sub-goals).

Write stub Verifiers (build/test/style/security) that return structured findings.

Implement GeneratePlanAndEdits() with your chosen LLM—just ensure it outputs {plan,edits,commands} JSON.

If you want, I can turn the pseudocode + Mermaid into a small skeleton (language of your choice) using the exact contracts above.

You said:

I wrote down my reactions to this plan. I want you to play the role of facilitator here, to facilitate my "search" of the decisions I'm trying to make, by first thinking through what you think the key decision points are, then prompting me to make these decisions, until we've arrived at good place.
	- I want the permissions/grants to be global/inherited. I'm just trying to keep this simple to start out. It should be thought of as one agent call, with that sort of contract structure (some blend of the sdk interface and the sub-agent interface?). But I guess, as long as we can reliably construct a yaml for each sub-agent that, by default to start, just passes down the parameters that we want to be inherited, then it should work.
		- I suppose to get just a little fancier, we could have specify, for each/any param, and let's pick permissions to keep this example simple, a "parameter pass down figure-outer" (basically, configure some concrete implementation of a function that takes in some params, maybe just the parent permissions, and returns the child permissions. With the "inherit" implementation just returning the parent's...)...I realize this is already getting complicated, but the idea just keeps coming up, so I'm not sure what to think about this...maybe just put a pin in it and inherit by default, or only have one implementation available (inherit), but at least that gives us a little structure for the future...hmmm...maybe. I could go either way right now. I'm interested in teasing out the general idea more, but also want simplicity to just get something to try...
	- Need to think about this "budgets" concept.  Again, aiming for simplicity, maybe just some global timer/total agent calls per application instance? Or maybe even to start, just none. I guess I just need to brainstorm this a little more.
		- I suppose to start, we can keep it basically as is, I'll just configure these to be very high. Unless we can think of a better approach.
	- I like the split_after_repeated_error idea
	- How do the verifiers get built? Do these tie into the constraints/acceptance section? Let me read more to see if it's answered...
	- Git tag...is that a good way of having these temporary "commits"? No, not really. You'd just have multiple tags on a commit. I'm really looking for traceability of each agential step. And/or, to be able to rewind to any given point in the process, should I be watching it live, or come back to it later and realize it did a good job up until a certain point...
	- I'm still not sure on the verifiers...my idea was to have those be model/agent calls. Now, not necessarily our primary "AgentCall", but a "neural" call (or some combo of neural/explicitly programmed function)
	- Is GeneratePlanAndEdits the actual claude code agent call? I think it should be. I don't want it to return edits, and manage all that. I'm looking to offload this part of the process to the claude code/sdk agent.
		- And for future reference, let's just call it that. I'll just use the claude code sdk for now, for all my "neural" calls, maybe passing along certain parameters when I want it to just act as an llm with a response, or actually do something... And to distinguish it from our "AgentCall", let's re-brand that to "CodeTaskAgent".
		- After reading through further now, I think this "Produces **exact edits** (patches)" type approach could work, but I'm just not sure. I think that's the sweet spot of claude code, when it's given the correct level of responsibility, and something I don't want to re-invent that. I want to work with that, and work around its limitation, through my robustness wrapper. Actually that's worth noting loudly, because again this inversion of control thing keeps coming up. I just want to find a way to conceptually stick to "do this thing/return this data" type of function, where the function can be implemented via any concrete implementation, as long as it conforms to the interface. Maybe even my app/top-level agent method could be considered potentially to be implemented by my robustness framework, dependent on the configuration..yeah...I mean, once again, I'm going around in circles, but want to keep these thoughts here, in the hopes that the key ideas can be drawn out as we keep working on this...
	- I like the flow of the Decide section. In particular, the shouldSplit, otherwise try again. I don't see it yet, but I think the main input into "shouldSplit" should be how many retries have occurred for the current task.
	- I think I get the makeChildSpecs and specWithFeedback parts, and I like the general idea. Interested in the actual implementation now I think.
	- Let's just get rid of the test step for now
	- Let's keep the build step, but that should really almost be handled by some instructions. Maybe we could keep it simple with a claude code agent call that just says effectively "make sure this builds", with a strength indicator where in the higher-level layers, we want a guarantee, but in lower level ones, we just have claude code do a textual pass...
	- Let's ignore security for now
	- I really really want to figure out how to add a big picture evaluation (bigger/different than product/architectural evaluation) that focuses on how well these changes fit in to the parent tasks/description/spec, and the next task's description/spec. Again, not sure how to realize this dream, but it's key here...
ChatGPT said:
Thought for 47s

Love it — let’s lock this down by making a few crisp decisions. I’ll propose defaults that match what you already said; change anything you don’t like. Reply with something like: 1A, 2B(max_attempts=3,max_depth=3), 3A…

Decision points (pick one per line)

Call contract & inheritance

A (default): Single CodeTaskAgent(spec, ctx) everywhere. Global permissions/grants inherited by default. Keep a stub “pass-down strategy” interface but only ship inherit.

B: Same as A plus a second strategy slot (e.g., inherit | restrict) wired but not used yet.

C: Fully pluggable pass-down policy now.

Budgets / limits

A (default): Minimal: max_attempts, max_depth. No global timer for v1.

B: Add a hard time limit per call.

C: Start with no budgets (collect metrics only).

→ If A/B, give numbers (e.g., max_attempts=3, max_depth=3, time_limit=15m).

Verification set (v1)

A (default): Build + TaskAlignment + BigPictureFit. (No tests, no security.)

B: Same as A plus Style/Lint (quick heuristic).

C: Build only (push alignment checks to later).

Build policy

A (default): must-pass → instruct Claude Code to actually run the build and fix until green.

B: textual-verify (LLM evaluates build steps without running).

C: Depth-based: parent = must-pass, child = textual-verify.

Verifier implementation style

A (default): All 3 verifiers are neural (Claude Code) with structured outputs {severity, code, msg}.

B: Build neural (runs shell), TaskAlignment/BigPicture neural; Style (if enabled) is static tool.

C: Keep stubs only (log TODOs) and skip for v1.

Traceability / rewind strategy

A (recommended): Commit each attempt on a working branch (agent/<task-id>), with metadata file runs/<run-id>/attempt-<n>.json. Easy rewind.

B: Commit only on success gates; store per-attempt patch files in runs/.

C: Separate worktree per attempt (heavier but very clean isolation).

Retry & split rules

A (default): Retry until max_attempts. Split if the same error code recurs twice and attempt ≥ 2.

B: Split based on category (e.g., any ARCH_* twice).

C: No split in v1 (retry only).

→ If A/B, confirm thresholds (e.g., repeat=2).

Child spec synthesis

A (default): Auto-generate child specs from findings (one child per dominant error code), carrying inherited permissions and shrunk budgets.

B: Single consolidated child spec (aggregate all errors).

C: Defer child specs (log a TODO; human decides).

Task relationships for BigPictureFit

A (default): spec.parent_id and optional spec.next_ids[]; agent pulls short excerpts (snapshots) of those specs into context for evaluation.

B: Embed inline summaries of parent/next in the spec itself (no registry).

C: Only parent for now; ignore next.

Finding taxonomy (v1)

A (default): BUILD_FAIL, SPEC_DIVERGENCE, CONTEXT_MISALIGN (big-picture), STYLE_LINT (only if 3B).

B: Add LAYER_VIOLATION (arch) placeholder now.

C: Keep just BUILD_FAIL and SPEC_DIVERGENCE.

Claude Code usage

A (default): Claude Code is the only neural backend for now. Two modes:

mode: edit for the main “do the work”

mode: verify for each verifier

B: Allow a plain LLM (no tools) for TaskAlignment/BigPictureFit.

C: Abstract provider now (Claude default), keep switchable.

Commit message & logs

A (default): Per attempt: commit message [{task-id}] attempt {n}: {decision}; store plan.json, findings.json, and raw transcript under runs/<run-id>/attempt-<n>/.

B: Same but single run.json accumulating attempts.

C: Minimal logs (stdout + final findings).

Spec format

A (default): Markdown with YAML front-matter (id/title/constraints/acceptance/budgets/policy/parent/next).

B: Pure YAML file.

C: JSON.

Names

A (default): Orchestrator function name: CodeTaskAgent. Neural calls: ClaudeCode(mode).

B: Different names (tell me).

“Build via agent” scope

A (default): Permit Shell tool for dotnet build only (no network unless explicitly allowed).

B: Permit Shell broadly during verify.

C: No shell; rely on textual verification.

Optional quick knobs (defaults shown)

retry_on_warning=false

split_after_repeated_error=2

commit_on_every_attempt=true

child_budgets = { max_attempts: 2, max_depth: parent.max_depth-1 }

If you answer with your choices + any numbers, I’ll consolidate these into a v1 spec template and the exact prompts/contracts for CodeTaskAgent and ClaudeCode(mode).

You said:
1B, 2A, 3B, 4C, 5A. 6A. Still thinking. Just capturing my current decisions. Will let you know when I'm done.
ChatGPT said:
Thought for 18s

Perfect—captured. Here’s your current set, plus the remaining choices to lock in. Reply compactly (e.g., 2A(max_attempts=3,max_depth=3), 7A(repeat=2), 8A(child_attempts=2,child_depth=-1), 9A, 10A…).

Locked so far

1B — Single CodeTaskAgent with global/inherited grants; pass-down strategy slot wired (inherit | restrict), default inherit.

2A — Budgets: minimal (max_attempts, max_depth). → need numbers.

3B — Verifiers: Build + TaskAlignment + BigPictureFit + Style/Lint (quick).

4C — Build policy: parent = must-pass, children = textual-verify.

5A — Verifiers are neural (Claude Code) with structured {severity, code, msg}.

6A — Commit each attempt on a working branch + per-attempt run artifacts.

Decide the rest (with sane defaults)

Retry & split rules

A (default): Retry to max_attempts; split if the same error code repeats ≥2 times and attempt ≥ 2.
→ Provide threshold: repeat=? (suggest 2).

Child spec synthesis

A (default): One child per dominant error code; inherit grants, shrink budgets.
→ Provide child budgets (suggest child_attempts=2, child_depth = parent_depth-1).

BigPictureFit relationships

A (default): Use parent_id and optional next_ids[]; agent pulls short snapshots of those specs.

Finding taxonomy

A (default): BUILD_FAIL, SPEC_DIVERGENCE, CONTEXT_MISALIGN, STYLE_LINT.

Claude Code usage

A (default): Claude Code only: mode: edit (do work) and mode: verify (checks).

Commit message & logs

A (default): Commit msg [<task-id>] attempt <n>: <decision>; store plan.json, findings.json, transcript under runs/<run-id>/attempt-<n>/.

Spec format

A (default): Markdown + YAML front-matter.

Names

A (default): Orchestrator = CodeTaskAgent; neural = ClaudeCode(mode).

“Build via agent” scope

A (default): Allow Shell only for dotnet build (no network unless explicitly granted).

Also needed: numbers for #2A

Propose: max_attempts=3, max_depth=3.

Fire back your picks + numbers. I’ll consolidate into a v1 spec and prompt contracts next.

You said:
7A, 8A, 9A. I don't understand 10
ChatGPT said:
Thought for 26s

Locked: 7A, 8A, 9A ✅

Here’s what #10 “Finding taxonomy” means, plus a default to pick.

What it is

A short, fixed list of finding codes your verifiers emit.
These codes drive decisions (retry/split), logs, and metrics.
Message text can be free-form; the code is the key.

Default (10A) — small + useful now

BUILD_FAIL — the workspace likely doesn’t build (parent uses must-pass; children use textual-check but still emit BUILD_FAIL if failure is likely).

SPEC_DIVERGENCE — the change doesn’t satisfy this task’s acceptance/constraints.

CONTEXT_MISALIGN — change harms the parent/next task fit (your “big picture” check).

STYLE_LINT — obvious style/lint issues (still neural per your 5A).

Example finding payload

[
  {"severity":"error","code":"BUILD_FAIL","msg":"dotnet build failed on MyProj.csproj"},
  {"severity":"warning","code":"CONTEXT_MISALIGN","msg":"Change removes extension point needed by next task X"}
]


If you want an extra future-proof code for architecture later, add LAYER_VIOLATION, but it’s fine to keep it out for v1.

Still need your picks / numbers

2A (budgets): propose max_attempts=3, max_depth=3.

7A (threshold): propose repeat=2 (trigger split when the same code repeats twice).

8A (child budgets): propose child_attempts=2, child_depth = parent_depth-1.

Reply compactly, e.g.:

10A, 2A(max_attempts=3,max_depth=3), 7A(repeat=2), 8A(child_attempts=2,child_depth=-1)


Once you confirm, I’ll consolidate into the v1 spec + prompt contracts.

You said:
I want them to emit whatever the state is
ChatGPT said:
Thought for 33s

Got it — you want verifiers to emit the raw state, not force everything into a tiny code list. 👍
Let’s lock a design that keeps control-flow deterministic while letting verifiers “say what they see.”

Pick your “state-first” model

S2 (recommended): Open-state only, no mandatory codes

Verifiers return a state object per channel.

The orchestrator (not the verifier) maps state → decisions (retry/split/succeed) using rules/thresholds.

Benefits: simple verifiers, all logic lives in your outer loop.

S3: Open-state + tags

Same as S2, but verifiers may add free-form tags: [] (e.g., ["build:fail","style:naming"]) to help rules.

Slightly richer signals; still simple.

(If you still want a tiny taxonomy later, we can add derived codes in the aggregator, without changing verifiers.)

Minimal schemas (state the verifiers emit)
{
  "build": {
    "attempted": true,
    "exitCode": 1,
    "errors": [{"file":"X.cs","message":"CS1002 ; expected"}],
    "warnings": 5,
    "durationSec": 18.4,
    "logSample": "..."
  },
  "alignment": {
    "score": 0.62,            // 0..1 match to acceptance/constraints
    "rationales": ["Missing filtered index migration"]
  },
  "bigPicture": {
    "score": 0.55,            // 0..1 fit with parent/next specs
    "risks": ["Removes extension point needed by next task TDX-43"]
  },
  "style": {
    "issues": [
      {"rule":"IDE0058","count":3},
      {"rule":"SA1200","count":1}
    ]
  },
  "tags": ["build:fail","alignment:low"]   // include only if you choose S3
}

Orchestrator rule table (you control this)

Default thresholds you can tweak; no fixed “codes” required.

rules:
  - name: build-must-pass-parent
    when: "ctx.depth == 0"
    if: "state.build.attempted && state.build.exitCode != 0"
    action: "retry"
    fingerprint: "hash(errors.messages|join)"
    split_after_repeats: 2       # ← ties into your 7A

  - name: build-textual-child
    when: "ctx.depth > 0"
    if: "state.build.exitCode != 0 || state.alignment.score < 0.5"
    action: "retry"
    fingerprint: "hash(alignment.rationales|join)"
    split_after_repeats: 2

  - name: alignment-threshold
    if: "state.alignment.score < 0.70"
    action: "retry"

  - name: bigpicture-threshold
    if: "state.bigPicture.score < 0.70"
    action: "retry"

  - name: style-heuristic
    if: "sum(style.issues[*].count) > 8"
    action: "retry_on_warning_if_enabled"

defaults:
  retry_on_warning: false


Decision outputs still drive your chosen policies: retry, split (same-fingerprint repeat), success gate, etc.

Prompts for verifiers (neural, but stateful)

Build (parent depth):

Analyze the repo and ensure it builds. If allowed, run dotnet build. Return ONLY JSON build{attempted,exitCode,errors[],warnings,durationSec,logSample}. Do not classify; do not give advice.

TaskAlignment:

Compare changes against acceptance and constraints. Return ONLY JSON alignment{score:0..1,rationales[]}.

BigPictureFit:

Using snapshots of parent and next specs, judge fit. Return ONLY JSON bigPicture{score:0..1,risks[]}.

Style/Lint (quick):

Heuristically scan for obvious style issues. Return ONLY JSON style{issues:[{rule,count}]}.

(If you prefer S3, append: tags:[...] with short, kebab-case labels.)

How “repeat detection” works without codes

We compute a fingerprint from stable parts of the state (e.g., build error class names, top N messages, or rationale strings).

If the same fingerprint recurs ≥ repeat (you picked 7A), we split.

What I need from you (compact picks)

State model → choose one:

S2 (open-state only) [recommended]

S3 (open-state + tags)

Thresholds (ok to accept defaults):

alignment.score_min = 0.70

bigPicture.score_min = 0.70

style.total_issue_warn = 8

Fingerprint recipe (pick one):

F1 = hash of first 10 build error messages or alignment rationales (default)

F2 = hash of (files + error codes) only

F3 = custom (describe)

Still-open numbers

2A(max_attempts=?, max_depth=?) (suggest 3, 3)

7A(repeat=?) (suggest 2)

8A(child_attempts=?, child_depth=?) (suggest 2, -1 meaning “parent_depth-1”)

Reply like:

S2, thresholds(default), F1,
2A(max_attempts=3,max_depth=3), 7A(repeat=2),
8A(child_attempts=2,child_depth=-1)


I’ll consolidate everything into your v1 spec + the exact prompts/contracts for CodeTaskAgent and the four verifiers.

You said:
Let's swing back to this later. For the rest: 11A, 12A, 13A, 14A, 15B (no additional restrictions at all right now)
ChatGPT said:
Thought for 37s

Locked—nice. Here’s your current config and exactly what’s still open. I also dropped in a tiny spec skeleton you can copy later.

Decisions locked

1B Single CodeTaskAgent; global/inherited grants. Pass-down strategy slot wired (inherit | restrict), default inherit.

2A Budgets = minimal (numbers TBD).

3B Verifiers: Build + TaskAlignment + BigPictureFit + Style/Lint (quick).

4C Build policy: parent = must-pass, children = textual-verify.

5A Verifiers are neural (Claude Code) with structured JSON state.

6A Commit each attempt (+ per-attempt artifacts).

7A Retry to max; split on repeated same issue (threshold TBD).

8A Child spec per dominant issue; inherit grants; shrink budgets (TBD).

9A BigPicture uses parent_id + optional next_ids[] snapshots.

11A Claude Code only (mode: edit / mode: verify).

12A Commit msg & run artifacts per attempt.

13A Spec = Markdown + YAML front-matter.

14A Names: CodeTaskAgent / ClaudeCode(mode).

15B Shell broadly allowed during verify (no extra restrictions for now).

Still open (when you’re ready)

Budgets → 2A(max_attempts=?, max_depth=?) (suggest 3/3).

Split trigger → 7A(repeat=?) (suggest 2).

Child budgets → 8A(child_attempts=?, child_depth=?) (suggest 2, parent_depth−1).

State model for verifiers (your “emit whatever the state is”):

S2 Open-state only (no tags) [simple]

S3 Open-state + optional tags:[]

Optional thresholds (default proposal): alignment ≥ 0.70, bigPicture ≥ 0.70, style issue warn at 8.

Fingerprint recipe (for “same issue” repeat detection): F1 (hash top messages/rationales) recommended.

Minimal v1 spec skeleton (copy later)
---
id: "TASK-001"
title: "Example task"
repo: "./"
constraints:
  language: "C#/.NET"
acceptance:
  - "Build succeeds"
  - "Meets acceptance bullets above"
grants:
  inherit: true
budgets:
  max_attempts: TBD
  max_depth: TBD
policy:
  retry_on_warning: false
  split_after_repeated_error: TBD
relationships:
  parent_id: null
  next_ids: []
orchestrator:
  build_policy: { parent: "must-pass", child: "textual-verify" }
  verify_set: ["build","alignment","bigPicture","style"]
  state_model: S2|S3
  fingerprint: F1|F2
logging:
  commit_each_attempt: true
  runs_dir: "runs"
---
(Notes/rationale here…)

Tiny controller reminders (per your picks)

Every attempt commits on agent/<task-id> with artifacts under runs/<run-id>/attempt-<n>/.

ClaudeCode(mode=edit) does the work; ClaudeCode(mode=verify) returns raw JSON state (no forced codes).

Shell is allowed broadly during verify (log every command/exits for traceability).

When you’re ready to resume, reply compactly, e.g.:

2A(3,3), 7A(repeat=2), 8A(child_attempts=2,child_depth=-1),
S2, thresholds(default), fingerprint(F1)

You said:
Just pick something for all those, as long as I can change them later. But we really need to dive into the details of the verifiers, how we make sure that they understand their criteria and access to the evaluation.
ChatGPT said:
Thought for 36s

Great—I'll pick sensible defaults you can tweak later, then go deep on verifier design so they “know what to check” and have the right access.

Defaults I’m locking in (editable)

Budgets: max_attempts=3, max_depth=3.

Split trigger: same-issue repeat = 2 (after attempt ≥ 2).

Child budgets: child_attempts=2, child_depth = parent_depth-1.

Verifier state model: S2 (open state; no mandatory codes).

Thresholds: alignment ≥ 0.70, bigPicture ≥ 0.70, style warn if total issues > 8.

Fingerprint recipe: F1 (hash top N messages/rationales).

Verifier design (how they understand criteria & get context)
0) Common contract (all verifiers)

Call: ClaudeCode(mode="verify", allowed_tools=["Read","Shell"], no edits)
Input payload (JSON you attach):

{
  "spec": {
    "id": "TASK-001",
    "title": "…",
    "acceptance": ["…"],
    "constraints": {"language":"C#/.NET", "style":["…"]},
    "relationships": {"parent_id": null, "next_ids": []}
  },
  "context": {
    "depth": 0,
    "attempt": 1,
    "budgets": {"max_attempts":3,"max_depth":3}
  },
  "workspace": {
    "root": "./",
    "tree": ["src/…", "tests/…", "MyApp.sln", "…"],      // truncated list
    "changed_files": ["src/Foo.cs", "…"],
    "diff_unified": "…",                                  // unified diff since last checkpoint (trim big files)
    "summaries": [{"path":"src/Foo.cs","summary":"…"}]    // optional short semantic summaries of large files
  },
  "relations": {
    "parent_excerpt": { "id":"TASK-000", "goals":[…], "acceptance":[…], "notes":"…" },
    "next_excerpts": [ { "id":"TASK-002", "goals":[…] }, { "id":"TASK-003", "goals":[…] } ]
  },
  "policy": {
    "build":{"mode": "must-pass|textual-verify"},         // set by depth per your 4C
    "thresholds":{"alignment":0.70,"bigPicture":0.70,"styleWarnTotal":8}
  }
}


Output (state-only JSON): each verifier returns a single top-level key with a strict schema (below). No prose.

1) Build verifier
Parent depth (must-pass)

Access: Shell (dotnet build or project-specific build command); Read for build logs.

Prompt (strict JSON):

You are verifying whether the repo builds.

- You MAY run shell commands (e.g., 'dotnet build') in the workspace root.
- Return ONLY this JSON object:

{
  "build": {
    "attempted": true|false,
    "exitCode": <int>,
    "errors": [{"file":"…","message":"…"}],
    "warnings": <int>,
    "durationSec": <number>,
    "executed": ["<cmd>", "..."],
    "logSample": "<first/last ~20 lines or key excerpt>"
  }
}

Do not include any other text.

Child depth (textual-verify)

Same schema, but the model does not run the build; instead it infers likely status from the diff and project files:

- Do NOT run shell.
- Infer whether the project likely builds from the diff, csproj/sln changes, and acceptance.
- Use exitCode=0 if likely clean; else 1 and include reasons in errors[].


Aggregation (orchestrator) default

Parent: exitCode != 0 → retry.

Child: exitCode != 0 OR alignment < 0.5 → retry.

Fingerprint: hash of top 10 error messages (file+first 120 chars).

2) TaskAlignment verifier

Checks the task against this spec’s acceptance & constraints using only repo state + diff.

Prompt (strict JSON):

Assess how well the latest changes satisfy the current task’s acceptance and constraints.

Return ONLY:
{
  "alignment": {
    "score": 0.0..1.0,                 // overall fit
    "coverage": [
      {"acceptance":"<bullet 1>", "met": true|false, "why":"…"},
      {"acceptance":"<bullet 2>", "met": true|false, "why":"…"}
    ],
    "constraint_issues": [
      {"constraint":"style: …", "impact":"low|med|high", "why":"…"}
    ],
    "rationales": ["…","…"]
  }
}
No other text.


Aggregation defaults

alignment.score < 0.70 → retry

0.70–0.89 → warning

Fingerprint: hash of coverage.met==false bullets + constraint_issues.constraint.

3) BigPictureFit verifier

Judges whether this change helps/hurts the parent and next tasks.

Prompt (strict JSON):

Evaluate big-picture fit:
- Does this change enable the parent task goals?
- Does it set up the listed next tasks?

Return ONLY:
{
  "bigPicture": {
    "score": 0.0..1.0,
    "supports_parent": true|false,
    "supports_next": [{"id":"TASK-002","supports":true|false,"risk":"…"}],
    "risks": ["…","…"],
    "rationales": ["…"]
  }
}


Aggregation defaults

bigPicture.score < 0.70 → retry

Fingerprint: hash of risks[].

4) Style/Lint (quick, neural)

Heuristic pass on diff only (fast, low-noise).

Prompt (strict JSON):

Scan the unified diff for obvious style/lint issues. Focus on clarity and common C#/.NET analyzer patterns.
Return ONLY:
{
  "style": {
    "issues": [
      {"rule":"IDE0058","count":3,"examples":["line refs or short snippets"]},
      {"rule":"SA1200","count":1,"examples":["…"]}
    ],
    "total": <sum of counts>
  }
}


Aggregation defaults

total > 8 → warning (respect retry_on_warning=false for now)

Fingerprint: hash of top 3 rule ids.

5) Orchestrator combine -> decision

Merge the four JSON fragments into state.

Apply rule table:

parent build fail → retry; repeat (same fingerprint) twice → split.

alignment/bigPicture thresholds as above.

style above threshold → warning (no retry unless you flip the flag).

On retry: embed a compact feedback JSON (not prose) back into ClaudeCode(mode="edit"):

{
  "feedback": {
    "build": {"topErrors":[{"file":"…","message":"…"}]},
    "alignment": {"notMet":[ "<bullet>","<bullet>" ]},
    "bigPicture": {"risks":[ "…","…" ]},
    "style": {"topRules":[ "IDE0058","SA1200" ]}
  }
}

6) What the orchestrator must assemble for verifiers

Workspace pack

tree: first ~300 entries; always include *.sln, *.csproj, /src, /tests.

changed_files: from git diff --name-only.

diff_unified: git diff --unified=0 (cap by bytes, include only changed hunks).

Optional summaries: for any file > N KB, add a short summary (produced by ClaudeCode in a separate prep call).

Relations pack

parent_excerpt + next_excerpts: {id, title, goals (≤5), acceptance (≤5), notes≤600 chars}—never dump entire specs.

Policy pack

build mode by depth (must-pass at depth 0; textual-verify otherwise).

thresholds & fingerprints.

Tooling

In verify calls, allow Shell broadly (per your 15B) but the agent won’t edit files; log every executed command + exit code.

7) Minimal orchestrator code sketch (verify phase)
def run_verifiers(pack):
    results = {}
    for name, prompt in VERIFIER_PROMPTS.items():
        out = ClaudeCode.verify(prompt, input_json=pack,
                                allowed_tools=["Read","Shell"],
                                edits_allowed=False,
                                timeout_sec=120)
        results.update(out)  # each returns {"build":{…}} or {"alignment":{…}}, etc.
    return results

8) Observability (so verifiers are debuggable)

Save each verifier’s input pack and output state under runs/<run-id>/attempt-<n>/<verifier>.json.

Keep executed shell commands in build.state.executed.

Compute and store fingerprint per verifier for split logic.

If you want, I can turn these prompts and JSON schemas into a small contracts file (verifiers.yml) plus a Python stub that assembles the pack, calls Claude Code in verify mode, and writes artifacts.

You said:
Summarize the most critical pieces of this conversation
ChatGPT said:
Thought for 11s

Here’s the tight core of what we decided and how it fits together.

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

You said:

Please condense this conversation into a **faithful, compressed interaction** between me (the user) and you (the assistant).

This is **not** a summary or narrative recap. Instead, rewrite the conversation as a **multi-turn dialogue** that retains the key flow of questions, clarifications, and answers across multiple back-and-forth turns.

**Purpose:** The result will be used to initialize a new conversation with another assistant. It should allow that assistant to fully understand:
- What I was trying to accomplish
- The core steps we explored
- Key clarifications and insights along the way
- Where we left off

**Requirements:**
- Keep the conversation in **dialogue format**:
    User: [My input]  Assistant: [Your response]  User: [My follow-up]  Assistant: [Follow-up reply]  ...
- Preserve **multiple rounds** of interaction, not just one question and one answer
- Omit fluff, repetition, or tangents—but **do not collapse important clarifications into a single line**
- The tone, intent, and structure should match the original conversation, just with tighter phrasing and fewer redundant turns
- The first (1) pair of interactions in the conversation, and the last (1) pair of interactions in the conversation, should remain exactly as they were. Do not summarize or condense them. This ensures that the original intent and starting point, along with the recent specific discussions in the conversation, are retained.

**Goal:** After reading the compressed dialogue, a new assistant should be able to jump in and continue naturally, as if it had followed the original thread.
ChatGPT said:
Thought for 23s

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
---
id: "TDX-42"
title: "Add filtered index to Tickets; remove key lookup"
repo: "./"
entrypoint: "Explain & implement changes"
context:
  goals:
    - "Eliminate key lookups on query X"
    - "Keep EF model consistent"
constraints:
  lang: "C#/.NET"
  style: ["FxCop/IDE analyzers clean", "Async only"]
  security: ["No secrets", "No PII logging"]
tools:
  allowed: ["Bash", "Read", "Edit", "WebSearch"]
  mcp_config: ".mcp.json"   # optional
subagents:
  - "code-reviewer"
  - "debugger"
acceptance:
  - "EF migration compiles"
  - "SELECT plan shows no Key Lookup"
  - "All unit tests green"
retry_policy:
  max_attempts: 3
  on_warning_retry: false
git:
  commit_on_success_gate: true
  branch: "agent/TDX-42"
---
Rationale / links / notes below the front-matter…


(Subagents format & storage mirror Claude Code’s agent files. )

4) Controller skeleton (Python)
import asyncio, subprocess, json, time, pathlib, yaml
from typing import List, Dict
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions  # pip install claude-code-sdk

def run(cmd, cwd="."):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

def load_task(path="task.md"):
    # parse YAML front-matter; keep body as context attachment
    import re
    t = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)$", t, re.S)
    meta = yaml.safe_load(m.group(1)); body = m.group(2)
    return meta, body

async def call_agent(prompt: str, meta: Dict, body: str):
    opts = ClaudeCodeOptions(
        system_prompt=f"You are a precise coding agent. Follow constraints: {meta.get('constraints',{})}",
        allowed_tools=meta.get("tools",{}).get("allowed", []),
        max_turns=5,  # tune
        permission_mode="acceptEdits",  # or "plan" for dry-run
        cwd=meta.get("repo","./"),
    )
    async with ClaudeSDKClient(options=opts) as client:
        await client.query(f"""{prompt}

<task-frontmatter>
{yaml.safe_dump(meta)}
</task-frontmatter>

<task-body>
{body}
</task-body>

Respond with a concise plan, the exact edits to apply, and commands to run for verification.""")
        # You can also stream; here we just wait for the result:
        out = []
        async for msg in client.receive_response():
            if hasattr(msg, "content"):
                for block in msg.content:
                    if hasattr(block, "text"): out.append(block.text)
        return "".join(out)

def verify(meta: Dict) -> List[Dict]:
    findings = []
    # Fast checks first (examples):
    if run(["git","diff","--quiet"]).returncode != 0:
        pass
    b = run(["dotnet","build","-warnaserror"]); 
    if b.returncode != 0: findings.append({"severity":"error", "msg":"Build failed", "detail": b.stderr[:1000]})
    t = run(["dotnet","test","-l:trx;LogFileName=test.trx"])
    if t.returncode != 0: findings.append({"severity":"error","msg":"Tests failed"})
    # Add linters/security (e.g., run(["pwsh","-c","Invoke-Semgrep ..."]))
    return findings

def decide(findings: List[Dict], policy) -> str:
    if any(f["severity"]=="error" for f in findings): return "RETRY"
    if any(f["severity"]=="warning" for f in findings) and policy.get("on_warning_retry"): return "RETRY"
    return "DONE"

async def main():
    meta, body = load_task()
    run(["git","switch","-c",meta["git"]["branch"]], cwd=meta["repo"])
    attempts = 0
    while attempts < meta["retry_policy"]["max_attempts"]:
        attempts += 1
        log = pathlib.Path(f"runs/run-{int(time.time())}.md"); log.write_text("starting…")
        result = await call_agent(meta["entrypoint"], meta, body)
        log.write_text(result)
        findings = verify(meta)
        decision = decide(findings, meta.get("retry_policy",{}))
        if decision == "DONE":
            if meta["git"].get("commit_on_success_gate"):
                run(["git","add","-A"]); run(["git","commit","-m", f"{meta['id']} pass {attempts}"])
            break
    else:
        print("GIVE_UP")

if __name__ == "__main__":
    asyncio.run(main())


(Using Claude Code Python SDK and options mirrors docs; permission_mode, allowed_tools, cwd, and CLI parity come from SDK/CLI references. )

5) Mapping “stakeholders” → subagents & tools

Create .claude/agents/ files for code-reviewer, security, arch-review, etc., each with its own tool grants (e.g., Read,Grep,Edit,Bash) and concise checklists. Claude will delegate automatically or on request.

Attach MCP servers (Jira, GitHub, Notion, Sentry…) via claude mcp add … and check in project-scoped .mcp.json when it’s safe.

6) Control-flow contract (outer-loop)

Signals in → actions out

errors>0 → single consolidated retry (feed all findings; don’t “parallel-fix”).

warnings>0 & on_warning_retry=true → retry; else continue with “comments”.

attempts == max → GIVE_UP.

Optional SPLIT rule: if the same error class repeats twice, create child tasks (new task.md) for the agent.

7) Milestones (one week of evenings)

Bootstrap: Python project; task.md loader; run Claude Code in plan mode; write logs.

Edit + Gate: switch to acceptEdits; add build/test linters; basic retry logic; commit-on-gate.

Stakeholders: add subagents + security/arch checklists; MCP for Jira/GitHub if desired.

Task splitting: failure taxonomer → spawn child tasks; simple dashboard of runs.

8) Practical notes

Use --output-format json (or SDK result types) when you want structured steps/edits for auditing.

Permission modes: plan for read-only planning, acceptEdits to apply changes without pausing.

If you expect heavy usage, be aware of Claude Code weekly usage limits on Pro/Max as of late Aug 2025.

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