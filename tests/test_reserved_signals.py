#!/usr/bin/env python3
"""
Reserved 信号处理测试
测试 reserved 信号的解析、SV 跳过、Excel 灰色标注
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import Signal, SignalType, DynamicSignalParser


class TestReservedSignalDetection(unittest.TestCase):
    """测试 reserved 信号检测"""

    def test_reserved_signal_flag_input_format(self):
        """测试 Input Port 格式中 reserved 信号被正确标记"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0
input[15:0] config                                       ，  //efuse_default_value: 0x1234"""
        parser = DynamicSignalParser()
        signals = parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertFalse(signals[0].is_reserved)  # data
        self.assertTrue(signals[1].is_reserved)   # reserved
        self.assertFalse(signals[2].is_reserved)  # config

    def test_reserved_signal_flag_csv_format(self):
        """测试 CSV 格式中 reserved 信号被正确标记"""
        text = """[7:0],data,0x1
[3:0],reserved,0
[15:0],config,0x1234"""
        parser = DynamicSignalParser()
        signals = parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertFalse(signals[0].is_reserved)
        self.assertTrue(signals[1].is_reserved)
        self.assertFalse(signals[2].is_reserved)

    def test_reserved_signal_flag_hdl_format(self):
        """测试 HDL 格式中 reserved 信号被正确标记"""
        text = """logic [7:0] data 0x1
logic [3:0] reserved 0
logic [15:0] config 0x1234"""
        parser = DynamicSignalParser()
        signals = parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertFalse(signals[0].is_reserved)
        self.assertTrue(signals[1].is_reserved)
        self.assertFalse(signals[2].is_reserved)

    def test_reserved_signal_name_case_insensitive(self):
        """测试 reserved 检测不区分大小写"""
        text = """input[3:0] Reserved                                      ，  //efuse_default_value: 0
input[3:0] RESERVED                                      ，  //efuse_default_value: 0
input[3:0] Reserved                                      ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        signals = parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        # 第一个 Reserved 保留原名，后续重复添加后缀
        self.assertTrue(signals[0].is_reserved)
        self.assertTrue(signals[1].is_reserved)
        self.assertTrue(signals[2].is_reserved)

    def test_reserved_signal_in_segments(self):
        """测试 reserved 信号在 segments 中包含 is_reserved 标记"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()

        self.assertFalse(segments['data']['is_reserved'])
        self.assertTrue(segments['reserved']['is_reserved'])


class TestReservedSignalSVGeneration(unittest.TestCase):
    """测试 reserved 信号在 SV 生成中被跳过"""

    def test_reserved_skipped_in_sv_module(self):
        """测试 reserved 信号不出现在 SV module 输出端口中"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0
input[15:0] config                                       ，  //efuse_default_value: 0x1234"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()
        sv = parser.generate_sv_module(segments)

        # reserved 信号不应出现在输出端口声明中
        self.assertNotIn("output logic", sv.split("always_comb")[0].split("reserved"))
        # data 和 config 应该出现
        self.assertIn("data", sv)
        self.assertIn("config", sv)
        # reserved 不应该作为输出端口
        self.assertNotRegex(sv, r"output\s+logic\s+\[?\d?:?\d?\]?\s*reserved")

    def test_reserved_skipped_in_sv_assignments(self):
        """测试 reserved 信号不出现在 always_comb 块中"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()
        sv = parser.generate_sv_module(segments)

        # 在 always_comb 块中不应该有 reserved 的赋值
        always_comb_block = sv.split("always_comb begin")[1].split("end")[0]
        self.assertNotIn("reserved =", always_comb_block)

    def test_reserved_skipped_in_struct(self):
        """测试 reserved 信号不出现在 struct 定义中"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()
        struct = parser.generate_struct_definition(segments)

        self.assertNotIn("reserved", struct)
        self.assertIn("data", struct)

    def test_reserved_bit_width_preserved_in_total(self):
        """测试 reserved 信号的位宽仍计入总位宽"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0
input[15:0] config                                       ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()

        # 总位宽应包含 reserved 的 4 位
        max_end = max(seg['end_bit'] for seg in segments.values())
        self.assertEqual(max_end, 27)  # 8 + 4 + 16 - 1 = 27

    def test_only_reserved_signals(self):
        """测试全部是 reserved 信号的情况"""
        text = """input[7:0] reserved                                      ，  //efuse_default_value: 0
input[3:0] reserved                                      ，  //efuse_default_value: 0"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()
        sv = parser.generate_sv_module(segments)

        # 模块应该仍然有效，但没有输出端口
        self.assertIn("module param_distributor", sv)
        self.assertIn("always_comb begin", sv)
        # 不应该有输出端口
        self.assertNotIn("output logic", sv)


class TestReservedSignalExcel(unittest.TestCase):
    """测试 reserved 信号在 Excel 中使用灰色"""

    def test_reserved_color_constant_defined(self):
        """测试 RESERVED_COLOR 常量已定义"""
        from dynamic_signal_parser import RESERVED_COLOR
        self.assertEqual(RESERVED_COLOR, "D3D3D3")

    def test_excel_generation_with_reserved(self):
        """测试 Excel 生成包含 reserved 信号时不报错"""
        try:
            from openpyxl import Workbook
        except ImportError:
            self.skipTest("openpyxl not installed")

        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] reserved                                      ，  //efuse_default_value: 0
input[15:0] config                                       ，  //efuse_default_value: 0x1234"""
        parser = DynamicSignalParser()
        parser.parse_signals(text)
        segments = parser.analyze_segments()

        output_file = os.path.join(os.path.dirname(__file__), '..', 'generated', 'test_reserved.xlsx')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # 不应该抛出异常
        parser.generate_byte_table_excel(segments, output_file)
        self.assertTrue(os.path.exists(output_file))

        # 清理
        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
