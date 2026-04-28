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


if __name__ == "__main__":
    unittest.main(verbosity=2)
