"""
================================================================================
测试 10 Template Method 练习题
================================================================================
"""

import pytest
from exercise import (
    DataExporter, CSVExporter, JSONExporter,
    GameLevel, ForestLevel, CastleLevel,
    DataMining, CSVDataMining, PDFDataMining
)


# ============================================================================
# 测试第1题：数据导出器
# ============================================================================

class TestDataExporter:
    """测试数据导出器"""

    def test_csv_exporter_format(self):
        """测试 CSV 导出器的格式输出"""
        exporter = CSVExporter()
        result = exporter.export()

        assert result is not None
        assert isinstance(result, str)
        assert "name" in result
        assert "张三" in result

    def test_json_exporter_format(self):
        """测试 JSON 导出器的格式输出"""
        exporter = JSONExporter()
        result = exporter.export()

        assert result is not None
        assert isinstance(result, str)
        assert "张三" in result
        # 验证是 JSON 格式
        import json
        data = json.loads(result)
        assert len(data) == 2
        assert data[0]["name"] == "张三"

    def test_export_follows_template_steps(self):
        """测试导出流程是否完整执行"""
        exporter = CSVExporter()
        result = exporter.export()
        # 验证结果包含正确内容
        assert "张三" in result
        assert "李四" in result


# ============================================================================
# 测试第2题：游戏关卡模板
# ============================================================================

class TestGameLevel:
    """测试游戏关卡模板"""

    def test_forest_level_play(self):
        """测试森林关卡 play 流程"""
        level = ForestLevel()
        result = level.play()
        # 验证通关（end_level 被调用）
        assert result == "恭喜通关！"

    def test_castle_level_play(self):
        """测试城堡关卡 play 流程"""
        level = CastleLevel()
        result = level.play()
        assert result == "恭喜通关！"

    def test_forest_level_enemies(self):
        """测试森林关卡的敌人"""
        level = ForestLevel()
        enemies = level.init_enemies()
        assert "野狼" in enemies
        assert "蜘蛛" in enemies

    def test_castle_level_enemies(self):
        """测试城堡关卡的敌人"""
        level = CastleLevel()
        enemies = level.init_enemies()
        assert "骷髅兵" in enemies
        assert "黑暗骑士" in enemies


# ============================================================================
# 测试第3题：带钩子的数据挖掘模板
# ============================================================================

class TestDataMining:
    """测试数据挖掘模板"""

    def test_csv_mining_includes_analysis(self):
        """测试 CSV 挖掘包含分析步骤"""
        miner = CSVDataMining()
        result = miner.mine("test.csv")

        assert result is not None
        assert "分析数据" in result
        assert "name" in result

    def test_pdf_mining_skips_analysis(self):
        """测试 PDF 挖掘跳过分析步骤（钩子控制）"""
        miner = PDFDataMining()
        result = miner.mine("test.pdf")

        assert result is not None
        assert "分析数据" not in result

    def test_csv_mining_parsed_data(self):
        """测试 CSV 挖掘的解析结果"""
        miner = CSVDataMining()
        data = miner.parse()
        assert len(data) == 2
        assert data[0]["name"] == "张三"
        assert data[1]["age"] == "30"

    def test_should_analyze_hook(self):
        """测试钩子方法 should_analyze"""
        csv_miner = CSVDataMining()
        pdf_miner = PDFDataMining()

        assert csv_miner.should_analyze() is True
        assert pdf_miner.should_analyze() is False

    def test_open_close_called(self):
        """测试 open_file 和 close 被调用"""
        miner = CSVDataMining()
        result = miner.mine("data.csv")

        assert "打开文件" in result
        assert "关闭文件" in result
