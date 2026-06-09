"""
================================================================================
 Lesson 9: Observer — 观察者模式（模式实现）
================================================================================
  上节课的 bad_observer.py 我们看到了硬编码通知的问题，
  现在来看看观察者模式怎么解决。

 📐 设计模式定义：
    观察者模式(Observer Pattern)定义了对象之间的一对多依赖关系，
    当一个对象状态发生变化时，所有依赖它的对象都会收到通知并自动更新。

 🎯 解决的问题：
    - 对象之间的一对多通知关系
    - 避免硬编码的通知列表
    - 让主题（Subject）和观察者（Observer）解耦

 💡 核心角色：
    1. Subject（主题/可观察者）：维护观察者列表，提供注册/注销/通知方法
    2. Observer（观察者）：定义 update 接口，接收主题的通知
    3. ConcreteSubject（具体主题）：状态变化时通知所有观察者
    4. ConcreteObserver（具体观察者）：实现 update，处理通知

  📤 推送(push) vs 📥 拉取(pull)：
    - Push：主题将数据推送给观察者（update(data)）
    - Pull：观察者从主题拉取数据（update()，然后 subject.getXxx()）
    - Python 特色：可以同时支持两种方式
================================================================================
"""

import abc
from typing import List, Optional, Callable


# ============================================================================
# 观察者接口
# ============================================================================

class Observer(abc.ABC):
    """
    👁 观察者接口（抽象基类）

    所有观察者必须实现 update() 方法。
    当主题数据变化时，会调用每个观察者的 update()。
    """

    @abc.abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float):
        """
        接收主题推送的数据（Push 模式）。

        :param temperature: 温度 (°C)
        :param humidity: 湿度 (%)
        :param pressure: 气压 (hPa)
        """
        pass


class Subject(abc.ABC):
    """
    📡 主题接口（可观察者）

    定义观察者的注册、注销、通知方法。
    """

    @abc.abstractmethod
    def register_observer(self, observer: Observer):
        """注册观察者"""
        pass

    @abc.abstractmethod
    def remove_observer(self, observer: Observer):
        """注销观察者"""
        pass

    @abc.abstractmethod
    def notify_observers(self):
        """通知所有观察者"""
        pass


# ============================================================================
# 实现 1：经典观察者模式（Push 推送方式）
# ============================================================================

class WeatherData(Subject):
    """
    ☀️ 具体主题：天气数据

    职责：
      1. 维护观察者列表
      2. 测量数据变化时通知所有观察者
      3. 观察者可以动态注册/注销

    对比反模式 WeatherStation：
      - 不再硬编码面板列表
      - 新增面板不需要修改 WeatherData 代码
      - 可以在运行时动态增减面板
    """

    def __init__(self):
        self._observers: List[Observer] = []  # 观察者列表
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    # ---- 观察者管理 ----

    def register_observer(self, observer: Observer):
        """注册观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"  [注册] {observer.__class__.__name__} 已加入订阅")

    def remove_observer(self, observer: Observer):
        """注销观察者"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"  [注销] {observer.__class__.__name__} 已取消订阅")

    # ---- 通知机制 ----

    def notify_observers(self):
        """
        通知所有观察者（Push 方式）。

        Push 方式：主题主动把数据推给观察者。
        优点是观察者不需要主动拉取，适合实时更新场景。
        缺点是如果数据量很大或观察者只需要部分数据，会有浪费。
        """
        print(f"\n  [通知] 向 {len(self._observers)} 个观察者推送数据...")
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    # ---- 数据更新 ----

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        """
        设置新数据并自动通知所有观察者。

        当测量值变化时，主题自动通知所有观察者。
        观察者无需轮询（pull），符合"好莱坞原则"：Don't call us, we'll call you.
        """
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure

        print(f"\n  [WeatherData] 新测量值: {temperature}°C, {humidity}%, {pressure}hPa")
        self.notify_observers()


# ============================================================================
# 具体观察者
# ============================================================================

class CurrentConditionsDisplay(Observer):
    """
    📊 当前天气面板

    显示当前的温度、湿度、气压。
    """

    def update(self, temperature: float, humidity: float, pressure: float):
        print(f"  [当前天气] 🌡 {temperature}°C | 💧 {humidity}% | 🌀 {pressure}hPa")


