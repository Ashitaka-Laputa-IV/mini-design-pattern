"""
================================================================================
Lesson 11: Command — 命令模式（模式实现）
================================================================================
  上节课的 bad_command.py 我们看到了硬编码遥控器的问题，
  现在来看看命令模式怎么优雅解决。

📐 设计模式定义：
   命令模式(Command)将"请求"封装成对象，以便使用不同的请求、
   队列或者日志来参数化其他对象。命令模式也支持可撤销的操作。

🎯 解决的问题：
   - 将"请求发起者"和"请求执行者"解耦
   - 支持撤销/重做操作
   - 支持命令队列和日志
   - 支持宏命令（组合命令）

🏗 结构：
   ┌──────────┐     ┌──────────────────┐
   │  Client  │────→│    Command       │ (接口)
   └──────────┘     ├──────────────────┤
                    │ + execute()      │
                    │ + undo()         │
                    └────────┬─────────┘
                             △
                             │
               ┌─────────────┼─────────────┐
               │             │             │
   ┌───────────┴────┐ ┌─────┴──────┐ ┌────┴────────┐
   │ LightOnCommand │ │ FanOnCmd   │ │ MacroCmd    │
   ├────────────────┤ ├────────────┤ ├─────────────┤
   │ + execute()    │ │ + execute  │ │ + execute() │
   │ + undo()       │ │ + undo()   │ │ + undo()    │
   └───────┬────────┘ └─────┬──────┘ └─────────────┘
           │                │
           ▼                ▼
       ┌────────┐     ┌────────┐
       │  Light │     │  Fan   │  (Receiver)
       └────────┘     └────────┘

   ┌─────────────┐
   │  Invoker    │  (遥控器)
   ├─────────────┤
   │ + setCmd()  │
   │ + pressBtn()│
   │ + undoBtn() │
   └─────────────┘
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ============================================================================
# 接收者（Receiver）：家电
# ============================================================================

class Light:
    """灯——命令的接收者之一"""

    def __init__(self, name: str = "客厅灯"):
        self.name = name
        self._is_on = False

    def on(self):
        self._is_on = True
        print(f"  💡 {self.name} 打开了")

    def off(self):
        self._is_on = False
        print(f"  💡 {self.name} 关闭了")

    @property
    def is_on(self) -> bool:
        return self._is_on


class Fan:
    """风扇——命令的接收者之一"""

    def __init__(self, name: str = "客厅风扇"):
        self.name = name
        self._is_on = False

    def on(self):
        self._is_on = True
        print(f"  🌀 {self.name} 打开了")

    def off(self):
        self._is_on = False
        print(f"  🌀 {self.name} 关闭了")

    @property
    def is_on(self) -> bool:
        return self._is_on


class Stereo:
    """音响——命令的接收者之一"""

    def __init__(self, name: str = "客厅音响"):
        self.name = name
        self._is_on = False
        self._volume = 0

    def on(self):
        self._is_on = True
        print(f"  🔊 {self.name} 打开了")

    def off(self):
        self._is_on = False
        self._volume = 0
        print(f"  🔊 {self.name} 关闭了")

    def set_volume(self, vol: int):
        self._volume = vol
        print(f"  🔊 {self.name} 音量设置为 {vol}")

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def volume(self) -> int:
        return self._volume


# ============================================================================
# 命令接口（Command）
# ============================================================================

class Command(ABC):
    """
    命令接口——所有命令都要实现 execute() 和 undo()

    为什么需要 undo()？
      因为命令模式的一个重要用途就是支持"撤销"。
      每个命令保存了执行前的状态，undo() 可以恢复到之前的状态。
    """

    @abstractmethod
    def execute(self):
        """执行命令"""
        pass

    @abstractmethod
    def undo(self):
        """撤销命令——恢复到执行前的状态"""
        pass


# ============================================================================
# 具体命令：Light 的命令
# ============================================================================

class LightOnCommand(Command):
    """
    开灯命令

    每个命令保存了一个"接收者"（Receiver）引用，
    execute() 时调用接收者的具体方法。
    """

    def __init__(self, light: Light):
        self.light = light
        self._prev_state = False  # 保存执行前的状态，用于撤销

    def execute(self):
        self._prev_state = self.light.is_on
        self.light.on()

    def undo(self):
        """撤销：如果之前是关的，现在关掉；反之亦然"""
        if self._prev_state:
            self.light.on()
        else:
            self.light.off()


class LightOffCommand(Command):
    """关灯命令"""

    def __init__(self, light: Light):
        self.light = light
        self._prev_state = False

    def execute(self):
        self._prev_state = self.light.is_on
        self.light.off()

    def undo(self):
        if self._prev_state:
            self.light.on()
        else:
            self.light.off()


# ============================================================================
# 具体命令：Fan 的命令
# ============================================================================

class FanOnCommand(Command):
    """开风扇命令"""

    def __init__(self, fan: Fan):
        self.fan = fan
        self._prev_state = False

    def execute(self):
        self._prev_state = self.fan.is_on
        self.fan.on()

    def undo(self):
        if self._prev_state:
            self.fan.on()
        else:
            self.fan.off()


class FanOffCommand(Command):
    """关风扇命令"""

    def __init__(self, fan: Fan):
        self.fan = fan
        self._prev_state = False

    def execute(self):
        self._prev_state = self.fan.is_on
        self.fan.off()

    def undo(self):
        if self._prev_state:
            self.fan.on()
        else:
            self.fan.off()


# ============================================================================
# 具体命令：Stereo 的命令
# ============================================================================

class StereoOnCommand(Command):
    """开音响命令"""

    def __init__(self, stereo: Stereo):
        self.stereo = stereo
        self._prev_state = False
        self._prev_volume = 0

    def execute(self):
        self._prev_state = self.stereo.is_on
        self._prev_volume = self.stereo.volume
        self.stereo.on()
        self.stereo.set_volume(10)  # 默认音量 10

    def undo(self):
        """撤销：恢复到之前的状态和音量"""
        if self._prev_state:
            self.stereo.on()
        else:
            self.stereo.off()
        self.stereo.set_volume(self._prev_volume)


class StereoOffCommand(Command):
    """关音响命令"""

    def __init__(self, stereo: Stereo):
        self.stereo = stereo
        self._prev_state = False
        self._prev_volume = 0

    def execute(self):
        self._prev_state = self.stereo.is_on
        self._prev_volume = self.stereo.volume
        self.stereo.off()

    def undo(self):
        if self._prev_state:
            self.stereo.on()
        else:
            self.stereo.off()
        self.stereo.set_volume(self._prev_volume)


# ============================================================================
# 空命令（No Command）
# ============================================================================

class NoCommand(Command):
    """
    空命令——Null Object 模式

    用途：
      - 避免在 Invoker 中频繁检查命令是否为 None
      - 提供一个"什么都不做"的默认命令
      - 符合"让默认行为无害"的设计原则
    """

    def execute(self):
        """什么都不做"""
        pass

    def undo(self):
        """什么都不做"""
        pass


# ============================================================================
# 调用者（Invoker）：遥控器
# ============================================================================

class RemoteControl:
    """
    遥控器——命令的调用者（Invoker）

    关键改进：
      ✅ 不依赖具体家电，只依赖 Command 接口
      ✅ 新增家电不需要修改遥控器代码
      ✅ 支持撤销操作
      ✅ 可以预设按钮布局
    """

    def __init__(self, slots: int = 7):
        """
        初始化遥控器，预设多个按钮槽位。

        每个槽位有两个命令：开(on)和关(off)。
        默认使用 NoCommand（什么都不做）。
        """
        self.on_commands: List[Command] = [NoCommand()] * slots
        self.off_commands: List[Command] = [NoCommand()] * slots
        self._undo_command: Command = NoCommand()  # 记录上一步操作，用于撤销

    def set_command(self, slot: int, on_command: Command, off_command: Command):
        """
        设置指定槽位的命令

        参数：
          slot: 按钮槽位编号 (0~slots-1)
          on_command: 按下"开"按钮执行的命令
          off_command: 按下"关"按钮执行的命令
        """
        if 0 <= slot < len(self.on_commands):
            self.on_commands[slot] = on_command
            self.off_commands[slot] = off_command
        else:
            raise IndexError(f"槽位 {slot} 超出范围 (0~{len(self.on_commands)-1})")

    def on_button_pressed(self, slot: int):
        """按下第 slot 个槽位的"开"按钮"""
        print(f"\n  [按下] 槽位 {slot} 的开按钮:")
        self.on_commands[slot].execute()
        self._undo_command = self.on_commands[slot]  # 记录最后执行的命令

    def off_button_pressed(self, slot: int):
        """按下第 slot 个槽位的"关"按钮"""
        print(f"\n  [按下] 槽位 {slot} 的关按钮:")
        self.off_commands[slot].execute()
        self._undo_command = self.off_commands[slot]  # 记录最后执行的命令

    def undo_button_pressed(self):
        """按下"撤销"按钮——撤销上一步操作"""
        print("\n  [撤销] 按下撤销按钮:")
        self._undo_command.undo()

    def __str__(self):
        """显示遥控器当前的按钮配置"""
        lines = []
        lines.append("\n" + "=" * 50)
        lines.append("🎮 遥控器配置")
        lines.append("=" * 50)
        for i in range(len(self.on_commands)):
            on_cmd = self.on_commands[i].__class__.__name__
            off_cmd = self.off_commands[i].__class__.__name__
            lines.append(f"  [槽位 {i}] 开: {on_cmd:20s}  关: {off_cmd}")
        lines.append(f"  [撤销] 上次操作: {self._undo_command.__class__.__name__}")
        lines.append("=" * 50)
        return "\n".join(lines)


# ============================================================================
# 进阶：宏命令（Macro Command）
# ============================================================================

class MacroCommand(Command):
    """
    宏命令——组合多个命令，一次执行

    用途：
      - "一键派对模式"：开灯 + 开风扇 + 开音响
      - "一键离家模式"：关灯 + 关风扇 + 关音响
      - 任何需要组合多个操作的场景

    💡 宏命令本身也是一个 Command！
      这意味着宏命令可以嵌套、可以放在命令队列中、
      可以和普通命令一样支持撤销。
    """

    def __init__(self, commands: List[Command], name: str = "宏命令"):
        self.commands = commands
        self.name = name

    def execute(self):
        """依次执行所有子命令"""
        print(f"\n  🎯 执行宏命令 [{self.name}]:")
        for cmd in self.commands:
            cmd.execute()

    def undo(self):
        """
        撤销宏命令——按相反顺序撤销每个子命令

        为什么要相反顺序？
          如果顺序执行：开灯→开风扇→开音响
          撤销时应该：关音响→关风扇→关灯
          就像脱衣服：先穿上的最后脱。
        """
        print(f"\n  ↩️  撤销宏命令 [{self.name}]:")
        for cmd in reversed(self.commands):
            cmd.undo()


# ============================================================================
# 🧪 测试
# ============================================================================

def test_command():
    print("\n" + "=" * 50)
    print("🎮 命令模式 演示")
    print("=" * 50)

    # 1. 创建接收者（家电）
    living_room_light = Light("客厅灯")
    kitchen_light = Light("厨房灯")
    fan = Fan("卧室风扇")
    stereo = Stereo("客厅音响")

    # 2. 创建命令
    lr_light_on = LightOnCommand(living_room_light)
    lr_light_off = LightOffCommand(living_room_light)
    k_light_on = LightOnCommand(kitchen_light)
    k_light_off = LightOffCommand(kitchen_light)
    fan_on = FanOnCommand(fan)
    fan_off = FanOffCommand(fan)
    stereo_on = StereoOnCommand(stereo)
    stereo_off = StereoOffCommand(stereo)

    # 3. 设置遥控器
    remote = RemoteControl(5)
    remote.set_command(0, lr_light_on, lr_light_off)
    remote.set_command(1, k_light_on, k_light_off)
    remote.set_command(2, fan_on, fan_off)
    remote.set_command(3, stereo_on, stereo_off)

    print(remote)

    # 4. 测试基本操作
    print("\n--- 基本操作 ---")
    remote.on_button_pressed(0)   # 开客厅灯
    remote.on_button_pressed(2)   # 开风扇
    remote.on_button_pressed(3)   # 开音响

    # 5. 测试撤销
    print("\n--- 撤销测试 ---")
    remote.undo_button_pressed()  # 撤销：关音响
    remote.undo_button_pressed()  # 撤销：关风扇

    # 6. 测试宏命令
    print("\n\n--- 宏命令测试 ---")

    party_on = MacroCommand(
        [lr_light_on, fan_on, stereo_on],
        name="派对模式"
    )
    party_off = MacroCommand(
        [lr_light_off, fan_off, stereo_off],
        name="派对结束"
    )

    remote.set_command(4, party_on, party_off)

    print("\n🎉 一键派对模式:")
    remote.on_button_pressed(4)

    print("\n\n🚪 一键结束派对:")
    remote.off_button_pressed(4)

    # 7. 验证开闭原则
    print("\n\n--- 开闭原则验证 ---")
    print("  新增家电（如空调）只需要:")
    print("    1. 创建 AirConditioner 类 ✅")
    print("    2. 创建 ACOnCommand / ACOffCommand ✅")
    print("    3. remote.set_command(5, ac_on, ac_off) ✅")
    print("  不需要修改 RemoteControl 任何代码！")


if __name__ == "__main__":
    test_command()


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 命令模式和策略模式的区别？
    命令模式：
      - 把"一个请求/操作"封装成对象
      - 关注的是"执行什么操作"和"如何撤销"
      - 用途：解耦调用者和执行者、支持撤销/重做

    策略模式：
      - 把"一组算法"封装成对象
      - 关注的是"如何完成一个任务"
      - 用途：运行时切换算法

    口诀：命令 = 操作封装（点餐），策略 = 算法封装（怎么去做）

Q2: 如何实现撤销重做（Undo/Redo）？
    撤销：
      - 每个命令保存执行前的状态（_prev_state）
      - Invoker 维护一个"历史命令栈"
      - undo() 恢复之前的状态

    重做：
      - 再维护一个"重做栈"
      - 撤销时把命令从历史栈移到重做栈
      - 重做时从重做栈取出重新 execute()

    注意：要深拷贝状态，否则引用会导致状态共享问题。

Q3: 命令模式在 GUI 中的应用？
    - 菜单项点击：每个菜单项对应一个 Command
    - 工具栏按钮：每个按钮对应一个 Command
    - 快捷键：每个快捷键对应一个 Command
    - 操作历史（Undo/Redo）：维护命令栈
    - 宏录制：把用户操作记录为命令序列

    Qt 的 QAction、Swing 的 Action 接口都是命令模式的体现。

Q4: 命令模式和回调函数（Callback）的关系？
    命令模式本质上是"面向对象版本的回调函数"。
    - 回调函数：函数指针 / lambda / 闭包
    - 命令对象：封装了操作的对象
    
    命令对象的优势：
      - 可以保存状态（支持撤销）
      - 可以有多个方法（execute + undo）
      - 可以通过继承扩展（宏命令）

Q5: 命令模式的缺点？
    - 类数量爆炸：每个操作都要创建一个命令类
    - 代码量增加：简单的操作也要包装成命令
    
    缓解方式：
      - 使用 lambda/函数对象（Python/C++11）
      - 使用函数式编程风格的命令

Q6: 什么是"日志命令"（Logging Command）？
    除了执行操作，命令还保存自己的"快照"。
    可以序列化到文件，在程序崩溃后重新执行。
    这就是"事务日志"的基本原理。

    应用场景：
      - 数据库事务日志
      - 文件系统操作日志
      - 游戏操作回放

💡 面试官变种题：实现一个"可配置的遥控器"。
    用户可以通过配置文件（JSON/YAML）来配置按钮功能。
    思路：用"命令注册表"根据字符串创建对应的命令对象。
"""
