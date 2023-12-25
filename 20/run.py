#!/usr/bin/env python

import abc
import collections
import dataclasses
import enum
import pathlib
from typing import Deque

from rich import print as rprint


class Pulse(enum.Enum):
    LOW = 0
    HIGH = 1


@dataclasses.dataclass
class Message:
    pulse: Pulse
    source: str
    destination: str


@dataclasses.dataclass
class Module(abc.ABC):
    name: str
    destinations: list[str]

    @abc.abstractmethod
    def process(self, message: Message | None = None) -> list[Message]:
        ...


@dataclasses.dataclass
class FlipFlopModule(Module):
    on: bool = False

    def process(self, message: Message | None = None) -> list[Message]:
        assert message is not None
        pulse = message.pulse
        if pulse == Pulse.HIGH:
            return []
        else:
            if self.on:
                self.on = False
                return [
                    Message(Pulse.LOW, self.name, dest)
                    for dest in self.destinations
                ]
            else:
                self.on = True
                return [
                    Message(Pulse.HIGH, self.name, dest)
                    for dest in self.destinations
                ]


@dataclasses.dataclass
class ConjunctionModule(Module):
    inputs: dataclasses.InitVar[list[str]]
    input_states: dict[str, Pulse] = dataclasses.field(init=False)

    def __post_init__(self, inputs: list[str]) -> None:
        self.input_states = {input_: Pulse.LOW for input_ in inputs}

    def process(self, message: Message | None = None) -> list[Message]:
        assert message is not None
        self.input_states[message.source] = message.pulse
        if all(pulse == Pulse.HIGH for pulse in self.input_states.values()):
            return [
                Message(Pulse.LOW, self.name, dest)
                for dest in self.destinations
            ]
        else:
            return [
                Message(Pulse.HIGH, self.name, dest)
                for dest in self.destinations
            ]


@dataclasses.dataclass
class BroadcasterModule(Module):
    def process(self, message: Message | None = None) -> list[Message]:
        assert message is not None
        return [
            Message(message.pulse, self.name, dest)
            for dest in self.destinations
        ]


@dataclasses.dataclass
class ButtonModule(Module):
    def process(self, message: Message | None = None) -> list[Message]:
        assert message is None
        return [
            Message(Pulse.LOW, self.name, dest) for dest in self.destinations
        ]


def read_modules(path: str) -> dict[str, Module]:
    modules: dict[str, Module] = {}
    inputs = collections.defaultdict(list)
    conjunction_destinations = {}

    for line in pathlib.Path(path).read_text().splitlines():
        module_spec, destinations_str = line.split(" -> ")
        destinations = destinations_str.split(", ")

        if module_spec == "broadcaster":
            modules["broadcaster"] = BroadcasterModule(
                "broadcaster", destinations
            )
            continue

        name = module_spec[1:]
        for destination in destinations:
            inputs[destination].append(name)
        if module_spec.startswith("%"):
            modules[name] = FlipFlopModule(name, destinations)
        else:
            conjunction_destinations[name] = destinations

    for name, destinations in conjunction_destinations.items():
        modules[name] = ConjunctionModule(name, destinations, inputs[name])

    modules["button"] = ButtonModule("button", ["broadcaster"])
    return modules


def part1(modules: dict[str, Module]) -> int:
    highs = 0
    lows = 0
    for _ in range(1000):
        modules["button"].process()
        queue: Deque[Message] = collections.deque(modules["button"].process())
        while queue:
            message = queue.popleft()
            match message.pulse:
                case Pulse.HIGH:
                    highs += 1
                case Pulse.LOW:
                    lows += 1
            module = modules.get(message.destination)
            if module is not None:
                next_messages = module.process(message)
                for next_message in next_messages:
                    queue.append(next_message)

    return highs * lows


def main():
    assert part1(read_modules("example1.txt")) == 32000000
    assert part1(read_modules("example2.txt")) == 11687500
    assert part1(read_modules("input.txt")) == 743090292
    rprint("All tests passed.")


if __name__ == "__main__":
    main()
