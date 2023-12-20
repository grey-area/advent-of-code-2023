from pathlib import Path
import re
from collections import defaultdict, deque


class Module:
    @staticmethod
    def get_function(type, senders):
        if type == "broadcaster":
            def f(pulse, sender):
                return pulse
        elif type == "%":
            state = 0
            def f(pulse, sender):
                nonlocal state

                if not pulse:
                    state = 1 - state
                    return state
                else:
                    return None
        elif type == "&":
            memory = {sender: 0 for sender in senders}
            def f(pulse, sender):
                nonlocal memory

                memory[sender] = pulse
                if all(memory.values()):
                    return 0
                else:
                    return 1
        return f

    def __init__(self, type, senders, targets):
        self.f = self.get_function(type, senders)
        self.targets = targets

    def __call__(self, pulse, sender):
        return self.f(pulse, sender)


class Network:
    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()

        names, types, targets_list = zip(*map(self.parse_line, lines))
        senders = defaultdict(list)
        for name, targets in zip(names, targets_list):
            for target in targets:
                senders[target].append(name)

        self.modules = {name: Module(type, senders[name], targets) for name, type, targets in zip(names, types, targets_list)}
        self.pulses = deque()
        self.pulse_counts = [0, 0]

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
            self.pulse_counts[value] += 1
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

    @property
    def score(self):
        return self.pulse_counts[0] * self.pulse_counts[1]


if __name__ == "__main__":
    network = Network("input.txt")
    for _ in range(1000):
        network.push_the_button()
    print(network.score)