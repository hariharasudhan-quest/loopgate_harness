"""Pure, deterministic Hangman game state."""

from __future__ import annotations

import secrets
import string


class GameState:
    """Track a Hangman word, guessed letters, and remaining attempts.

    This class performs no I/O and has no terminal dependencies.

    Args:
        word: Optional word to guess. When omitted, a word is chosen from the
            built-in list using ``secrets.choice``.

    Attributes:
        _word (str): The word the player must guess.
        _guessed (set[str]): Letters the player has already guessed.
        _attempts (int): Wrong guesses remaining before the game is lost.
        guessed_letters (str): Sorted string of guessed letters.
        attempts_remaining (int): Number of wrong guesses still allowed.
    """

    _WORD_LIST: tuple[str, ...] = (
        "apple",
        "banana",
        "cherry",
        "dragon",
        "eagle",
        "falcon",
        "garden",
        "harbor",
        "island",
        "jungle",
        "kernel",
        "lemon",
    )
    _MAX_ATTEMPTS: int = 6

    def __init__(self, word: str | None = None) -> None:
        """Initialize state with a chosen or provided word."""
        self._word = (word or secrets.choice(self._WORD_LIST)).lower()
        self._guessed: set[str] = set()
        self._attempts: int = self._MAX_ATTEMPTS
        self.guessed_letters: str = ""
        self.attempts_remaining: int = self._attempts

    def guess_letter(self, char: str) -> bool:
        """Record one letter guess.

        Args:
            char: The guessed letter.

        Returns:
            True when the guess is accepted (a new single ASCII letter), False
            when the input is invalid or the letter was already guessed.
        """
        if len(char) != 1 or char.lower() not in string.ascii_lowercase:
            return False
        letter = char.lower()
        if letter in self._guessed:
            return False
        self._guessed.add(letter)
        if letter not in self._word:
            self._attempts -= 1
            self.attempts_remaining = self._attempts
        self.guessed_letters = "".join(sorted(self._guessed))
        return True

    def check_win(self) -> bool:
        """Return True when every letter in the word has been guessed."""
        return all(letter in self._guessed for letter in self._word)

    def check_loss(self) -> bool:
        """Return True when no attempts remain."""
        return self._attempts <= 0

    @property
    def word_display(self) -> str:
        """The masked word with unguessed letters hidden as underscores."""
        return " ".join(letter if letter in self._guessed else "_" for letter in self._word)
