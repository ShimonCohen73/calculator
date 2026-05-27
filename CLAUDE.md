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

## GUI

The GUI is built with **PyQt6 (6.4.0+)** and launched via the `calc-gui` entry point.

### Standard Mode
The existing calculator mode featuring:
- Dark theme with red/orange/purple/gray color scheme
- Arithmetic operations, trig functions (sin, cos, tan, inv, rad)
- Calculation history panel with clear history support

### Programmer Mode
A planned mode for software developers, embedded engineers, and anyone working with binary or hexadecimal numbers. It coexists with Standard mode via a mode-switcher UI element that feels native to the existing dark theme.

**Number system conversions:** DEC, HEX, OCT, BIN

**Bitwise operations:** AND, OR, XOR, NOT, left shift `<<`, right shift `>>`

**Integer size selection:** Byte (8-bit), Word (16-bit), DWord (32-bit), QWord (64-bit)

## Testing

Tests use pytest with shared fixtures in `conftest.py` (`sample_history_entries`, `populated_history`, `empty_history`). Core tests use `@pytest.mark.parametrize` extensively for input variations.