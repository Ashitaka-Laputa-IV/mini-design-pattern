"""
================================================================================
练习题 11: Command — 命令模式
================================================================================
📐 命令模式(Command)将"请求"封装成对象，以便使用不同的请求、
   队列或者日志来参数化其他对象。命令模式也支持可撤销的操作。

💡 本练习包含 3 道题：
   第1题（基础）: 实现文本编辑器的撤销命令
   第2题（综合）: 实现智能家居遥控器
   第3题（拓展）: 实现宏命令（一键离家模式）
================================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ============================================================================
# 第1题（基础）: 文本编辑器命令
# ============================================================================
#
# 实现一个简单的文本编辑器，支持写入、删除和撤销操作。
#
# 要求：
#   1. TextEditor 有 text 属性保存当前文本内容
#   2. write(text) 方法：在末尾追加文本
#   3. delete(n) 方法：删除末尾 n 个字符
#   4. undo() 方法：撤销上一次操作
#   5. WriteCommand 和 DeleteCommand 分别封装写入和删除操作
#   6. 每次执行命令后，命令被压入历史栈，undo 时弹出并撤销

class Command(ABC):
    """命令接口"""

    @abstractmethod
    def execute(self):
        """执行命令"""
        pass

    @abstractmethod
    def undo(self):
        """撤销命令"""
        pass


class TextEditor:
    """文本编辑器（接收者）"""

    def __init__(self):
        self.text = ""

    def write(self, text: str):
        """在末尾写入文本"""
        self.text += text

    def delete(self, n: int):
        """删除末尾 n 个字符"""
        if n > 0 and len(self.text) >= n:
            self.text = self.text[:-n]


class WriteCommand(Command):
    """写入命令"""

    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self):
        """执行写入"""
        # TODO: 调用 editor.write(self.text)

    def undo(self):
        """撤销写入：删除刚写入的文本"""
        # TODO: 调用 editor.delete(len(self.text))


class DeleteCommand(Command):
    """删除命令"""

    def __init__(self, editor: TextEditor, n: int):
        self.editor = editor
        self.n = n
        self._deleted_text = ""  # 保存被删除的文本，用于撤销

    def execute(self):
        """执行删除，并保存被删除的内容"""
        # TODO: 先保存被删除的文本到 self._deleted_text
        #       然后调用 editor.delete(self.n)

    def undo(self):
        """撤销删除：恢复被删除的文本"""
        # TODO: 调用 editor.write(self._deleted_text)


class EditorInvoker:
    """编辑器调用者（Invoker），管理命令历史"""

    def __init__(self):
        self._history: List[Command] = []

    def execute_command(self, command: Command):
        """执行命令并记录到历史"""
        # TODO: 执行命令，然后压入 _history 栈
        pass

    def undo(self):
        """撤销上一次操作"""
        if self._history:
            # TODO: 弹出最后一条命令并调用它的 undo()
            pass


# ============================================================================
# 第2题（综合）: 智能家居遥控器
# ============================================================================
#
# 实现一个智能家居遥控器，支持多种设备和撤销。
#
# 设备：TV（电视）、AirConditioner（空调）、Curtains（窗帘）
# 命令：TurnOnCommand、TurnOffCommand、SetTemperatureCommand
# 遥控器：支持多按钮槽位和撤销
#
# 要求：
#   1. 每个设备有独立的开关和状态
#   2. TurnOnCommand/TurnOffCommand 控制设备的开关
#   3. SetTemperatureCommand 设置空调温度
#   4. RemoteControl 有多个槽位，每个槽位可设置命令
#   5. 支持撤销（undo）上一次操作

# ---- 设备（接收者） ----

class TV:
    """电视"""

    def __init__(self):
        self.is_on = False

    def on(self):
        self.is_on = True

    def off(self):
        self.is_on = False


class AirConditioner:
    """空调"""

    def __init__(self):
        self.is_on = False
        self.temperature: int = 26  # 默认 26 度

    def on(self):
        self.is_on = True

    def off(self):
        self.is_on = False

    def set_temperature(self, temp: int):
        """设置温度"""
        self.temperature = temp


class Curtains:
    """窗帘"""

    def __init__(self):
        self.is_open = False

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False


# ---- 命令 ----

class TurnOnCommand(Command):
    """打开设备命令"""

    def __init__(self, device):
        self.device = device
        self._prev_state = False

    def execute(self):
        # TODO: 保存设备状态到 _prev_state，然后调用 device.on()
        pass

    def undo(self):
        # TODO: 根据 _prev_state 恢复设备状态
        # 如果之前是关的，调用 device.off()
        # 如果之前是开的，调用 device.on()
        pass


class TurnOffCommand(Command):
    """关闭设备命令"""

    def __init__(self, device):
        self.device = device
        self._prev_state = False

    def execute(self):
        # TODO: 保存设备状态到 _prev_state，然后调用 device.off()
        pass

    def undo(self):
        # TODO: 根据 _prev_state 恢复设备状态
        pass


class SetTemperatureCommand(Command):
    """设置空调温度命令"""

    def __init__(self, ac: AirConditioner, temperature: int):
        self.ac = ac
        self.temperature = temperature
        self._prev_temp = 26

    def execute(self):
        # TODO: 保存当前温度到 _prev_temp，然后设置新温度

    def undo(self):
        # TODO: 恢复到之前的温度


class NoCommand(Command):
    """空命令（Null Object 模式）"""

    def execute(self):
        pass

    def undo(self):
        pass


# ---- 遥控器（Invoker） ----

class RemoteControl:
    """智能家居遥控器"""

    def __init__(self, slots: int = 5):
        self._commands: List[Command] = [NoCommand()] * slots
        self._undo_command: Command = NoCommand()

    def set_command(self, slot: int, command: Command):
        """设置指定槽位的命令"""
        # TODO: 将 command 设置到指定槽位

    def press_button(self, slot: int):
        """按下指定槽位的按钮"""
        # TODO: 执行命令并记录到 _undo_command

    def press_undo(self):
        """按下撤销按钮"""
        # TODO: 调用 _undo_command.undo()


# ============================================================================
# 第3题（拓展）: 宏命令
# ============================================================================
#
# 实现宏命令 MacroCommand，可以组合多个命令一次执行/撤销。
# 并实现"一键离家模式"宏：关灯 + 关空调 + 关电视 + 拉窗帘
#
# 要求：
#   1. MacroCommand 实现 Command 接口（可嵌套！）
#   2. execute() 依次执行所有子命令
#   3. undo() 按相反顺序撤销所有子命令
#   4. 实现 create_leave_home_macro() 工厂函数，返回离家模式宏命令

class MacroCommand(Command):
    """宏命令：组合多个命令"""

    def __init__(self, commands: List[Command], name: str = "宏命令"):
        self.commands = commands
        self.name = name

    def execute(self):
        """依次执行所有子命令"""
        # TODO: 遍历 self.commands，执行每个命令

    def undo(self):
        """按相反顺序撤销所有子命令"""
        # TODO: 逆序遍历 self.commands，撤销每个命令


def create_leave_home_macro() -> MacroCommand:
    """
    创建"一键离家模式"宏命令
    顺序：关灯 → 关空调 → 关电视 → 拉窗帘
    """
    # TODO: 创建 TV, AirConditioner, Curtains 实例
    # TODO: 创建对应的 TurnOffCommand
    # TODO: 创建 CurtainsCloseCommand（需要额外实现）
    # TODO: 组合成 MacroCommand 返回
    pass
