"""
================================================================================
测试 09 Observer 练习题
================================================================================
"""

import pytest
from exercise import (
    Stock, IndividualInvestor,
    UserManager, EmailNotifier, SMSNotifier, Logger,
    NewsAgency, NewsChannel
)


# ============================================================================
# 测试第1题：股票通知系统
# ============================================================================

class TestStockNotification:
    """测试股票通知系统"""

    def test_price_change_notifies_investor(self):
        """测试价格变化时通知投资者"""
        stock = Stock("腾讯", 300.0)
        investor = IndividualInvestor("张三")
        stock.register(investor)

        stock.price = 310.0

        assert len(investor.notifications) == 1
        assert "腾讯" in investor.notifications[0]
        assert "310.0" in investor.notifications[0]

    def test_multiple_investors_receive_notification(self):
        """测试多个投资者都收到通知"""
        stock = Stock("阿里巴巴", 200.0)
        investor1 = IndividualInvestor("张三")
        investor2 = IndividualInvestor("李四")

        stock.register(investor1)
        stock.register(investor2)
        stock.price = 210.0

        assert len(investor1.notifications) == 1
        assert len(investor2.notifications) == 1

    def test_unregistered_investor_not_notified(self):
        """测试注销后不再收到通知"""
        stock = Stock("百度", 150.0)
        investor = IndividualInvestor("张三")

        stock.register(investor)
        stock.unregister(investor)
        stock.price = 160.0

        assert len(investor.notifications) == 0

    def test_multiple_price_changes(self):
        """测试多次价格变化"""
        stock = Stock("拼多多", 100.0)
        investor = IndividualInvestor("张三")
        stock.register(investor)

        stock.price = 110.0
        stock.price = 120.0
        stock.price = 130.0

        assert len(investor.notifications) == 3


# ============================================================================
# 测试第2题：事件驱动的用户注册系统
# ============================================================================

class TestUserRegistration:
    """测试用户注册事件系统"""

    def test_email_notifier_receives_event(self):
        """测试邮件通知器收到注册事件"""
        manager = UserManager()
        email_notifier = EmailNotifier()

        manager.register_observer(email_notifier)
        manager.register_user("test_user", "test@example.com", "13800138000")

        assert len(email_notifier.sent_emails) == 1
        assert "test@example.com" in email_notifier.sent_emails[0]

    def test_all_notifiers_receive_event(self):
        """测试所有通知器都收到注册事件"""
        manager = UserManager()
        email = EmailNotifier()
        sms = SMSNotifier()
        logger = Logger()

        manager.register_observer(email)
        manager.register_observer(sms)
        manager.register_observer(logger)
        manager.register_user("alice", "alice@test.com", "13900139000")

        assert len(email.sent_emails) == 1
        assert len(sms.sent_sms) == 1
        assert len(logger.logs) == 1

    def test_observer_removed_not_notified(self):
        """测试移除观察者后不再收到通知"""
        manager = UserManager()
        logger = Logger()

        manager.register_observer(logger)
        manager.remove_observer(logger)
        manager.register_user("bob", "bob@test.com", "13700137000")

        assert len(logger.logs) == 0

    def test_multiple_registrations(self):
        """测试多次注册"""
        manager = UserManager()
        logger = Logger()

        manager.register_observer(logger)
        manager.register_user("user1", "u1@test.com", "111")
        manager.register_user("user2", "u2@test.com", "222")

        assert len(logger.logs) == 2


# ============================================================================
# 测试第3题：Pull 模式的观察者
# ============================================================================

class TestPullObserver:
    """测试 Pull 模式的观察者"""

    def test_channel_receives_latest_news(self):
        """测试频道拉取到最新新闻"""
        agency = NewsAgency()
        channel = NewsChannel("体育频道", agency)
        agency.register_channel(channel)

        agency.publish_news("中国队夺冠！")

        assert len(channel.received_news) == 1
        assert "中国队夺冠" in channel.received_news[0]

    def test_multiple_news_published(self):
        """测试发布多条新闻"""
        agency = NewsAgency()
        channel = NewsChannel("综合频道", agency)
        agency.register_channel(channel)

        agency.publish_news("新闻1")
        agency.publish_news("新闻2")
        agency.publish_news("新闻3")

        assert len(channel.received_news) == 3

    def test_unregistered_channel_not_notified(self):
        """测试注销后不再拉取新闻"""
        agency = NewsAgency()
        channel = NewsChannel("测试频道", agency)

        agency.register_channel(channel)
        agency.unregister_channel(channel)
        agency.publish_news("独家新闻")

        assert len(channel.received_news) == 0

    def test_agency_holds_all_news(self):
        """测试 NewsAgency 保存所有新闻"""
        agency = NewsAgency()
        agency.publish_news("新闻A")
        agency.publish_news("新闻B")

        all_news = agency.get_all_news()
        assert len(all_news) == 2
        assert "新闻A" in all_news
        assert "新闻B" in all_news

    def test_latest_news_getter(self):
        """测试 get_latest_news 返回最新新闻"""
        agency = NewsAgency()
        agency.publish_news("旧闻")
        agency.publish_news("最新消息")

        assert agency.get_latest_news() == "最新消息"
