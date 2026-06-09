"""
================================================================================
Lesson 6: Decorator (装饰器模式) — 练习题
================================================================================
"""

from abc import ABC, abstractmethod


# ==============================================================================
# 第1题：基础 — 文本格式化装饰器
# ==============================================================================

class TextComponent(ABC):
    """文本组件抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass


class PlainText(TextComponent):
    """纯文本 — 基础组件"""

    def __init__(self, text: str):
        self._text = text

    def render(self) -> str:
        return self._text


class TextDecorator(TextComponent):
    """文本装饰器抽象类"""

    def __init__(self, component: TextComponent):
        self._component = component

    @abstractmethod
    def render(self) -> str:
        pass


# TODO: 实现 BoldDecorator，在文本外层添加 <b></b> 标签
class BoldDecorator(TextDecorator):
    def render(self) -> str:
        pass


# TODO: 实现 ItalicDecorator，在文本外层添加 <i></i> 标签
class ItalicDecorator(TextDecorator):
    def render(self) -> str:
        pass


# ==============================================================================
# 第2题：综合 — 数据管道装饰器
# ==============================================================================

class DataSource(ABC):
    """数据源抽象接口"""

    @abstractmethod
    def write(self, data: str):
        pass

    @abstractmethod
    def read(self) -> str:
        pass


class FileDataSource(DataSource):
    """文件数据源 — 基础组件"""

    def __init__(self, data: str = ""):
        self._data = data

    def write(self, data: str):
        self._data = data

    def read(self) -> str:
        return self._data


class DataSourceDecorator(DataSource):
    """数据源装饰器抽象类"""

    def __init__(self, source: DataSource):
        self._source = source

    def write(self, data: str):
        self._source.write(data)

    def read(self) -> str:
        return self._source.read()


# TODO: 实现 CompressionDecorator
#   write(data) 时：将 data 加上 "[压缩]" 前缀（模拟压缩）
#   read() 时：从被装饰者读取数据，去掉 "[压缩]" 前缀（模拟解压）
#   注意：如果数据没有 "[压缩]" 前缀，read() 直接返回原数据
class CompressionDecorator(DataSourceDecorator):
    def write(self, data: str):
        pass

    def read(self) -> str:
        pass


# TODO: 实现 EncryptionDecorator
#   write(data) 时：将 data 加上 "[加密]" 前缀（模拟加密）
#   read() 时：从被装饰者读取数据，去掉 "[加密]" 前缀（模拟解密）
#   注意：如果数据没有 "[加密]" 前缀，read() 直接返回原数据
class EncryptionDecorator(DataSourceDecorator):
    def write(self, data: str):
        pass

    def read(self) -> str:
        pass


# ==============================================================================
# 第3题：拓展 — 价格计算装饰器链
# ==============================================================================

class PriceComponent(ABC):
    """价格组件抽象接口"""

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def calculate(self) -> float:
        pass


class BasePrice(PriceComponent):
    """基础价格"""

    def __init__(self, amount: float, description: str = "商品价格"):
        self._amount = amount
        self._description = description

    def get_description(self) -> str:
        return self._description

    def calculate(self) -> float:
        return self._amount


class PriceDecorator(PriceComponent):
    """价格装饰器抽象类"""

    def __init__(self, component: PriceComponent):
        self._component = component

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def calculate(self) -> float:
        pass


# TODO: 实现 DiscountDecorator
#   在 calculate() 中：原价 × (1 - discount_rate)
#   在 get_description() 中：原描述 + " (折扣 -{discount_rate*100}%)"
class DiscountDecorator(PriceDecorator):
    def __init__(self, component: PriceComponent, discount_rate: float):
        super().__init__(component)
        self._discount_rate = discount_rate

    def get_description(self) -> str:
        pass

    def calculate(self) -> float:
        pass


# TODO: 实现 TaxDecorator
#   在 calculate() 中：原价 × (1 + tax_rate)
#   在 get_description() 中：原描述 + " (税 +{tax_rate*100}%)"
class TaxDecorator(PriceDecorator):
    def __init__(self, component: PriceComponent, tax_rate: float):
        super().__init__(component)
        self._tax_rate = tax_rate

    def get_description(self) -> str:
        pass

    def calculate(self) -> float:
        pass


# TODO: 实现 ShippingDecorator
#   在 calculate() 中：原价 + shipping_fee
#   在 get_description() 中：原描述 + " (运费 ¥{shipping_fee})"
class ShippingDecorator(PriceDecorator):
    def __init__(self, component: PriceComponent, shipping_fee: float):
        super().__init__(component)
        self._shipping_fee = shipping_fee

    def get_description(self) -> str:
        pass

    def calculate(self) -> float:
        pass
