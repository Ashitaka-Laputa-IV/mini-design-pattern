"""
================================================================================
Lesson 8: Strategy (策略模式) — 练习题
================================================================================
"""

from abc import ABC, abstractmethod
from typing import Callable, List


# ==============================================================================
# 第1题：基础 — 排序策略
# ==============================================================================

def bubble_sort(data: list) -> list:
    """对列表进行冒泡排序，返回排序后的新列表（不修改原列表）"""
    # TODO: 实现冒泡排序逻辑
    raise NotImplementedError


def quick_sort(data: list) -> list:
    """对列表进行快速排序，返回排序后的新列表（不修改原列表）"""
    # TODO: 实现快速排序逻辑
    raise NotImplementedError


def python_sort(data: list) -> list:
    """使用 Python 内置 sorted() 对列表排序"""
    # TODO: 调用 sorted() 并返回结果
    raise NotImplementedError


class Sorter:
    """
    排序器 — 接受排序策略函数
    """

    def __init__(self, strategy: Callable[[list], list]):
        self._strategy = strategy

    def set_strategy(self, strategy: Callable[[list], list]):
        """运行时切换排序策略"""
        self._strategy = strategy

    def sort(self, data: list) -> list:
        """执行排序"""
        return self._strategy(data)


# ==============================================================================
# 第2题：综合 — 促销策略
# ==============================================================================

class DiscountStrategy(ABC):
    """折扣策略抽象接口"""

    @abstractmethod
    def apply_discount(self, total: float) -> float:
        """对原价应用折扣，返回折后价"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """返回策略描述"""
        pass


class NoDiscount(DiscountStrategy):
    """无折扣"""

    def apply_discount(self, total: float) -> float:
        return total

    def get_description(self) -> str:
        return "无折扣"


class PercentageDiscount(DiscountStrategy):
    """按百分比打折，如 10% 折扣 → 原价 × (1 - 0.10)"""

    def __init__(self, percent: float):
        self._percent = percent

    def apply_discount(self, total: float) -> float:
        # TODO: 按百分比计算折后价
        raise NotImplementedError

    def get_description(self) -> str:
        # TODO: 返回如 "8折" 的字符串
        raise NotImplementedError


class FixedDiscount(DiscountStrategy):
    """固定金额折扣，注意折后价不能小于 0"""

    def __init__(self, amount: float):
        self._amount = amount

    def apply_discount(self, total: float) -> float:
        # TODO: 减去固定金额，确保结果 >= 0
        raise NotImplementedError

    def get_description(self) -> str:
        # TODO: 返回如 "满减 ¥50" 的字符串
        raise NotImplementedError


class BOGOFree(DiscountStrategy):
    """买一送一：total >= 100 时 5 折，否则不打折"""

    def apply_discount(self, total: float) -> float:
        # TODO: 当 total >= 100 返回 total/2，否则返回 total
        raise NotImplementedError

    def get_description(self) -> str:
        # TODO: 返回 "买一送一" 或 "无折扣"
        raise NotImplementedError


class ShoppingCart:
    """
    购物车 — 持有折扣策略
    """

    def __init__(self, strategy: DiscountStrategy = None):
        self._items: List[tuple] = []  # (name, price) 列表
        self._strategy = strategy or NoDiscount()

    def add_item(self, name: str, price: float):
        self._items.append((name, price))

    def get_total(self) -> float:
        """计算商品原价总和"""
        return sum(price for _, price in self._items)

    def set_strategy(self, strategy: DiscountStrategy):
        """切换折扣策略"""
        self._strategy = strategy

    def checkout(self) -> dict:
        """
        结算：返回包含原价、折扣描述和最终价格的字典
        """
        total = self.get_total()
        final_price = self._strategy.apply_discount(total)
        return {
            "original_total": total,
            "discount": self._strategy.get_description(),
            "final_price": final_price,
        }


# ==============================================================================
# 第3题：拓展 — 验证策略链
# ==============================================================================

class ValidationStrategy(ABC):
    """验证策略抽象接口"""

    @abstractmethod
    def validate(self, value: str) -> bool:
        """验证值是否通过，通过返回 True"""
        pass

    @abstractmethod
    def get_error_message(self) -> str:
        """返回验证失败时的错误信息"""
        pass


class NotEmptyValidator(ValidationStrategy):
    """非空验证"""

    def validate(self, value: str) -> bool:
        return bool(value and value.strip())

    def get_error_message(self) -> str:
        return "值不能为空"


class LengthValidator(ValidationStrategy):
    """验证字符串长度是否在 [min_len, max_len] 范围内
    min_len/max_len 为 None 时不检查对应边界"""

    def __init__(self, min_len: int = None, max_len: int = None):
        self._min_len = min_len
        self._max_len = max_len

    def validate(self, value: str) -> bool:
        # TODO: 检查长度是否在范围内
        raise NotImplementedError

    def get_error_message(self) -> str:
        # TODO: 返回长度范围描述，如 "长度必须在 3~20 之间"
        raise NotImplementedError


class EmailValidator(ValidationStrategy):
    """验证是否为合法的电子邮件格式（包含 @ 且 @ 前后有内容）"""

    def validate(self, value: str) -> bool:
        # TODO: 检查是否包含 @ 且 @ 前后有内容
        raise NotImplementedError

    def get_error_message(self) -> str:
        # TODO: 返回 "不是有效的邮箱格式"
        raise NotImplementedError


class RegexValidator(ValidationStrategy):
    """使用正则表达式验证（提示：用 re.match）"""

    def __init__(self, pattern: str, error_message: str = "格式不匹配"):
        self._pattern = pattern
        self._error_message = error_message

    def validate(self, value: str) -> bool:
        # TODO: 用 re.match(self._pattern, value) 验证
        raise NotImplementedError

    def get_error_message(self) -> str:
        # TODO: 返回 self._error_message
        raise NotImplementedError


class Validator:
    """
    验证器 — 持有多个验证策略，全部通过才算通过
    """

    def __init__(self, strategies: List[ValidationStrategy] = None):
        self._strategies = strategies or []

    def add_strategy(self, strategy: ValidationStrategy):
        """添加验证策略"""
        self._strategies.append(strategy)

    def validate(self, value: str) -> dict:
        """
        执行所有验证策略
        返回字典：{"is_valid": bool, "errors": [错误信息列表]}
        """
        errors = []
        for strategy in self._strategies:
            if not strategy.validate(value):
                errors.append(strategy.get_error_message())
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
        }
