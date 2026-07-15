# Hangman Game Specification

## 1. Overview
Build a simple, terminal-based Hangman game in Python. The game selects a random word from a predefined list; the player guesses letters to reveal the word. Too many wrong guesses and the player loses.

## 2. Code Structure & Libraries
The code is split into a pure logic layer and a terminal presentation layer for testability.

### Allowed Libraries
Only the Python standard library for the game implementation; `pytest` is allowed only for tests.
- `secrets` for word selection (avoids SAST warnings about pseudo-random generators).
- `sys` for `sys.stdin` / `sys.stdout` in the CLI layer.
- `os` for reading the optional `HANGMAN_WORD` environment variable in the CLI layer.

### Directory Structure
```
src/
  __init__.py     # Package marker so src imports work for pylint and tests
  game_state.py   # Pure logic layer
  game_cli.py     # Presentation/CLI loop layer
tests/
  test_game_state.py  # Logic tests
  test_game_cli.py    # End-to-end CLI tests
```

## 3. Core Requirements: GameState (`src/game_state.py`)
Zero I/O or terminal logic; pure state only.

- **Word Selection**: Hardcode at least 10 words. A word is chosen on initialization using `secrets.choice`.
- **Internal State**: Private by underscore prefix (e.g. `_word`, `_guessed`, `_attempts`).
- **Methods**:
  - `guess_letter(char: str) -> bool`: Updates state. Returns `True` if the guess is accepted (new single ASCII letter), `False` if already guessed or invalid.
  - `check_win() -> bool`: `True` when every letter in the word has been guessed.
  - `check_loss() -> bool`: `True` when remaining attempts reach 0.
- **Public API**:
  - `word_display` property: Masked word as a string with letters separated by spaces (e.g. `_ p p _ e`).
  - `guessed_letters` attribute: Sorted string of guessed letters (kept as a public attribute so the class fits the 5 public-method lint cap).
  - `attempts_remaining` attribute: Integer count of attempts left (starts at 6).

## 4. Terminal Interface: GameCLI (`src/game_cli.py`)
Drives the loop, reads from `sys.stdin`, writes to `sys.stdout`. Interacts only with `GameState`'s public API.

- **Execution Loop**: Runs until `check_win()` or `check_loss()` is true.
- **Display**: Each turn writes an ANSI clear escape sequence, then:
  - The masked word state.
  - The guessed letters.
  - The remaining attempts count.
  - A prompt for the user.
- **Input handling**: Skips empty input, reprompts on invalid or already-guessed letters, decrements attempts on wrong guesses.
- **Entry point**: `python -m src.game_cli` executes `GameCLI().run()` and exits with the win/loss code.
- **Determinism hook**: `GameCLI` reads `HANGMAN_WORD` from the environment when no state is injected, enabling end-to-end tests of the module entry point.

## 5. Code Quality & Testing
- Comprehensive unit tests in `tests/test_game_state.py` and `tests/test_game_cli.py`.
- Tests cover winning, losing, correct/incorrect/duplicate guesses, invalid input, empty input, screen clearing, and the default entry point.
- 100% coverage for `src/game_state.py` and `src/game_cli.py`.
- Pass Pyright strict, Ruff, Pylint, Complexipy, and Semgrep checks with the 110-character line-length limit.

## 6. Milestones
- **Milestone 1**: Implement `GameState` logic (`src/game_state.py`) and tests (`tests/test_game_state.py`). ✅ Complete.
- **Milestone 2**: Implement the CLI loop (`src/game_cli.py`) and tests (`tests/test_game_cli.py`). ✅ Complete.

## Acceptance Criteria
- `pytest --cov --cov-report=term-missing --cov-fail-under=100` passes.
- `harness gate` passes.
- `python -m src.game_cli` can be executed end-to-end with deterministic input/output in tests.

## Changelog
- 0001-opencode iteration 1/2: implemented GameState, GameCLI, full test suite, and updated spec to match the 5 public-method lint cap.
