# AGENTS.md - OTP Parameter Distributor Generator

## Project Overview

This is a **Python-based EDA tool** for hardware chip design that generates SystemVerilog RTL code for OTP (One-Time Programmable) / eFuse parameter distributors. The tool parses signal lists and produces distributer modules with configurable bit-inversion logic based on efuse_default_value settings.

**Key Domain Knowledge:**
- **Target Domain**: Hardware chip design (ASIC/FPGA)
- **Output**: SystemVerilog RTL modules for eFuse parameter distribution
- **Inversion Logic**: Security feature where `efuse_default_value` determines which bits are inverted (`~`) in the generated RTL

---

## Project Structure

```
├── src/
│   └── dynamic_signal_parser.py    # Main generator (1000+ lines)
├── tests/                          # Comprehensive test suite
│   ├── test_signal_parser.py       # Core parsing tests
│   ├── test_inversion_logic.py     # Bit-inversion logic tests
│   ├── test_excel_generator.py     # Excel output tests
│   ├── test_validation.py          # Input validation tests
│   ├── test_duplicate_signals.py   # Duplicate name handling
│   └── test_advanced_features.py   # Extended functionality
├── input/                          # Example input files
│   ├── cygnetpluse_otp_map.txt     # Main example (Input Port format)
│   ├── my_signal.csv               # CSV format example
│   └── signals.txt                 # HDL format example
├── generated/                      # Output directory
├── docs/
│   ├── DESIGN.md                   # Design documentation (Chinese)
│   └── INPUT_FORMAT.md             # Input format specification
├── generate.py                     # User-friendly wrapper script
├── run.bat                         # Windows batch wrapper
├── run_tests.bat                   # Windows test runner
├── Makefile                        # Build automation (Git Bash/MinGW)
└── QWEN.md                         # Additional design notes
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python >= 3.7 |
| Required Packages | `openpyxl` (for Excel generation) |
| Optional Packages | `coverage` (for test coverage) |
| Test Framework | pytest / unittest |
| Build Tool | Makefile (Git Bash/MinGW) or batch scripts (Windows) |

---

## Core Classes and Data Structures

### SignalType (Enum)
```python
class SignalType(Enum):
    LOGIC = "logic"
    BIT = "bit"
    WIRE = "wire"
    REG = "reg"
```

### Signal (Dataclass)
```python
@dataclass
class Signal:
    name: str           # Signal name
    width: int          # Bit width
    value: int          # efuse_default_value (determines inversion)
    signal_type: SignalType = SignalType.LOGIC
    explicit_width: bool = False
```

### DynamicSignalParser
Main parser class with auto format detection.

**Key Methods:**
- `parse_signals(text: str) -> List[Signal]` - Parse signals from text (auto-detect format)
- `analyze_segments(strategy='auto') -> Dict` - Analyze signal bit positioning
- `generate_sv_module(segments, module_name) -> str` - Generate SystemVerilog
- `generate_byte_table_excel(segments, output_path)` - Generate Excel documentation

### DistributorGenerator
Code generator class for SV output.

---

## Input Formats (Auto-Detection)

The parser automatically detects and supports **3 input formats**:

### 1. HDL Format
```
logic [31:0] signal_name 0xValue
logic [31:0] uuid 0x12345678
logic [7:0]  chip_id 0xAB
```

### 2. CSV Format
```
bitwidth,signal_name,default_value
[31:0],uuid,0x12345678
[7:0],chip_id,0xAB
,flag,0x1          # Empty bitwidth = 1-bit
```

### 3. Input Port Format (Primary Use Case)
```verilog
// Uses CHINESE comma ， as delimiter
input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008
input      flag                                          ，  //efuse_default_value: 0x1
```

**⚠️ Important**: The Input Port format uses a Chinese comma `，` (U+FF0C) not ASCII comma `,`.

---

## Critical Logic: Bit-Inversion Rules

The most important business logic is in `_generate_rhs()` method. The `efuse_default_value` determines how each signal is wired:

| Condition | Inversion Rule | Example Output |
|-----------|---------------|----------------|
| `value == 0` | No inversion (pass-through) | `chip_param[7:0]` |
| `width == 1` and `value != 0` | Full inversion (`~`) | `~chip_param[5]` |
| `width > 1` and `value != 0` | Per-bit inversion | `{~bit[7], bit[6], ~bit[5], ...}` |

**Example:**
```python
# 8-bit signal with value=0x81 (10000001)
# bit[7]=1 -> inverted, bit[0]=1 -> inverted
# Result: {~chip_param[15], chip_param[14], ..., chip_param[9], ~chip_param[8]}
```

---

## Usage Commands

### Quick Start (Recommended)
```bash
# Using wrapper script
python generate.py