class StatsDisplay(Observer):
    """
    📈 统计面板

    追踪最高/最低/平均温度。
    """

    def __init__(self):
        self._temperatures: List[float] = []

    def update(self, temperature: float, humidity: float, pressure: float):
        self._temperatures.append(temperature)
        avg = sum(self._temperatures) / len(self._temperatures)
        print(f"  [统计面板] 最高={max(self._temperatures)}°C, "
              f"最低={min(self._temperatures)}°C, "
              f"平均={avg:.1f}°C ({len(self._temperatures)} 次采样)")


class ForecastDisplay(Observer):
    """
    🔮 预报面板

    根据气压变化做简单预报：
      - 气压上升 → 天气转好
      - 气压下降 → 可能下雨
    """

    def __init__(self):
        self._last_pressure = 0.0

    def update(self, temperature: float, humidity: float, pressure: float):
        if self._last_pressure == 0.0:
            forecast = "数据不足，无法预报"
        elif pressure > self._last_pressure:
            forecast = "天气转好 ☀️"
        elif pressure < self._last_pressure:
            forecast = "注意：可能有雨 🌧"
        else:
            forecast = "天气稳定"

        self._last_pressure = pressure
        print(f"  [预报面板] {forecast}")


# ============================================================================
# 实现 2：Pull（拉取）方式
# ============================================================================

"""
📥 Pull 模式 vs 📤 Push 模式

Push（推送）——上面的实现：
  update(temperature, humidity, pressure)
  主题把所有数据推给观察者。

Pull（拉取）：
  update()  →  观察者通过主题的 getter 自己拉取需要的数据
  主题只通知"数据变了"，观察者决定自己要什么。

Pull 的优点：
  - 观察者只拿自己需要的数据（节省带宽/计算）
  - 主题不需要知道观察者需要什么

Pull 的缺点：
  - 观察者需要持有主题的引用
  - 多了一次方法调用（先通知，再拉取）

Python 中可以同时支持两种方式。
"""


class PullWeatherData(Subject):
    """
    Pull 方式的天气数据主题。

    通知时只调用 update() 不传数据，
    观察者通过 getter 自己拉取感兴趣的数据。
    """

    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def register_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        """Pull 方式：只通知，不传数据"""
        print(f"\n  [Pull通知] 数据已更新，观察者自行拉取...")
        for observer in self._observers:
            observer.update()  # 注意：不传数据！

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify_observers()

    # ---- Pull 方式需要提供的 getter ----
    def get_temperature(self) -> float:
        return self._temperature

    def get_humidity(self) -> float:
        return self._humidity

    def get_pressure(self) -> float:
        return self._pressure


class PullCurrentConditionsDisplay(Observer):
    """
    Pull 方式的当前天气面板。

    只拉取自己需要的温度数据。
    """

    def __init__(self, weather_data: PullWeatherData):
        self._weather_data = weather_data  # 持有主题引用

    def update(self):
        # 只拉取温度（因为当前面板只关心温度）
        temp = self._weather_data.get_temperature()
        print(f"  [Pull-当前天气] 温度: {temp}°C")


# ============================================================================
# 实现 3：Python 特色——使用 __call__ 替代观察者接口
# ============================================================================

"""
🐍 Python 特色实现：

Python 中，只要对象实现了 __call__ 方法，它就可以像函数一样被调用。
我们可以用 __call__ 替代完整的 Observer 接口，让观察者模式更轻量。

这类似于回调函数（callback）的思想：
  - 主题不需要知道观察者是什么类型
  - 只要求观察者是一个可调用对象（Callable）
  - 更灵活，更 Pythonic

对比 C++：
  - C++ 可以用 std::function 实现类似效果
  - 但 C++ 的传统做法是用虚函数接口
"""


