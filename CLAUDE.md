# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Install with GUI support
pip install -e ".[dev,gui]"

# Run tests
pytest tests/ -v

# Run specific test class or method
pytest tests/test_core.py::TestDivide -v
pytest tests/test_core.py::TestDivide::test_divide_by_zero_raises_value_error -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run CLI
calc

# Build docs
cd docs && make html
```

## Architecture

Python 3.10+ calculator with three layers in `src/calculator/`:

- **core.py** - Pure mathematical functions (add, subtract, multiply, divide, power, square_root, modulo). All raise `ValueError` for invalid inputs (division by zero, negative square root).
- **history.py** - `CalculationHistory` class with `HistoryEntry` dataclass for tracking calculations with timestamps.
- **cli.py** - REPL interface that parses expressions via regex, delegates to core functions, and stores results in history.

Entry points defined in pyproject.toml: `calc` (CLI) and `calc-gui` (GUI).

Type alias `Number = Union[int, float]` is used throughout for numeric parameters.

## Testing

Tests use pytest with shared fixtures in `conftest.py` (`sample_history_entries`, `populated_history`, `empty_history`). Core tests use `@pytest.mark.parametrize` extensively for input variations.
