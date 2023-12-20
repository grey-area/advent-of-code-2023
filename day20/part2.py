from pathlib import Path
import re
from collections import defaultdict, deque
from copy import deepcopy
from math import lcm


class Module:
    def identity(self, pulse, sender):
        return pulse

    def flip_flop(self, pulse, sender):
        if not pulse:
            self.state = 1 - self.state
            return self.state
        else:
            return None

    def conjunction(self, pulse, sender):
        self.memory[sender] = pulse
        return not all(self.memory.values())

    def __init__(self, type, senders, targets):
        self.type = type
        self.targets = targets

        self.state = 0
        self.memory = {sender: 0 for sender in senders}

    def __call__(self, pulse, sender):
        if self.type == "broadcaster":
            return self.identity(pulse, sender)
        elif self.type == "%":
            return self.flip_flop(pulse, sender)
        else:
            return self.conjunction(pulse, sender)


class Network:
    def __init__(self, filename, broadcaster_destination_name):
        lines = Path(filename).read_text().splitlines()

        names, types, targets_list = zip(*map(self.parse_line, lines))
        senders = defaultdict(list)
        for name, targets in zip(names, targets_list):
            for target in targets:
                senders[target].append(name)

        self.modules = {name: Module(type, senders[name], targets) for name, type, targets in zip(names, types, targets_list)}
        self.modules["broadcaster"].targets = [broadcaster_destination_name]

        self.pulses = deque()
        self.jz_received_high = False
        self.set_initial_state()

    @property
    def state(self):
        return {name: (module.state, module.memory) for name, module in self.modules.items()}

    @property
    def in_initial_state(self):
        return self.state == self.initial_state

    def set_initial_state(self):
        self.initial_state = deepcopy(self.state)

    @staticmethod
    def parse_line(line):
        match = re.match(r"(.+) -> (.+)", line)
        lhs, rhs = match.groups()

        if lhs.startswith("&") or lhs.startswith("%"):
            type = lhs[0]
            name = lhs[1:]
        else:
            type = name = lhs
        targets = rhs.split(", ")
        return name, type, targets

    def process_queue(self):
        while self.pulses:
            receiver_name, sender, value = self.pulses.popleft()

            if receiver_name == "jz" and value:
                self.jz_received_high = True
            if receiver_name not in self.modules:
                continue

            module = self.modules[receiver_name]
            output_value = module(value, sender)

            if output_value is not None:
                new_pulses = [(target, receiver_name, output_value) for target in module.targets]
                self.pulses.extend(new_pulses)

    def push_the_button(self):
        self.pulses.append(("broadcaster", "button", 0))
        self.process_queue()

    def find_cycle_length(self):
        button_pushes = 0
        while not self.jz_received_high:
            self.push_the_button()
            button_pushes += 1
        return button_pushes

if __name__ == "__main__":
    """
    By inspection of the graph, there are four subgraphs that receive from the broadcaster
    and feed into node jz.
    rx will receive low when jz has received high from all four subgraphs,
    so compute LCM of the cycle lengths.
    """

    networks = [Network("input.txt", br_rx) for br_rx in ["qt", "rc", "qs", "bt"]]
    cycle_lengths = [network.find_cycle_length() for network in networks]
    print(lcm(*cycle_lengths))

    """
    The solution doesn't account for the fact that the cycles might not start at button push 0,
    but they do in this case.

    The states of the subgraphs are not the same between iterations of the cycle,
    but they must be equivalent wrt to the operations performed...?
    """