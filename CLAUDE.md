# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

Python EDA tool that parses hardware signal lists from 3 input formats (HDL, CSV, Input Port) and generates:
1. **SystemVerilog RTL** — OTP/eFuse parameter distributor modules with bit-inversion logic
2. **Excel byte/bit mapping tables** — color-coded signal documentation

The core business rule is in `_generate_rhs()`: `efuse_default_value` determines per-bit inversion (`~`) in the generated RTL. Value=0 means pass-through; nonzero means bits set to 1 in the value get inverted.

## Commands

```bash
# Run the tool
python generate.py                                         # default input
python generate.py input/my_signal.csv my_distributor.sv   # custom
python src/dynamic_signal_parser.py -i input/cygnetpluse_otp_map.txt -o distributor.sv  # direct

# Tests
python -m pytest tests/                                    # all tests
python -m pytest tests/test_signal_parser.py               # single test file
python -m pytest tests/test_inversion_logic.py::TestClassName::test_method_name  # single test

# Coverage
python -m coverage run -m unittest discover tests
python -m coverage report --include=src/dynamic_signal_parser.py

# Makefile (Git Bash/MinGW)
make cygnet          # generate from primary example
make test            # tests with coverage
make clean           # remove generated files
make gen INPUT=... OUTPUT=...
```

## Architecture

Everything lives in **`src/dynamic_signal_parser.py`** (~1095 lines). No other source modules.

**Data flow:**
```
Input file → parse_signals() [auto-detects format] → List[Signal]
  → analyze_segments() [assigns bit positions] → Dict[segment_info]
    → generate_sv_module() / generate_byte_table_excel() → output files
```

**Key classes:**
- `Signal` (dataclass) — name, width, value, signal_type
- `DynamicSignalParser` — parser + code generator (all logic lives here)
- `DistributorGenerator` — higher-level wrapper for SV generation

**Input format auto-detection priority:** CSV → Input Port (Chinese comma `，`) → HDL (fallback)

**Duplicate signal names** get `_1`, `_2` etc. suffixes automatically.

## CLI Arguments

```
-i, --input       Input signal list file (required)
-o, --output      Output SV filename (default: param_distributor.sv)
-d, --output-dir  Output directory (default: generated)
-s, --strategy    Segmentation strategy: auto, equal, functional
--struct          Include struct definition (default: true)
```

## Dependencies

```bash
pip install openpyxl      # required for Excel generation
pip install coverage      # optional, for coverage reports
```

## Coding Notes

- Source and docs use Chinese comments; docs in `docs/` are in Chinese
- UTF-8 encoding with GBK fallback for legacy input files
- Tests use `unittest.TestCase` with `sys.path` manipulation to import from `src/`
- No linter/formatter configured
- Generated SV uses `always_comb` blocks; Excel uses a 12-color palette cycling for signals
