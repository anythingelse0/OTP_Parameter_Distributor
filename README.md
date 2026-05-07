# OTP Parameter Distributor Generator

Python EDA tool that parses hardware signal lists and generates SystemVerilog OTP/eFuse parameter distributor modules with bit-inversion logic, plus Excel byte/bit mapping tables.

## Quick Start

```bash
pip install openpyxl

# Run with default input
python generate.py

# Custom input/output
python generate.py input/my_signal.csv my_distributor.sv

# Batch script (Windows)
run.bat
```

## CLI Usage

```bash
python src/dynamic_signal_parser.py -i <input> [-o <output>] [-d <dir>] [-s <strategy>] [-v] [-q] [--no-struct]
```

| Flag | Description |
|------|-------------|
| `-i, --input` | Input signal list file (required) |
| `-o, --output` | Output SV filename (default: `param_distributor.sv`) |
| `-d, --output-dir` | Output directory (default: `generated`) |
| `-s, --strategy` | Segmentation strategy: `auto`, `equal`, `functional` |
| `-v, --verbose` | Print detailed analysis, byte table, stats, and SV preview |
| `-q, --quiet` | Suppress all console output except generation result |
| `--no-struct` | Exclude struct definition from generated SV |

## Testing

```bash
python -m pytest tests/                  # all tests
python -m pytest tests/test_signal_parser.py  # single file
```

## Documentation

- [Design Document](docs/DESIGN.md) - Architecture, data flow, and core logic
- [Input Format](docs/INPUT_FORMAT.md) - Supported input formats (HDL, CSV, Input Port)

## Project Structure

```
src/
  dynamic_signal_parser.py   # Core parser + code generator (~1100 lines)
input/                       # Example signal lists
generated/                   # Output directory (SV + Excel)
tests/                       # Unit tests
docs/                        # Documentation
```
