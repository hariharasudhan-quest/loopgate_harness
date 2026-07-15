"""End-to-end tests for the terminal Hangman CLI."""

from __future__ import annotations

import runpy
import sys
from io import StringIO

import pytest

from src.game_cli import GameCLI
from src.game_state import GameState


def test_winning_game_exits_zero() -> None:
    """A winning sequence prints the final word and exits with code 0."""
    stdin = StringIO("c\na\nt\n")
    stdout = StringIO()
    state = GameState(word="cat")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 0
    output = stdout.getvalue()
    assert "Word: c a t" in output
    assert "You win!" in output


def test_losing_game_exits_one() -> None:
    """A losing sequence exits with code 1 and reports the loss."""
    stdin = StringIO("q\nx\nz\nv\nw\nb\n")
    stdout = StringIO()
    state = GameState(word="cat")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 1
    output = stdout.getvalue()
    assert "Attempts remaining: 0" in output
    assert "You lose!" in output


def test_invalid_input_is_reprompted() -> None:
    """Invalid or multi-character input is skipped and the loop continues."""
    stdin = StringIO("1\n\nab\na\n")
    stdout = StringIO()
    state = GameState(word="a")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 0
    output = stdout.getvalue()
    assert "Invalid or already guessed. Try again." in output
    assert "You win!" in output


def test_duplicate_guess_is_reprompted() -> None:
    """Guessing the same letter twice is rejected and the loop continues."""
    stdin = StringIO("a\na\nb\n")
    stdout = StringIO()
    state = GameState(word="ab")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 0
    output = stdout.getvalue()
    assert "Invalid or already guessed. Try again." in output


def test_eof_exits_as_loss() -> None:
    """If stdin closes before the game ends, the CLI exits with code 1."""
    stdin = StringIO("a")
    stdout = StringIO()
    state = GameState(word="cat")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 1


def test_whitespace_around_guess_is_accepted() -> None:
    """Leading and trailing whitespace around a guess is stripped."""
    stdin = StringIO("  a  \n")
    stdout = StringIO()
    state = GameState(word="a")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 0
    assert "You win!" in stdout.getvalue()


def test_eof_after_invalid_input_exits_as_loss() -> None:
    """An invalid guess followed by end-of-file exits with code 1."""
    stdin = StringIO("1")
    stdout = StringIO()
    state = GameState(word="a")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    exit_code = cli.run()

    assert exit_code == 1
    assert "Invalid or already guessed. Try again." in stdout.getvalue()


def test_screen_is_cleared_each_turn() -> None:
    """Every rendered turn starts with the ANSI clear escape sequence."""
    stdin = StringIO("a\n")
    stdout = StringIO()
    state = GameState(word="a")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    cli.run()

    output = stdout.getvalue()
    assert output.count("\033[2J\033[H") >= 1


def test_masked_word_guessed_letters_and_attempts_are_displayed() -> None:
    """The current game state is shown on every turn."""
    stdin = StringIO("a\nz\nb\n")
    stdout = StringIO()
    state = GameState(word="ab")
    cli = GameCLI(stdin=stdin, stdout=stdout, state=state)

    cli.run()

    output = stdout.getvalue()
    assert "Word: a b" in output
    assert "Guessed: a" in output
    assert "Attempts remaining: 5" in output


def test_package_import_uses_src_prefixed_import() -> None:
    """Importing as a package module exercises the src-prefixed import branch."""
    import src.game_cli as cli_module  # noqa: PLC0415

    assert cli_module.__package__ == "src"
    assert cli_module.GameCLI is not None


def test_main_block_runs_entry_point(monkeypatch: pytest.MonkeyPatch) -> None:
    """Executing the module as __main__ runs GameCLI and exits with the win code."""
    stdin = StringIO("c\na\nt\n")
    stdout = StringIO()
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setenv("HANGMAN_WORD", "cat")
    sys.modules.pop("src.game_cli", None)
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("src.game_cli", run_name="__main__")
    assert exc_info.value.code == 0
    assert "You win!" in stdout.getvalue()


def test_main_block_loses_on_eof(monkeypatch: pytest.MonkeyPatch) -> None:
    """Executing the module as __main__ exits with code 1 at end-of-file."""
    stdin = StringIO("")
    stdout = StringIO()
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setenv("HANGMAN_WORD", "cat")
    sys.modules.pop("src.game_cli", None)
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("src.game_cli", run_name="__main__")
    assert exc_info.value.code == 1


def test_default_state_uses_env_word(monkeypatch: pytest.MonkeyPatch) -> None:
    """When no state is injected, GameCLI reads HANGMAN_WORD from the environment."""
    monkeypatch.setenv("HANGMAN_WORD", "a")
    stdin = StringIO("a\n")
    stdout = StringIO()
    cli = GameCLI(stdin=stdin, stdout=stdout)

    assert cli.state.word_display == "_"
    exit_code = cli.run()

    assert exit_code == 0
    assert "You win!" in stdout.getvalue()


def test_default_state_without_env_word(monkeypatch: pytest.MonkeyPatch) -> None:
    """When no state is injected and no env word is set, a random word is chosen."""
    import secrets  # noqa: PLC0415

    monkeypatch.delenv("HANGMAN_WORD", raising=False)
    monkeypatch.setattr(secrets, "choice", lambda _words: "a")
    stdin = StringIO("a\n")
    stdout = StringIO()
    cli = GameCLI(stdin=stdin, stdout=stdout)

    exit_code = cli.run()

    assert exit_code == 0
    assert "You win!" in stdout.getvalue()
