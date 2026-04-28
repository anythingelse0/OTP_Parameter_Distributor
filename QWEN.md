# Qwen Code Project Context

## Project Overview

OTP Parameter Distributor 是一个用于 eFuse/OTP 信号解析和 SystemVerilog 代码生成的自动化工具，位于 `D:\test\codex` 目录。

该工具根据输入的信号列表，自动生成带有按位取反逻辑的参数分发器 RTL 代码，同时生成带颜色编码的 Excel 字节/位映射表供参考。

## Project Type

**Software/Code Project** - Python 脚本工具

## Directory Structure

```
D:\test\codex\
├── run.bat                      # Windows 批处理快捷脚本（双击运行）
├── generate.py                  # Python 快捷脚本
├── Makefile                     # Make 命令支持（需 Git Bash/MinGW）
├── QWEN.md                      # 本文件
├── src/
│   └── dynamic_signal_parser.py # 主程序（880 行）
├── input/                       # 输入信号列表目录
│   ├── cygnetpluse_otp_map.txt  # 主示例：Input port 格式（25 信号，124-bit）
│   ├── my_signal.csv            # CSV 格式示例
│   ├── my_signal2.txt           # HDL 格式示例
│   ├── signals.txt              # 测试信号
│   ├── signals_lot.txt          # Lot ID 测试信号
│   └── efuse_signal_list.txt    # EFuse 信号列表示例
├── generated/                   # 生成输出（自动创建）
│   ├── cygnetpluse_otp_distributor.sv
│   └── cygnetpluse_otp_distributor_byte_table_*.xlsx
└── docs/
    ├── INPUT_FORMAT.md          # 输入格式详细说明
    └── DESIGN.md                # 架构设计文档
```

## Core Classes

| 类名 | 文件 | 职责 |
|------|------|------|
| `DynamicSignalParser` | `src/dynamic_signal_parser.py` | 核心解析器，处理所有输入格式，生成信号段映射 |
| `SVGenerator` | `src/dynamic_signal_parser.py` | SystemVerilog 代码生成器，包含 struct、module、assignment 生成 |
| `ExcelExporter` | `src/dynamic_signal_parser.py` | Excel 表格生成器，创建带颜色编码的字节/位映射表 |
| `Signal` | `src/dynamic_signal_parser.py` | 信号数据类，包含 name、width、value、description |

## Key Files

### Main Source
- **`src/dynamic_signal_parser.py`** (880 lines)
  - `SignalParser.parse_signals()` - 入口方法，自动检测格式
  - `_is_csv_format()`, `_is_input_format()` - 格式检测
  - `_parse_csv()`, `_parse_input()`, `_parse_hdl()` - 格式解析器
  - `generate_sv_module()` - 生成 SystemVerilog 模块
  - `generate_byte_table_excel()` - 生成 Excel 映射表

### Input Examples
- **`input/cygnetpluse_otp_map.txt`** - 主要测试文件
  - 25 个信号，总位宽 124-bit
  - Input port 格式（带中文逗号和 efuse_default_value 注释）

### Documentation
- **`docs/DESIGN.md`** - 完整架构设计和流程图
- **`docs/INPUT_FORMAT.md`** - 三种输入格式的详细说明和示例

## Input Formats Supported

工具自动检测三种输入格式：

### 1. HDL 格式
```systemverilog
logic [31:0] uuid 0x12345678
logic [7:0]  chip_id 0xAB
```

### 2. CSV 格式
```csv
bitwidth,name,default_value
32,uuid,0x12345678
8,chip_id,0xAB
```

### 3. Verilog Input Port 格式
```systemverilog
input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008
input      efuse_val_csr_cfg_xtal_div2_en                ，  //efuse_default_value: 0x0
```

**注意**：使用中文逗号 `，` 作为分隔符，注释需包含 `efuse_default_value:`。

## Inversion Logic Rules

根据 `efuse_default_value` 自动生成取反逻辑：

| 条件 | 生成逻辑 | 说明 |
|------|----------|------|
| `value == 0` | `signal = chip_param[N]` | 直接连接，无取反 |
| `width == 1 && value != 0` | `signal = ~chip_param[N]` | 1-bit 全取反 |
| `width > 1 && value != 0` | 逐位判断：value 对应 bit 为 1 取反，为 0 不取反 | 按位取反 |