# Or with arguments
python generate.py -i input/my_signal.csv -o my_distributor.sv
```

### Direct Usage
```bash
python src/dynamic_signal_parser.py -i input/cygnetpluse_otp_map.txt -o cygnetpluse_otp_distributor.sv
```

### Using Makefile
```bash
make gen INPUT=input/my_signal.csv OUTPUT=my_distributor.sv

# Other targets
make test           # Run tests with coverage
make test-html      # Generate HTML coverage report
```

### Using Batch Scripts (Windows)
```batch
run.bat input\cygnetpluse_otp_map.txt cygnetpluse_otp_distributor.sv
run_tests.bat       # Run regression tests
run_tests.bat html  # Generate HTML coverage report
```

---

## Output Artifacts

When generation completes, two files are created in `generated/`:

1. **`{name}.sv`** - SystemVerilog module with:
   - Struct definition (packed)
   - Module with `input [MAX:0] chip_param`
   - `always_comb` distributor logic with inversions

2. **`{name}_byte_table_{timestamp}.xlsx`** - Excel documentation:
   - Byte/bit mapping table
   - Color-coded signal segments
   - Default value annotations

---

## Testing

### Running Tests
```bash
# All tests
python -m pytest tests/

# With coverage
python -m coverage run -m unittest discover tests
python -m coverage report --include=src/dynamic_signal_parser.py

# HTML report
python -m coverage html --include=src/dynamic_signal_parser.py -d coverage_html
```

### Test Files Overview
| Test File | Coverage Area |
|-----------|---------------|
| `test_signal_parser.py` | 3 format parsing, Signal dataclass |
| `test_inversion_logic.py` | `_generate_rhs()` inversion rules |
| `test_excel_generator.py` | openpyxl Excel generation |
| `test_validation.py` | Width/value mismatch warnings |
| `test_duplicate_signals.py` | Auto-suffix `_1`, `_2` for duplicates |
| `test_advanced_features.py` | CLI args, edge cases, file operations |

---

## Validation Warnings

The parser emits warnings when values exceed bit-width capacity:

```
⚠️  VALUE VALIDATION WARNINGS:
   Signal 'test_1bit' (1-bit) has value=7, exceeds max value for 1-bit signals (max 0x1)
   Signal 'test_nibble' (4-bit) has value=21, exceeds max value for 4-bit signals (max 0xF)
```

**Note**: Warnings don't block execution; they inform the user of potential misconfigurations.

---

## Duplicate Signal Handling

Signals with duplicate names are automatically renamed:

```
Input: efuse_val_csr_10g_sds_pll_band_w (appears in sds0 and sds1 sections)
Output:
  - First: efuse_val_csr_10g_sds_pll_band_w
  - Second: efuse_val_csr_10g_sds_pll_band_w_1
  - Third: efuse_val_csr_10g_sds_pll_band_w_2
```

---

## Reserved Signal Handling

Signals named `reserved` (case-insensitive) are automatically detected and handled:

- **SV generation**: Skipped in output ports, struct, and always_comb assignments
- **Excel generation**: Marked with gray color (D3D3D3)
- **Console output**: Shown with `(R)` marker
- **Bit width**: Still counted in total parameter width

```
Input:
  input[7:0] data       ，  //efuse_default_value: 0x1
  input[3:0] reserved   ，  //efuse_default_value: 0
  input[15:0] config    ，  //efuse_default_value: 0

SV output: Only data and config ports generated (reserved skipped)
Excel: reserved cells shown in gray
```

---

## Coding Style Notes

- **Comments**: Predominantly Chinese comments in source code
- **File Encoding**: UTF-8 (with GBK fallback for legacy files)
- **String Quotes**: Mixed single/double quotes
- **Line Length**: No strict limit (up to ~120 chars)
- **Naming**: snake_case for Python, snake_case for SV signals

---

## Common Tasks

### Adding a New Input Format
1. Add detection method `_is_new_format()`
2. Add parser method `_parse_new_format()`
3. Update `parse_signals()` to call new parser
4. Add tests in `test_signal_parser.py`

### Modifying Inversion Logic
1. Edit `_generate_rhs()` in `DynamicSignalParser`
2. Update tests in `test_inversion_logic.py`
3. Verify with existing input examples

### Adding New Output Formats
1. Extend `DistributorGenerator` class
2. Add generation method following existing patterns
3. Update CLI in `main()` if needed

---

## Key File References

| File | Purpose |
|------|---------|
| `src/dynamic_signal_parser.py` | Main implementation (~1100 lines) |
| `docs/INPUT_FORMAT.md` | Detailed format specification |
| `docs/DESIGN.md` | Architecture design (Chinese) |
| `input/cygnetpluse_otp_map.txt` | Reference Input Port format example |
| `input/my_signal.csv` | Reference CSV format example |

---

## Dependencies Installation

```bash
# Required
pip install openpyxl

# Optional (for coverage reports)
pip install coverage

# Or install all (if requirements.txt exists)
pip install -r requirements.txt
```
