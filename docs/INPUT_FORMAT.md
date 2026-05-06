# Dynamic Signal Parser - 输入格式说明

## 支持的输入格式

本脚本支持以下三种输入格式，会自动检测文件格式并解析：

---

## 格式一：HDL 格式（SystemVerilog/Verilog）

### 语法
```systemverilog
logic [msb:lsb] signal_name [value]
input [msb:lsb] signal_name [value]
output [msb:lsb] signal_name [value]
wire [msb:lsb] signal_name [value]
reg [msb:lsb] signal_name [value]
```

### 示例
```systemverilog
logic [3:0]  param_a           0x5
logic [7:0]  param_b           0x12
logic        valid             0x1
logic [2:0]  config           
```

### 说明
- `signal_name`: 信号名称（必填）
- `[msb:lsb]`: 位宽定义（可选，默认 1-bit）。缺少位宽定义的行会产生警告
- `value`: 默认值/反转值（可选，默认 0）
  - `0`: 直接输出，不取反
  - `非0`: 根据位宽决定取反方式
    - 1-bit: 整体取反 `~`
    - 多bit: 逐bit取反（value 的每一位决定对应位是否取反）

---

## 格式二：CSV 格式

### 语法
```csv
bitwidth,signal_name,default_value
```

### 示例
```csv
bitwidth,efuse_signals,default_value
,efuse_val_csr_single_bit,0x1
[3:0],efuse_val_csr_4bit,0x5
[7:0],efuse_val_csr_8bit,0x12
```

### 说明
- `bitwidth`: 位宽定义（可选）
  - 空字符串 = 1-bit 信号
  - `[msb:lsb]` 格式 = 多bit信号，如 `[7:0]`
- `signal_name`: 信号名称（必填）
- `default_value`: 默认值（必填）
  - 支持十六进制：`0x1`、`0xFF`
  - 支持十进制：`0`、`255`

### 注意事项
- 第一行可以是表头（会被自动跳过）
- 以 `;` 开头的行被视为注释
- 行内字段数不足时会产生未解析行警告

---

## 格式三：Input 端口格式（带中文注释）

### 语法
```systemverilog
input [msb:lsb] signal_name ， //efuse_default_value: value
input signal_name ， //efuse_default_value: value
input signal_name; //efuse_default_value: value
```

### 示例
```systemverilog
input               efuse_val_csr_single_bit           ，  //efuse_default_value: 0x1
input [3:0]         efuse_val_csr_4bit                 ，  //efuse_default_value: 0x5
input [7:0]         efuse_val_csr_8bit                 ，  //efuse_default_value: 0x12
input [13:0]        reserved                           ，  //efuse_default_value: 0x0
input efuse_val_csr_1000_p0_en_vga_op_outbias_ch0;     //efuse_default_value: 0x0
```

### 说明
- 以 `input` 关键字开头
- `[msb:lsb]` 位宽定义（可选，默认 1-bit）
- `signal_name`: 信号名称（必填）
- 分隔符: 中文逗号 `，`、英文逗号 `,` 或分号 `;`（三选一）
- `//efuse_default_value:`: 注释标记默认值（必填）
- `value`: 默认值（支持 `0x` 十六进制或十进制）

### Reserved 信号
信号名称为 `reserved`（不区分大小写）时自动识别为保留信号：
- SV 输出中跳过该信号（不生成端口和赋值）
- Excel 中用灰色（#D3D3D3）标注
- 位宽仍计入总参数宽度

### 未解析行警告
以下情况会产生警告：
- 缺少 `efuse_default_value` 注释
- 缺少逗号/分号分隔符

---

## Value 字段的反转逻辑

根据 `value` 和位宽，生成的 RTL 代码会有不同的取反逻辑：

| value | 位宽 | 生成的代码 | 说明 |
|-------|------|-----------|------|
| 0 | 任意 | `param[i]` | 原值，不取反 |
| 非0 | 1 | `~param[i]` | 整体取反 |
| 0x5 (0101) | 4 | `{param[3], ~param[2], param[1], ~param[0]}` | 逐bit取反，value 的 bit 为 1 的位置取反 |

### 示例
```
signal: logic [3:0] data, value = 0x5 (二进制 0101)
生成: data = {chip_param[3], ~chip_param[2], chip_param[1], ~chip_param[0]}
```

---

## 输出文件

运行脚本后会生成以下文件：

1. **{output_name}.sv**: SystemVerilog 模块代码
   - 包含打包结构体定义
   - 组合逻辑分发器 always_comb

2. **{output_name}_byte_table_{timestamp}.xlsx**: Excel 字节映射表
   - Byte/Bit 映射关系
   - 多bit信号自动合并单元格
   - 不同信号用不同背景色区分

---

## 使用方法

```bash
python dynamic_signal_parser.py -i input_file.txt -o output_file.sv
```

### 参数说明
- `-i, --input`: 输入信号列表文件
- `-o, --output`: 输出 SV 文件（默认 `param_distributor.sv`）
- `-d, --output-dir`: 输出目录（默认 `generated`）
- `-s, --strategy`: 分段策略（`auto`、`equal`、`functional`，默认 `auto`）
- `--struct`: 是否生成 struct 定义（默认 `true`）

---

## 格式检测优先级

脚本按以下顺序自动检测输入格式：

1. **CSV 格式**: 检查逗号分隔和 3 列结构
2. **Input 格式**: 检查 `input` 关键字和分隔符（`，`、`,`、`;`）及 `efuse_default_value` 注释
3. **HDL 格式**: 作为默认格式解析

---

## 示例文件

参见项目目录下的示例文件：
- `signals.txt` - HDL 格式示例
- `my_signal.csv` - CSV 格式示例  
- `my_signal2.txt` - Input 端口格式示例
