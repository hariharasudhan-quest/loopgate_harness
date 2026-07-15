"""Tests for the pure Hangman game state."""

from __future__ import annotations

import secrets
from io import StringIO

import pytest

from src.game_state import GameState


def test_init_uses_provided_word() -> None:
    """A supplied word becomes the target word."""
    state = GameState(word="python")
    assert state.word_display == "_ _ _ _ _ _"


def test_init_chooses_random_word_from_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """When no word is supplied, secrets.choice picks from the built-in list."""
    monkeypatch.setattr(secrets, "choice", lambda _words: "lemon")
    state = GameState()
    assert state.word_display == "_ _ _ _ _"


def test_correct_guess_reveals_letter() -> None:
    """A correct guess is recorded and does not consume an attempt."""
    state = GameState(word="apple")
    assert state.guess_letter("a") is True
    assert state.word_display == "a _ _ _ _"
    assert state.attempts_remaining == 6
    assert state.guessed_letters == "a"


def test_incorrect_guess_consumes_attempt() -> None:
    """An incorrect guess reduces the remaining attempts."""
    state = GameState(word="apple")
    assert state.guess_letter("z") is True
    assert state.attempts_remaining == 5
    assert state.word_display == "_ _ _ _ _"


def test_duplicate_guess_is_rejected() -> None:
    """Guessing the same letter twice returns False without changing state."""
    state = GameState(word="apple")
    state.guess_letter("a")
    assert state.guess_letter("a") is False
    assert state.attempts_remaining == 6
    assert state.guessed_letters == "a"


def test_invalid_inputs_are_rejected() -> None:
    """Empty, multi-character, numeric, and symbol guesses are rejected."""
    state = GameState(word="apple")
    assert state.guess_letter("") is False
    assert state.guess_letter("ab") is False
    assert state.guess_letter("1") is False
    assert state.guess_letter("!") is False
    assert state.attempts_remaining == 6
    assert not state.guessed_letters


def test_uppercase_guess_is_normalized() -> None:
    """Uppercase letters are treated as lowercase guesses."""
    state = GameState(word="apple")
    assert state.guess_letter("A") is True
    assert state.word_display == "a _ _ _ _"
    assert state.guessed_letters == "a"


def test_check_win_false_until_all_letters_guessed() -> None:
    """check_win is False until every unique letter is revealed."""
    state = GameState(word="cat")
    state.guess_letter("c")
    state.guess_letter("a")
    assert state.check_win() is False
    state.guess_letter("t")
    assert state.check_win() is True


def test_check_loss_after_six_wrong_guesses() -> None:
    """check_loss becomes True after exhausting all attempts."""
    state = GameState(word="cat")
    for letter in ("q", "x", "z", "v", "w", "b"):
        state.guess_letter(letter)
    assert state.check_loss() is True


def test_check_loss_false_with_attempts_remaining() -> None:
    """check_loss is False while attempts remain."""
    state = GameState(word="cat")
    state.guess_letter("q")
    assert state.check_loss() is False


def test_word_display_reveals_multiple_matching_letters() -> None:
    """Repeated letters in the word are all revealed at once."""
    state = GameState(word="apple")
    state.guess_letter("p")
    assert state.word_display == "_ p p _ _"


def test_guessed_letters_is_sorted() -> None:
    """Guessed letters are returned in alphabetical order."""
    state = GameState(word="python")
    state.guess_letter("y")
    state.guess_letter("p")
    state.guess_letter("h")
    assert state.guessed_letters == "hpy"


def test_attempts_remaining_tracks_wrong_guesses() -> None:
    """Remaining attempts count only incorrect guesses."""
    state = GameState(word="python")
    state.guess_letter("p")  # correct
    state.guess_letter("z")  # wrong
    state.guess_letter("y")  # correct
    assert state.attempts_remaining == 5


def test_state_has_no_stdout_dependency() -> None:
    """GameState never writes to stdout."""
    stdout = StringIO()
    state = GameState(word="test")
    state.guess_letter("t")
    assert state.word_display == "t _ _ t"
    assert not stdout.getvalue()
