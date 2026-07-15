# Project Status

> Current truth of the repo. Keep it short and current < 100 lines. Human-agent interface document.

## Current Focus

- Active spec: `docs/specs/hangman.md` — terminal Hangman game.
- Milestones 1 and 2 are both complete.

## Current State

- `src/game_state.py`: pure `GameState` class with `secrets.choice` word selection, private state, and public methods/properties.
- `src/game_cli.py`: `GameCLI` class driving the terminal loop over `sys.stdin`/`sys.stdout` with ANSI screen clearing and a `HANGMAN_WORD` env hook for deterministic tests.
- `tests/test_game_state.py` and `tests/test_game_cli.py`: 30 behavioral tests covering win/loss, invalid/duplicate/non-ASCII input, EOF, whitespace handling, screen clearing, and the module entry point.
- All hangman source files reach 100% coverage.

## Checks

- `harness preflight`: green (hangman source passes lint/format/complexipy)
- `harness gate`: blocked — 2 harness tests fail and coverage drops below 100 because of an uncommitted edit in `harness/cli.py`
- Hangman tests: `pytest tests/` passes (30/30)

## Next

1. Resolve `harness/cli.py` formatting and update `harness/tests/test_cli.py` expectations for the new `opencode` agent entry. This is a forbidden path for agents; needs human commit or an exception.
2. Human review of the `HANGMAN_WORD` env hook in `GameCLI`.
3. Human review of the public-attribute compromise in `GameState` (kept to satisfy the 5 public-method lint cap).

## Changelog

- 0002-opencode iteration 2/2: added edge-case tests for non-ASCII guesses, uppercase-word normalization, whitespace-padded input, and EOF after invalid input. Recovered onto `main` after the harness created a stray `new_branch_oak`. `harness gate` still blocked by `harness/` forbidden-path changes.
- 0002-opencode iteration 1/2: verified Hangman implementation is complete; gate is blocked by pre-existing `harness/` changes. Updated `docs/PROJECT_STATUS.md` to current truth.
- 0001-opencode iteration 2/2: reconciled `docs/plan.md` with the implementation and `docs/specs/hangman.md`; gate was green at that commit.
- Commit: `2a910f0`; pushed to fork branch `0001-opencode-hangman-2-2` because origin is read-only.
- 0001-opencode iteration 1/2: implemented the Hangman game end-to-end; gate was green at that commit.
- Commit: `19a3c6e`; pushed to fork branch `0001-opencode-hangman-1-2` because origin is read-only.

## Blockers

- `harness/cli.py` has an uncommitted, unformatted addition of the `opencode` agent that makes `harness/tests/test_cli.py` assertions fail.
- `harness/` is a forbidden path for agents, so the gate cannot be cleared without human action or an explicit exception.
