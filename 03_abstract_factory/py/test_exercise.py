"""
================================================================================
Lesson 3: Abstract Factory — 抽象工厂模式（测试）
================================================================================
"""

import pytest
from exercise import (
    Button,
    Input,
    ThemeFactory,
    DarkThemeFactory,
    LightThemeFactory,
    DarkButton,
    DarkInput,
    LightButton,
    LightInput,
    HighContrastButton,
    HighContrastInput,
    HighContrastThemeFactory,
    Application,
)


class TestAbstractFactoryExercise:
    """测试抽象工厂练习题"""

    # ========================================================================
    # 题目 1：基础测试 — Dark/Light 主题工厂
    # ========================================================================

    def test_dark_theme_factory_creates_correct_products(self):
        """测试深色主题工厂创建正确的产品类型"""
        factory = DarkThemeFactory()
        button = factory.create_button()
        input_box = factory.create_input()

        assert isinstance(button, DarkButton), "DarkThemeFactory 应创建 DarkButton"
        assert isinstance(input_box, DarkInput), "DarkThemeFactory 应创建 DarkInput"
        assert isinstance(button, Button), "DarkButton 应继承 Button"
        assert isinstance(input_box, Input), "DarkInput 应继承 Input"

    def test_light_theme_factory_creates_correct_products(self):
        """测试浅色主题工厂创建正确的产品类型"""
        factory = LightThemeFactory()
        button = factory.create_button()
        input_box = factory.create_input()

        assert isinstance(button, LightButton), "LightThemeFactory 应创建 LightButton"
        assert isinstance(input_box, LightInput), "LightThemeFactory 应创建 LightInput"
        assert isinstance(button, Button), "LightButton 应继承 Button"
        assert isinstance(input_box, Input), "LightInput 应继承 Input"

    def test_dark_components_render_correctly(self):
        """测试深色组件 render() 输出正确的描述"""
        button = DarkButton()
        input_box = DarkInput()

        assert "深色" in button.render() or "Dark" in button.render(), \
            "DarkButton.render() 应包含主题描述"
        assert "深色" in input_box.render() or "Dark" in input_box.render(), \
            "DarkInput.render() 应包含主题描述"

    def test_light_components_render_correctly(self):
        """测试浅色组件 render() 输出正确的描述"""
        button = LightButton()
        input_box = LightInput()

        assert "浅色" in button.render() or "Light" in button.render(), \
            "LightButton.render() 应包含主题描述"
        assert "浅色" in input_box.render() or "Light" in input_box.render(), \
            "LightInput.render() 应包含主题描述"

    # ========================================================================
    # 题目 2：综合测试 — HighContrast 主题族
    # ========================================================================

    def test_high_contrast_theme_factory_exists(self):
        """测试 HighContrast 主题族已正确实现"""
        factory = HighContrastThemeFactory()
        button = factory.create_button()
        input_box = factory.create_input()

        assert isinstance(button, HighContrastButton), \
            "HighContrastThemeFactory 应创建 HighContrastButton"
        assert isinstance(input_box, HighContrastInput), \
            "HighContrastThemeFactory 应创建 HighContrastInput"
        assert isinstance(button, Button), "HighContrastButton 应继承 Button"
        assert isinstance(input_box, Input), "HighContrastInput 应继承 Input"

    def test_high_contrast_render(self):
        """测试 HighContrast 组件的 render() 输出"""
        button = HighContrastButton()
        input_box = HighContrastInput()

        render_result = button.render()
        assert isinstance(render_result, str) and len(render_result) > 0, \
            "HighContrastButton.render() 应返回非空字符串"

        render_result = input_box.render()
        assert isinstance(render_result, str) and len(render_result) > 0, \
            "HighContrastInput.render() 应返回非空字符串"

    # ========================================================================
    # 题目 3：拓展测试 — Application 工厂注入与主题切换
    # ========================================================================

    def test_application_creates_ui_with_factory(self):
        """测试 Application 通过工厂注入创建 UI"""
        factory = DarkThemeFactory()
        app = Application(factory)
        app.create_ui()
        render_result = app.render()

        assert isinstance(render_result, str), "render() 应返回字符串"
        assert len(render_result) > 0, "render() 不应为空"

    def test_application_switch_theme(self):
        """测试 Application 运行时切换主题"""
        dark_factory = DarkThemeFactory()
        light_factory = LightThemeFactory()

        app = Application(dark_factory)
        app.create_ui()
        dark_render = app.render()

        app.switch_theme(light_factory)
        light_render = app.render()

        # 切换主题后渲染结果应不同
        assert dark_render != light_render, \
            "切换主题后 render() 输出应不同"

    def test_application_with_all_themes(self):
        """测试 Application 使用所有主题都能正常工作"""
        factories = [
            DarkThemeFactory(),
            LightThemeFactory(),
            HighContrastThemeFactory(),
        ]

        for factory in factories:
            app = Application(factory)
            app.create_ui()
            result = app.render()
            assert isinstance(result, str) and len(result) > 0, \
                f"{factory.__class__.__name__} 的 render() 输出无效"
