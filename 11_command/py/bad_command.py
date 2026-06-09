"""
================================================================================
Lesson 11: Command — 命令模式 [行为型]
================================================================================
  📖 本课采用"反模式驱动"方式：
     先看一段"糟糕的代码"，分析它的问题，
     再引入设计模式来拯救它。

🔑 面试频率：★★★★☆
================================================================================
"""

"""
===============================================================================
🎬 场景：你在做一个"智能家居遥控器"程序

  需求：遥控器上有多个按钮，按下不同按钮控制不同家电。

  家电清单：
    1. 💡 灯（Light）：可以开/关
    2. 🌀 风扇（Fan）：可以开/关
    3. 🔊 音响（Stereo）：可以开/关、调节音量

  你的同事写了一个 RemoteControl 类，把所有控制逻辑
  都硬编码在了按钮点击事件里……

  请你先停在这里想一想：
    1. 如果新增一个家电（比如空调），需要改哪些代码？
    2. 如果按钮布局变了（比如把"开灯"和"关灯"拆成两个按钮），需要改哪些代码？
    3. 怎么实现"撤销"功能？按下"开灯"后，按"撤销"应该关灯。
    4. 怎么实现"宏命令"？按一个键同时执行"开灯+开风扇+开音响"？

  🧠 思考 10 秒钟...
    .
    .
    .
    .
    .
    .
    .
    .
    想好了吗？往下翻看同事的代码 👇
===============================================================================
"""

# ============================================================================
# 反模式：硬编码的遥控器
# ============================================================================

class Light:
    """灯"""

    def on(self):
        print("  💡 灯打开了")

    def off(self):
        print("  💡 灯关闭了")


class Fan:
    """风扇"""

    def on(self):
        print("  🌀 风扇打开了")

    def off(self):
        print("  🌀 风扇关闭了")


class Stereo:
    """音响"""

    def on(self):
        print("  🔊 音响打开了")

    def off(self):
        print("  🔊 音响关闭了")

    def set_volume(self, vol: int):
        print(f"  🔊 音量设置为 {vol}")


class RemoteControl:
    """
    遥控器——把所有控制逻辑硬编码在按钮事件里

    😱 问题：
      1. 新增家电需要修改 RemoteControl 类——违反"开闭原则"
      2. 按钮和家电紧密耦合——无法独立变化
      3. 无法实现撤销功能——没有记录操作历史
      4. 无法实现宏命令——一个按钮执行多个操作
    """

    def __init__(self):
        self.light = Light()
        self.fan = Fan()
        self.stereo = Stereo()

    def on_button_pressed(self, btn: str):
        """按钮被按下——硬编码的判断逻辑"""
        if btn == "light_on":
            self.light.on()
        elif btn == "light_off":
            self.light.off()
        elif btn == "fan_on":
            self.fan.on()
        elif btn == "fan_off":
            self.fan.off()
        elif btn == "stereo_on":
            self.stereo.on()
        elif btn == "stereo_off":
            self.stereo.off()
        elif btn == "stereo_vol_up":
            self.stereo.set_volume(10)
        else:
            print(f"  ❌ 未知按钮: {btn}")


"""
❌ 这个方案的问题：

  问题 1：违反开闭原则
    如果新增"空调"：
      - 创建 AirConditioner 类 ✅
      - 修改 RemoteControl 添加 if-elif ❌（改已有代码）
    每次新增家电，RemoteControl 都要改，风险很大。

  问题 2：无法撤销
    按下"开灯"后，遥控器没有记录这个操作。
    用户说"撤销"——遥控器不知道刚才做了什么。

  问题 3：无法组合
    按一个键同时"开灯+开风扇+开音响"？
    需要额外写一个 if 分支，或者新按钮。

  问题 4：紧密耦合
    RemoteControl 直接依赖 Light, Fan, Stereo 具体类。
    如果 Light 的接口变了（on() → turnOn()），
    RemoteControl 也要跟着改。

  💡 本质问题：
    "请求的发起者"（遥控器）和"请求的执行者"（家电）直接耦合了。
    我们需要一种方式把"请求"封装成一个独立的对象，
    让遥控器不依赖具体的家电，只依赖"命令接口"。
    这就是——命令模式（Command）！
"""


# ============================================================================
# 🤔 如果你来设计，你会怎么做？
#
# 命令模式的核心思想：把"操作"封装成对象。
#
# 想象一个餐厅场景：
#   - 顾客（Client）告诉服务员（Invoker）要什么菜
#   - 服务员写下菜单（Command）
#   - 厨师（Receiver）根据菜单做菜
#   服务员不关心厨师怎么做菜，只关心"菜单"。
#
# 对应到我们的遥控器：
#   - 用户（Client）按下按钮
#   - 遥控器（Invoker）持有命令对象
#   - 家电（Receiver）执行具体操作
#   遥控器不关心家电怎么工作，只关心"命令"。
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🎮 反模式：硬编码遥控器")
    print("=" * 50)

    remote = RemoteControl()

    print("\n 按下 'light_on' 按钮:")
    remote.on_button_pressed("light_on")

    print("\n 按下 'fan_on' 按钮:")
    remote.on_button_pressed("fan_on")

    print("\n 按下 'stereo_on' 按钮:")
    remote.on_button_pressed("stereo_on")

    print("\n 按下 'stereo_vol_up' 按钮:")
    remote.on_button_pressed("stereo_vol_up")

    # 问题演示：新增空调需要改 RemoteControl
    print("\n 按下 'ac_on' 按钮（空调）:")
    remote.on_button_pressed("ac_on")  # ❌ 输出 "未知按钮"
