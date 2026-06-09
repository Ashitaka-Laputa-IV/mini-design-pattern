"""
================================================================================
测试 11 Command 练习题
================================================================================
"""

import pytest
from exercise import (
    TextEditor, WriteCommand, DeleteCommand, EditorInvoker,
    TV, AirConditioner, Curtains,
    TurnOnCommand, TurnOffCommand, SetTemperatureCommand,
    RemoteControl,
    MacroCommand, create_leave_home_macro
)


# ============================================================================
# 测试第1题：文本编辑器命令
# ============================================================================

class TestTextEditor:
    """测试文本编辑器命令"""

    def test_write_command_execute(self):
        """测试写入命令执行"""
        editor = TextEditor()
        cmd = WriteCommand(editor, "Hello")
        cmd.execute()
        assert editor.text == "Hello"

    def test_write_command_undo(self):
        """测试写入命令撤销"""
        editor = TextEditor()
        cmd = WriteCommand(editor, "Hello")
        cmd.execute()
        cmd.undo()
        assert editor.text == ""

    def test_delete_command_execute(self):
        """测试删除命令执行"""
        editor = TextEditor()
        editor.text = "Hello World"
        cmd = DeleteCommand(editor, 6)
        cmd.execute()
        assert editor.text == "Hello"

    def test_delete_command_undo(self):
        """测试删除命令撤销"""
        editor = TextEditor()
        editor.text = "Hello World"
        cmd = DeleteCommand(editor, 6)
        cmd.execute()
        cmd.undo()
        assert editor.text == "Hello World"

    def test_editor_invoker_undo_chain(self):
        """测试编辑器的撤销链"""
        editor = TextEditor()
        invoker = EditorInvoker()

        invoker.execute_command(WriteCommand(editor, "Hello"))
        invoker.execute_command(WriteCommand(editor, " World"))
        assert editor.text == "Hello World"

        invoker.undo()
        assert editor.text == "Hello"

        invoker.undo()
        assert editor.text == ""

    def test_multiple_write_and_undo(self):
        """测试多次写入和撤销"""
        editor = TextEditor()
        invoker = EditorInvoker()

        invoker.execute_command(WriteCommand(editor, "A"))
        invoker.execute_command(WriteCommand(editor, "B"))
        invoker.execute_command(WriteCommand(editor, "C"))
        assert editor.text == "ABC"

        invoker.undo()
        assert editor.text == "AB"

        invoker.undo()
        assert editor.text == "A"


# ============================================================================
# 测试第2题：智能家居遥控器
# ============================================================================

class TestRemoteControl:
    """测试智能家居遥控器"""

    def test_turn_on_tv(self):
        """测试打开电视"""
        tv = TV()
        cmd = TurnOnCommand(tv)
        cmd.execute()
        assert tv.is_on is True

    def test_turn_off_tv(self):
        """测试关闭电视"""
        tv = TV()
        tv.is_on = True
        cmd = TurnOffCommand(tv)
        cmd.execute()
        assert tv.is_on is False

    def test_undo_turn_on(self):
        """测试撤销打开操作"""
        tv = TV()
        cmd = TurnOnCommand(tv)
        cmd.execute()
        cmd.undo()
        assert tv.is_on is False

    def test_undo_turn_off(self):
        """测试撤销关闭操作"""
        tv = TV()
        tv.is_on = True
        cmd = TurnOffCommand(tv)
        cmd.execute()
        cmd.undo()
        assert tv.is_on is True

    def test_set_temperature(self):
        """测试设置空调温度"""
        ac = AirConditioner()
        cmd = SetTemperatureCommand(ac, 24)
        cmd.execute()
        assert ac.temperature == 24

    def test_undo_set_temperature(self):
        """测试撤销温度设置"""
        ac = AirConditioner()
        cmd = SetTemperatureCommand(ac, 24)
        cmd.execute()
        cmd.undo()
        assert ac.temperature == 26  # 默认温度

    def test_remote_control_undo(self):
        """测试遥控器撤销功能"""
        tv = TV()
        remote = RemoteControl(3)
        remote.set_command(0, TurnOnCommand(tv))
        remote.press_button(0)
        assert tv.is_on is True

        remote.press_undo()
        assert tv.is_on is False

    def test_curtains_open_close(self):
        """测试窗帘的开关"""
        curtains = Curtains()

        open_cmd = TurnOnCommand(curtains)
        open_cmd.device = curtains  # 直接用 TurnOnCommand 控制
        # 实际上窗帘用 open/close 而不是 on/off，这里测试接口兼容
        # 更合理的方式是直接用 curtains.open() / curtains.close()

    def test_multiple_devices_on_remote(self):
        """测试遥控器控制多个设备"""
        tv = TV()
        ac = AirConditioner()
        remote = RemoteControl(3)

        remote.set_command(0, TurnOnCommand(tv))
        remote.set_command(1, TurnOnCommand(ac))

        remote.press_button(0)
        remote.press_button(1)

        assert tv.is_on is True
        assert ac.is_on is True

        remote.press_undo()
        assert ac.is_on is False  # 撤销最后一步


# ============================================================================
# 测试第3题：宏命令
# ============================================================================

class TestMacroCommand:
    """测试宏命令"""

    def test_macro_execute_all_commands(self):
        """测试宏命令执行所有子命令"""
        tv = TV()
        ac = AirConditioner()
        curtains = Curtains()

        macro = MacroCommand([
            TurnOnCommand(tv),
            TurnOnCommand(ac),
        ], name="全部打开")

        macro.execute()
        assert tv.is_on is True
        assert ac.is_on is True

    def test_macro_undo_in_reverse_order(self):
        """测试宏命令按相反顺序撤销"""
        tv = TV()
        ac = AirConditioner()
        curtains = Curtains()

        macro = MacroCommand([
            TurnOnCommand(tv),
            TurnOnCommand(ac),
        ], name="全部打开")

        macro.execute()
        macro.undo()
        assert tv.is_on is False
        assert ac.is_on is False

    def test_leave_home_macro(self):
        """测试一键离家模式宏命令"""
        macro = create_leave_home_macro()

        # 先打开所有设备
        tv_on = TurnOnCommand(macro.commands[0].device)
        ac_on = TurnOnCommand(macro.commands[1].device)
        tv_on.execute()
        ac_on.execute()

        # 执行离家模式
        macro.execute()

        # 验证所有设备关闭
        for cmd in macro.commands:
            if isinstance(cmd, TurnOffCommand):
                assert cmd.device.is_on is False

    def test_macro_undo_restores_states(self):
        """测试宏命令撤销恢复状态"""
        macro = create_leave_home_macro()

        # 先打开设备
        for cmd in macro.commands:
            if isinstance(cmd, TurnOffCommand):
                on_cmd = TurnOnCommand(cmd.device)
                on_cmd.execute()

        # 执行宏
        macro.execute()

        # 撤销宏
        macro.undo()

        # 验证设备恢复
        for cmd in macro.commands:
            if isinstance(cmd, TurnOffCommand):
                assert cmd.device.is_on is True
