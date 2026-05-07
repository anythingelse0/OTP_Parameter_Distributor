#!/usr/bin/env python3
"""
信号解析单元测试
测试三种输入格式：HDL、CSV、Input Port
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import Signal, SignalType, DynamicSignalParser


class TestSignal(unittest.TestCase):
    """测试 Signal 数据类"""

    def test_signal_creation(self):
        """测试信号对象创建"""
        signal = Signal(name="test_sig", width=32, value=0x12345678)
        self.assertEqual(signal.name, "test_sig")
        self.assertEqual(signal.width, 32)
        self.assertEqual(signal.value, 0x12345678)
        self.assertEqual(signal.signal_type, SignalType.LOGIC)

    def test_1bit_signal_bit_range(self):
        """测试 1-bit 信号 bit_range 为空"""
        signal = Signal(name="single_bit", width=1)
        self.assertEqual(signal.bit_range, "")

    def test_multibit_signal_bit_range(self):
        """测试多位信号 bit_range 格式"""
        signal = Signal(name="multi_bit", width=32)
        self.assertEqual(signal.bit_range, "[31:0]")
        
        signal2 = Signal(name="byte", width=8)
        self.assertEqual(signal2.bit_range, "[7:0]")

    def test_signal_type_str(self):
        """测试信号类型字符串"""
        signal = Signal(name="s", width=1, signal_type=SignalType.LOGIC)
        self.assertEqual(signal.type_str, "logic")


class TestInputFormatParser(unittest.TestCase):
    """测试 Input Port 格式解析"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_1bit_input_signal(self):
        """测试解析 1-bit input 信号"""
        text = "input      test_1bit                                          ，  //efuse_default_value: 0x1"
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "test_1bit")
        self.assertEqual(signals[0].width, 1)
        self.assertEqual(signals[0].value, 1)

    def test_parse_multibit_input_signal(self):
        """测试解析多位宽 input 信号"""
        text = "input[63:0] uuid                                          ，  //efuse_default_value: 0"
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 64)
        self.assertEqual(signals[0].value, 0)

    def test_parse_multiple_input_signals(self):
        """测试解析多个 input 信号"""
        text = """input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008
input      single_bit                                   ，  //efuse_default_value: 0x1"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        
        # 验证第一个信号
        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 64)
        self.assertEqual(signals[0].value, 0)
        
        # 验证第二个信号
        self.assertEqual(signals[1].name, "chip_id")
        self.assertEqual(signals[1].width, 16)
        self.assertEqual(signals[1].value, 0x9008)
        
        # 验证第三个信号
        self.assertEqual(signals[2].name, "single_bit")
        self.assertEqual(signals[2].width, 1)
        self.assertEqual(signals[2].value, 1)

    def test_parse_hex_value_lowercase(self):
        """测试小写十六进制值"""
        text = "input[7:0] reg_val                                      ，  //efuse_default_value: 0xab"
        signals = self.parser.parse_signals(text)
        self.assertEqual(signals[0].value, 0xAB)

    def test_parse_hex_value_uppercase(self):
        """测试大写十六进制值"""
        text = "input[7:0] reg_val                                      ，  //efuse_default_value: 0xAB"
        signals = self.parser.parse_signals(text)
        self.assertEqual(signals[0].value, 0xAB)

    def test_parse_decimal_value(self):
        """测试十进制值"""
        text = "input[7:0] dec_val                                      ，  //efuse_default_value: 255"
        signals = self.parser.parse_signals(text)
        self.assertEqual(signals[0].value, 255)


class TestCSVFormatParser(unittest.TestCase):
    """测试 CSV 格式解析"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_simple_csv(self):
        """测试简单 CSV 格式"""
        text = "bitwidth,name,default_value\n[31:0],uuid,0x12345678"
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 32)
        self.assertEqual(signals[0].value, 0x12345678)

    def test_parse_csv_multiple_signals(self):
        """测试 CSV 多行信号"""
        text = """bitwidth,name,default_value
[31:0],uuid,0x12345678
[7:0],chip_id,0xAB
,flag,1"""

        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 3)

        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 32)

        self.assertEqual(signals[1].name, "chip_id")
        self.assertEqual(signals[1].width, 8)

        self.assertEqual(signals[2].name, "flag")
        self.assertEqual(signals[2].width, 1)

    def test_parse_csv_with_spaces(self):
        """测试带空格的 CSV"""
        text = "bitwidth,name,default_value\n  [31:0]  ,  uuid  ,  0x12345678  "
        signals = self.parser.parse_signals(text)

        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 32)


