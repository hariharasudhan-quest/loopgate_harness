# Plan

> The human vision. Agents read this for direction; `specs/` turns it into concrete, prioritized work. Humans own this file.

## Goal

Build a fully functioning, terminal-based Hangman game in Python with 100% test coverage and cleanly separated logic and rendering layers.

## Approach To Reach Goal

The game is split into two distinct layers to keep the logic fully testable:

- **Logic Layer (`src/game_state.py`)**: A `GameState` class that holds the word, guessed letters, and remaining attempts. This class must have zero terminal or I/O dependencies — pure, deterministic Python only.
- **Presentation Layer (`src/game_cli.py`)**: A `GameCLI` class that reads from `sys.stdin` and writes to `sys.stdout`. It drives the game loop by calling into `GameState`.

### Allowed Libraries

Use **only the Python standard library** for the game itself:

- `secrets` — for cryptographically random word selection (avoids SAST warnings about pseudo-random generators).
- `sys` — for `sys.stdin` / `sys.stdout` in the CLI layer.
- `os` — for the optional `HANGMAN_WORD` environment variable used by tests to make the module entry point deterministic.

For **tests**, `pytest` is available and is the only test dependency allowed.

### Code Structure

```
src/
  __init__.py     # Package marker so src imports work for pylint and tests
  game_state.py   # GameState class — logic only, no I/O
  game_cli.py     # GameCLI class — reads/writes terminal, drives game loop
tests/
  test_game_state.py  # Unit tests for GameState
  test_game_cli.py    # End-to-end CLI tests
```

### Key Design Rules

- `GameState` must expose: `guess_letter(char)`, `check_win()`, `check_loss()`, `word_display` (masked word), `guessed_letters` (sorted string), `attempts_remaining` (int).
- All attributes in `GameState` that are internal implementation details must be prefixed with `_` (e.g. `_word`, `_guessed`).
- `word_display` is computed via an `@property` decorator.
- `guessed_letters` and `attempts_remaining` are kept as public attributes so the class stays within the 5 public-method lint cap while still exposing the required values.
- `GameCLI` must not access `GameState._word` or any other private members. It must only call the public API.
- Screen clearing uses an ANSI escape sequence written to `sys.stdout` instead of `os.system("clear")` to avoid subprocess-related security checks and keep the layer testable.
- Quality: code must pass `ruff check` (linting) and `ruff format` (formatting). Line length limit is **110 characters**.

## Milestones

1. **Milestone 1**: Core game logic (`GameState`) and comprehensive unit tests for all methods.
2. **Milestone 2**: The interactive Terminal CLI loop and `GameCLI` presentation rendering.

## Non-goals and Constraints

- Do not use any external dependencies outside of the Python standard library for the game implementation.
- No graphical interfaces — stick to plain terminal text output.
- No curses — use `sys.stdout.write()` with an ANSI clear sequence for screen clearing.
