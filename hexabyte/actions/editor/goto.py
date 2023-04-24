"""Goto Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.enums import OffsetType
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.misc import str_to_int

from .._action import ActionError, UndoError
from ._editor_action import ReversibleEditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Goto(ReversibleEditorAction):
    """Goto Action.

    Supports a one arg and two arg form:

    goto 0x1000

    goto byte 0x1000

    goto bit 0x1000
    """

    CMD = "goto"

    MIN_ARGS = 1
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        try:
            if self.argc == self.MIN_ARGS:
                self.offset_type = OffsetType("byte")
                self.offset = str_to_int(argv[0]) * BYTE_BITS
            else:
                self.offset_type = OffsetType(self.argv[0])
                if self.offset_type == OffsetType.BYTE:
                    self.offset = str_to_int(argv[1]) * BYTE_BITS
                else:
                    self.offset = str_to_int(argv[1])
            self.previous_offset = 0
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        self.previous_offset = self.target.cursor
        self.target.cursor = self.offset
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        self.target.cursor = self.previous_offset
        self.applied = False