class TestHDLFormatParser(unittest.TestCase):
    """测试 HDL 格式解析"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_hdl_simple(self):
        """测试简单 HDL 格式"""
        text = "logic [31:0] uuid 0x12345678"
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "uuid")
        self.assertEqual(signals[0].width, 32)
        self.assertEqual(signals[0].value, 0x12345678)

    def test_parse_hdl_no_value(self):
        """测试无值的 HDL 格式"""
        text = "logic [7:0] status"
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "status")
        self.assertEqual(signals[0].width, 8)
        self.assertEqual(signals[0].value, 0)

    def test_parse_hdl_1bit(self):
        """测试 1-bit HDL - 格式: logic [0:0] flag 0x1"""
        text = "logic [0:0] flag 0x1"
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "flag")
        self.assertEqual(signals[0].width, 1)


class TestFormatDetection(unittest.TestCase):
    """测试格式自动检测"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_detect_input_format(self):
        """测试识别 Input Port 格式"""
        text = "input[63:0] uuid ，  //efuse_default_value: 0"
        # 检测方法被 parse_signals 内部调用，这里测试解析结果
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "uuid")

    def test_detect_csv_format(self):
        """测试识别 CSV 格式"""
        text = "bitwidth,name,default_value\n[31:0],uuid,0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "uuid")


class TestSemicolonDelimiter(unittest.TestCase):
    """测试分号分隔符变体（cygnetpluse_otp_map.txt 使用的格式）"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_semicolon_delimiter(self):
        """测试分号分隔：input [15:0] name;//efuse_default_value: 0x0"""
        text = "input [15:0]            efuse_val_reg2_data;//efuse_default_value: 0x0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_val_reg2_data")
        self.assertEqual(signals[0].width, 16)
        self.assertEqual(signals[0].value, 0)

    def test_parse_space_before_colon(self):
        """测试冒号前有空格：efuse_default_value : 0x0"""
        text = "input [7:0]             efuse_val_test;//efuse_default_value : 0x5"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].value, 0x5)

    def test_parse_space_after_double_slash(self):
        """测试 // 后有空格：// efuse_default_value : 0x0"""
        text = "input                   efuse_val_test;// efuse_default_value : 0x3"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_val_test")
        self.assertEqual(signals[0].value, 0x3)


class TestInputLogicFormat(unittest.TestCase):
    """测试 input logic [N:0] 格式"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_input_logic(self):
        """测试 input logic [3:0] name 格式"""
        text = "input logic [3:0]       efuse_val_test;//efuse_default_value: 0x5"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_val_test")
        self.assertEqual(signals[0].width, 4)

    def test_parse_input_logic_1bit(self):
        """测试 input logic 1-bit（无位宽声明）"""
        text = "input logic             efuse_val_test;//efuse_default_value : 0x0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_val_test")
        self.assertEqual(signals[0].width, 1)


class TestExpressionWidth(unittest.TestCase):
    """测试表达式位宽 [N-1:0] 格式"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_expression_width(self):
        """测试 [4-1:0] 格式解析为宽度 4"""
        text = "input [4-1:0]           test_signal ，  //efuse_default_value: 0x3"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "test_signal")
        self.assertEqual(signals[0].width, 4)
        self.assertTrue(signals[0].explicit_width)


class TestNegativeBitRange(unittest.TestCase):
    """测试非法位宽范围校验"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_inverted_range_hdl(self):
        """测试 HDL 格式反转位宽 [0:3] 被跳过"""
        text = "logic [0:3] bad_signal 0x0\nlogic [7:0] good_signal 0x1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "good_signal")

    def test_inverted_range_input(self):
        """测试 Input 格式反转位宽被跳过"""
        text = "input [0:3]             bad_signal ，  //efuse_default_value: 0x0\ninput [7:0]             good_signal ，  //efuse_default_value: 0x1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "good_signal")

    def test_inverted_range_csv(self):
        """测试 CSV 格式反转位宽被跳过"""
        text = "bitwidth,name,default_value\n[0:3],bad_signal,0x0\n[7:0],good_signal,0x1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "good_signal")


class TestBareSignals(unittest.TestCase):
    """测试无位宽声明的裸信号（隐式1-bit）"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_bare_signal_with_hex_value(self):
        """测试裸信号 name 0x0 格式"""
        text = "efuse_val_csr_cfg_xtal_div2_en\t0x0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_val_csr_cfg_xtal_div2_en")
        self.assertEqual(signals[0].width, 1)
        self.assertEqual(signals[0].value, 0)

    def test_bare_signal_with_decimal_value(self):
        """测试裸信号 name 1 格式"""
        text = "efuse_test_signal\t1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "efuse_test_signal")
        self.assertEqual(signals[0].width, 1)
        self.assertEqual(signals[0].value, 1)

    def test_bare_signal_mixed_with_ranged(self):
        """测试裸信号与有位宽信号混合"""
        text = "[3:0]	efuse_val_csr_digpll_bias_ext	0x5\n\tefuse_val_csr_cfg_xtal_div2_en	0x0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].name, "efuse_val_csr_digpll_bias_ext")
        self.assertEqual(signals[0].width, 4)
        self.assertEqual(signals[1].name, "efuse_val_csr_cfg_xtal_div2_en")
        self.assertEqual(signals[1].width, 1)

    def test_bare_signal_explicit_width_false(self):
        """测试裸信号的 explicit_width 为 False"""
        text = "efuse_test_signal\t0x0"
        signals = self.parser.parse_signals(text)
        self.assertFalse(signals[0].explicit_width)


