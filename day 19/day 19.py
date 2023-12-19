import time

def get_workflows(workflows_raw: list):
    workflows = dict()
    for line in workflows_raw:
        workflow_name, workflow_rules_raw = line[:-1].split('{')
        workflow_rules = workflow_rules_raw.split(',')
        this_workflow = list()
        for workflow_rule in workflow_rules[:-1]:
            workflow_rule_test, workflow_rule_goto = workflow_rule.split(':')
            this_workflow.append((workflow_rule_test[0], workflow_rule_test[1], int(workflow_rule_test[2:]), workflow_rule_goto))
        
        # Optimization: Clean up unnecessary rules in the end of a workflow
        while len(this_workflow) > 0 and this_workflow[-1][3] == workflow_rules[-1]: this_workflow.pop()

        workflows[workflow_name] = this_workflow + [workflow_rules[-1]]

    return workflows

def is_part_rating_accepted(part_rating, workflows):
    cur_workflow = 'in'
    # debug_workflow_steps = []
    exit_steps = {'A', 'R'}
    while cur_workflow not in exit_steps:
        # debug_workflow_steps.append(cur_workflow)
        for step in workflows[cur_workflow]:
            if type(step) is tuple: # Rule to be evaluated
                match step[1]:
                    case '<':
                        if part_rating[step[0]] < step[2]:
                            cur_workflow = step[3]
                            break
                    case '>':
                        if part_rating[step[0]] > step[2]:
                            cur_workflow = step[3]
                            break
            else: cur_workflow = step

    # debug_workflow_steps.append(cur_workflow)
    # print(f'{part_rating}: {" -> ".join(debug_workflow_steps)}')
    return cur_workflow == 'A'

def get_accepted_part_ratings_sum(part_ratings_raw: list, workflows: dict):
    acc = 0
    for line in part_ratings_raw:
        line_list = line[1:-1].split(',')
        part_rating = {'x': int(line_list[0][2:]), 'm': int(line_list[1][2:]), 'a': int(line_list[2][2:]), 's': int(line_list[3][2:])}
        if is_part_rating_accepted(part_rating, workflows):
            acc += sum(part_rating.values())
    return acc


def get_accepted_part_rating_combinations(part_rating_span: dict, workflows: dict):
    process_queue = [ ('in', part_rating_span) ]
    finalized_spans = {'A': [], 'R': []}

    while len(process_queue) > 0:
        current = process_queue.pop(0)
        workflow = current[0]
        if workflow in ('A', 'R'):
            finalized_spans[workflow].append(current[1])
            continue

        for step in workflows[workflow]:
            if type(step) is tuple:
                current_range = current[1][step[0]]
                match step[1]:
                    case '<':
                        if current_range[0] < step[2] <= current_range[1]:
                            extracted = current[1].copy()
                            extracted[step[0]] = (current_range[0], step[2]-1)
                            process_queue.append((step[3], extracted))
                            current[1][step[0]] = (step[2], current_range[1])
                        elif current_range[1] < step[2]:
                            process_queue.append((step[3], current[1]))
                            break
                    case '>':
                        if current_range[0] <= step[2] < current_range[1]:
                            extracted = current[1].copy()
                            extracted[step[0]] = (step[2]+1, current_range[1])
                            process_queue.append((step[3], extracted))
                            current[1][step[0]] = (current_range[0], step[2])
                        elif step[2] < current_range[0]:
                            process_queue.append((step[3], current[1]))
                            break
            else:
                process_queue.append((step, current[1]))

    result = 0
    for span in finalized_spans['A']:
        acc = 1
        for l, r in span.values():
            acc *= r - l + 1
        result += acc

    return result


#
# Process input
#
with open('day 19/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
start_time = time.time()
workflows_raw, part_ratings_raw = content.split('\n\n')
workflows = get_workflows(workflows_raw.splitlines())
print(f'Puzzle 1 solution is: {get_accepted_part_ratings_sum(part_ratings_raw.splitlines(), workflows)} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2
#
start_time = time.time()
part_rating_span = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
print(f'Puzzle 2 solution is: {get_accepted_part_rating_combinations(part_rating_span, workflows)} (in {time.time() - start_time:.3f} seconds)')