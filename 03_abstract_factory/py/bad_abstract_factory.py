"""
================================================================================
 Lesson 3: Abstract Factory — 抽象工厂模式 [创建型]
================================================================================
 📖 本课采用"反模式驱动"方式：
    先展示坏的代码，分析问题，再引入设计模式。

 🔑 面试频率：★★★★☆
================================================================================
"""

"""
===============================================================================
 🎬 场景：你和同事在做一个"跨平台 GUI 库"

 需求：
   需要支持三种平台的 GUI 风格：
     - Windows: 圆角按钮、边框输入框、下拉菜单
     - Mac: 毛玻璃按钮、搜索框、顶部菜单
     - Linux: 扁平按钮、简洁输入框、传统菜单

 每种平台都有三种组件：Button(按钮)、Input(输入框)、Menu(菜单)

 你的同事把不同平台的组件创建代码混在一起，用 if-else 判断平台类型。

 😕 问题来了：
   1. 所有平台的创建逻辑都耦合在一起
   2. 添加新平台（比如 Android）需要改很多文件
   3. 如果不小心混用了不同平台的组件（比如 Windows 的按钮 + Mac 的菜单），
      程序界面会变得很奇怪
   4. 产品之间存在"约束"——同一平台的产品必须一起使用

 请你先停在这里想一想：
    1. "产品族"这个概念——为什么 Windows 按钮和 Mac 菜单不能混用？
    2. 怎么保证"同一平台的产品"总是一起被创建？
    3. 有没有一种方式，让客户端代码完全不知道具体平台？

 🧠 思考 10 秒钟...
   .
   .
   .
   .
   .
   .
   .
   .
   想好了吗？往下翻看反例代码 👇
===============================================================================
"""

from abc import ABC, abstractmethod


# ============================================================================
# 先定义产品接口（各种 GUI 组件）
# ============================================================================

class Button(ABC):
    """按钮抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> str:
        pass


class Input(ABC):
    """输入框抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def get_value(self) -> str:
        pass


class Menu(ABC):
    """菜单抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def select_item(self, index: int) -> str:
        pass


# ============================================================================
# 各种平台的组件实现
# ============================================================================

# ---------- Windows 风格 ----------

class WindowsButton(Button):
    def render(self) -> str:
        return "渲染 [Windows 按钮] — 圆角、蓝色背景"

    def on_click(self) -> str:
        return "Windows 按钮被点击"


class WindowsInput(Input):
    def render(self) -> str:
        return "渲染 [Windows 输入框] — 带边框、白色背景"

    def get_value(self) -> str:
        return "Windows 输入框的内容"


class WindowsMenu(Menu):
    def render(self) -> str:
        return "渲染 [Windows 菜单] — 下拉式、带图标"

    def select_item(self, index: int) -> str:
        return f"Windows 菜单选中第 {index} 项"


# ---------- Mac 风格 ----------

class MacButton(Button):
    def render(self) -> str:
        return "渲染 [Mac 按钮] — 毛玻璃效果、圆润"

    def on_click(self) -> str:
        return "Mac 按钮被点击"


class MacInput(Input):
    def render(self) -> str:
        return "渲染 [Mac 输入框] — 搜索框风格、无边框"

    def get_value(self) -> str:
        return "Mac 输入框的内容"


class MacMenu(Menu):
    def render(self) -> str:
        return "渲染 [Mac 菜单] — 顶部菜单栏、全局"

    def select_item(self, index: int) -> str:
        return f"Mac 菜单选中第 {index} 项"


# ---------- Linux 风格 ----------

class LinuxButton(Button):
    def render(self) -> str:
        return "渲染 [Linux 按钮] — 扁平、极简风格"

    def on_click(self) -> str:
        return "Linux 按钮被点击"


class LinuxInput(Input):
    def render(self) -> str:
        return "渲染 [Linux 输入框] — 简洁、灰色边框"

    def get_value(self) -> str:
        return "Linux 输入框的内容"


class LinuxMenu(Menu):
    def render(self) -> str:
        return "渲染 [Linux 菜单] — 传统下拉、右键菜单"

    def select_item(self, index: int) -> str:
        return f"Linux 菜单选中第 {index} 项"


# ============================================================================
# ❌ 反模式：用 if-else 创建整个产品族
# ============================================================================

class GUIFactory:
    """
    ❌ 坏味道：一个工厂类用 if-else 创建所有平台的所有组件

    问题分析：
      1. 所有平台的创建逻辑都堆在一个类里
      2. 每次新增平台，需要改 3 个方法（create_button, create_input, create_menu）
      3. 每次新增组件类型，需要改所有平台的创建逻辑
      4. 如果某个平台的某个组件需要特殊配置，这个方法签名会变得很复杂
      5. 违反单一职责原则——这个类同时负责多个平台的创建
      6. 违反开闭原则——扩展新平台需要修改已有代码
    """

    def __init__(self, platform: str):
        self._platform = platform

    def create_button(self) -> Button:
        """⚠ 每次加新平台都要加一个 elif"""
        if self._platform == "windows":
            return WindowsButton()
        elif self._platform == "mac":
            return MacButton()
        elif self._platform == "linux":
            return LinuxButton()
        else:
            raise ValueError(f"不支持的平台: {self._platform}")

    def create_input(self) -> Input:
        """⚠ 同样的问题：每个方法都要判断一次"""
        if self._platform == "windows":
            return WindowsInput()
        elif self._platform == "mac":
            return MacInput()
        elif self._platform == "linux":
            return LinuxInput()
        else:
            raise ValueError(f"不支持的平台: {self._platform}")

    def create_menu(self) -> Menu:
        """⚠ 三个方法都有 if-else，代码重复"""
        if self._platform == "windows":
            return WindowsMenu()
        elif self._platform == "mac":
            return MacMenu()
        elif self._platform == "linux":
            return LinuxMenu()
        else:
            raise ValueError(f"不支持的平台: {self._platform}")


# ============================================================================
# 测试反模式
# ============================================================================

def test_bad_abstract_factory():
    print("=" * 60)
    print("❌ 反模式：if-else 创建产品族")
    print("=" * 60)

    platforms = ["windows", "mac", "linux"]

    for platform in platforms:
        print(f"\n--- 创建 {platform.upper()} 平台的组件 ---")
        factory = GUIFactory(platform)

        button = factory.create_button()
        input_box = factory.create_input()
        menu = factory.create_menu()

        print(f"  {button.render()}")
        print(f"  {input_box.render()}")
        print(f"  {menu.render()}")

    print()
    print("⚠  问题总结：")
    print("   1. 添加新平台（如 Android）要改 3 个方法")
    print("   2. 添加新组件（如 Checkbox）要改所有平台的创建逻辑")
    print("   3. 所有平台耦合在一起，代码难以维护")
    print("   4. 没有约束保证同一平台的组件被一起使用")


if __name__ == "__main__":
    test_bad_abstract_factory()
