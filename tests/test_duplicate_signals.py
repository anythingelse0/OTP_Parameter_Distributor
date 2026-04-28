#!/usr/bin/env python3
"""
测试重复信号名处理功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dynamic_signal_parser import DynamicSignalParser, Signal


class TestDuplicateSignalNames(unittest.TestCase):
    """测试重复信号名自动添加后缀功能"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_no_duplicate_names(self):
        """测试无重复信号时保持原名称"""
        text = """input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_b ，  //efuse_default_value: 0
input[7:0] signal_c ，  //efuse_default_value: 0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[1].name, 'signal_b')
        self.assertEqual(signals[2].name, 'signal_c')

    def test_single_duplicate_name(self):
        """测试单个重复信号名添加 _1 后缀"""
        text = """input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_b ，  //efuse_default_value: 0
input[7:0] signal_a ，  //efuse_default_value: 0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].name, 'signal_a')      # 首次出现，无后缀
        self.assertEqual(signals[1].name, 'signal_b')
        self.assertEqual(signals[2].name, 'signal_a_1')  # 重复，加后缀

    def test_multiple_duplicates_same_name(self):
        """测试同一信号名多次重复"""
        text = """input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_a ，  //efuse_default_value: 0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[1].name, 'signal_a_1')
        self.assertEqual(signals[2].name, 'signal_a_2')

    def test_multiple_duplicate_names_mixed(self):
        """测试多个不同的重复信号名混合"""
        text = """input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_b ，  //efuse_default_value: 0
input[7:0] signal_a ，  //efuse_default_value: 0
input[7:0] signal_b ，  //efuse_default_value: 0
input[7:0] signal_a ，  //efuse_default_value: 0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 5)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[1].name, 'signal_b')
        self.assertEqual(signals[2].name, 'signal_a_1')
        self.assertEqual(signals[3].name, 'signal_b_1')
        self.assertEqual(signals[4].name, 'signal_a_2')

    def test_sds_sections_duplicate_names(self):
        """测试类似 sds1/sds0 的重复端口场景（使用中文逗号）"""
        text = """// sds1 section
input[8:0]       efuse_val_csr_10g_sds_pll_band_w          ，    //efuse_default_value:  0x0
input            efuse_val_csr_en_pcie_lp                  ，    //efuse_default_value:  0x0

// sds0 section
input[8:0]       efuse_val_csr_10g_sds_pll_band_w          ，    //efuse_default_value:  0x0
input            efuse_val_csr_en_pcie_lp                  ，    //efuse_default_value:  0x0"""

        signals = self.parser.parse_signals(text)

        self.assertEqual(len(signals), 4)
        # sds1 section - 首次出现，无后缀
        self.assertEqual(signals[0].name, 'efuse_val_csr_10g_sds_pll_band_w')
        self.assertEqual(signals[0].width, 9)
        self.assertEqual(signals[1].name, 'efuse_val_csr_en_pcie_lp')
        self.assertEqual(signals[1].width, 1)
        # sds0 section - 重复，加 _1 后缀
        self.assertEqual(signals[2].name, 'efuse_val_csr_10g_sds_pll_band_w_1')
        self.assertEqual(signals[2].width, 9)
        self.assertEqual(signals[3].name, 'efuse_val_csr_en_pcie_lp_1')
        self.assertEqual(signals[3].width, 1)

    def test_duplicate_with_different_values(self):
        """测试重复信号名但不同 efuse_default_value"""
        text = """input[7:0] signal_a ，  //efuse_default_value: 0x0
input[7:0] signal_a ，  //efuse_default_value: 0xFF"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[0].value, 0)
        self.assertEqual(signals[1].name, 'signal_a_1')
        self.assertEqual(signals[1].value, 0xFF)

    def test_counter_reset_on_new_parse(self):
        """测试每次 parse_signals 调用时计数器重置"""
        text1 = "input[7:0] signal_a ，  //efuse_default_value: 0"
        text2 = "input[7:0] signal_a ，  //efuse_default_value: 0"
        
        # 第一次解析
        signals1 = self.parser.parse_signals(text1)
        self.assertEqual(signals1[0].name, 'signal_a')
        
        # 第二次解析（新实例或重置后）
        parser2 = DynamicSignalParser()
        signals2 = parser2.parse_signals(text2)
        self.assertEqual(signals2[0].name, 'signal_a')  # 应该重新计数，无后缀

    def test_csv_format_duplicate_names(self):
        """测试 CSV 格式重复信号名处理"""
        text = """,signal_a,0x0
,signal_b,0x0
,signal_a,0x0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[1].name, 'signal_b')
        self.assertEqual(signals[2].name, 'signal_a_1')

    def test_hdl_format_duplicate_names(self):
        """测试 HDL 格式重复信号名处理"""
        text = """logic [7:0] signal_a 0x0
logic [7:0] signal_b 0x0
logic [7:0] signal_a 0x0"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[1].name, 'signal_b')
        self.assertEqual(signals[2].name, 'signal_a_1')

    def test_unique_name_preserves_width_and_value(self):
        """测试重命名后保留原始信号的位宽和值"""
        text = """input[15:0] signal_a ，  //efuse_default_value: 0xABCD
input[7:0] signal_a ，  //efuse_default_value: 0x12"""
        
        signals = self.parser.parse_signals(text)
        
        self.assertEqual(signals[0].name, 'signal_a')
        self.assertEqual(signals[0].width, 16)
        self.assertEqual(signals[0].value, 0xABCD)
        
        self.assertEqual(signals[1].name, 'signal_a_1')
        self.assertEqual(signals[1].width, 8)
        self.assertEqual(signals[1].value, 0x12)


class TestUniqueSignalNameMethod(unittest.TestCase):
    """直接测试 _get_unique_signal_name 方法"""

    def setUp(self):
        self.parser = DynamicSignalParser()

    def test_first_occurrence_no_suffix(self):
        """测试首次出现无后缀"""
        name = self.parser._get_unique_signal_name('test_signal')
        self.assertEqual(name, 'test_signal')

    def test_second_occurrence_suffix_1(self):
        """测试第二次出现后缀为 _1"""
        self.parser._get_unique_signal_name('test_signal')  # 首次
        name = self.parser._get_unique_signal_name('test_signal')  # 第二次
        self.assertEqual(name, 'test_signal_1')

    def test_third_occurrence_suffix_2(self):
        """测试第三次出现后缀为 _2"""
        self.parser._get_unique_signal_name('test_signal')
        self.parser._get_unique_signal_name('test_signal')
        name = self.parser._get_unique_signal_name('test_signal')
        self.assertEqual(name, 'test_signal_2')

    def test_different_signals_independent_counters(self):
        """测试不同信号名独立计数"""
        self.assertEqual(self.parser._get_unique_signal_name('sig_a'), 'sig_a')
        self.assertEqual(self.parser._get_unique_signal_name('sig_b'), 'sig_b')
        self.assertEqual(self.parser._get_unique_signal_name('sig_a'), 'sig_a_1')
        self.assertEqual(self.parser._get_unique_signal_name('sig_b'), 'sig_b_1')
        self.assertEqual(self.parser._get_unique_signal_name('sig_a'), 'sig_a_2')


if __name__ == '__main__':
    unittest.main()
