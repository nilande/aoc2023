from enum import Enum
import copy, math, functools

#
# Enum classes
#
class FlipFlopState(Enum):
    OFF = 0
    ON = 1

class Pulse(Enum):
    LOW = 0
    HIGH = 1

#
# Module Classes
#
class Module:
    def __init__(self, name: str, destination_modules: list):
        self.name = name
        self.destination_modules = destination_modules
        self.pulse_counter = { Pulse.LOW: 0, Pulse.HIGH: 0 }

    def debug_print(self, next_pulses: list):
        print(f'{self.name} sends: {next_pulses}')

    def get_next_pulses(self, pulse: Pulse):
        self.pulse_counter[pulse] += 1

    def get_pulse_counter(self):
        return self.pulse_counter

class FlipFlopModule(Module):
    def __init__(self, name: str, destination_modules: list):
        super().__init__(name, destination_modules)
        self.state = FlipFlopState.OFF

    def get_next_pulses(self, pulse: Pulse, *_):
        super().get_next_pulses(pulse)
        next_pulses = []
        if pulse == Pulse.HIGH: return next_pulses
        if self.state == FlipFlopState.ON:
            self.state = FlipFlopState.OFF
            for module_name in self.destination_modules: next_pulses.append((module_name, Pulse.LOW, self.name))
        else:
            self.state = FlipFlopState.ON
            for module_name in self.destination_modules: next_pulses.append((module_name, Pulse.HIGH, self.name))
        return next_pulses

class ConjunctionModule(Module):
    def __init__(self, name: str, destination_modules: list):
        super().__init__(name, destination_modules)
        self.most_recent_pulse = dict()
        self.most_recent_pulse_first_change_iteration = dict()
        self.mrp_output = False

    def add_input_module(self, input_module: str):
        self.most_recent_pulse[input_module] = Pulse.LOW
        self.most_recent_pulse_first_change_iteration[input_module] = None

    def activate_mrp_output(self):
        self.mrp_output = True

    def get_mrp_first_change_iteration(self):
        return self.most_recent_pulse_first_change_iteration

    def get_next_pulses(self, pulse: Pulse, input_module: str, iteration_counter):
        super().get_next_pulses(pulse)
        if self.mrp_output and self.most_recent_pulse[input_module] != pulse:
            if self.most_recent_pulse_first_change_iteration[input_module] is None: self.most_recent_pulse_first_change_iteration[input_module] = iteration_counter
        self.most_recent_pulse[input_module] = pulse
        next_pulses = []
        if all(mrp == Pulse.HIGH for mrp in self.most_recent_pulse.values()):
            for module_name in self.destination_modules: next_pulses.append((module_name, Pulse.LOW, self.name))
        else:
            for module_name in self.destination_modules: next_pulses.append((module_name, Pulse.HIGH, self.name))
        return next_pulses        

class BroadcastModule(Module):
    def get_next_pulses(self, pulse: Pulse, *_):
        super().get_next_pulses(pulse)
        next_pulses = []
        for module_name in self.destination_modules: next_pulses.append((module_name, pulse, self.name))
        return next_pulses

#
# Functions
#
def print_flipflop_states(modules: list):
    for name in modules:
        if type(modules[name]) is FlipFlopModule: print(f"Flip flop module '{modules[name].name}' has state '{modules[name].state}'")

output_pulse_counter = { Pulse.LOW: 0, Pulse.HIGH: 0 }
def press_button(modules, iteration_counter: int = None):
    pulse_queue = [ ('broadcaster', Pulse.LOW, 'button' ) ] # Button press
    while len(pulse_queue) > 0:
        name, pulse, input_module = pulse_queue.pop(0)
        if not name in modules:
            output_pulse_counter[pulse] += 1
            continue
        pulse_queue += modules[name].get_next_pulses(pulse, input_module, iteration_counter)

#
# Process input
#
with open('day 20/input.txt', 'r') as file:
    content = file.read()

modules = {} # Dictionary of module objects
input_modules = {}
for line in content.splitlines():
    mod_string, dest_string = line.split(' -> ')
    destinations = dest_string.split(', ')
    name = mod_string[1:] if mod_string[0] in ('%', '&') else mod_string
    match mod_string[0]:
        case '%': modules[name] = FlipFlopModule(name, destinations)
        case '&': modules[name] = ConjunctionModule(name, destinations)
        case _: modules[name] = BroadcastModule(name, destinations)
    for destination in destinations: input_modules.setdefault(destination, []).append(name)
for name in input_modules:
    if not name in modules: continue
    if type(modules[name]) is ConjunctionModule:
        for input_module in input_modules[name]: modules[name].add_input_module(input_module)

# Backup for Puzzle 2
modules_copy = copy.deepcopy(modules)

#
# Puzzle 1
#
for i in range(1000):
    press_button(modules)

high_pulses, low_pulses = output_pulse_counter[Pulse.HIGH], output_pulse_counter[Pulse.LOW]
for name in modules:
    high_pulses += modules[name].get_pulse_counter()[Pulse.HIGH]
    low_pulses += modules[name].get_pulse_counter()[Pulse.LOW]

print(f'Puzzle 1 solution is: {high_pulses * low_pulses} as a result of {low_pulses} low pulses and {high_pulses} high pulses')

#
# Puzzle 2
#

# Reset states
modules = modules_copy
modules['mf'].activate_mrp_output()
iteration_counter = 1
while any(mrp_iter is None for mrp_iter in modules['mf'].get_mrp_first_change_iteration().values()):
    press_button(modules, iteration_counter)
    iteration_counter += 1

result = functools.reduce(math.lcm, modules['mf'].get_mrp_first_change_iteration().values())

print(f'Puzzle 2 solution is: {result}')
