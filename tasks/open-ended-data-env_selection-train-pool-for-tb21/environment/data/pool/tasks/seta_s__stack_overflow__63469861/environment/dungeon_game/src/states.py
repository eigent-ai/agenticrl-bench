from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class GameState(ABC):
    """Abstract base class for all game states."""

    @abstractmethod
    def handle_event(self, event: str) -> Optional["GameState"]:
        """Process an event. Return the next state, or None to remain."""

    @abstractmethod
    def get_state_name(self) -> str:
        """Return a short name identifying this state."""


class PlayingState(GameState):
    def __init__(self) -> None:
        self.score: int = 0
        self.level: int = 1
        self._menu_state: Optional[GameState] = None
        self._paused_state: Optional[GameState] = None

    # ------------------------------------------------------------------
    # Wiring helpers (called by Game.__init__ to break circular deps)
    # ------------------------------------------------------------------
    def set_menu_state(self, menu_state: GameState) -> None:
        self._menu_state = menu_state

    def set_paused_state(self, paused_state: GameState) -> None:
        self._paused_state = paused_state

    def reset(self) -> None:
        """Return this state to its post-construction defaults."""
        self.score = 0
        self.level = 1

    def handle_event(self, event: str) -> Optional[GameState]:
        if event == "collect":
            self.score += 2
            return None
        if event == "pause":
            return self._paused_state
        if event == "die":
            self.reset()
            return self._menu_state
        if event == "quit_to_menu":
            self.reset()
            return self._menu_state
        return None

    def get_state_name(self) -> str:
        return "playing"


class MenuState(GameState):
    def __init__(self, playing_state: PlayingState) -> None:
        self._playing_state = playing_state

    def handle_event(self, event: str) -> Optional[GameState]:
        if event == "start":
            return self._playing_state
        return None

    def get_state_name(self) -> str:
        return "menu"


class PausedState(GameState):
    def __init__(self, menu_state: MenuState, playing_state: PlayingState) -> None:
        self.menu_state = menu_state
        self.playing_state = playing_state

    def handle_event(self, event: str) -> Optional[GameState]:
        if event == "resume":
            return self.playing_state
        if event == "quit_to_menu":
            return self.menu_state
        return None

    def get_state_name(self) -> str:
        return "paused"
