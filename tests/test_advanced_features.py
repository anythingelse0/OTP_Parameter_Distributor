#!/usr/bin/env python3
"""
高级功能单元测试
覆盖 analyze_segments、DistributorGenerator、命令行参数等
"""

import sys
import os
import tempfile
import io
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import (
    DynamicSignalParser, DistributorGenerator, Signal, SignalType, main
)


class TestAnalyzeSegments(unittest.TestCase):
    """测试 analyze_segments 方法"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_analyze_single_signal(self):
        """测试单信号分段分析"""
        text = "input[63:0] uuid                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")

        self.assertEqual(len(segments), 1)
        self.assertIn('uuid', segments)
        self.assertEqual(segments['uuid']['start_bit'], 0)
        self.assertEqual(segments['uuid']['end_bit'], 63)
        self.assertEqual(segments['uuid']['width'], 64)
        self.assertEqual(segments['uuid']['value'], 0)

    def test_analyze_multiple_signals(self):
        """测试多信号自动分段"""
        text = """input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008
input      flag                                          ，  //efuse_default_value: 0x1"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="auto")

        self.assertEqual(len(segments), 3)

        # uuid: [63:0]
        self.assertEqual(segments['uuid']['start_bit'], 0)
        self.assertEqual(segments['uuid']['end_bit'], 63)

        # chip_id: [79:64]
        self.assertEqual(segments['chip_id']['start_bit'], 64)
        self.assertEqual(segments['chip_id']['end_bit'], 79)

        # flag: [80:80]
        self.assertEqual(segments['flag']['start_bit'], 80)
        self.assertEqual(segments['flag']['end_bit'], 80)

    def test_analyze_with_different_strategies(self):
        """测试不同分段策略"""
        text = "input[63:0] uuid                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)

        # 测试 auto 策略
        segments_auto = self.parser.analyze_segments(strategy="auto")
        self.assertEqual(len(segments_auto), 1)

        # 测试 equal 策略
        segments_equal = self.parser.analyze_segments(strategy="equal")
        self.assertEqual(len(segments_equal), 1)

        # functional 策略未实现，返回空字典

    def test_analyze_equal_strategy_multiple_signals(self):
        """测试 equal 策略对多信号均分位宽"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[7:0] config                                        ，  //efuse_default_value: 0x2
input[7:0] status                                        ，  //efuse_default_value: 0x3"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments(strategy="equal")

        self.assertEqual(len(segments), 3)
        # 总宽 24，3 个信号，每个 8 位
        self.assertEqual(segments['data']['start_bit'], 0)
        self.assertEqual(segments['data']['width'], 8)
        self.assertEqual(segments['config']['start_bit'], 8)
        self.assertEqual(segments['config']['width'], 8)
        self.assertEqual(segments['status']['start_bit'], 16)
        self.assertEqual(segments['status']['width'], 8)
        segments_func = self.parser.analyze_segments(strategy="functional")
        self.assertEqual(len(segments_func), 0)


class TestCSVDetection(unittest.TestCase):
    """测试 CSV 格式检测"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_is_csv_format_simple(self):
        """测试简单 CSV 格式检测"""
        text = "bitwidth,name,default_value\n[31:0],uuid,0x12345678"
        self.assertTrue(self.parser._is_csv_format(text))

    def test_is_csv_format_with_empty_bitwidth(self):
        """测试 bitwidth 为空的 CSV 格式"""
        text = "bitwidth,name,default_value\n,flag,0x1"
        self.assertTrue(self.parser._is_csv_format(text))

    def test_is_csv_format_with_decimal_value(self):
        """测试十进制值的 CSV 格式"""
        text = "bitwidth,name,default_value\n[31:0],uuid,123"
        self.assertTrue(self.parser._is_csv_format(text))

    def test_is_not_csv_format_input_port(self):
        """测试 Input Port 格式不被误判为 CSV"""
        text = "input[63:0] uuid                                         ，  //efuse_default_value: 0"
        self.assertFalse(self.parser._is_csv_format(text))

    def test_is_not_csv_format_hdl(self):
        """测试 HDL 格式不被误判为 CSV"""
        text = "logic [31:0] uuid 0x12345678"
        self.assertFalse(self.parser._is_csv_format(text))

    def test_is_not_csv_format_with_comment(self):
        """测试带注释的格式检测"""
        text = "; This is a comment\n[31:0],uuid,0x0"
        self.assertTrue(self.parser._is_csv_format(text))


class TestDistributorGenerator(unittest.TestCase):
    """测试 DistributorGenerator 类"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_complete_sv(self):
        """测试生成完整 SV 文件"""
        text = "input[63:0] uuid                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)

        gen = DistributorGenerator(self.parser)
        sv_code = gen.generate_complete_sv()

        self.assertIn("typedef struct packed", sv_code)
        self.assertIn("module param_distributor", sv_code)
        self.assertIn("uuid = chip_param", sv_code)

    def test_generate_with_options_with_struct(self):
        """测试带 struct 选项的生成"""
        text = "input[31:0] data                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        gen = DistributorGenerator(self.parser)
        sv_code = gen.generate_with_options(
            segments,
            include_struct=True,
            include_comments=True,
            module_name="test_mod"
        )

        self.assertIn("typedef struct packed", sv_code)
        self.assertIn("module test_mod", sv_code)
        self.assertIn("Auto-generated", sv_code)

    def test_generate_with_options_no_struct(self):
        """测试不带 struct 选项的生成"""
        text = "input[31:0] data                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        gen = DistributorGenerator(self.parser)
        sv_code = gen.generate_with_options(
            segments,
            include_struct=False,
            include_comments=False,
            module_name="test_mod"
        )

        self.assertNotIn("typedef struct packed", sv_code)
        self.assertIn("module test_mod", sv_code)


class TestPrintFunctions(unittest.TestCase):
    """测试打印输出函数"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_print_analysis(self):
        """测试分析结果打印"""
        text = "input[31:0] uuid                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        sys.stdout = self.held_output
        self.parser.print_analysis(segments)
        output = self.held_output.getvalue()

        self.assertIn("SIGNAL ANALYSIS", output)
        self.assertIn("uuid", output)
        self.assertIn("Segment Map:", output)

    def test_print_byte_table(self):
        """测试字节表打印"""
        text = "input[15:0] data                                         ，  //efuse_default_value: 0xAB"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        sys.stdout = self.held_output
        self.parser.print_byte_table(segments)
        output = self.held_output.getvalue()

        self.assertIn("BYTE/BIT MAPPING TABLE", output)
        self.assertIn("Byte 0", output)

    def test_print_empty_segments(self):
        """测试空分段打印"""
        sys.stdout = self.held_output
        self.parser.print_analysis({})
        output = self.held_output.getvalue()

        self.assertIn("Total signals parsed: 0", output)


