"""
================================================================================
Lesson 8: Strategy (策略模式) — 练习测试
================================================================================
"""

import pytest
from exercise import (
    bubble_sort,
    quick_sort,
    python_sort,
    Sorter,
    NoDiscount,
    PercentageDiscount,
    FixedDiscount,
    BOGOFree,
    ShoppingCart,
    NotEmptyValidator,
    LengthValidator,
    EmailValidator,
    RegexValidator,
    Validator,
)


# ==============================================================================
# 第1题测试：排序策略
# ==============================================================================

class TestSortStrategies:
    """测试排序策略"""

    @pytest.fixture
    def unsorted_data(self):
        return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    def test_bubble_sort(self, unsorted_data):
        """测试冒泡排序"""
        result = bubble_sort(unsorted_data)
        assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        # 验证不修改原列表
        assert unsorted_data == [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    def test_quick_sort(self, unsorted_data):
        """测试快速排序"""
        result = quick_sort(unsorted_data)
        assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        assert unsorted_data == [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    def test_python_sort(self, unsorted_data):
        """测试 Python 内置排序"""
        result = python_sort(unsorted_data)
        assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        assert unsorted_data == [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    def test_empty_list_sort(self):
        """测试空列表排序"""
        assert bubble_sort([]) == []
        assert quick_sort([]) == []
        assert python_sort([]) == []

    def test_single_element(self):
        """测试单元素列表排序"""
        assert bubble_sort([42]) == [42]
        assert quick_sort([42]) == [42]
        assert python_sort([42]) == [42]

    def test_sorter_with_bubble_sort(self):
        """测试 Sorter 使用冒泡排序策略"""
        sorter = Sorter(bubble_sort)
        assert sorter.sort([3, 1, 2]) == [1, 2, 3]

    def test_sorter_switch_strategy(self):
        """测试 Sorter 运行时切换策略"""
        sorter = Sorter(bubble_sort)
        assert sorter.sort([3, 1, 2]) == [1, 2, 3]
        sorter.set_strategy(python_sort)
        assert sorter.sort([3, 1, 2]) == [1, 2, 3]

    def test_all_strategies_same_result(self):
        """测试所有排序策略对相同输入结果一致"""
        data = [9, 7, 5, 3, 1, 8, 6, 4, 2, 0]
        expected = sorted(data)
        assert bubble_sort(data) == expected
        assert quick_sort(data) == expected
        assert python_sort(data) == expected

    def test_duplicate_values(self):
        """测试重复值排序"""
        data = [5, 5, 5, 3, 3, 1]
        expected = [1, 3, 3, 5, 5, 5]
        assert bubble_sort(data) == expected
        assert quick_sort(data) == expected


# ==============================================================================
# 第2题测试：促销策略
# ==============================================================================

class TestDiscountStrategies:
    """测试折扣策略"""

    def test_no_discount(self):
        """测试无折扣"""
        cart = ShoppingCart(NoDiscount())
        cart.add_item("苹果", 30.0)
        cart.add_item("牛奶", 20.0)
        result = cart.checkout()
        assert result["original_total"] == 50.0
        assert result["final_price"] == 50.0
        assert "无折扣" in result["discount"]

    def test_percentage_discount(self):
        """测试百分比折扣"""
        cart = ShoppingCart(PercentageDiscount(10))
        cart.add_item("商品", 200.0)
        result = cart.checkout()
        assert result["final_price"] == 180.0  # 200 * 0.9

    def test_percentage_discount_full(self):
        """测试 100% 折扣（免费）"""
        cart = ShoppingCart(PercentageDiscount(100))
        cart.add_item("免费商品", 100.0)
        result = cart.checkout()
        assert result["final_price"] == 0.0

    def test_fixed_discount(self):
        """测试固定金额折扣"""
        cart = ShoppingCart(FixedDiscount(50))
        cart.add_item("商品", 200.0)
        result = cart.checkout()
        assert result["final_price"] == 150.0

    def test_fixed_discount_not_below_zero(self):
        """测试固定折扣不低于 0"""
        cart = ShoppingCart(FixedDiscount(100))
        cart.add_item("便宜商品", 30.0)
        result = cart.checkout()
        assert result["final_price"] == 0.0

    def test_bogo_free_qualifies(self):
        """测试买一送一（满足条件）"""
        cart = ShoppingCart(BOGOFree())
        cart.add_item("商品A", 60.0)
        cart.add_item("商品B", 60.0)
        result = cart.checkout()
        assert result["final_price"] == 60.0  # 120 * 0.5

    def test_bogo_free_not_qualify(self):
        """测试买一送一（不满足条件）"""
        cart = ShoppingCart(BOGOFree())
        cart.add_item("商品", 50.0)
        result = cart.checkout()
        assert result["final_price"] == 50.0  # 不满足条件，不打折

    def test_switch_strategy_at_runtime(self):
        """测试运行时切换折扣策略"""
        cart = ShoppingCart(NoDiscount())
        cart.add_item("商品", 200.0)
        assert cart.checkout()["final_price"] == 200.0

        cart.set_strategy(PercentageDiscount(20))
        assert cart.checkout()["final_price"] == 160.0

        cart.set_strategy(FixedDiscount(50))
        assert cart.checkout()["final_price"] == 150.0

    def test_multiple_items(self):
        """测试多个商品的折扣计算"""
        cart = ShoppingCart(PercentageDiscount(15))
        cart.add_item("苹果", 10.0)
        cart.add_item("香蕉", 5.0)
        cart.add_item("樱桃", 25.0)
        result = cart.checkout()
        assert result["original_total"] == 40.0
        assert result["final_price"] == 34.0  # 40 * 0.85


# ==============================================================================
# 第3题测试：验证策略链
# ==============================================================================

class TestValidationChain:
    """测试验证策略链"""

    def test_not_empty_valid(self):
        """测试非空验证通过"""
        validator = Validator([NotEmptyValidator()])
        result = validator.validate("hello")
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0

    def test_not_empty_invalid(self):
        """测试非空验证不通过"""
        validator = Validator([NotEmptyValidator()])
        result = validator.validate("")
        assert result["is_valid"] is False
        assert "不能为空" in result["errors"][0]

    def test_not_empty_whitespace(self):
        """测试纯空白字符串"""
        validator = Validator([NotEmptyValidator()])
        result = validator.validate("   ")
        assert result["is_valid"] is False

    def test_length_validator(self):
        """测试长度验证"""
        validator = Validator([LengthValidator(min_len=3, max_len=10)])
        assert validator.validate("abc")["is_valid"] is True
        assert validator.validate("abcdefghij")["is_valid"] is True
        assert validator.validate("ab")["is_valid"] is False
        assert validator.validate("abcdefghijk")["is_valid"] is False

    def test_length_no_min(self):
        """测试仅设最大长度的验证"""
        validator = Validator([LengthValidator(max_len=5)])
        assert validator.validate("")["is_valid"] is True
        assert validator.validate("abc")["is_valid"] is True
        assert validator.validate("abcdef")["is_valid"] is False

    def test_length_no_max(self):
        """测试仅设最小长度的验证"""
        validator = Validator([LengthValidator(min_len=3)])
        assert validator.validate("abc")["is_valid"] is True
        assert validator.validate("a" * 100)["is_valid"] is True
        assert validator.validate("ab")["is_valid"] is False

    def test_email_validator(self):
        """测试邮箱验证"""
        validator = Validator([EmailValidator()])
        assert validator.validate("user@example.com")["is_valid"] is True
        assert validator.validate("a@b")["is_valid"] is True
        assert validator.validate("")["is_valid"] is False
        assert validator.validate("noatsign")["is_valid"] is False
        assert validator.validate("@nouser")["is_valid"] is False
        assert validator.validate("user@")["is_valid"] is False

    def test_regex_validator(self):
        """测试正则验证"""
        # 仅允许数字
        validator = Validator([RegexValidator(r"^\d+$", "只允许数字")])
        assert validator.validate("123")["is_valid"] is True
        assert validator.validate("abc")["is_valid"] is False
        assert "数字" in validator.validate("abc")["errors"][0]

    def test_chain_all_pass(self):
        """测试验证链全部通过"""
        validator = Validator([
            NotEmptyValidator(),
            LengthValidator(min_len=5, max_len=20),
            EmailValidator(),
        ])
        result = validator.validate("user@example.com")
        assert result["is_valid"] is True

    def test_chain_one_fails(self):
        """测试验证链中某个失败"""
        validator = Validator([
            NotEmptyValidator(),
            LengthValidator(min_len=5, max_len=20),
            EmailValidator(),
        ])
        # 长度不够
        result = validator.validate("a@b")
        assert result["is_valid"] is False
        # 应该只有长度验证的报错
        assert len(result["errors"]) == 1

    def test_chain_multiple_fail(self):
        """测试验证链多个失败"""
        validator = Validator([
            NotEmptyValidator(),
            LengthValidator(min_len=5, max_len=10),
            EmailValidator(),
        ])
        # 空字符串同时触发 NotEmpty 和 Length 失败
        result = validator.validate("")
        assert result["is_valid"] is False
        assert len(result["errors"]) >= 2

    def test_real_world_registration(self):
        """模拟真实注册场景验证"""
        validator = Validator([
            NotEmptyValidator(),
            LengthValidator(min_len=3, max_max=30),
            RegexValidator(r"^[a-zA-Z0-9_]+$", "用户名只能包含字母、数字和下划线"),
        ])
        # 有效用户名
        assert validator.validate("alice_123")["is_valid"] is True
        # 无效用户名（包含空格）
        result = validator.validate("alice 123")
        assert result["is_valid"] is False