class TestDetectType(unittest.TestCase):
    """测试 _detect_type 信号类型检测"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_detect_bit_type(self):
        """测试 bit 类型检测"""
        from dynamic_signal_parser import SignalType
        self.assertEqual(self.parser._detect_type("output bit flag"), SignalType.BIT)

    def test_detect_wire_type(self):
        """测试 wire 类型检测"""
        from dynamic_signal_parser import SignalType
        self.assertEqual(self.parser._detect_type("wire [7:0] data"), SignalType.WIRE)

    def test_detect_reg_type(self):
        """测试 reg 类型检测"""
        from dynamic_signal_parser import SignalType
        self.assertEqual(self.parser._detect_type("reg [3:0] state"), SignalType.REG)

    def test_detect_logic_type(self):
        """测试 logic 类型检测"""
        from dynamic_signal_parser import SignalType
        self.assertEqual(self.parser._detect_type("logic [7:0] data"), SignalType.LOGIC)

    def test_detect_default_type(self):
        """测试无关键字时默认 logic"""
        from dynamic_signal_parser import SignalType
        self.assertEqual(self.parser._detect_type("[7:0] data"), SignalType.LOGIC)


class TestCSVEdgeCases(unittest.TestCase):
    """测试 CSV 格式边界情况"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_csv_skip_empty_lines(self):
        """测试 CSV 跳过空行"""
        text = "bitwidth,name,default_value\n[7:0],sig_a,0x1\n\n[3:0],sig_b,0x2"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 2)

    def test_csv_skip_comment_lines(self):
        """测试 CSV 跳过分号注释行"""
        text = "bitwidth,name,default_value\n;this is a comment\n[7:0],sig_a,0x1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)

    def test_csv_skip_header_line(self):
        """测试 CSV 跳过 bitwith 表头"""
        text = "bitwidth,name,default_value\n[7:0],sig_a,0x1"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)


class TestGenerateAssignmentLogic(unittest.TestCase):
    """测试 generate_assignment_logic 函数"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_assignment_logic_basic(self):
        """测试基本的组合逻辑生成"""
        text = "logic [7:0] data 0x0\nlogic [3:0] config 0x5"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        code = self.parser.generate_assignment_logic(segments)

        self.assertIn("always_comb begin", code)
        self.assertIn("data =", code)
        self.assertIn("config =", code)
        self.assertIn("end", code)

    def test_assignment_logic_skips_reserved(self):
        """测试 assignment_logic 跳过 reserved 信号"""
        text = "logic [7:0] data 0x0\nlogic [3:0] reserved 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        code = self.parser.generate_assignment_logic(segments)

        self.assertIn("data =", code)
        self.assertNotIn("reserved =", code)

    def test_assignment_logic_inversion(self):
        """测试 assignment_logic 生成取反逻辑"""
        text = "logic [7:0] data 0xFF"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        code = self.parser.generate_assignment_logic(segments)

        self.assertIn("~", code)


class TestGenerateSVModule(unittest.TestCase):
    """测试 generate_sv_module 函数"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_sv_module_implicit_1bit(self):
        """测试隐式1-bit信号在SV模块中的输出格式"""
        from dynamic_signal_parser import DistributorGenerator
        text = "logic [7:0] data 0x0\nefuse_test_flag 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        gen = DistributorGenerator(self.parser)
        code = gen.generate_with_options(segments, include_struct=False, module_name="test")

        # 隐式1-bit 不应有 [0:0]
        self.assertIn("output logic                   efuse_test_flag", code)
        self.assertNotIn("[0:0]      efuse_test_flag", code)

    def test_sv_module_explicit_1bit(self):
        """测试显式1-bit信号在SV模块中的输出格式"""
        from dynamic_signal_parser import DistributorGenerator
        text = "logic [0:0] flag 0x1\nlogic [7:0] data 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        gen = DistributorGenerator(self.parser)
        code = gen.generate_with_options(segments, include_struct=False, module_name="test")

        # 显式1-bit 应有 [0:0]
        self.assertIn("[0:0]      flag", code)


