"""
================================================================================
练习题 9: Observer — 观察者模式
================================================================================
📐 观察者模式(Observer Pattern)定义了对象之间的一对多依赖关系，
   当一个对象状态发生变化时，所有依赖它的对象都会收到通知并自动更新。

💡 本练习包含 3 道题：
   第1题（基础）: 实现股票通知系统
   第2题（综合）: 实现事件驱动的用户注册系统
   第3题（拓展）: 实现 Pull 模式的观察者
================================================================================
"""

import abc
from typing import List


# ============================================================================
# 第1题（基础）: 股票通知系统
# ============================================================================
#
# 实现一个简单的股票价格通知系统。
# 当 Stock 的 price 属性变化时，通知所有注册的 Investor。
#
# 要求：
#   1. Stock 作为 Subject（主题），维护投资者列表
#   2. Investor 作为 Observer（观察者），实现 update(stock_name, price) 方法
#   3. 当 Stock.price 被设置新值时，自动通知所有投资者
#   4. 支持注册(register)和注销(unregister)投资者
#
# 提示：
#   - 参考 observer.py 中的 Subject/Observer 接口设计
#   - 用 @property 装饰 price，在 setter 中触发通知

class Investor(abc.ABC):
    """观察者接口：投资者"""

    @abc.abstractmethod
    def update(self, stock_name: str, price: float):
        """接收股票价格更新通知"""
        pass


class Stock:
    """主题：股票"""

    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
        self._investors: List[Investor] = []

    def register(self, investor: Investor):
        """注册投资者（观察者）"""
        # TODO: 将 investor 添加到 _investors 列表中
        raise NotImplementedError

    def unregister(self, investor: Investor):
        """注销投资者（观察者）"""
        # TODO: 从 _investors 列表中移除 investor
        raise NotImplementedError

    def _notify_investors(self):
        """通知所有投资者"""
        # TODO: 遍历 _investors 列表，调用每个投资者的 update(stock_name, price)
        raise NotImplementedError

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float):
        """设置新价格并自动通知"""
        # TODO: 更新 _price，然后调用 _notify_investors()
        raise NotImplementedError


# 具体观察者：个人投资者
class IndividualInvestor(Investor):
    def __init__(self, name: str):
        self.name = name
        self.notifications: List[str] = []

    def update(self, stock_name: str, price: float):
        notification = f"{self.name} 收到通知: {stock_name} 价格变为 {price}"
        self.notifications.append(notification)


# ============================================================================
# 第2题（综合）: 事件驱动的用户注册系统
# ============================================================================
#
# 实现一个用户注册事件通知系统。
# UserManager 在注册用户时触发事件，多个观察者各自处理通知。
#
# 要求：
#   1. UserManager 作为主题，提供 register_user(username) 方法
#   2. EmailNotifier: 发送欢迎邮件（记录到列表）
#   3. SMSNotifier: 发送短信通知（记录到列表）
#   4. Logger: 记录注册日志（记录到列表）
#   5. 支持注册和注销观察者
#   6. 事件类型用字符串表示，如 "user_registered"

class Observer(abc.ABC):
    """观察者接口"""

    @abc.abstractmethod
    def update(self, event_type: str, data: dict):
        """处理事件通知"""
        pass


class UserManager:
    """主题：用户管理器"""

    def __init__(self):
        self._observers: List[Observer] = []

    def register_observer(self, observer: Observer):
        """注册观察者"""
        # TODO: 将 observer 添加到 _observers 列表中
        raise NotImplementedError

    def remove_observer(self, observer: Observer):
        """移除观察者"""
        # TODO: 从 _observers 列表中移除 observer
        raise NotImplementedError

    def notify_observers(self, event_type: str, data: dict):
        """通知所有观察者"""
        # TODO: 遍历 _observers，调用每个观察者的 update(event_type, data)
        raise NotImplementedError

    def register_user(self, username: str, email: str, phone: str):
        """
        注册新用户并触发通知
        data 应包含: username, email, phone
        """
        # TODO: 调用 notify_observers("user_registered", data)
        raise NotImplementedError


# 具体观察者：邮件通知器
class EmailNotifier(Observer):
    def __init__(self):
        self.sent_emails: List[str] = []

    def update(self, event_type: str, data: dict):
        if event_type == "user_registered":
            msg = f"发送欢迎邮件到 {data['email']}，用户: {data['username']}"
            self.sent_emails.append(msg)


# 具体观察者：短信通知器
class SMSNotifier(Observer):
    def __init__(self):
        self.sent_sms: List[str] = []

    def update(self, event_type: str, data: dict):
        if event_type == "user_registered":
            msg = f"发送短信到 {data['phone']}，用户: {data['username']}"
            self.sent_sms.append(msg)


# 具体观察者：日志记录器
class Logger(Observer):
    def __init__(self):
        self.logs: List[str] = []

    def update(self, event_type: str, data: dict):
        if event_type == "user_registered":
            msg = f"[LOG] 用户注册: {data['username']}"
            self.logs.append(msg)


# ============================================================================
# 第3题（拓展）: Pull 模式的观察者
# ============================================================================
#
# 实现 Pull（拉取）模式的观察者。
# 主题只通知"数据变了"（update() 无参数），
# 观察者自己调用主题的 getter 获取最新的值。
#
# 场景：一个新闻聚合系统。
#   NewsAgency（新闻社）发布新闻，NewsChannel（新闻频道）拉取最新新闻。
#
# 要求：
#   1. NewsAgency 维护新闻列表，有新新闻时通知所有频道
#   2. 通知时只调用 update()，不传数据（Pull 模式）
#   3. NewsChannel 通过 NewsAgency 的 getter 获取最新新闻
#   4. 每个 NewsChannel 可以拉取全部或部分新闻（按需拉取）

class PullObserver(abc.ABC):
    """Pull 模式观察者接口"""

    @abc.abstractmethod
    def update(self):
        """收到通知，自行拉取数据"""
        pass


class NewsAgency:
    """Pull 模式的主题：新闻社"""

    def __init__(self):
        self._channels: List[PullObserver] = []
        self._news_list: List[str] = []

    def register_channel(self, channel: PullObserver):
        """注册频道（观察者）"""
        # TODO: 将 channel 添加到 _channels 列表中
        raise NotImplementedError

    def unregister_channel(self, channel: PullObserver):
        """注销频道（观察者）"""
        # TODO: 从 _channels 列表中移除 channel
        raise NotImplementedError

    def notify_channels(self):
        """Pull 方式：只通知，不传数据"""
        # TODO: 遍历 _channels，调用每个 channel 的 update()
        raise NotImplementedError

    def publish_news(self, news: str):
        """发布新新闻"""
        # TODO: 添加新闻到 _news_list，然后调用 notify_channels()
        raise NotImplementedError

    def get_all_news(self) -> List[str]:
        """返回所有新闻列表"""
        # TODO: 返回 _news_list
        raise NotImplementedError

    def get_latest_news(self) -> str:
        """返回最后一条新闻"""
        # TODO: 如果 _news_list 不为空，返回最后一条；否则返回空字符串
        raise NotImplementedError


# 具体观察者：新闻频道（Pull 模式）
class NewsChannel(PullObserver):
    def __init__(self, name: str, agency: NewsAgency):
        self.name = name
        self._agency = agency
        self.received_news: List[str] = []

    def update(self):
        """
        Pull 模式：收到通知后，自己从 NewsAgency 拉取最新新闻
        """
        # TODO: 通过 self._agency 的 getter 获取最新新闻并添加到 received_news
        pass
