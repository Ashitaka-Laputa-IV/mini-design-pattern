"""
================================================================================
练习题 10: Template Method — 模板方法模式
================================================================================
📐 模板方法模式(Template Method)定义一个操作中的算法骨架，
   而将一些步骤延迟到子类中实现。模板方法使得子类可以不改变
   一个算法的结构即可重定义该算法的某些特定步骤。

💡 本练习包含 3 道题：
   第1题（基础）: 实现数据导出器
   第2题（综合）: 实现游戏关卡模板
   第3题（拓展）: 实现带钩子的数据挖掘模板
================================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


# ============================================================================
# 第1题（基础）: 数据导出器
# ============================================================================
#
# 实现一个数据导出器。DataExporter 定义模板方法 export()，
# 固定步骤：connect() / query_data() / format_output() / close()
#
# 要求：
#   1. DataExporter 是抽象基类，export() 是模板方法（不可重写）
#   2. connect() 和 close() 在基类中实现（公共步骤）
#   3. query_data() 和 format_output() 是抽象方法（子类实现）
#   4. 实现 CSVExporter 和 JSONExporter 子类

class DataExporter(ABC):
    """抽象基类：数据导出器"""

    def export(self):
        """
        🎯 模板方法：定义数据导出的算法骨架
        步骤顺序：连接 → 查询 → 格式化 → 关闭
        """
        # TODO: 按顺序调用 connect(), query_data(), format_output(), close()
        pass

    def connect(self):
        """公共步骤：连接数据库"""
        print("  连接数据库...")

    def close(self):
        """公共步骤：关闭连接"""
        print("  关闭连接...")

    @abstractmethod
    def query_data(self) -> List[Dict[str, Any]]:
        """抽象方法：查询数据"""
        pass

    @abstractmethod
    def format_output(self, data: List[Dict[str, Any]]) -> str:
        """抽象方法：格式化输出"""
        pass


class CSVExporter(DataExporter):
    """CSV 导出器"""

    def query_data(self) -> List[Dict[str, Any]]:
        return [
            {"name": "张三", "age": 25, "city": "北京"},
            {"name": "李四", "age": 30, "city": "上海"},
        ]

    def format_output(self, data: List[Dict[str, Any]]) -> str:
        """格式化为 CSV 字符串"""
        if not data:
            return ""
        # TODO: 将数据格式化为 CSV 字符串
        # 第一行为表头，后续每行为一条记录
        pass


class JSONExporter(DataExporter):
    """JSON 导出器"""

    def query_data(self) -> List[Dict[str, Any]]:
        return [
            {"name": "张三", "age": 25, "city": "北京"},
            {"name": "李四", "age": 30, "city": "上海"},
        ]

    def format_output(self, data: List[Dict[str, Any]]) -> str:
        """格式化为 JSON 字符串"""
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)


# ============================================================================
# 第2题（综合）: 游戏关卡模板
# ============================================================================
#
# 实现一个游戏关卡模板。GameLevel 定义 play() 流程：
#   load_assets() / init_enemies() / start_playing() / end_level()
#
# 要求：
#   1. GameLevel 是抽象基类，play() 是模板方法
#   2. load_assets() 是公共步骤，在基类实现
#   3. init_enemies() 和 start_playing() 是抽象方法
#   4. end_level() 是公共步骤，打印通关信息
#   5. 实现 ForestLevel（森林关卡）和 CastleLevel（城堡关卡）

class GameLevel(ABC):
    """抽象基类：游戏关卡"""

    def play(self):
        """
        🎯 模板方法：定义关卡进行的流程
        步骤顺序：加载资源 → 初始化敌人 → 开始游戏 → 结束关卡
        """
        # TODO: 按顺序调用各个步骤

    def load_assets(self):
        """公共步骤：加载关卡资源"""
        print("  加载关卡资源...")

    @abstractmethod
    def init_enemies(self):
        """抽象方法：初始化敌人"""
        pass

    @abstractmethod
    def start_playing(self):
        """抽象方法：开始游戏"""
        pass

    def end_level(self):
        """公共步骤：结束关卡"""
        print("  恭喜通关！")


class ForestLevel(GameLevel):
    """森林关卡"""

    def init_enemies(self):
        print("  初始化森林敌人：野狼、蜘蛛、毒蛇")

    def start_playing(self):
        print("  在森林中探险，击败所有敌人！")


class CastleLevel(GameLevel):
    """城堡关卡"""

    def init_enemies(self):
        print("  初始化城堡敌人：骷髅兵、石像鬼、黑暗骑士")

    def start_playing(self):
        print("  攻入城堡，击败最终 Boss！")


# ============================================================================
# 第3题（拓展）: 带钩子的数据挖掘模板
# ============================================================================
#
# 实现带钩子的数据挖掘模板。DataMining 定义模板方法 mine(path)，
# 步骤：open_file() / extract() / parse() / analyze() / close()
#
# 要求：
#   1. DataMining 定义模板方法 mine(path)
#   2. open_file(path) 和 close() 是公共步骤
#   3. extract() 和 parse() 是抽象方法
#   4. analyze() 是钩子方法（Hook），默认执行，子类可重写
#   5. should_analyze() 是钩子，默认返回 True，子类可重写控制流程
#   6. 实现 CSVDataMining（需要 analyze）和 PDFDataMining（不需要 analyze）

class DataMining(ABC):
    """抽象基类：数据挖掘器"""

    def mine(self, path: str):
        """
        🎯 模板方法：定义数据挖掘流程
        步骤：打开文件 → 提取数据 → 解析数据 → 分析数据 → 关闭文件
        """
        # TODO: 按顺序调用各步骤
        # 注意：analyze() 只在 should_analyze() 返回 True 时才执行
        pass

    def open_file(self, path: str):
        """公共步骤：打开文件"""
        print(f"  打开文件: {path}")

    def close(self):
        """公共步骤：关闭文件"""
        print("  关闭文件")

    @abstractmethod
    def extract(self) -> str:
        """抽象方法：提取原始数据"""
        pass

    @abstractmethod
    def parse(self) -> List[Dict[str, Any]]:
        """抽象方法：解析数据"""
        pass

    def analyze(self, data: List[Dict[str, Any]]):
        """
        🪝 钩子方法：分析数据
        默认实现执行简单分析，子类可重写
        """
        print(f"  分析数据: 共 {len(data)} 条记录")
        if data:
            print(f"  字段: {list(data[0].keys())}")

    def should_analyze(self) -> bool:
        """
        🪝 钩子方法：是否执行分析步骤
        默认返回 True，子类可重写返回 False 跳过分析
        """
        return True


class CSVDataMining(DataMining):
    """CSV 数据挖掘器"""

    def __init__(self):
        self._raw_data = ""

    def extract(self) -> str:
        self._raw_data = "name,age\n张三,25\n李四,30"
        return self._raw_data

    def parse(self) -> List[Dict[str, Any]]:
        """解析 CSV 数据"""
        lines = self._raw_data.strip().split("\n")
        if len(lines) < 2:
            return []
        headers = lines[0].split(",")
        result = []
        for line in lines[1:]:
            values = line.split(",")
            result.append(dict(zip(headers, values)))
        return result


class PDFDataMining(DataMining):
    """PDF 数据挖掘器——不需要 analyze 步骤"""

    def __init__(self):
        self._raw_data = ""

    def extract(self) -> str:
        self._raw_data = "PDF 原始文本内容"
        return self._raw_data

    def parse(self) -> List[Dict[str, Any]]:
        """解析 PDF 数据"""
        return [{"content": self._raw_data}]

    def should_analyze(self) -> bool:
        """
        重写钩子：PDF 不需要分析步骤
        """
        # TODO: 返回 False 跳过 analyze 步骤
        pass