class TestGenerateStructDefinition(unittest.TestCase):
    """测试 generate_struct_definition 函数"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_struct_1bit_signal(self):
        """测试 struct 中1-bit信号的格式"""
        from dynamic_signal_parser import DistributorGenerator
        text = "logic [7:0] data 0x0\nefuse_test_flag 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        gen = DistributorGenerator(self.parser)
        code = gen.generate_with_options(segments, include_struct=True, module_name="test")

        # 1-bit signal in struct should have no bit range
        self.assertIn("logic              efuse_test_flag;", code)
        # multi-bit should have bit range
        self.assertIn("logic [7:0]  data;", code)


class TestGenerateByteTable(unittest.TestCase):
    """测试 generate_byte_table 函数"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_byte_table_empty_segments(self):
        """测试空 segments 返回空字符串"""
        result = self.parser.generate_byte_table({})
        self.assertEqual(result, "")

    def test_byte_table_single_bit_range(self):
        """测试单bit信号的字节表显示"""
        text = "logic [0:0] flag 0x1"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        table = self.parser.generate_byte_table(segments)

        self.assertIn("BYTE/BIT MAPPING TABLE", table)
        self.assertIn("flag", table)

    def test_byte_table_multi_bit_signal(self):
        """测试多位信号在字节表中显示位范围"""
        text = "logic [7:0] data 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        table = self.parser.generate_byte_table(segments)

        self.assertIn("data[7:0]", table)

    def test_byte_table_single_bit_implicit(self):
        """测试隐式1-bit信号在字节表中不显示位范围"""
        text = "logic [7:0] data 0x0\nefuse_flag 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        table = self.parser.generate_byte_table(segments)

        # 隐式1-bit 不应有 [0:0]
        self.assertIn("efuse_flag", table)
        self.assertNotIn("efuse_flag[0:0]", table)

    def test_byte_table_single_bit_span(self):
        """测试多位信号跨字节时单bit显示 [N] 格式"""
        # 9-bit signal at start_bit=0: Byte 0 covers [7:0], Byte 1 covers [8]
        text = "logic [8:0] data 0x0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")
        table = self.parser.generate_byte_table(segments)

        # Byte 1 should show data[8] (single bit)
        self.assertIn("data[8]", table)


class TestWarningBranches(unittest.TestCase):
    """测试验证警告的分支路径"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_value_validation_warning_printed(self):
        """测试值超出范围时打印警告"""
        import io
        from contextlib import redirect_stdout

        # 2-bit signal with value 0xFF (exceeds max 0x3)
        text = "input [1:0]             test_sig ，  //efuse_default_value: 0xFF"
        f = io.StringIO()
        with redirect_stdout(f):
            self.parser.parse_signals(text)
        output = f.getvalue()

        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("test_sig", output)


class TestPrintAnalysis(unittest.TestCase):
    """测试 print_analysis 终端输出"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_print_analysis_output(self):
        """测试 print_analysis 生成分析输出"""
        import io
        from contextlib import redirect_stdout

        text = "logic [7:0] data 0x0\nlogic [3:0] reserved 0x0\nlogic [0:0] flag 0x1\nlogic [7:0] invert 0xF0"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")

        f = io.StringIO()
        with redirect_stdout(f):
            self.parser.print_analysis(segments)
        output = f.getvalue()

        self.assertIn("SIGNAL ANALYSIS & SEGMENTATION", output)
        self.assertIn("reserved (R)", output)
        self.assertIn("none", output)
        self.assertIn("full (~)", output)
        self.assertIn("per-bit", output)

    def test_print_analysis_single_bit_range(self):
        """测试 print_analysis 单bit信号显示 [N] 格式"""
        import io
        from contextlib import redirect_stdout

        text = "logic [0:0] flag 0x1"
        signals = self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")

        f = io.StringIO()
        with redirect_stdout(f):
            self.parser.print_analysis(segments)
        output = f.getvalue()

        self.assertIn("[0]", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
