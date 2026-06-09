"""
================================================================================
 Lesson 9: Observer — 观察者模式 [行为型] · 反模式
================================================================================
  📖 本课采用"反模式驱动"方式：
     先看一段糟糕的代码，分析问题，再引入设计模式。

 🔑 面试频率：★★★★★（几乎必问，尤其在 GUI 和事件驱动编程中）
================================================================================
"""

"""
===============================================================================
 🎬 场景：天气站系统

  你做一个气象监测系统，WeatherStation 收集温度、湿度、气压数据。
  数据变化时，三个面板需要更新：
    1. CurrentConditionsDisplay —— 显示当前天气
    2. StatsDisplay —— 显示统计数据（平均/最高/最低温度）
    3. ForecastDisplay —— 显示天气预报

  同事的做法：在 WeatherStation 里直接调用各个面板的更新方法。

  请你先停在这里想一想：
    1. 如果新增一个"空气质量面板"，需要改哪些代码？
    2. 如果想删除"预报面板"，又需要改哪些代码？
    3. 如果面板的更新频率不一样（一个每秒更新，一个每5秒更新）？
    .
    .
    .
    想好了吗？往下翻看"硬编码通知"的写法 👇
===============================================================================
"""


# ============================================================================
# 反模式：硬编码通知
# ============================================================================

class CurrentConditionsDisplay:
    """
    当前天气面板。
    """

    def update(self, temperature: float, humidity: float, pressure: float):
        """接收更新数据"""
        print(f"  [当前天气] {temperature}°C, {humidity}%, {pressure}hPa")


class StatsDisplay:
    """
    统计面板：记录最高、最低、平均温度。
    """

    def __init__(self):
        self.temps = []

    def update(self, temperature: float, humidity: float, pressure: float):
        self.temps.append(temperature)
        avg = sum(self.temps) / len(self.temps)
        print(f"  [统计面板] 最高={max(self.temps)}°C, "
              f"最低={min(self.temps)}°C, 平均={avg:.1f}°C")


class ForecastDisplay:
    """
    预报面板：简单的预报逻辑（气压低 → 下雨）。
    """

    def update(self, temperature: float, humidity: float, pressure: float):
        forecast = "晴天" if pressure > 1013 else "可能有雨"
        print(f"  [预报面板] {forecast}")


class WeatherStation:
    """
    ❌ 反模式：硬编码通知

    这个 WeatherStation 的问题是：
      1. 直接依赖了具体面板类（高耦合）
      2. 每次数据变化，手动调用每个面板的 update
      3. 新增面板必须修改 WeatherStation 代码（违反开闭原则）
      4. 面板之间是"硬编码"的关系，无法运行时动态增减

    😱 这就像你的手机系统每次更新都要改内核代码才能支持新 App！
    """

    def __init__(self):
        self.temperature = 0.0
        self.humidity = 0.0
        self.pressure = 0.0

        # 硬编码创建面板——注意这里的强依赖关系！
        self.current_display = CurrentConditionsDisplay()
        self.stats_display = StatsDisplay()
        self.forecast_display = ForecastDisplay()

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        """
        设置新数据并通知所有面板。

        ❌ 问题：如果新增一个面板，必须在这里加一行新的 update 调用。
                  如果删除一个面板，也必须在这里删除对应的行。
                  如果面板类改名了，这里也必须改。
        """
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

        print(f"\n  [WeatherStation] 新数据: {temperature}°C, {humidity}%, {pressure}hPa")
        print(f"  [通知] 开始通知所有面板...")

        # ---------- 硬编码的通知列表 ----------
        self.current_display.update(temperature, humidity, pressure)
        self.stats_display.update(temperature, humidity, pressure)
        self.forecast_display.update(temperature, humidity, pressure)
        # 如果再加一个 AirQualityDisplay：
        # self.air_quality_display.update(temperature, humidity, pressure)
        # ❌ 每次都要改这里！

        print(f"  [通知] 所有面板通知完毕")


# ============================================================================
# 🧪 测试反模式代码
# ============================================================================

def test_bad_observer():
    print("=" * 60)
    print("❌ 反模式：硬编码通知 天气站系统")
    print("=" * 60)

    station = WeatherStation()

    station.set_measurements(25.0, 65, 1012)
    station.set_measurements(26.5, 70, 1008)
    station.set_measurements(24.0, 80, 1005)

    print("\n" + "=" * 60)
    print("🤔 思考：")
    print("  现在产品经理说：")
    print("    1. 新增一个'空气质量面板'（PM2.5）")
    print("    2. 用户可以选择关闭'预报面板'")
    print("  你需要改哪些代码？")
    print("    - 改 WeatherStation.__init__：创建新面板")
    print("    - 改 set_measurements：增加/减少 update 调用")
    print("    - 这种改动非常脆弱，一不小心就漏改或改错")
    print("=" * 60)


"""
===============================================================================
 反模式总结

 ❌ 存在的问题：
    1. 紧耦合（Tight Coupling）
       → WeatherStation 直接依赖具体面板类
       → 面板变化 = WeatherStation 必须跟着变

    2. 违反开闭原则（Open/Closed Principle）
       → 新增面板需要修改 WeatherStation（对修改开放）
       → 而不是通过扩展来增加功能（对扩展关闭）

    3. 无法运行时动态管理
       → 不能动态添加/删除面板
       → 不能按需订阅/取消订阅

    4. 通知方式单一
       → 所有面板收到同样的数据，无法筛选
       → 无法实现"某些面板只关心特定事件"

 ✅ 解决思路：观察者模式
   将"谁关心数据变化"这件事抽象出来：
   主题（Subject）维护观察者列表，数据变化时自动通知所有观察者。
   观察者可以动态注册/注销。

   翻到 observer.py 看正解 👉
===============================================================================
"""


if __name__ == "__main__":
    test_bad_observer()
