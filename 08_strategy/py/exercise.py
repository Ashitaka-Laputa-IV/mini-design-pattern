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

# TODO: 实现 BubbleSort 排序函数
#   对列表进行冒泡排序，返回排序后的新列表（不修改原列表）
def bubble_sort(data: list) -> list:
    pass


# TODO: 实现 quick_sort 排序函数
#   对列表进行快速排序，返回排序后的新列表（不修改原列表）
def quick_sort(data: list) -> list:
    pass


# TODO: 实现 python_sort 排序函数
#   直接使用 Python 内置 sorted() 对列表排序
def python_sort(data: list) -> list:
    pass


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


# TODO: 实现 PercentageDiscount
#   按百分比打折，如 10% 折扣 → 原价 × (1 - 0.10)
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        """
        :param percent: 折扣百分比，如 10 表示 10% 折扣
        """
        self._percent = percent

    def apply_discount(self, total: float) -> float:
        pass

    def get_description(self) -> str:
        pass


# TODO: 实现 FixedDiscount
#   固定金额折扣，如满 200 减 50
#   注意：如果折后价小于 0，应返回 0
class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self._amount = amount

    def apply_discount(self, total: float) -> float:
        pass

    def get_description(self) -> str:
        pass


# TODO: 实现 BOGOFree（买一送一）
#   策略：当 total >= 100 时，打 5 折（模拟买一送一）
#   否则不打折
class BOGOFree(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        pass

    def get_description(self) -> str:
        pass


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


# TODO: 实现 LengthValidator
#   验证字符串长度是否在 [min_len, max_len] 范围内
#   如果 min_len 为 None，不检查最小值
#   如果 max_len 为 None，不检查最大值
class LengthValidator(ValidationStrategy):
    def __init__(self, min_len: int = None, max_len: int = None):
        self._min_len = min_len
        self._max_len = max_len

    def validate(self, value: str) -> bool:
        pass

    def get_error_message(self) -> str:
        pass


# TODO: 实现 EmailValidator
#   验证是否为合法的电子邮件格式
#   简单规则：包含 @ 且 @ 前后都有内容
class EmailValidator(ValidationStrategy):
    def validate(self, value: str) -> bool:
        pass

    def get_error_message(self) -> str:
        pass


# TODO: 实现 RegexValidator
#   使用正则表达式验证
#   提示：使用 re.match(pattern, value) 进行匹配
class RegexValidator(ValidationStrategy):
    def __init__(self, pattern: str, error_message: str = "格式不匹配"):
        self._pattern = pattern
        self._error_message = error_message

    def validate(self, value: str) -> bool:
        pass

    def get_error_message(self) -> str:
        pass


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
