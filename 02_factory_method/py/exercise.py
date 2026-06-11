"""
================================================================================
 Lesson 02: Factory Method — 工厂方法模式练习
================================================================================
 本文件包含 3 道练习题，难度递进：
    练习1：简单工厂 — NotificationFactory
    练习2：工厂方法模式重构 — NotificationCreator
    练习3：拓展题 — FileParserFactory

 说明：
   - 所有 TODO 处需要你补全代码
   - 完成练习后，运行 test_exercise.py 验证正确性
================================================================================
"""

from abc import ABC, abstractmethod


# ============================================================================
# 练习1：简单工厂 (Simple Factory)
# ============================================================================
# 实现通知系统，要求：
#   1. EmailNotification / SMSNotification / PushNotification 都有 send(message) 方法
#   2. NotificationFactory.create_notification(type_str) 根据类型字符串创建对应实例
#   3. 支持类型："email", "sms", "push"
# ============================================================================

class EmailNotification:
    """邮件通知"""

    def send(self, message: str) -> str:
        # TODO: 返回 "[邮件] xxx" 格式字符串
        raise NotImplementedError


class SMSNotification:
    """短信通知"""

    def send(self, message: str) -> str:
        # TODO: 返回 "[短信] xxx" 格式字符串
        raise NotImplementedError


class PushNotification:
    """推送通知"""

    def send(self, message: str) -> str:
        # TODO: 返回 "[推送] xxx" 格式字符串
        raise NotImplementedError


class NotificationFactory:
    """通知工厂 — 简单工厂模式"""

    @staticmethod
    def create_notification(notification_type: str):
        """根据类型创建对应的通知对象

        Args:
            notification_type: "email", "sms", "push" 之一

        Returns:
            对应的通知实例

        Raises:
            ValueError: 不支持的 notification_type
        """
        # TODO: 用 if-elif-else 判断类型并创建对应对象
        raise NotImplementedError


# ============================================================================
# 练习2：工厂方法模式 (Factory Method)
# ============================================================================
# 用工厂方法模式重构通知系统，要求：
#   1. NotificationCreator 抽象类，定义 factory_method() 和 send_notification()
#   2. EmailCreator / SMSCreator / PushCreator 实现工厂方法
# ============================================================================

class Notification(ABC):
    """通知抽象接口"""

    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotificationV2(Notification):
    """邮件通知"""

    def send(self, message: str) -> str:
        # TODO: 实现发送逻辑
        raise NotImplementedError


class SMSNotificationV2(Notification):
    """短信通知"""

    def send(self, message: str) -> str:
        # TODO: 实现发送逻辑
        raise NotImplementedError


class PushNotificationV2(Notification):
    """推送通知"""

    def send(self, message: str) -> str:
        # TODO: 实现发送逻辑
        raise NotImplementedError


class NotificationCreator(ABC):
    """抽象创建者 — 定义工厂方法"""

    @abstractmethod
    def create_notification(self) -> Notification:
        """工厂方法：子类实现此方法创建具体的 Notification"""
        pass

    def send_notification(self, message: str) -> str:
        """使用工厂方法的业务方法

        Args:
            message: 要发送的消息

        Returns:
            发送结果字符串
        """
        # TODO: 调用 create_notification() 创建通知对象，然后调用 send()
        raise NotImplementedError


class EmailCreator(NotificationCreator):
    """邮件通知创建者"""

    def create_notification(self) -> Notification:
        # TODO: 返回 EmailNotificationV2 实例
        raise NotImplementedError


class SMSCreator(NotificationCreator):
    """短信通知创建者"""

    def create_notification(self) -> Notification:
        # TODO: 返回 SMSNotificationV2 实例
        raise NotImplementedError


class PushCreator(NotificationCreator):
    """推送通知创建者"""

    def create_notification(self) -> Notification:
        # TODO: 返回 PushNotificationV2 实例
        raise NotImplementedError


# ============================================================================
# 练习3：拓展题 — FileParserFactory
# ============================================================================
# 实现文件解析器工厂，要求：
#   1. CsvParser / JsonParser / XmlParser 都有 parse(filepath) 方法
#   2. FileParserFactory.create_parser(filepath) 根据扩展名创建对应解析器
#   3. 支持扩展名：.csv, .json, .xml
# ============================================================================

class CsvParser:
    """CSV 文件解析器"""

    def parse(self, filepath: str) -> list:
        # TODO: 返回模拟解析结果，如 [{"name": "Alice", "age": "30"}, ...]
        raise NotImplementedError


class JsonParser:
    """JSON 文件解析器"""

    def parse(self, filepath: str) -> dict:
        # TODO: 返回模拟解析结果，如 {"name": "Alice", "age": 30}
        raise NotImplementedError


class XmlParser:
    """XML 文件解析器"""

    def parse(self, filepath: str) -> dict:
        # TODO: 返回模拟解析结果，如 {"name": "Alice", "age": "30"}
        raise NotImplementedError


class FileParserFactory:
    """文件解析器工厂 — 根据文件扩展名创建对应解析器"""

    @staticmethod
    def create_parser(filepath: str):
        """根据文件路径的扩展名创建对应的解析器

        Args:
            filepath: 文件路径（如 "data.csv", "config.json"）

        Returns:
            对应的解析器实例

        Raises:
            ValueError: 不支持的扩展名
        """
        # TODO: 解析文件扩展名并创建对应的解析器
        # 提示：可以用 filepath.endswith() 或 os.path.splitext()
        raise NotImplementedError
