#!/usr/bin/env python3
"""
模块统计功能测试
测试 // module:xxx 标记解析和每模块 bit 统计
"""

import sys
import os
import io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import DynamicSignalParser


class TestModuleMarkerParsing(unittest.TestCase):
    """测试 // module:xxx 标记解析"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_module_markers_input_format(self):
        """测试 Input Port 格式中 module 标记"""
        text = """// module:top_ctrl
input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] config                                        ，  //efuse_default_value: 0
// module:phy_cfg
input[15:0] phy_reg                                      ，  //efuse_default_value: 0xAB"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].module, "top_ctrl")
        self.assertEqual(signals[1].module, "top_ctrl")
        self.assertEqual(signals[2].module, "phy_cfg")

    def test_module_markers_csv_format(self):
        """测试 CSV 格式中 module 标记"""
        text = """// module:mod_a
[7:0],data,0x1
[3:0],config,0
// module:mod_b
[15:0],phy_reg,0xAB"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].module, "mod_a")
        self.assertEqual(signals[1].module, "mod_a")
        self.assertEqual(signals[2].module, "mod_b")

    def test_module_markers_hdl_format(self):
        """测试 HDL 格式中 module 标记"""
        text = """// module:mod_x
logic [7:0] data 0x1
logic [3:0] config 0
// module:mod_y
logic [15:0] phy_reg 0xAB"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].module, "mod_x")
        self.assertEqual(signals[1].module, "mod_x")
        self.assertEqual(signals[2].module, "mod_y")

    def test_signals_before_marker_are_unnamed(self):
        """测试标记前的信号属于 (unnamed)"""
        text = """input[7:0] global_data                                      ，  //efuse_default_value: 0
// module:top_ctrl
input[7:0] data                                          ，  //efuse_default_value: 0x1"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].module, "")
        self.assertEqual(signals[1].module, "top_ctrl")

    def test_no_module_markers(self):
        """测试没有 module 标记时所有信号 module 为空"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] config                                        ，  //efuse_default_value: 0"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].module, "")
        self.assertEqual(signals[1].module, "")

    def test_module_in_segments(self):
        """测试 segments 中包含 module 信息"""
        text = """// module:ctrl
input[7:0] data                                          ，  //efuse_default_value: 0x1"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        self.assertEqual(segments['data']['module'], "ctrl")

    def test_multiple_module_switches(self):
        """测试多次切换模块"""
        text = """// module:mod_a
input[7:0] sig_a                                         ，  //efuse_default_value: 0
// module:mod_b
input[7:0] sig_b                                         ，  //efuse_default_value: 0
// module:mod_c
input[7:0] sig_c                                         ，  //efuse_default_value: 0
// module:mod_a
input[7:0] sig_a2                                        ，  //efuse_default_value: 0"""
        signals = self.parser.parse_signals(text)

        self.assertEqual(signals[0].module, "mod_a")
        self.assertEqual(signals[1].module, "mod_b")
        self.assertEqual(signals[2].module, "mod_c")
        self.assertEqual(signals[3].module, "mod_a")


class TestModuleBitStatistics(unittest.TestCase):
    """测试模块 bit 统计输出"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_module_stats_output(self):
        """测试模块统计输出内容"""
        text = """// module:top_ctrl
input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] config                                        ，  //efuse_default_value: 0
// module:phy_cfg
input[15:0] phy_reg                                      ，  //efuse_default_value: 0xAB
input[7:0] status                                        ，  //efuse_default_value: 0"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        sys.stdout = self.held_output
        self.parser.print_module_stats(segments)
        output = self.held_output.getvalue()

        self.assertIn("MODULE BIT STATISTICS", output)
        self.assertIn("top_ctrl", output)
        self.assertIn("phy_cfg", output)
        self.assertIn("12", output)   # top_ctrl: 8+4=12 bits
        self.assertIn("24", output)   # phy_cfg: 16+8=24 bits
        self.assertIn("Total", output)

    def test_module_stats_with_unnamed(self):
        """测试包含 unnamed 信号的统计"""
        text = """input[7:0] global                                         ，  //efuse_default_value: 0
// module:ctrl
input[7:0] data                                          ，  //efuse_default_value: 0x1"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        sys.stdout = self.held_output
        self.parser.print_module_stats(segments)
        output = self.held_output.getvalue()

        self.assertIn("(unnamed)", output)
        self.assertIn("ctrl", output)

    def test_module_stats_empty_segments(self):
        """测试空 segments 不输出"""
        sys.stdout = self.held_output
        self.parser.print_module_stats({})
        output = self.held_output.getvalue()

        self.assertEqual(output, "")

    def test_module_stats_no_markers(self):
        """测试无 module 标记时全部为 unnamed"""
        text = """input[7:0] data                                          ，  //efuse_default_value: 0x1
input[3:0] config                                        ，  //efuse_default_value: 0"""
        self.parser.parse_signals(text)
        segments = self.parser.analyze_segments()

        sys.stdout = self.held_output
        self.parser.print_module_stats(segments)
        output = self.held_output.getvalue()

        self.assertIn("(unnamed)", output)
        self.assertNotIn("top_ctrl", output)


if __name__ == '__main__':
    unittest.main()
