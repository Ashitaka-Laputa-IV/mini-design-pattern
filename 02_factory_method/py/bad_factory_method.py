"""
================================================================================
 Lesson 2: Factory Method — 工厂方法模式 [创建型]
================================================================================
 📖 本课采用"反模式驱动"方式：
    先展示坏的代码，分析问题，再引入设计模式。

 🔑 面试频率：★★★★☆
================================================================================
"""

"""
===============================================================================
 🎬 场景：你和同事在做一个"日志系统"

 需求：
   系统需要支持不同格式的日志输出：
     1. 控制台日志 (ConsoleLogger) — 直接打印到终端
     2. 文件日志 (FileLogger) — 写入到文件
     3. 网络日志 (NetworkLogger) — 通过 HTTP 发送到远程服务器

 你的同事写了一个 LoggerFactory 类，用 if-else 判断字符串类型来创建
 不同的 Logger。一开始只有 2 种类型，后来增加到 3 种、4 种...

 😕 问题来了：
   每次新增一种日志类型，都要去改 LoggerFactory 的 create_logger() 方法。
   这违反了"开闭原则"(Open-Closed Principle)：
     "对扩展开放，对修改封闭"
     — 增加新功能时不应该修改已有的代码。

 请你先停在这里想一想：
    1. 如果新增"数据库日志""消息队列日志"，你会改哪几个文件？
    2. 怎么才能让"加新类型"和"已有代码"解耦？
    3. 有没有一种方式，让新增类型时不需要改工厂代码？

 🧠 思考 10 秒钟...
   .
   .
   .
   .
   .
   .
   .
   .
   想好了吗？往下翻看反例代码 👇
===============================================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import time


# ============================================================================
# 反模式：用 if-else 创建对象
# ============================================================================
# 先定义产品类（各种 Logger）

class ConsoleLogger:
    """控制台日志"""

    def log(self, message: str):
        print(f"[控制台 {datetime.now()}] {message}")


class FileLogger:
    """文件日志"""

    def __init__(self):
        # 模拟打开文件
        self._file = "app.log"

    def log(self, message: str):
        print(f"[文件 {self._file} {datetime.now()}] {message}")
        # 实际会写入文件，这里只是模拟


class NetworkLogger:
    """网络日志"""

    def __init__(self):
        self._endpoint = "https://logs.example.com/api"

    def log(self, message: str):
        print(f"[网络 {self._endpoint} {datetime.now()}] {message}")
        # 实际会发送 HTTP 请求，这里只是模拟


# 然后是这个"罪魁祸首"——不断膨胀的工厂类

class LoggerFactory:
    """
    ❌ 坏味道：对象创建工厂，用 if-else 判断类型

    问题分析：
      1. 每增加一种日志类型，就要在这里加一个 elif
      2. 这违反了"开闭原则"——对扩展开放，对修改封闭
      3. 随着类型增多，这个类会越来越庞大
      4. 所有的创建逻辑耦合在一起，测试困难
      5. 如果创建逻辑复杂（比如 FileLogger 需要传入路径），
         这个方法的参数也会越来越复杂
    """

    def create_logger(self, logger_type: str):
        """
        根据类型创建对应的 Logger

        Args:
            logger_type: "console", "file", "network" 之一

        Returns:
            对应的 Logger 实例

        Raises:
            ValueError: 不支持的日志类型
        """
        print(f"  [工厂] 正在创建 {logger_type} 日志...")

        # ⚠ 这里就是问题所在：
        # 每次新增类型都要在这个方法里加一个 elif
        if logger_type == "console":
            return ConsoleLogger()
        elif logger_type == "file":
            return FileLogger()
        elif logger_type == "network":
            return NetworkLogger()
        # 如果哪天要加 DatabaseLogger:
        # elif logger_type == "database":
        #     return DatabaseLogger()  # 又改了这个方法！
        else:
            raise ValueError(f"不支持的日志类型: {logger_type}")


# ============================================================================
# 测试反模式
# ============================================================================

def test_bad_factory():
    print("=" * 60)
    print("❌ 反模式：if-else 工厂方法")
    print("=" * 60)

    factory = LoggerFactory()

    # 使用工厂创建不同 Logger
    loggers = ["console", "file", "network"]

    for logger_type in loggers:
        logger = factory.create_logger(logger_type)
        logger.log(f"这是一条 {logger_type} 日志")

    print()
    print("⚠  现在想加一个 DatabaseLogger...")
    print("   必须修改 LoggerFactory.create_logger() 方法！")
    print("   这就是"开闭原则"被违反的典型案例。")


# ============================================================================
# 面试追问点：这个反模式叫什么名字？
# ============================================================================
"""
Q: 这个用 if-else 创建对象的模式有名字吗？
A: 有的。它被称为"简单工厂"(Simple Factory) 或 "静态工厂"(Static Factory)。
   但它不是 GoF 23 种设计模式之一——因为它只是一个编程习惯（idiom）。

   简单工厂 vs 工厂方法的区别：
   - 简单工厂：用一个类集中管理所有对象的创建（if-else 分支）
   - 工厂方法：把创建逻辑延迟到子类（每个子类只创建一种产品）

   简单工厂的问题就是上面展示的：违反开闭原则。
"""


if __name__ == "__main__":
    test_bad_factory()
