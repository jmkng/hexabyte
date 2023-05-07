"""Find Action."""
from __future__ import annotations

import struct
from ast import literal_eval
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.context import context
from hexabyte.utils.misc import int_fmt_str

from .._action import ActionError
from ._editor_action import EditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Find(EditorAction):
    r"""Find Action.

    Supports a one arg and two arg form:

    find LITERAL
        - find "hello"
        - find b'\xff\xff'
        - find 256
    find [ @ | < | > | ! ] INTEGER_VALUE
        - find @ 0xffff
        - find < 65535
        - find ! 0b1111111111111111

    """

    CMD = "find"
    MIN_ARGS = 1
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == self.MIN_ARGS:
                endian = "@"
                raw_val = argv[0]
            else:
                endian = argv[0]
                raw_val = argv[1]
            try:
                val = literal_eval(raw_val)
            except ValueError:
                val = literal_eval(f"{raw_val!r}")
            if isinstance(val, bytes):
                self.find_bytes = val
            elif isinstance(val, str):
                self.find_bytes = val.encode("utf-8")
            elif isinstance(val, int):
                self.find_bytes = struct.pack(int_fmt_str(val, endian=endian), val)
            else:
                raise TypeError("Literal must be a bytes, int, or str.")
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
        model = self.target.model
        offset = model.find(self.find_bytes, self.target.cursor // BYTE_BITS)
        if offset == -1:
            raise InvalidCommandError(f"{self.find_bytes!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = offset * BYTE_BITS
        context.find_bytes = self.find_bytes
        self.applied = True


class FindNext(Find):
    """FindNext Action.

    Supports zero arguments

    findnext
    """

    CMD = "findnext"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if context.find_bytes is None:
            raise InvalidCommandError(" ".join([self.CMD, *argv]))
        self.previous_offset = 0

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        offset = model.find(self.find_bytes, self.target.cursor // BYTE_BITS + 1)
        if offset == -1:
            raise InvalidCommandError(f"{self.find_bytes!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = offset * BYTE_BITS
        context.find_bytes = self.find_bytes
        self.applied = True


class FindPrev(FindNext):
    """FindPrev Action.

    Supports zero arguments

    findprev
    """

    CMD = "findprev"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        offset = self.target.model.find(context.find_bytes, start=self.target.cursor // BYTE_BITS - 1, reverse=True)
        if offset == -1:
            raise InvalidCommandError(f"{context.find_bytes!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = offset * BYTE_BITS
        self.applied = True