### Example (chip_id: width=16, value=0x9008)
```systemverilog
chip_id = {
    ~chip_param[79],  // value[15]=1, 取反
     chip_param[78],  // value[14]=0, 不取反
     chip_param[77],  // value[13]=0, 不取反
    ~chip_param[76],  // value[12]=1, 取反
    ...
     chip_param[64]   // value[0]=0, 不取反
};
```

## Building and Running

### Windows Batch (Recommended)
```bash
# 双击运行或命令行
run.bat input\cygnetpluse_otp_map.txt cygnetpluse_otp_distributor.sv

# 不带参数显示帮助
run.bat
```

### Python Script
```bash
# 默认使用 cygnetpluse_otp_map.txt
python generate.py

# 自定义输入
python generate.py input/my_signal.csv my_distributor.sv
```

### Makefile (Git Bash/MinGW)
```bash
make cygnet     # 生成 cygnetpluse 版本
make csv        # 生成 CSV 输入版本
make all        # 生成全部
make clean      # 清理生成的文件
make list       # 列出可用输入文件

# 自定义生成
make gen INPUT=input/myfile.txt OUTPUT=myout.sv
```

### Direct Python Execution
```bash
python src/dynamic_signal_parser.py -i input/cygnetpluse_otp_map.txt -o distributor.sv

# Parameters:
#   -i, --input: Input signal list file
#   -o, --output: Output SV filename (default: param_distributor.sv)
```

## Output Files

### 1. SystemVerilog Module
**Location**: `generated/{name}_distributor.sv`

**Contents**:
- Packed struct 定义（`param_struct_t`）
- Distributor 模块（`param_distributor`）
- `always_comb` 赋值逻辑（带 `// value: 0xXX` 注释）

### 2. Excel Byte/Bit Mapping Table
**Location**: `generated/{name}_byte_table_{timestamp}.xlsx`

**Features**:
- Byte/Bit 映射表
- 多 bit 信号自动合并单元格
- 12 色轮询背景色区分不同信号
- 文件名带时间戳避免文件锁定冲突

## Development Conventions

### Code Style
- Python 3.7+ with type hints (`List[Signal]`, `Dict[str, Any]`)
- dataclass for data structures
- Enum for signal types
- 4-space indentation

### Key Constants
```python
# 12-color palette for Excel
COLORS = ['FFE6E6', 'E6F7FF', 'E6FFE6', 'FFF4E6', 'F3E6FF', 
          'E6FFFF', 'FFE6F7', 'F0F0F0', 'FFFACD', 'E0FFE0', 
          'FFE0E0', 'E0E0FF']
```

### Auto-detection Priority
1. CSV format (check comma separation and 3-column structure)
2. Input port format (check `input` keyword and Chinese comma `，`)
3. HDL format (default fallback)

## Dependencies

```
Python >= 3.7
openpyxl >= 3.0.0    # Excel generation
```

Install:
```bash
pip install openpyxl
```

## Important Notes

1. **Bit Alignment**: Signals are allocated continuously, not aligned to byte boundaries
2. **Empty Bits**: Some bytes may have empty cells (e.g., bit 91), shown as blank in Excel
3. **File Locking**: Excel filenames include timestamps to avoid Windows file lock conflicts
4. **Color Coding**: 12 colors cycle through; same signal has same color across different bytes

## Common Tasks

### Add New Signal Format Support
Edit `src/dynamic_signal_parser.py`:
1. Add detection method `_is_new_format()`
2. Add parser method `_parse_new_format()`
3. Update `parse_signals()` to include new format check

### Modify Inversion Logic
Edit `_generate_rhs()` method in `DynamicSignalParser` class.

### Add New Output Format
Extend `SVGenerator` class or create new generator class following the same pattern.

## Version History

Current implementation supports:
- 3 input formats (HDL, CSV, Input port)
- Value-based inversion logic (none/full/per-bit)
- SystemVerilog module generation
- Excel byte/bit mapping with colors and merged cells
- Batch/Makefile shortcuts for easy execution
