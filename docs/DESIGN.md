# OTP Parameter Distributor 设计文档

## 1. 项目概述

OTP Parameter Distributor 是一个用于 eFuse/OTP 信号解析和 SystemVerilog 代码生成的自动化工具。它根据输入的信号列表，自动生成带有按位取反逻辑的参数分发器 RTL 代码，同时生成 Excel 格式的字节/位映射表供参考。

### 1.1 主要功能
- 支持多种输入格式（HDL、CSV、Verilog input port）
- 根据 efuse_default_value 自动生成取反逻辑
- 生成 SystemVerilog distributor 模块
- 生成带颜色编码的 Excel 字节/位映射表
- 自动计算信号位宽和地址分配

## 2. 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    Input Signal Files                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐   │
│  │ HDL fmt  │  │ CSV fmt  │  │ Verilog input port fmt   │   │
│  └────┬─────┘  └────┬─────┘  └───────────┬──────────────┘   │
└───────┼─────────────┼────────────────────┼──────────────────┘
        │             │                    │
        └─────────────┴────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   SignalParser (Core)   │
              │  - 格式自动检测         │
              │  - 信号解析             │
              │  - 位宽计算             │
              │  - 取反逻辑生成         │
              └────────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌─────▼──────┐
│ SV Generator │  │ Excel Generator │  │ SV Module  │
│ (struct/def) │  │ (byte/bit table)│  │ Generator  │
└───────┬──────┘  └────────┬────────┘  └─────┬──────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
              ┌────────────▼────────────┐
              │      Output Files       │
              │  - *_distributor.sv     │
              │  - *_byte_table.xlsx    │
              └─────────────────────────┘
```

### 2.1 核心类说明

| 类名 | 职责 |
|------|------|
| `Signal` | 信号数据类，包含 name、width、value、signal_type、is_reserved 等字段 |
| `SignalType` | 信号类型枚举：LOGIC、BIT、WIRE、REG |
| `DynamicSignalParser` | 核心解析器，处理所有输入格式，生成信号段映射、SV 模块和 Excel 表格 |
| `DistributorGenerator` | 高层封装，提供 `generate_complete_sv()` 和 `generate_with_options()` 接口 |

## 3. 输入格式支持

工具支持 **3 种** 输入格式，自动检测无需手动指定：

### 3.1 HDL 格式
```systemverilog
// 格式: logic [bitwidth] name default_value
logic [31:0] uuid 0x12345678
logic [7:0]  chip_id 0xAB
```

### 3.2 CSV 格式
```csv
// 格式: bitwidth,name,default_value
32,uuid,0x12345678
8,chip_id,0xAB
```

### 3.3 Verilog Input Port 格式
```systemverilog
// 格式: input[width] name ， //efuse_default_value: value
input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008
input      efuse_val_csr_xtal_div2_en                    ，  //efuse_default_value: 0x0
```

**注意**：使用中文逗号 `，`、英文逗号 `,` 或分号 `;` 作为分隔符。

## 4. 特殊信号处理

### 4.1 Reserved 信号自动识别

信号名称为 `reserved`（不区分大小写）时，自动标记为保留信号：

- **SV 生成**: 跳过输出端口、struct 定义和 always_comb 赋值
- **Excel 生成**: 使用灰色（#D3D3D3）标注
- **控制台输出**: 显示 `(R)` 标记
- **位宽计算**: 仍计入总参数位宽

```
输入:
  input[7:0] data       ，  //efuse_default_value: 0x1
  input[3:0] reserved   ，  //efuse_default_value: 0
  input[15:0] config    ，  //efuse_default_value: 0

SV 输出: 仅生成 data 和 config 端口（reserved 被跳过）
Excel: reserved 单元格显示为灰色
```

### 4.2 重名信号自动处理

信号名称重复时自动添加后缀：

```
输入（两处出现 pll_band_w）:
  efuse_val_csr_10g_sds_pll_band_w  → 第一个保持原名
  efuse_val_csr_10g_sds_pll_band_w  → 第二个变为 pll_band_w_1
  efuse_val_csr_10g_sds_pll_band_w  → 第三个变为 pll_band_w_2