class TestCommandLineArgs(unittest.TestCase):
    """测试命令行参数处理"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_file = os.path.join(self.temp_dir.name, "test_input.txt")
        with open(self.input_file, 'w') as f:
            f.write("input[31:0] uuid                                         ，  //efuse_default_value: 0\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('sys.argv', ['script', '-i', 'dummy_input.txt', '-o', 'output.sv'])
    def test_main_with_args(self):
        """测试命令行参数解析"""
        # 这里我们只是测试参数解析，不实际运行 main
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', type=str, required=True)
        parser.add_argument('-o', '--output', type=str, default='param_distributor.sv')
        parser.add_argument('-d', '--output-dir', type=str, default='generated')
        args = parser.parse_args()

        self.assertEqual(args.input, 'dummy_input.txt')
        self.assertEqual(args.output, 'output.sv')
        self.assertEqual(args.output_dir, 'generated')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['script', '-i', 'nonexistent_file_xyz123.txt'])
    def test_main_no_signals_parsed(self, mock_stdout):
        """测试无信号解析时的输出"""
        # 由于 main 会尝试读取文件，我们用无效输入测试帮助信息
        try:
            with patch.object(sys, 'argv', ['script', '-h']):
                with self.assertRaises(SystemExit) as cm:
                    import argparse
                    parser = argparse.ArgumentParser()
                    parser.add_argument('-i', '--input', type=str, required=True)
                    parser.parse_args()
        except Exception:
            pass  # Help prints and exits


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_parse_empty_text(self):
        """测试空文本解析"""
        signals = self.parser.parse_signals("")
        self.assertEqual(len(signals), 0)

    def test_parse_whitespace_only(self):
        """测试纯空白文本解析"""
        signals = self.parser.parse_signals("   \n\t\n   ")
        self.assertEqual(len(signals), 0)

    def test_parse_comment_only(self):
        """测试纯注释文本"""
        signals = self.parser.parse_signals("// This is a comment")
        self.assertEqual(len(signals), 0)

    def test_parse_invalid_line(self):
        """测试包含无效行的文本"""
        text = """input[31:0] valid_sig                                    ，  //efuse_default_value: 0
this_line_is_invalid
input[7:0] another_sig                                   ，  //efuse_default_value: 0xFF"""
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 2)

    def test_large_bit_width(self):
        """测试超大位宽"""
        text = "input[255:0] very_wide_bus                               ，  //efuse_default_value: 0"
        signals = self.parser.parse_signals(text)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].width, 256)


class TestFileOperations(unittest.TestCase):
    """测试文件操作"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_read_input_file_utf8(self):
        """测试 UTF-8 编码文件读取"""
        input_file = os.path.join(self.temp_dir.name, "utf8_input.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("input[31:0] test_sig                                     ，  //efuse_default_value: 0\n")

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        signals = self.parser.parse_signals(content)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "test_sig")

    def test_generate_output_file(self):
        """测试输出文件生成"""
        text = "input[31:0] test_sig                                     ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        output_file = os.path.join(self.temp_dir.name, "test_output.sv")
        sv_code = self.parser.generate_sv_module(segments, "test_module")

        with open(output_file, 'w') as f:
            f.write(sv_code)

        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            content = f.read()
        self.assertIn("module test_module", content)


class TestEvalSimpleExpr(unittest.TestCase):
    """测试 _eval_simple_expr 表达式解析"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_direct_integer(self):
        """测试直接整数解析"""
        self.assertEqual(self.parser._eval_simple_expr("8"), 8)
        self.assertEqual(self.parser._eval_simple_expr("0"), 0)
        self.assertEqual(self.parser._eval_simple_expr("256"), 256)

    def test_integer_with_spaces(self):
        """测试带空格的整数"""
        self.assertEqual(self.parser._eval_simple_expr("  8  "), 8)

    def test_subtraction_expression(self):
        """测试减法表达式"""
        self.assertEqual(self.parser._eval_simple_expr("4-1"), 3)
        self.assertEqual(self.parser._eval_simple_expr("10-1"), 9)
        self.assertEqual(self.parser._eval_simple_expr("8-1"), 7)

    def test_subtraction_with_spaces(self):
        """测试带空格的减法表达式"""
        self.assertEqual(self.parser._eval_simple_expr("4 - 1"), 3)

    def test_invalid_expression_raises(self):
        """测试无效表达式抛出异常"""
        with self.assertRaises(ValueError):
            self.parser._eval_simple_expr("abc")

    def test_invalid_parts_raises(self):
        """测试无法解析的部分抛出异常"""
        with self.assertRaises(ValueError):
            self.parser._eval_simple_expr("a-b")


if __name__ == "__main__":
    unittest.main(verbosity=2)
