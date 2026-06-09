"""
================================================================================
 Lesson 02: Factory Method — 单元测试
================================================================================
 运行方式：pytest test_exercise.py -v
================================================================================
"""

import pytest
from exercise import (
    # 练习1
    EmailNotification,
    SMSNotification,
    PushNotification,
    NotificationFactory,
    # 练习2
    Notification,
    EmailNotification_v2,
    SMSNotification_v2,
    PushNotification_v2,
    NotificationCreator,
    EmailCreator,
    SMSCreator,
    PushCreator,
    # 练习3
    CsvParser,
    JsonParser,
    XmlParser,
    FileParserFactory,
)


# ============================================================================
# 测试练习1：简单工厂
# ============================================================================

class TestNotificationFactory:
    """测试简单工厂模式"""

    def test_create_email(self):
        """测试创建邮件通知"""
        notif = NotificationFactory.create_notification("email")
        assert isinstance(notif, EmailNotification)
        assert notif.send("Hello") == "[邮件] Hello"

    def test_create_sms(self):
        """测试创建短信通知"""
        notif = NotificationFactory.create_notification("sms")
        assert isinstance(notif, SMSNotification)
        assert notif.send("验证码1234") == "[短信] 验证码1234"

    def test_create_push(self):
        """测试创建推送通知"""
        notif = NotificationFactory.create_notification("push")
        assert isinstance(notif, PushNotification)
        assert notif.send("你有新消息") == "[推送] 你有新消息"

    def test_invalid_type(self):
        """测试不支持的 type 抛出异常"""
        with pytest.raises(ValueError, match="不支持的通知类型"):
            NotificationFactory.create_notification("wechat")

    def test_empty_type(self):
        """测试空字符串抛出异常"""
        with pytest.raises(ValueError):
            NotificationFactory.create_notification("")

    def test_case_sensitivity(self):
        """测试类型区分大小写"""
        with pytest.raises(ValueError):
            NotificationFactory.create_notification("EMAIL")


# ============================================================================
# 测试练习2：工厂方法模式
# ============================================================================

class TestNotificationCreator:
    """测试工厂方法模式"""

    def test_email_creator(self):
        """测试邮件创建者"""
        creator = EmailCreator()
        notif = creator.create_notification()
        assert isinstance(notif, EmailNotification_v2)
        assert isinstance(notif, Notification)

    def test_sms_creator(self):
        """测试短信创建者"""
        creator = SMSCreator()
        notif = creator.create_notification()
        assert isinstance(notif, SMSNotification_v2)
        assert isinstance(notif, Notification)

    def test_push_creator(self):
        """测试推送创建者"""
        creator = PushCreator()
        notif = creator.create_notification()
        assert isinstance(notif, PushNotification_v2)
        assert isinstance(notif, Notification)

    def test_send_notification(self):
        """测试通过创建者发送通知"""
        creator = EmailCreator()
        result = creator.send_notification("测试消息")
        assert result == "[邮件] 测试消息"

    def test_all_creators_polymorphism(self):
        """测试多态：所有创建者统一接口"""
        creators = [EmailCreator(), SMSCreator(), PushCreator()]
        results = [c.send_notification(f"消息{i}") for i, c in enumerate(creators)]
        assert results == [
            "[邮件] 消息0",
            "[短信] 消息1",
            "[推送] 消息2",
        ]

    def test_abstract_class_cannot_instantiate(self):
        """测试抽象类不能实例化"""
        with pytest.raises(TypeError):
            Notification()  # type: ignore
        with pytest.raises(TypeError):
            NotificationCreator()  # type: ignore

    def test_factory_method_open_closed(self):
        """验证工厂方法模式符合开闭原则（模拟新增类型）"""
        # 验证已有功能
        creator = EmailCreator()
        result = creator.send_notification("开闭原则测试")
        assert result == "[邮件] 开闭原则测试"


# ============================================================================
# 测试练习3：文件解析器工厂
# ============================================================================

class TestFileParserFactory:
    """测试文件解析器工厂"""

    def test_create_csv_parser(self):
        """测试创建 CSV 解析器"""
        parser = FileParserFactory.create_parser("data.csv")
        assert isinstance(parser, CsvParser)
        result = parser.parse("data.csv")
        assert isinstance(result, list)
        assert len(result) > 0
        assert "name" in result[0]

    def test_create_json_parser(self):
        """测试创建 JSON 解析器"""
        parser = FileParserFactory.create_parser("config.json")
        assert isinstance(parser, JsonParser)
        result = parser.parse("config.json")
        assert isinstance(result, dict)
        assert "name" in result

    def test_create_xml_parser(self):
        """测试创建 XML 解析器"""
        parser = FileParserFactory.create_parser("data.xml")
        assert isinstance(parser, XmlParser)
        result = parser.parse("data.xml")
        assert isinstance(result, dict)
        assert "name" in result

    def test_create_with_path(self):
        """测试带路径的文件名"""
        parser = FileParserFactory.create_parser("/home/user/data.csv")
        assert isinstance(parser, CsvParser)

    def test_create_with_relative_path(self):
        """测试相对路径"""
        parser = FileParserFactory.create_parser("./subdir/config.json")
        assert isinstance(parser, JsonParser)

    def test_invalid_extension(self):
        """测试不支持的文件扩展名"""
        with pytest.raises(ValueError, match="不支持的文件格式"):
            FileParserFactory.create_parser("data.txt")

    def test_no_extension(self):
        """测试没有扩展名的文件"""
        with pytest.raises(ValueError, match="不支持的文件格式"):
            FileParserFactory.create_parser("README")

    def test_csv_parser_return_type(self):
        """测试 CSV 解析器返回列表"""
        parser = FileParserFactory.create_parser("report.csv")
        result = parser.parse("report.csv")
        assert isinstance(result, list)

    def test_json_parser_return_type(self):
        """测试 JSON 解析器返回字典"""
        parser = FileParserFactory.create_parser("settings.json")
        result = parser.parse("settings.json")
        assert isinstance(result, dict)
