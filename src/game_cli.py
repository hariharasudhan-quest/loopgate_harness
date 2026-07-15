"""Terminal presentation layer for the Hangman game."""

from __future__ import annotations

import os
import sys
from typing import TextIO

from src.game_state import GameState


class GameCLI:
    """Drive the Hangman game loop using ``sys.stdin`` and ``sys.stdout``.

    The CLI only uses the public API of :class:`GameState`.

    Args:
        stdin: Text stream to read guesses from. Defaults to ``sys.stdin``.
        stdout: Text stream to write rendered output to. Defaults to ``sys.stdout``.
        state: Pre-built :class:`GameState` for deterministic tests. A fresh
            state is created when omitted.
    """

    _CLEAR_SCREEN: str = "\033[2J\033[H"

    def __init__(
        self,
        stdin: TextIO | None = None,
        stdout: TextIO | None = None,
        state: GameState | None = None,
    ) -> None:
        """Initialize streams and game state."""
        self._stdin = stdin if stdin is not None else sys.stdin
        self._stdout = stdout if stdout is not None else sys.stdout
        self._state = state if state is not None else GameState(word=os.environ.get("HANGMAN_WORD"))

    def run(self) -> int:
        """Run the game loop until the player wins or loses.

        Returns:
            0 when the player wins, 1 when the player loses or input ends.
        """
        while not self._state.check_win() and not self._state.check_loss():
            self._render()
            guess = self._read_guess()
            if guess is None:
                return 1
            if not self._state.guess_letter(guess):
                self._stdout.write("Invalid or already guessed. Try again.\n")
                self._stdout.flush()
        self._render(game_over=True)
        if self._state.check_win():
            self._stdout.write("You win!\n")
        else:
            self._stdout.write("You lose!\n")
        self._stdout.flush()
        return 0 if self._state.check_win() else 1

    @property
    def state(self) -> GameState:
        """The current game state."""
        return self._state

    def _render(self, game_over: bool = False) -> None:
        """Draw the current screen to stdout."""
        self._stdout.write(self._CLEAR_SCREEN)
        self._stdout.write(f"Word: {self._state.word_display}\n")
        self._stdout.write(f"Guessed: {self._state.guessed_letters}\n")
        self._stdout.write(f"Attempts remaining: {self._state.attempts_remaining}\n")
        if not game_over:
            self._stdout.write("Guess a letter: ")
        self._stdout.flush()

    def _read_guess(self) -> str | None:
        """Read one non-empty line from stdin.

        Returns:
            The stripped guess, or ``None`` at end-of-file.
        """
        line = self._stdin.readline()
        if not line:
            return None
        return line.strip()


if __name__ == "__main__":
    raise SystemExit(GameCLI().run())
