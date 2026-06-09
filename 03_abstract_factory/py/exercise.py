"""
================================================================================
Lesson 3: Abstract Factory — 抽象工厂模式（练习题）
================================================================================
"""

from abc import ABC, abstractmethod


# ============================================================================
# 题目 1：实现 Theme 抽象工厂（基础）
# ============================================================================
# 请实现一组 Theme 抽象工厂，分别创建 Dark 和 Light 主题的 UI 组件。
# - DarkButton/DarkInput: 深色主题组件
# - LightButton/LightInput: 浅色主题组件
# - 每个组件都有 render() 方法，返回描述字符串
# ============================================================================

class Button(ABC):
    """按钮抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass


class Input(ABC):
    """输入框抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass


# ---- 请在下方实现 DarkButton 和 DarkInput ----


# ---- 请在下方实现 LightButton 和 LightInput ----


class ThemeFactory(ABC):
    """抽象工厂：定义创建一组主题组件的接口"""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_input(self) -> Input:
        pass


class DarkThemeFactory(ThemeFactory):
    """深色主题工厂"""
    # TODO: 实现 create_button() 和 create_input()，返回对应的深色组件


class LightThemeFactory(ThemeFactory):
    """浅色主题工厂"""
    # TODO: 实现 create_button() 和 create_input()，返回对应的浅色组件


# ============================================================================
# 题目 2：新增 HighContrast 主题族（综合）
# ============================================================================
# 请新增 HighContrast 主题族，包含 HighContrastButton 和 HighContrastInput，
# 以及对应的 HighContrastThemeFactory。
# ============================================================================

# TODO: 实现 HighContrastButton（render() 返回 "渲染 [高对比度按钮] — 亮黄色背景、黑色文字"）
# TODO: 实现 HighContrastInput（render() 返回 "渲染 [高对比度输入框] — 黑色背景、黄色文字、粗边框"）
# TODO: 实现 HighContrastThemeFactory


# ============================================================================
# 题目 3：Application 类（拓展）
# ============================================================================
# 实现 Application 类，通过抽象工厂配置界面，支持跨主题切换。
# Application 接收一个 ThemeFactory，创建一组组件，并提供 render() 方法。
# 同时实现 switch_theme() 方法，允许运行时切换主题。
# ============================================================================

class Application:
    """应用程序，通过抽象工厂配置界面"""

    def __init__(self, factory: ThemeFactory):
        # TODO: 初始化工厂和组件
        pass

    def create_ui(self):
        """创建 UI 组件"""
        # TODO: 使用工厂创建 button 和 input
        pass

    def render(self) -> str:
        """渲染所有组件，返回描述字符串"""
        # TODO: 调用各组件的 render() 并拼接结果
        pass

    def switch_theme(self, factory: ThemeFactory):
        """切换主题"""
        # TODO: 替换工厂并重新创建 UI
        pass
