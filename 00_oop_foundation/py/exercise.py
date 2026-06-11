"""
================================================================================
 Lesson 00: OOP Foundation — 面向对象编程基础练习
================================================================================
 本文件包含 3 道练习题，难度递进：
    练习1：封装 (Encapsulation) — BankAccount 类
    练习2：多态 (Polymorphism) — 支付系统接口
    练习3：组合 (Composition) — Computer 类

 说明：
   - 所有 TODO 处需要你补全代码
   - 完成练习后，运行 test_exercise.py 验证正确性
================================================================================
"""

from abc import ABC, abstractmethod


# ============================================================================
# 练习1：封装 (Encapsulation)
# ============================================================================
# 实现一个 BankAccount 类，要求：
#   1. 用 _balance 作为私有属性存储余额
#   2. deposit(amount) — 存款，金额必须为正数
#   3. withdraw(amount) — 取款，金额必须为正数且不能超过余额
#   4. get_balance() — 返回当前余额
# ============================================================================

class BankAccount:
    """银行账户类 — 练习封装"""

    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        """存款

        Args:
            amount: 存款金额（必须为正数）

        Raises:
            ValueError: 如果金额 <= 0
        """
        # TODO: 补全存款逻辑（验证金额 > 0，更新余额）
        raise NotImplementedError

    def withdraw(self, amount: float) -> None:
        """取款

        Args:
            amount: 取款金额（必须为正数且不超过余额）

        Raises:
            ValueError: 如果金额 <= 0 或余额不足
        """
        # TODO: 补全取款逻辑（验证金额 > 0，验证余额充足，更新余额）
        raise NotImplementedError

    def get_balance(self) -> float:
        """获取当前余额"""
        # TODO: 返回 _balance 的值
        raise NotImplementedError


# ============================================================================
# 练习2：多态 (Polymorphism)
# ============================================================================
# 实现支付系统接口 Payment 及其三个实现类：
#   1. Payment — 抽象基类，声明 pay(amount) 方法
#   2. Alipay — 支付宝支付，返回 "[支付宝] 支付 ¥xxx"
#   3. WeChatPay — 微信支付，返回 "[微信支付] 支付 ¥xxx"
#   4. BankCard — 银行卡支付，返回 "[银行卡] 支付 ¥xxx"
# ============================================================================

class Payment(ABC):
    """支付接口 — 所有支付方式的抽象基类"""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """执行支付

        Args:
            amount: 支付金额

        Returns:
            支付结果的描述字符串
        """
        pass


class Alipay(Payment):
    """支付宝支付"""

    def pay(self, amount: float) -> str:
        # TODO: 返回 "[支付宝] 支付 ¥xxx" 格式的字符串
        raise NotImplementedError


class WeChatPay(Payment):
    """微信支付"""

    def pay(self, amount: float) -> str:
        # TODO: 返回 "[微信支付] 支付 ¥xxx" 格式的字符串
        raise NotImplementedError


class BankCard(Payment):
    """银行卡支付"""

    def pay(self, amount: float) -> str:
        # TODO: 返回 "[银行卡] 支付 ¥xxx" 格式的字符串
        raise NotImplementedError


# ============================================================================
# 练习3：组合 (Composition)
# ============================================================================
# 实现 Computer 类，组合 CPU / Memory / Storage 部件：
#   1. CPU — 有 name 属性和 get_info() 方法
#   2. Memory — 有 capacity 属性和 get_info() 方法
#   3. Storage — 有 capacity / type 属性和 get_info() 方法
#   4. Computer — 组合以上三个部件，有 get_spec() 方法返回完整配置
# ============================================================================

class CPU:
    """CPU 部件"""

    def __init__(self, name: str, cores: int):
        self.name = name
        self.cores = cores

    def get_info(self) -> str:
        # TODO: 返回 CPU 信息，如 "Intel i7-12700 (12核)"
        raise NotImplementedError


class Memory:
    """内存部件"""

    def __init__(self, capacity: str):
        self.capacity = capacity

    def get_info(self) -> str:
        # TODO: 返回内存信息，如 "16GB DDR4"
        raise NotImplementedError


class Storage:
    """存储部件"""

    def __init__(self, capacity: str, storage_type: str = "SSD"):
        self.capacity = capacity
        self.storage_type = storage_type

    def get_info(self) -> str:
        # TODO: 返回存储信息，如 "512GB SSD"
        raise NotImplementedError


class Computer:
    """电脑类 — 使用组合 (has-a 关系)"""

    def __init__(self, brand: str, cpu: CPU, memory: Memory, storage: Storage):
        self.brand = brand
        self.cpu = cpu
        self.memory = memory
        self.storage = storage

    def get_spec(self) -> str:
        """返回完整的电脑配置字符串

        Returns:
            格式如："品牌: Dell | CPU: Intel i7-12700 (12核) | 内存: 16GB DDR4 | 存储: 512GB SSD"
        """
        # TODO: 组合各部件的 get_info() 返回完整配置字符串
        raise NotImplementedError
