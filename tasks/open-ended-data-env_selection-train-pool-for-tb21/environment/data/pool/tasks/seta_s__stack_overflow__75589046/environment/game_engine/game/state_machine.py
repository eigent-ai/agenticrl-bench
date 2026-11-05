"""Hierarchical state machine for entity behaviors.

Each entity can have a StateMachine that manages transitions between
State objects.  Guards on transitions can prevent illegal state changes.
"""

import logging

logger = logging.getLogger("state_machine")


class State:
    """Base class for a single state in the machine."""

    name = "base"

    def __init__(self, entity, machine):
        self.entity = entity
        self.machine = machine
        self.elapsed = 0.0

    def enter(self):
        self.elapsed = 0.0

    def exit(self):
        pass

    def tick(self, dt):
        self.elapsed += dt

    def can_exit(self):
        return True


class IdleState(State):
    name = "idle"

    def __init__(self, entity, machine, duration=2.0):
        super().__init__(entity, machine)
        self.duration = duration

    def tick(self, dt):
        super().tick(dt)
        if self.elapsed >= self.duration:
            self.machine.transition_to("charge")


class ChargeState(State):
    name = "charge"

    def __init__(self, entity, machine, duration=0.8):
        super().__init__(entity, machine)
        self.duration = duration

    def tick(self, dt):
        super().tick(dt)
        if self.elapsed >= self.duration:
            self.machine.transition_to("attack")


class AttackState(State):
    name = "attack"

    def __init__(self, entity, machine, on_attack=None):
        super().__init__(entity, machine)
        self.on_attack = on_attack
        self._attacked = False

    def enter(self):
        super().enter()
        self._attacked = False

    def tick(self, dt):
        super().tick(dt)
        if not self._attacked:
            if self.on_attack:
                self.on_attack(self.entity)
            self._attacked = True
            self.machine.transition_to("cooldown")


class CooldownState(State):
    name = "cooldown"

    def __init__(self, entity, machine, duration=1.5):
        super().__init__(entity, machine)
        self.duration = duration

    def tick(self, dt):
        if self.elapsed >= self.duration:
            self.machine.transition_to("idle")
        self.elapsed += dt

    def can_exit(self):
        physics = self.entity.get_property("physics_body")
        if physics and not physics.is_on_floor():
            return False
        return True


class StateMachine:
    """Manages a set of named states and guarded transitions."""

    def __init__(self, entity):
        self.entity = entity
        self._states = {}
        self._current = None
        self._log = []

    def add_state(self, state):
        self._states[state.name] = state

    def start(self, state_name):
        self._current = self._states[state_name]
        self._current.enter()
        self._log.append(("enter", state_name, 0))

    @property
    def current_state(self):
        return self._current.name if self._current else None

    def transition_to(self, target_name):
        if target_name not in self._states:
            logger.error("Unknown state: %s", target_name)
            return False

        if self._current and not self._current.can_exit():
            logger.warning(
                "State transition failed: %s -> %s for %s",
                self._current.name, target_name, self.entity.name,
            )
            return False

        if self._current:
            self._current.exit()

        self._current = self._states[target_name]
        self._current.enter()
        self._log.append(("enter", target_name, self._current.elapsed))
        return True

    def tick(self, dt):
        if self._current:
            self._current.tick(dt)

    def get_log(self):
        return list(self._log)
