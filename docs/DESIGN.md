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
| `SignalParser` | 核心解析器，处理所有输入格式，生成信号段映射 |
| `SVGenerator` | SystemVerilog 代码生成器，包含 struct、module、assignment 生成 |
| `ExcelExporter` | Excel 表格生成器，创建带颜色编码的字节/位映射表 |

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

**注意**：使用中文逗号 `，` 作为分隔符，与 Verilog 语法区分。

## 4. 取反逻辑规则

工具根据 `efuse_default_value` 自动生成以下三种取反逻辑：

### 4.1 规则定义

| 条件 | 生成逻辑 | 说明 |
|------|----------|------|
| `value == 0` | `signal = chip_param[N]` | 直接连接，无取反 |
| `width == 1 && value != 0` | `signal = ~chip_param[N]` | 1-bit 全取反 |
| `width > 1 && value != 0` | 逐位判断：value 对应 bit 为 1 取反，为 0 不取反 | 按位取反 |

### 4.2 示例

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

## 5. 输出文件

### 5.1 SystemVerilog 模块

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

### 5.2 Excel 字节/位映射表

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

## 6. 快速使用

### 6.1 命令行方式

```bash
# 基础用法
python src/dynamic_signal_parser.py -i input/cygnetpluse_otp_map.txt -o distributor.sv

# 带参数
python src/dynamic_signal_parser.py \
    -i input/my_signal.csv \
    -o my_distributor.sv
```

### 6.2 快捷脚本

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

## 7. 项目目录结构

```
D:\test\codex\
├── run.bat                      # Windows 批处理快捷脚本
├── generate.py                  # Python 快捷脚本
├── Makefile                     # Make 命令支持
├── src/
│   └── dynamic_signal_parser.py # 主程序
├── input/                       # 输入信号列表
│   ├── cygnetpluse_otp_map.txt  # 示例：Input port 格式
│   ├── my_signal.csv            # 示例：CSV 格式
│   ├── my_signal2.txt           # 示例：HDL 格式
│   └── ...
├── generated/                   # 生成输出（自动创建）
│   ├── cygnetpluse_otp_distributor.sv
│   └── cygnetpluse_otp_distributor_byte_table_*.xlsx
└── docs/
    ├── INPUT_FORMAT.md          # 输入格式详细说明
    └── DESIGN.md                # 本文档
```

## 8. 信号解析流程

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

## 9. 注意事项

1. **位宽对齐**: 信号按顺序连续分配，不会自动对齐到字节边界
2. **空 bit**: Byte 10-11 等可能存在空位（如 bit 91），Excel 中空单元格表示
3. **文件名时间戳**: Excel 文件名包含时间戳，避免文件锁定冲突
4. **颜色编码**: 12 色循环使用，相同信号在不同 byte 中颜色一致

## 10. 依赖

```
Python >= 3.7
openpyxl >= 3.0.0    (Excel 生成)
```

安装依赖：
```bash
pip install openpyxl
```