```

### 4.3 未解析行警告

解析完成后，工具会检查可能被跳过的行并发出警告：

- **Input 格式**: 缺少 `efuse_default_value` 注释、缺少逗号/分号分隔符
- **HDL 格式**: 缺少位宽定义 `[msb:lsb]`
- **CSV 格式**: 行内字段数不足

```
  [WARN] UNPARSED LINE WARNINGS (2)
  Missing 'efuse_default_value' comment: input [8:0] reserved
  Missing comma/semicolon delimiter: input [8:0] reserved  //efuse_default_value: 0
```

## 5. 取反逻辑规则

工具根据 `efuse_default_value` 自动生成以下三种取反逻辑：

### 5.1 规则定义

| 条件 | 生成逻辑 | 说明 |
|------|----------|------|
| `value == 0` | `signal = chip_param[N]` | 直接连接，无取反 |
| `width == 1 && value != 0` | `signal = ~chip_param[N]` | 1-bit 全取反 |
| `width > 1 && value != 0` | 逐位判断：value 对应 bit 为 1 取反，为 0 不取反 | 按位取反 |

### 5.2 示例

```python
# 输入信号
chip_id: width=16, value=0x9008 (0b1001000000001000)

# 生成的 RTL
chip_id = {
    ~chip_param[79],  // value[15]=1, 取反
     chip_param[78],  // value[14]=0, 不取反
     chip_param[77],  // value[13]=0, 不取反
    ~chip_param[76],  // value[12]=1, 取反
    ...
     chip_param[64]   // value[0]=0, 不取反
};
```

## 6. 输出文件

### 6.1 SystemVerilog 模块

**文件名**: `generated/{name}_distributor.sv`

**包含内容**:
1. **Packed Struct 定义**（可选）
   ```systemverilog
   typedef struct packed {
       logic [63:0]  uuid;
       logic [15:0]  chip_id;
       logic              efuse_val_csr_cfg_xtal_div2_en;
       ...
   } param_struct_t;
   ```

2. **Distributor 模块**
   ```systemverilog
   module param_distributor (
       input  logic [123:0]  chip_param,
       output logic [63:0]   uuid,
       output logic [15:0]   chip_id,
       ...
   );
   
       always_comb begin
           uuid = chip_param[63:0]; // value: 0x0
           chip_id = {~chip_param[79], ..., chip_param[64]}; // value: 0x9008
           ...
       end
   
   endmodule
   ```

**特性**:
- 每条赋值语句附带 `// value: 0xXX` 注释
- 自动推导总位宽（如 `[123:0]`）
- 按 start_bit 排序输出

### 6.2 Excel 字节/位映射表

**文件名**: `generated/{name}_byte_table_{timestamp}.xlsx`

**内容**:
| Byte | Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
|------|-------|-------|-------|-------|-------|-------|-------|-------|
| 0 | | | | | | | | uuid[0] |
| 1 | | | | | | | | uuid[8] |
| ... | | | | | | | | |

**特性**:
- 多 bit 信号自动合并单元格
- 不同信号使用不同背景颜色（12色轮询）
- 信号名标注 bit 范围（如 `uuid[7:0]`）

## 7. 快速使用

### 7.1 命令行方式

```bash
# 基础用法
python src/dynamic_signal_parser.py -i input/cygnetpluse_otp_map.txt -o distributor.sv

# 带参数
python src/dynamic_signal_parser.py \
    -i input/my_signal.csv \
    -o my_distributor.sv \
    -d generated \
    -s auto
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i, --input` | 输入信号列表文件 | （必填） |
| `-o, --output` | 输出 SV 文件名 | `param_distributor.sv` |
| `-d, --output-dir` | 输出目录 | `generated` |
| `-s, --strategy` | 分段策略：`auto`、`equal`、`functional` | `auto` |
| `--struct` | 是否生成 struct 定义 | `true` |

### 7.2 快捷脚本

```bash
# Windows 批处理
run.bat input\cygnetpluse_otp_map.txt cygnetpluse_otp_distributor.sv

# Python 脚本
python generate.py input/my_signal.csv my_distributor.sv

# Makefile (需 Git Bash)
make cygnet
make csv
make all
```