class CallableWeatherData:
    """
    使用回调函数（Callable）的天气数据主题。

    观察者不再是"类"，而是"可调用对象"。
    这比经典观察者模式更灵活：
      - 可以是函数、lambda、实现了 __call__ 的类
      - 不需要继承 Observer 接口
      - 更符合 Python 的鸭子类型哲学
    """

    def __init__(self):
        self._callbacks: List[Callable[[float, float, float], None]] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def register_callback(self, callback: Callable[[float, float, float], None]):
        """注册回调函数"""
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[float, float, float], None]):
        """注销回调函数"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        print(f"\n  [CallbackWeatherData] 新数据: {temperature}°C, {humidity}%, {pressure}hPa")
        for callback in self._callbacks:
            callback(temperature, humidity, pressure)


# 用普通函数作为观察者
def log_to_file_callback(temp: float, humidity: float, pressure: float):
    """一个简单的日志回调函数"""
    print(f"  [日志回调] 记录数据: {temp}°C, {humidity}%, {pressure}hPa")


# 用 lambda 作为观察者
alert_callback = lambda t, h, p: print(f"  [警报回调] 温度={t}°C" if t > 30 else f"  [警报回调] 温度正常")


# ============================================================================
# 🧪 测试观察者模式
# ============================================================================

def test_observer():
    print("=" * 60)
    print("✅ 经典观察者模式（Push 推送）")
    print("=" * 60)

    # 创建主题
    weather_data = WeatherData()

    # 创建观察者
    current = CurrentConditionsDisplay()
    stats = StatsDisplay()
    forecast = ForecastDisplay()

    # 注册观察者
    weather_data.register_observer(current)
    weather_data.register_observer(stats)
    weather_data.register_observer(forecast)

    # 模拟数据更新
    weather_data.set_measurements(25.0, 65, 1012)
    weather_data.set_measurements(26.5, 70, 1008)
    weather_data.set_measurements(24.0, 80, 1005)

    # ---------- 演示动态注册/注销 ----------
    print("\n" + "=" * 60)
    print("🔄 演示：动态注销/注册观察者")
    print("=" * 60)

    weather_data.remove_observer(forecast)  # 关闭预报面板
    weather_data.set_measurements(22.0, 60, 1018)  # 只有 current 和 stats 收到通知

    weather_data.register_observer(forecast)  # 重新开启预报面板
    weather_data.set_measurements(28.0, 55, 1010)  # 三个面板都收到通知

    # ---------- 演示 Callable 回调方式 ----------
    print("\n" + "=" * 60)
    print("🐍 Python 特色：Callback 回调方式")
    print("=" * 60)

    cb_weather = CallableWeatherData()
    cb_weather.register_callback(log_to_file_callback)
    cb_weather.register_callback(alert_callback)
    cb_weather.register_callback(
        lambda t, h, p: print(f"  [lambda面板] 湿度={h}% {'偏高' if h > 75 else '正常'}")
    )

    cb_weather.set_measurements(28.0, 80, 1015)  # 三个回调都触发
    cb_weather.set_measurements(32.0, 60, 1010)  # 温度>30触发警报


if __name__ == "__main__":
    test_observer()


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 观察者模式 vs 发布订阅模式（Pub-Sub）有什么区别？
    A: 这是面试最高频的陷阱题。
       - 观察者模式：Subject 直接通知 Observer（点对点）
         主题和观察者知道彼此的存在
       - 发布订阅模式：通过消息代理（Broker）中转（松耦合）
         发布者和订阅者不知道彼此，通过事件频道/主题通信
       - 观察者是"直接"的，Pub-Sub 是"间接"的
       - 观察者通常是同步的，Pub-Sub 可以是异步的

Q2: 内存泄漏问题？观察者没有被正确注销？
    A: 这是一个经典问题！
       - 如果主题持有观察者的引用，而观察者不再需要了，
         却没有调用 remove_observer，就会造成内存泄漏
       - 在 Python 中，这会导致观察者对象无法被 GC 回收
       - 解决方案：
         ① 使用弱引用（weakref）存储观察者
         ② 在观察者的 __del__ 中自动注销
         ③ 使用上下文管理器（with 语句）自动管理生命周期

Q3: 通知顺序重要吗？观察者之间有依赖关系怎么办？
    A: 观察者模式不保证通知顺序。
       如果观察者之间有依赖（A 需要在 B 之前更新），
       说明设计有问题——观察者应该是相互独立的。
       如果一定要控制顺序，可以用优先级队列。

Q4: 观察者模式有什么缺点？
    A: 1. 观察者可能收到不感兴趣的通知（Pull 方式可缓解）
       2. 通知风暴：频繁更新时，观察者被反复通知（可用事件节流）
       3. 循环依赖：A 观察 B，B 观察 A（需要检测环路）
       4. 性能：大量观察者时通知有开销（可考虑异步）

Q5: Python 中还有什么实现观察者模式的库？
    A: 1. blinker：轻量级信号库
       2. PyDispatcher：强大的事件分发系统
       3. asyncio 的事件循环：内置事件驱动
       4. Django 的信号系统：基于观察者模式

💡 面试官变种题：
   如果观察者更新非常频繁，怎么优化？
   思路：
     1. 批量更新：收集多个变化后一次性通知
     2. 事件过滤：只通知感兴趣的事件
     3. 异步通知：用线程池/协程处理
     4. 观察者分组：按优先级/类别分批通知
"""
