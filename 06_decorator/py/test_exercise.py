"""
================================================================================
Lesson 6: Decorator (装饰器模式) — 练习测试
================================================================================
"""

import pytest
from exercise import (
    PlainText,
    BoldDecorator,
    ItalicDecorator,
    FileDataSource,
    CompressionDecorator,
    EncryptionDecorator,
    BasePrice,
    DiscountDecorator,
    TaxDecorator,
    ShippingDecorator,
)


# ==============================================================================
# 第1题测试：文本格式化装饰器
# ==============================================================================

class TestTextDecorator:
    """测试文本格式化装饰器"""

    def test_plain_text(self):
        """测试基础纯文本"""
        text = PlainText("Hello")
        assert text.render() == "Hello"

    def test_bold_decorator(self):
        """测试加粗装饰器"""
        text = BoldDecorator(PlainText("Hello"))
        assert text.render() == "<b>Hello</b>"

    def test_italic_decorator(self):
        """测试斜体装饰器"""
        text = ItalicDecorator(PlainText("Hello"))
        assert text.render() == "<i>Hello</i>"

    def test_nested_bold_italic(self):
        """测试多层装饰：加粗 + 斜体"""
        text = BoldDecorator(ItalicDecorator(PlainText("Hello")))
        assert text.render() == "<b><i>Hello</i></b>"

    def test_nested_italic_bold(self):
        """测试多层装饰：斜体 + 加粗（顺序不同结果不同）"""
        text = ItalicDecorator(BoldDecorator(PlainText("Hello")))
        assert text.render() == "<i><b>Hello</b></i>"

    def test_triple_decorator(self):
        """测试三层装饰嵌套"""
        text = BoldDecorator(ItalicDecorator(BoldDecorator(PlainText("Hi"))))
        assert text.render() == "<b><i><b>Hi</b></i></b>"


# ==============================================================================
# 第2题测试：数据管道装饰器
# ==============================================================================

class TestDataPipeline:
    """测试数据管道装饰器"""

    def test_file_data_source(self):
        """测试基础数据源读写"""
        source = FileDataSource()
        source.write("hello world")
        assert source.read() == "hello world"

    def test_compression_write_read(self):
        """测试压缩装饰器：写入时压缩，读取时解压"""
        source = CompressionDecorator(FileDataSource())
        source.write("hello world")
        assert source.read() == "hello world"

    def test_encryption_write_read(self):
        """测试加密装饰器：写入时加密，读取时解密"""
        source = EncryptionDecorator(FileDataSource())
        source.write("secret data")
        assert source.read() == "secret data"

    def test_compress_then_encrypt(self):
        """测试先压缩再加密的管道"""
        # 先压缩，再加密
        source = EncryptionDecorator(
            CompressionDecorator(FileDataSource())
        )
        source.write("hello world")
        assert source.read() == "hello world"

    def test_encrypt_then_compress(self):
        """测试先加密再压缩的管道"""
        source = CompressionDecorator(
            EncryptionDecorator(FileDataSource())
        )
        source.write("secret data")
        assert source.read() == "secret data"

    def test_triple_pipeline(self):
        """测试三层管道：加密 → 压缩 → 加密"""
        source = EncryptionDecorator(
            CompressionDecorator(
                EncryptionDecorator(FileDataSource())
            )
        )
        source.write("top secret")
        assert source.read() == "top secret"

    def test_pipeline_with_initial_data(self):
        """测试带有初始数据的管道"""
        source = CompressionDecorator(FileDataSource("initial data"))
        assert source.read() == "initial data"
        source.write("new data")
        assert source.read() == "new data"


# ==============================================================================
# 第3题测试：价格计算装饰器链
# ==============================================================================

class TestPriceCalculator:
    """测试价格计算装饰器链"""

    def test_base_price(self):
        """测试基础价格"""
        price = BasePrice(100.0)
        assert price.calculate() == 100.0
        assert "商品价格" in price.get_description()

    def test_discount_only(self):
        """测试仅打折"""
        price = DiscountDecorator(BasePrice(100.0), 0.2)
        assert price.calculate() == 80.0
        assert "折扣" in price.get_description()

    def test_tax_only(self):
        """测试仅加税"""
        price = TaxDecorator(BasePrice(100.0), 0.1)
        assert price.calculate() == 110.0
        assert "税" in price.get_description()

    def test_shipping_only(self):
        """测试仅加运费"""
        price = ShippingDecorator(BasePrice(100.0), 15.0)
        assert price.calculate() == 115.0
        assert "运费" in price.get_description()

    def test_discount_then_tax(self):
        """测试先打折后加税"""
        price = TaxDecorator(
            DiscountDecorator(BasePrice(100.0), 0.2),
            0.1
        )
        # 100 * 0.8 * 1.1 = 88
        assert price.calculate() == 88.0

    def test_discount_tax_shipping(self):
        """测试完整装饰链：打折 → 加税 → 加运费"""
        price = ShippingDecorator(
            TaxDecorator(
                DiscountDecorator(BasePrice(200.0), 0.3),
                0.08
            ),
            20.0
        )
        # 200 * 0.7 * 1.08 + 20 = 151.2 + 20 = 171.2
        assert abs(price.calculate() - 171.2) < 0.001

    def test_all_decorators_order_matters(self):
        """测试装饰顺序影响最终价格"""
        # 方案A：先打折后加税再加运费
        price_a = ShippingDecorator(
            TaxDecorator(
                DiscountDecorator(BasePrice(100.0), 0.2),
                0.1
            ),
            10.0
        )
        # 100 * 0.8 * 1.1 + 10 = 98
        result_a = price_a.calculate()

        # 方案B：先加运费再打折后加税
        price_b = TaxDecorator(
            DiscountDecorator(
                ShippingDecorator(BasePrice(100.0), 10.0),
                0.2
            ),
            0.1
        )
        # (100 + 10) * 0.8 * 1.1 = 96.8
        result_b = price_b.calculate()

        # 顺序不同，价格不同
        assert result_a != result_b

    def test_decorator_description(self):
        """测试装饰链的描述信息"""
        price = ShippingDecorator(
            TaxDecorator(
                DiscountDecorator(BasePrice(100.0, "笔记本电脑"), 0.1),
                0.05
            ),
            30.0
        )
        desc = price.get_description()
        assert "笔记本电脑" in desc
        assert "折扣" in desc
        assert "税" in desc
        assert "运费" in desc
