#!/usr/bin/env python3

def execute_task(task_tree, environment):
    while has_pending_tasks(task_tree):
        task = find_next_task(task_tree)
        
        # Act (atomic only)
        if task and task["type"] == "atomic":
            result = execute(task)
            commit(f"ACT: {task['id']}")
        
        # Assess (all tasks)
        if task:
            observations = assess(task, task_tree)
            
            # Adapt (all tasks)
            task_tree = adapt(task, observations, task_tree)
            commit(f"ADAPT: {task['id']}")

# Stubs
def has_pending_tasks(tree): return False
def find_next_task(tree): pass
def execute(task): pass
def assess(task, tree): pass
def adapt(task, obs, tree): return tree
def commit(msg): print(msg)

if __name__ == "__main__":
    execute_task({}, ".")