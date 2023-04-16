"""Action Event Module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, ClassVar


class ActionError(Exception):
    """Raised when an action fails to execute."""


class RedoActionError(ActionError):
    """Raised during a failed redo operation."""


class UndoActionError(ActionError):
    """Raised during a failed undo operation."""


class ActionType(Enum):
    """Action Type by keyword."""

    INVALID = auto

    # Cursor Commands
    GOTO = "goto"  # GOTO(offset)
    FIND = "find"  # find(offset, value)
    FIND_NEXT = "findnext"
    FIND_PREV = "findprev"

    # Edit Commands
    SET = "set"  # SET(offset, value)
    UPDATE = "update"  # UPDATE(offset, data)
    INSERT = "insert"  # INSERT(offset, data)
    DELETE = "delete"  # DELETE(offset, len)

    # Cut/Copy/Paste Commands
    CUT = "cut"
    COPY = "copy"
    MOVE = "move"
    PASTE = "paste"

    # Selection Commands
    SELECT = "select"
    UNSELECT = "unselect"
    HIGHLIGHT = "highlight"
    MATCH = "match"

    # File Operations
    REVERT = "revert"
    SAVE = "save"
    SAVE_AS = "saveas"

    # App Commands
    UNDO = "undo"
    REDO = "redo"
    SWITCH_MODE = "view-mode"
    EXIT = "exit"
    QUIT = "quit"


@dataclass
class Selection:
    """Data selection."""

    offset: int
    length: int


class Action(ABC):
    """Action Abstract Class.

    An action that cannot be undone.
    """

    type: ClassVar[ActionType] = ActionType.INVALID
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize Action."""
        argc = len(argv)
        if argc < self.MIN_ARGS or argc > self.MAX_ARGS:
            raise ValueError(f"Invalid number of arguments ({argc}) - {self.MIN_ARGS} <= argc <= {self.MAX_ARGS}")
        self._argc = argc
        self._argv = argv
        self._target: Any | None = None
        self.applied = False

    @property
    def argc(self) -> int:
        """Return the argument count."""
        return self._argc

    @property
    def argv(self) -> tuple[str, ...]:
        """Return the argument count."""
        return self._argv

    @abstractmethod
    def do(self) -> None:  # pylint: disable=invalid-name
        """Implement all changes associated with action."""

    @property
    def target(self) -> Any | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Any | None) -> None:
        """Set action target."""
        self._target = target


class HandlerAction(Action):
    """Handler Action Abstract Class.

    Special actions involving action handler.
    """


class ReversibleAction(Action):
    """Reversible Action Abstract Class.

    An action that can be undone.
    """

    def redo(self) -> None:
        """Alias for self.do()."""
        self.do()

    @abstractmethod
    def undo(self) -> None:
        """Reverse all changes performed by the action."""