## 8. 项目目录结构

```
D:\test\codex\
├── run.bat                      # Windows 批处理快捷脚本
├── generate.py                  # Python 快捷脚本
├── Makefile                     # Make 命令支持
├── CLAUDE.md                    # Claude Code 项目指引
├── src/
│   └── dynamic_signal_parser.py # 主程序（~1174 行）
├── tests/                       # 测试套件
│   ├── test_signal_parser.py    # 核心解析测试
│   ├── test_inversion_logic.py  # 取反逻辑测试
│   ├── test_excel_generator.py  # Excel 生成测试
│   ├── test_validation.py       # 输入校验测试
│   ├── test_duplicate_signals.py# 重名信号测试
│   ├── test_advanced_features.py# 高级功能测试
│   └── test_reserved_signals.py # Reserved 信号测试
├── input/                       # 输入信号列表
│   ├── cygnetpluse_otp_map.txt  # 示例：Input port 格式
│   ├── my_signal.csv            # 示例：CSV 格式
│   ├── signals.txt              # 示例：HDL 格式
│   └── ...
├── generated/                   # 生成输出（自动创建）
│   ├── cygnetpluse_otp_distributor.sv
│   └── cygnetpluse_otp_distributor_byte_table_*.xlsx
└── docs/
    ├── INPUT_FORMAT.md          # 输入格式详细说明
    └── DESIGN.md                # 本文档
```

## 9. 信号解析流程

```
Input File
    │
    ▼
┌─────────────────┐
│ 1. 格式检测     │──┬──► CSV 格式？ ──► _parse_csv()
│    (自动)       │  │
└─────────────────┘  ├──► Input port？ ──► _parse_input()
    │                │
    ▼                └──► 默认 HDL ──► _parse_hdl()
┌─────────────────┐
│ 2. 信号解析     │──► 提取：name, width, value
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 3. 位宽分配     │──► 累加计算 start_bit
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 4. 取反逻辑     │──► 根据 value 生成 per-bit/full/none
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 5. 输出生成     │──► SV 模块 + Excel 表格
└─────────────────┘
```

## 10. 注意事项

1. **位宽对齐**: 信号按顺序连续分配，不会自动对齐到字节边界
2. **空 bit**: Byte 10-11 等可能存在空位（如 bit 91），Excel 中空单元格表示
3. **文件名时间戳**: Excel 文件名包含时间戳，避免文件锁定冲突
4. **颜色编码**: 12 色循环使用，相同信号在不同 byte 中颜色一致；reserved 信号使用灰色（#D3D3D3）
5. **Reserved 信号**: 名称为 `reserved`（不区分大小写）的信号在 SV 中被跳过，在 Excel 中灰色标注
6. **重名信号**: 自动添加 `_1`、`_2` 后缀避免冲突
7. **未解析行警告**: 解析完成后检查可能被跳过的行，输出警告信息
8. **编码**: 源文件使用 UTF-8 编码，对旧文件有 GBK 回退

## 11. 测试

### 运行测试
```bash
# 全部测试
python -m pytest tests/

# 单个测试文件
python -m pytest tests/test_reserved_signals.py

# 覆盖率
python -m coverage run -m pytest tests/
python -m coverage report --include=src/dynamic_signal_parser.py
```

### 测试文件

| 测试文件 | 覆盖范围 |
|----------|----------|
| `test_signal_parser.py` | 3 种格式解析、Signal 数据类 |
| `test_inversion_logic.py` | `_generate_rhs()` 取反规则 |
| `test_excel_generator.py` | openpyxl Excel 生成 |
| `test_validation.py` | 位宽/值不匹配警告 |
| `test_duplicate_signals.py` | 重名信号自动后缀处理 |
| `test_advanced_features.py` | CLI 参数、边界情况、表达式解析 |
| `test_reserved_signals.py` | Reserved 信号检测、SV 跳过、Excel 灰色、未解析行警告 |

## 12. 依赖

```
Python >= 3.7
openpyxl >= 3.0.0    (Excel 生成)
```

安装依赖：
```bash
pip install openpyxl
```
