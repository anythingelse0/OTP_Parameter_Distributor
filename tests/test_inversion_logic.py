#!/usr/bin/env python3
"""
取反逻辑单元测试
测试三种取反类型：none、full、per-bit
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import DynamicSignalParser, Signal, SignalType


class TestInversionLogic(unittest.TestCase):
    """测试 _generate_rhs 取反逻辑"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        # 添加一个测试信号，方便调用 _generate_rhs
        self.parser.signals = [Signal(name="test", width=64)]

    def test_no_inversion_value_zero(self):
        """测试 value=0 时不取反 (none)"""
        # start=0, end=31, width=32, value=0
        result = self.parser._generate_rhs(0, 31, 32, 0, "chip_param")
        self.assertEqual(result, "chip_param[31:0]")
        
        # 1-bit 情况
        result_1bit = self.parser._generate_rhs(5, 5, 1, 0, "chip_param")
        self.assertEqual(result_1bit, "chip_param[5]")

    def test_full_inversion_1bit(self):
        """测试 1-bit 且 value!=0 时整体取反 (full)"""
        # width=1, value=1 (任何非零值都应该整体取反)
        result = self.parser._generate_rhs(10, 10, 1, 1, "chip_param")
        self.assertEqual(result, "~chip_param[10]")
        
        # value=0x7 也应该整体取反（高位会被忽略）
        result_large = self.parser._generate_rhs(10, 10, 1, 0x7, "chip_param")
        self.assertEqual(result_large, "~chip_param[10]")

    def test_per_bit_inversion_4bit(self):
        """测试 4-bit 逐 bit 取反 (per-bit) - value=0x5 (0101)"""
        # start=0, end=3, width=4, value=0x5
        # bit[3]=0 -> chip_param[3]
        # bit[2]=1 -> ~chip_param[2]
        # bit[1]=0 -> chip_param[1]
        # bit[0]=1 -> ~chip_param[0]
        result = self.parser._generate_rhs(0, 3, 4, 0x5, "chip_param")
        self.assertEqual(result, "{chip_param[3], ~chip_param[2], chip_param[1], ~chip_param[0]}")

    def test_per_bit_inversion_4bit_value_A(self):
        """测试 4-bit 逐 bit 取反 - value=0xA (1010)"""
        # bit[3]=1 -> ~chip_param[3]
        # bit[2]=0 -> chip_param[2]
        # bit[1]=1 -> ~chip_param[1]
        # bit[0]=0 -> chip_param[0]
        result = self.parser._generate_rhs(4, 7, 4, 0xA, "chip_param")
        self.assertEqual(result, "{~chip_param[7], chip_param[6], ~chip_param[5], chip_param[4]}")

    def test_per_bit_inversion_8bit(self):
        """测试 8-bit 逐 bit 取反 - value=0x81 (10000001)"""
        # 只有最高位和最低位为 1
        result = self.parser._generate_rhs(0, 7, 8, 0x81, "chip_param")
        # 从高位到低位: bit[7]=1, bit[6]=0, bit[5]=0, bit[4]=0, bit[3]=0, bit[2]=0, bit[1]=0, bit[0]=1
        expected = "{~chip_param[7], chip_param[6], chip_param[5], chip_param[4], " \
                   "chip_param[3], chip_param[2], chip_param[1], ~chip_param[0]}"
        self.assertEqual(result, expected)

    def test_per_bit_inversion_all_zeros(self):
        """测试 value=0 的多位信号不取反"""
        result = self.parser._generate_rhs(0, 15, 16, 0, "chip_param")
        self.assertEqual(result, "chip_param[15:0]")

    def test_per_bit_inversion_all_ones(self):
        """测试 8-bit 全取反 - value=0xFF"""
        result = self.parser._generate_rhs(8, 15, 8, 0xFF, "chip_param")
        # 所有位都取反
        expected = "{~chip_param[15], ~chip_param[14], ~chip_param[13], ~chip_param[12], " \
                   "~chip_param[11], ~chip_param[10], ~chip_param[9], ~chip_param[8]}"
        self.assertEqual(result, expected)

    def test_per_bit_inversion_chip_id_example(self):
        """测试 chip_id 示例 - width=16, value=0x9008"""
        # 0x9008 = 1001_0000_0000_1000
        # bit[15]=1, bit[14]=0, bit[13]=0, bit[12]=1
        # bit[11:4]=0
        # bit[3]=1, bit[2:0]=0
        result = self.parser._generate_rhs(64, 79, 16, 0x9008, "chip_param")
        # 验证结果包含取反逻辑
        self.assertIn("~chip_param[79]", result)  # bit[15]=1
        self.assertIn("chip_param[78]", result)   # bit[14]=0
        self.assertIn("chip_param[77]", result)   # bit[13]=0
        self.assertIn("~chip_param[76]", result)  # bit[12]=1
        self.assertIn("~chip_param[67]", result)  # bit[3]=1


class TestSegmentMapping(unittest.TestCase):
    """测试信号段映射"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_simple_segmentation(self):
        """测试简单信号分段"""
        text = """input[63:0] uuid                                         ，  //efuse_default_value: 0
input[15:0] chip_id                                      ，  //efuse_default_value:0x9008"""
        
        signals = self.parser.parse_signals(text)
        
        # 64-bit uuid: [63:0]
        self.assertEqual(signals[0].width, 64)
        
        # 16-bit chip_id: [79:64]
        self.assertEqual(signals[1].width, 16)

    def test_1bit_segmentation(self):
        """测试 1-bit 信号分段"""
        text = "input      flag                                         ，  //efuse_default_value: 0x1"
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(signals[0].width, 1)


class TestSVModuleGeneration(unittest.TestCase):
    """测试 SystemVerilog 模块生成"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_module_contains_struct(self):
        """测试生成的模块包含 struct 定义"""
        text = "input[31:0] uuid                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)

        segments = {
            'uuid': {'start_bit': 0, 'end_bit': 31, 'width': 32, 'value': 0}
        }

        # generate_struct_definition 单独生成 struct
        struct_code = self.parser.generate_struct_definition(segments)
        self.assertIn("typedef struct packed", struct_code)
        self.assertIn("logic [31:0]  uuid", struct_code)

        # generate_sv_module 生成 module
        sv_code = self.parser.generate_sv_module(segments, "test_distributor")
        self.assertIn("module test_distributor", sv_code)
        self.assertIn("module test_distributor", sv_code)

    def test_module_contains_combinational_logic(self):
        """测试生成的模块包含 always_comb"""
        text = "input[7:0] data                                         ，  //efuse_default_value: 0"
        self.parser.parse_signals(text)
        
        segments = {
            'data': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0}
        }
        
        sv_code = self.parser.generate_sv_module(segments, "test_dist")
        
        self.assertIn("always_comb begin", sv_code)
        self.assertIn("data = chip_param[7:0]", sv_code)

    def test_module_with_inversion(self):
        """测试生成带取反逻辑的模块"""
        text = "input      flag                                         ，  //efuse_default_value: 0x1"
        self.parser.parse_signals(text)
        
        segments = {
            'flag': {'start_bit': 0, 'end_bit': 0, 'width': 1, 'value': 1}
        }
        
        sv_code = self.parser.generate_sv_module(segments, "test_dist")
        
        self.assertIn("flag = ~chip_param[0]", sv_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
