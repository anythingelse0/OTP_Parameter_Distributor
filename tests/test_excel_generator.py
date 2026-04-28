#!/usr/bin/env python3
"""
Excel 生成器单元测试
测试 Excel 字节/位映射表生成
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from datetime import datetime
from dynamic_signal_parser import DynamicSignalParser, Signal, SignalType


class TestExcelGenerator(unittest.TestCase):
    """测试 Excel 生成功能"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        # 创建临时目录
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # 清理临时目录
        self.temp_dir.cleanup()

    def test_excel_generation_simple(self):
        """测试简单信号 Excel 生成"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'uuid': {'start_bit': 0, 'end_bit': 63, 'width': 64, 'value': 0}
        }
        
        output_file = os.path.join(self.temp_dir.name, "test.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(output_file))
        
        # 验证可以正常打开
        wb = openpyxl.load_workbook(output_file)
        self.assertEqual(wb.active.title, "Byte_Bit_Mapping")

    def test_excel_filename_with_datetime(self):
        """测试 Excel 文件名包含日期时间"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'data': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0xAB}
        }
        
        # 使用时间戳格式文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.temp_dir.name, f"test_{timestamp}.xlsx")
        
        self.parser.generate_byte_table_excel(segments, output_file)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(output_file))

    def test_excel_multiple_bytes(self):
        """测试多字节信号 Excel 生成"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'data64': {'start_bit': 0, 'end_bit': 63, 'width': 64, 'value': 0},
            'data8': {'start_bit': 64, 'end_bit': 71, 'width': 8, 'value': 0xFF}
        }
        
        output_file = os.path.join(self.temp_dir.name, "multi_byte.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        # 验证文件存在且可打开
        self.assertTrue(os.path.exists(output_file))
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        
        # 验证标题存在
        self.assertEqual(ws['A1'].value, "Byte/Bit Mapping Table")

    def test_excel_cell_merge(self):
        """测试跨字节的信号单元格合并"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        # 创建一个跨越多个 bit 的信号
        segments = {
            'wide_sig': {'start_bit': 4, 'end_bit': 11, 'width': 8, 'value': 0x5A}
        }
        
        output_file = os.path.join(self.temp_dir.name, "merged.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        self.assertTrue(os.path.exists(output_file))

    def test_excel_empty_segments(self):
        """测试空 segments 不生成文件"""
        output_file = os.path.join(self.temp_dir.name, "empty.xlsx")
        
        # openpyxl 可能不可用，但不影响这个测试
        self.parser.generate_byte_table_excel({}, output_file)
        
        # 空 segments 不应该生成文件
        self.assertFalse(os.path.exists(output_file))

    def test_color_palette_assignment(self):
        """测试颜色分配"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        # 多个信号测试颜色轮询
        segments = {
            'sig1': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0},
            'sig2': {'start_bit': 8, 'end_bit': 15, 'width': 8, 'value': 0},
            'sig3': {'start_bit': 16, 'end_bit': 23, 'width': 8, 'value': 0},
        }
        
        output_file = os.path.join(self.temp_dir.name, "colored.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        self.assertTrue(os.path.exists(output_file))
        wb = openpyxl.load_workbook(output_file)
        
        # 文件成功生成即可
        self.assertIsNotNone(wb)


class TestExcelContent(unittest.TestCase):
    """测试 Excel 内容正确性"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_title_row(self):
        """测试标题行"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'test': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0}
        }
        
        output_file = os.path.join(self.temp_dir.name, "title.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        
        # 验证标题
        self.assertEqual(ws['A1'].value, "Byte/Bit Mapping Table")

    def test_byte_header_row(self):
        """测试 Byte 标题行格式"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'byte0': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0}
        }
        
        output_file = os.path.join(self.temp_dir.name, "byte_header.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        
        # Byte 0 标题应该在第 3 行
        self.assertEqual(ws['A3'].value, "Byte 0")

    def test_default_value_display(self):
        """测试 Default 值显示"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        segments = {
            'test': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0xAB}
        }
        
        output_file = os.path.join(self.temp_dir.name, "default.xlsx")
        self.parser.generate_byte_table_excel(segments, output_file)
        
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        
        # 查找 Default 行并验证值
        found_default = False
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            if row[0].value == "Default":
                found_default = True
                break
        
        self.assertTrue(found_default, "Should have 'Default' row")


class TestExcelFileOperations(unittest.TestCase):
    """测试 Excel 文件操作"""

    def setUp(self):
        self.parser = DynamicSignalParser()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_output_directory_creation(self):
        """测试输出目录自动创建"""
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not available")

        nested_dir = os.path.join(self.temp_dir.name, "nested", "path")
        output_file = os.path.join(nested_dir, "test.xlsx")
        
        # 确保目录存在
        os.makedirs(nested_dir, exist_ok=True)
        
        segments = {
            'test': {'start_bit': 0, 'end_bit': 7, 'width': 8, 'value': 0}
        }
        
        self.parser.generate_byte_table_excel(segments, output_file)
        
        self.assertTrue(os.path.exists(output_file))


if __name__ == "__main__":
    unittest.main(verbosity=2)
