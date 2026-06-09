"""
================================================================================
 Lesson 00: OOP Foundation — 单元测试
================================================================================
 运行方式：pytest test_exercise.py -v
================================================================================
"""

import pytest
from exercise import (
    BankAccount,
    Payment,
    Alipay,
    WeChatPay,
    BankCard,
    CPU,
    Memory,
    Storage,
    Computer,
)


# ============================================================================
# 测试练习1：封装 (Encapsulation)
# ============================================================================

class TestBankAccount:
    """测试 BankAccount 类的封装特性"""

    def test_deposit_normal(self):
        """测试正常存款"""
        account = BankAccount("Alice", 100)
        account.deposit(50)
        assert account.get_balance() == 150

    def test_withdraw_normal(self):
        """测试正常取款"""
        account = BankAccount("Bob", 500)
        account.withdraw(200)
        assert account.get_balance() == 300

    def test_deposit_negative_amount(self):
        """测试存款金额为负 — 应抛出异常"""
        account = BankAccount("Charlie", 100)
        with pytest.raises(ValueError, match="存款金额必须为正数"):
            account.deposit(-10)

    def test_deposit_zero_amount(self):
        """测试存款金额为零 — 应抛出异常"""
        account = BankAccount("David", 100)
        with pytest.raises(ValueError, match="存款金额必须为正数"):
            account.deposit(0)

    def test_withdraw_negative_amount(self):
        """测试取款金额为负 — 应抛出异常"""
        account = BankAccount("Eve", 100)
        with pytest.raises(ValueError, match="取款金额必须为正数"):
            account.withdraw(-5)

    def test_withdraw_insufficient_balance(self):
        """测试余额不足时取款 — 应抛出异常"""
        account = BankAccount("Frank", 100)
        with pytest.raises(ValueError, match="余额不足"):
            account.withdraw(200)

    def test_withdraw_exact_balance(self):
        """测试取款金额等于余额"""
        account = BankAccount("Grace", 300)
        account.withdraw(300)
        assert account.get_balance() == 0

    def test_deposit_withdraw_chain(self):
        """测试连续存取款"""
        account = BankAccount("Henry", 1000)
        account.deposit(500)
        account.withdraw(200)
        account.deposit(100)
        assert account.get_balance() == 1400

    def test_multiple_accounts_independent(self):
        """测试多个账户余额相互独立"""
        a1 = BankAccount("User1", 100)
        a2 = BankAccount("User2", 200)
        a1.withdraw(50)
        assert a1.get_balance() == 50
        assert a2.get_balance() == 200


# ============================================================================
# 测试练习2：多态 (Polymorphism)
# ============================================================================

class TestPayment:
    """测试支付系统的多态特性"""

    def test_alipay_pay(self):
        """测试支付宝支付"""
        pay = Alipay()
        result = pay.pay(100)
        assert result == "[支付宝] 支付 ¥100"

    def test_wechat_pay_pay(self):
        """测试微信支付"""
        pay = WeChatPay()
        result = pay.pay(200.50)
        assert result == "[微信支付] 支付 ¥200.5"

    def test_bank_card_pay(self):
        """测试银行卡支付"""
        pay = BankCard()
        result = pay.pay(999.99)
        assert result == "[银行卡] 支付 ¥999.99"

    def test_payment_zero_amount(self):
        """测试支付金额为零"""
        pay = Alipay()
        result = pay.pay(0)
        assert result == "[支付宝] 支付 ¥0"

    def test_payment_polymorphism(self):
        """测试多态：统一接口不同行为"""
        payments = [Alipay(), WeChatPay(), BankCard()]
        results = [p.pay(300) for p in payments]
        assert results == [
            "[支付宝] 支付 ¥300",
            "[微信支付] 支付 ¥300",
            "[银行卡] 支付 ¥300",
        ]

    def test_payment_is_instance(self):
        """测试支付类继承关系"""
        assert isinstance(Alipay(), Payment)
        assert isinstance(WeChatPay(), Payment)
        assert isinstance(BankCard(), Payment)

    def test_payment_abstract_cannot_instantiate(self):
        """测试抽象类不能实例化"""
        with pytest.raises(TypeError):
            Payment()  # type: ignore


# ============================================================================
# 测试练习3：组合 (Composition)
# ============================================================================

class TestComputer:
    """测试 Computer 类的组合特性"""

    def test_cpu_get_info(self):
        """测试 CPU 信息"""
        cpu = CPU("Intel i7-12700", 12)
        assert cpu.get_info() == "Intel i7-12700 (12核)"

    def test_memory_get_info(self):
        """测试内存信息"""
        memory = Memory("16GB DDR4")
        assert memory.get_info() == "16GB DDR4"

    def test_storage_get_info(self):
        """测试存储信息"""
        storage = Storage("512GB", "SSD")
        assert storage.get_info() == "512GB SSD"

    def test_storage_default_type(self):
        """测试存储默认类型为 SSD"""
        storage = Storage("1TB")
        assert storage.get_info() == "1TB SSD"

    def test_computer_get_spec(self):
        """测试电脑完整配置输出"""
        cpu = CPU("AMD Ryzen 7 5800X", 8)
        memory = Memory("32GB DDR5")
        storage = Storage("1TB", "NVMe SSD")
        computer = Computer("ASUS", cpu, memory, storage)
        spec = computer.get_spec()
        assert "ASUS" in spec
        assert "AMD Ryzen 7 5800X (8核)" in spec
        assert "32GB DDR5" in spec
        assert "1TB NVMe SSD" in spec

    def test_computer_multiple_instances(self):
        """测试多个电脑实例相互独立"""
        cpu1 = CPU("Intel i5", 6)
        mem1 = Memory("8GB DDR4")
        st1 = Storage("256GB")
        pc1 = Computer("Dell", cpu1, mem1, st1)

        cpu2 = CPU("Intel i9", 16)
        mem2 = Memory("64GB DDR5")
        st2 = Storage("2TB", "NVMe")
        pc2 = Computer("Apple", cpu2, mem2, st2)

        spec1 = pc1.get_spec()
        spec2 = pc2.get_spec()
        assert "Intel i5 (6核)" in spec1
        assert "8GB DDR4" in spec1
        assert "256GB SSD" in spec1
        assert "Dell" in spec1

        assert "Intel i9 (16核)" in spec2
        assert "64GB DDR5" in spec2
        assert "2TB NVMe" in spec2
        assert "Apple" in spec2

    def test_computer_spec_format(self):
        """测试 get_spec 输出格式"""
        cpu = CPU("M1", 8)
        memory = Memory("16GB LPDDR5")
        storage = Storage("512GB")
        computer = Computer("MacBook", cpu, memory, storage)
        spec = computer.get_spec()
        # 验证格式包含所有部件标签
        assert "品牌:" in spec
        assert "CPU:" in spec
        assert "内存:" in spec
        assert "存储:" in spec
