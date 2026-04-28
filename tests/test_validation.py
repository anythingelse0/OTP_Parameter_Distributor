#!/usr/bin/env python3
"""
值验证警告单元测试
测试 value 超位宽检测和警告输出
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from io import StringIO
from dynamic_signal_parser import DynamicSignalParser, Signal, SignalType


class TestValueValidation(unittest.TestCase):
    """测试值验证警告"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        # 捕获 stdout
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # 恢复 stdout
        sys.stdout = self.original_stdout

    def test_1bit_signal_value_larger_than_1(self):
        """测试 1-bit 信号 value > 1 触发警告"""
        # 1-bit 信号，value=7 (111)，应该触发警告
        text = "input      test_1bit                                          ，  //efuse_default_value: 0x7"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("test_1bit", output)
        self.assertIn("1-bit", output)

    def test_4bit_signal_value_exceeds_max(self):
        """测试 4-bit 信号 value > 0xF 触发警告"""
        # 4-bit max = 15 (0xF)，value=21 (0x15) 超出范围
        text = "input[3:0]  test_nibble                                        ，  //efuse_default_value: 0x15"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("test_nibble", output)
        self.assertIn("4-bit", output)
        self.assertIn("max 0xF", output)

    def test_2bit_signal_value_exceeds_max(self):
        """测试 2-bit 信号 value > 0x3 触发警告"""
        # 2-bit max = 3 (0x3)，value=5 (0x5) 超出范围
        text = "input[1:0]  test_2bit                                          ，  //efuse_default_value: 0x5"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("test_2bit", output)
        self.assertIn("2-bit", output)
        self.assertIn("max 0x3", output)

    def test_8bit_signal_value_exceeds_max(self):
        """测试 8-bit 信号 value > 0xFF 触发警告"""
        text = "input[7:0]  test_byte                                          ，  //efuse_default_value: 0x1FF"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("8-bit", output)
        self.assertIn("max 0xFF", output)

    def test_valid_1bit_value_0(self):
        """测试 1-bit value=0 不触发警告"""
        text = "input      valid_1bit                                          ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertNotIn("VALUE VALIDATION WARNINGS", output)

    def test_valid_1bit_value_1(self):
        """测试 1-bit value=1 不触发警告"""
        text = "input      valid_1bit                                          ，  //efuse_default_value: 0x1"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertNotIn("VALUE VALIDATION WARNINGS", output)

    def test_valid_4bit_max_value(self):
        """测试 4-bit max value=0xF 不触发警告"""
        text = "input[3:0]  valid_nibble                                        ，  //efuse_default_value: 0xF"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertNotIn("VALUE VALIDATION WARNINGS", output)

    def test_valid_4bit_value_boundary(self):
        """测试 4-bit boundary value=0xF (15)"""
        text = "input[3:0]  boundary_test                                        ，  //efuse_default_value: 15"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertNotIn("VALUE VALIDATION WARNINGS", output)

    def test_multiple_warnings(self):
        """测试多个信号同时触发警告"""
        text = """input[3:0]  sig_a                                        ，  //efuse_default_value: 0x20
input[1:0]  sig_b                                        ，  //efuse_default_value: 0xF
input      sig_c                                        ，  //efuse_default_value: 0xAB"""
        
        self.parser.parse_signals(text)
        output = self.held_output.getvalue()
        
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        # 所有三个信号都应该触发警告
        self.assertIn("sig_a", output)
        self.assertIn("sig_b", output)
        self.assertIn("sig_c", output)

    def test_warning_continues_execution(self):
        """测试警告不阻断执行"""
        text = "input[3:0]  bad_sig                                        ，  //efuse_default_value: 0xFF"
        
        # 应该正常返回解析结果，而不是抛出异常
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "bad_sig")

    def test_large_width_signal(self):
        """测试大位宽信号边界"""
        # 32-bit max = 0xFFFFFFFF
        text = "input[31:0]  large_sig                                        ，  //efuse_default_value: 0x1FFFFFFFF"
        self.parser.parse_signals(text)
        
        output = self.held_output.getvalue()
        self.assertIn("VALUE VALIDATION WARNINGS", output)
        self.assertIn("32-bit", output)
        self.assertIn("max 0xFFFFFFFF", output)


class TestSignalValueProperties(unittest.TestCase):
    """测试信号值的属性"""

    def test_value_storage(self):
        """测试值正确存储"""
        signal = Signal(name="test", width=4, value=0x5)
        self.assertEqual(signal.value, 0x5)

    def test_default_value_zero(self):
        """测试默认值 0"""
        signal = Signal(name="test", width=8)
        self.assertEqual(signal.value, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
