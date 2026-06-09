"""
================================================================================
 Lesson 8: Strategy — 策略模式（模式实现）
================================================================================
  上节课的 bad_strategy.py 我们看到了 if-else 地狱，
  现在来看看策略模式怎么解决。

 📐 设计模式定义：
    策略模式(Strategy Pattern)定义一系列算法，将每个算法封装起来，
    并使它们可以互相替换。算法的变化不会影响使用算法的客户端。

 🎯 解决的问题：
    - 大量 if-else / switch-case 分支判断
    - 同一行为有多个实现方式，需要在运行时切换
    - 避免算法代码污染业务逻辑

 💡 核心三要素：
    1. Context（上下文）：持有一个策略引用，委托策略执行
    2. Strategy（策略接口）：定义算法族的公共接口
    3. ConcreteStrategy（具体策略）：实现策略接口的具体算法

  🐍 Python 特色：
    因为函数是 Python 中的一等公民（first-class citizen），
    所以当策略只有一个方法时，可以直接传入函数作为策略。
    这是 Python 与 C++/Java 在策略模式实现上的一个重要区别。
================================================================================
"""

import abc
from typing import Callable, Optional


# ============================================================================
# 实现 1：经典策略模式（面向接口编程）
# ============================================================================

class Order:
    """
    订单数据类——只负责数据，不关心运费怎么算。
    """

    def __init__(self, region: str, member_level: str, total_weight: float):
        self.region = region
        self.member_level = member_level
        self.total_weight = total_weight

    def __str__(self):
        return f"Order({self.region}, {self.member_level}, {self.total_weight}kg)"


class ShippingStrategy(abc.ABC):
    """
    🧩 策略接口（抽象基类）

    定义所有运费策略的公共接口。
    使用 abc.ABC 和 @abstractmethod 来定义抽象方法。
    Python 中也可以不用 abc，直接定义普通基类（鸭子类型）。
    """

    @abc.abstractmethod
    def calculate(self, order: Order) -> float:
        """
        计算运费。

        :param order: 订单对象
        :return: 运费金额
        """
        pass

    def name(self) -> str:
        """返回策略名称（用于显示）"""
        return self.__class__.__name__


# ============================================================================
# 具体策略类：每种运费算法一个类
# ============================================================================

class DomesticStandard(ShippingStrategy):
    """
    国内普通：固定 10 元
    """

    def calculate(self, order: Order) -> float:
        return 10.0


class DomesticVIP(ShippingStrategy):
    """
    国内 VIP：免运费（固定 0 元）
    """

    def calculate(self, order: Order) -> float:
        return 0.0


class OverseasStandard(ShippingStrategy):
    """
    海外普通：重量 × 15 元/kg
    """

    def calculate(self, order: Order) -> float:
        return order.total_weight * 15.0


class OverseasVIP(ShippingStrategy):
    """
    海外 VIP：重量 × 10 元/kg
    """

    def calculate(self, order: Order) -> float:
        return order.total_weight * 10.0


# ============================================================================
# Context：策略持有者
# ============================================================================

class ShippingCalculator:
    """
    🎯 Context（上下文）—— 运费的"计算器"

    核心职责：
      1. 持有当前的运费策略对象
      2. 运行时可以切换策略（set_strategy）
      3. 委托策略对象执行计算

    好处：
      - ShippingCalculator 不需要知道策略的具体实现
      - 新增策略完全不需要修改 ShippingCalculator
      - 策略可以在运行时动态切换
    """

    def __init__(self, strategy: Optional[ShippingStrategy] = None):
        """
        :param strategy: 初始策略（可选，不传则后续通过 set_strategy 设置）
        """
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy):
        """
        运行时切换策略 🎯

        这是策略模式的关键能力：行为可以在运行时改变。
        在 C++/Java 中这是策略模式的核心卖点；
        在 Python 中也可以直接替换函数来实现同样的效果。
        """
        print(f"  [切换策略] {self._strategy.name() if self._strategy else 'None'} → {strategy.name()}")
        self._strategy = strategy

    def calculate(self, order: Order) -> float:
        """委托给当前策略计算运费"""
        if self._strategy is None:
            raise ValueError("请先设置运费策略！")
        cost = self._strategy.calculate(order)
        print(f"  [策略] {self._strategy.name()} → {order} → 运费: {cost} 元")
        return cost


# ============================================================================
# 实现 2：Python 特色——函数即策略
# ============================================================================

"""
🐍 Python 特色实现：

在 Python 中，函数是一等公民（first-class citizen），
可以作为参数传递、赋值给变量、作为返回值。

当策略只有一个方法（calculate）时，
直接用函数代替策略类是更 Pythonic 的方式。

对比 C++：
  - C++ 中函数指针 / std::function 也可以做到类似效果
  - 但 C++ 的面向对象传统更倾向于使用虚函数接口
  - Python 中函数作为策略更简洁，但丢失了"策略名称"等信息

适用场景：
  - 策略逻辑简单（一个函数就能搞定）
  - 不需要维护状态
  - 不需要策略名称等元信息
"""


def domestic_standard_func(order: Order) -> float:
    """国内普通运费策略（函数版）"""
    return 10.0


def domestic_vip_func(order: Order) -> float:
    """国内 VIP 运费策略（函数版）"""
    return 0.0


def overseas_standard_func(order: Order) -> float:
    """海外普通运费策略（函数版）"""
    return order.total_weight * 15.0


def overseas_vip_func(order: Order) -> float:
    """海外 VIP 运费策略（函数版）"""
    return order.total_weight * 10.0


class ShippingCalculatorWithFunc:
    """
    Context 的函数策略版本。

    直接接受一个可调用对象（callable）作为策略。
    这展示了 Python 中策略模式的一种"轻量级"实现。
    """

    def __init__(self, strategy: Optional[Callable[[Order], float]] = None):
        self._strategy = strategy

    def set_strategy(self, strategy: Callable[[Order], float]):
        self._strategy = strategy

    def calculate(self, order: Order) -> float:
        if self._strategy is None:
            raise ValueError("请先设置运费策略！")
        cost = self._strategy(order)
        print(f"  [函数策略] → {order} → 运费: {cost} 元")
        return cost


# ============================================================================
# 实现 3：使用 lambda 作为即时策略
# ============================================================================

"""
🚀 终极 Pythonic：lambda 表达式

当你只需要在某个地方临时使用一个简单策略，
lambda 可以让你不定义函数也不定义类，直接"即兴创作"。

示例：
  calc.set_strategy(lambda o: 0.0)           # 全场免运费
  calc.set_strategy(lambda o: o.weight * 5)   # 全场 5 元/kg

这是 Python 相比 C++ 策略模式的最大优势——灵活！
但注意：lambda 只适用于非常简单的逻辑，复杂逻辑还是用函数或类。
"""


# ============================================================================
# 🧪 测试策略模式
# ============================================================================

def test_strategy():
    print("=" * 60)
    print("✅ 策略模式：经典实现")
    print("=" * 60)

    orders = [
        Order("domestic", "normal", 5.0),
        Order("domestic", "vip", 5.0),
        Order("overseas", "normal", 2.0),
        Order("overseas", "vip", 3.0),
    ]

    # 创建计算器，依次使用不同策略
    calculator = ShippingCalculator()

    strategy_map = {
        ("domestic", "normal"): DomesticStandard(),
        ("domestic", "vip"): DomesticVIP(),
        ("overseas", "normal"): OverseasStandard(),
        ("overseas", "vip"): OverseasVIP(),
    }

    for order in orders:
        # 根据订单信息选择策略（这里也可以改成由工厂创建策略）
        strategy = strategy_map.get((order.region, order.member_level))
        if strategy:
            calculator.set_strategy(strategy)
            calculator.calculate(order)
        print()

    # ---------- 演示运行时切换策略 ----------
    print("\n" + "=" * 60)
    print("🔄 运行时切换策略演示")
    print("=" * 60)

    calc = ShippingCalculator(DomesticStandard())
    calc.calculate(Order("domestic", "normal", 1.0))

    calc.set_strategy(DomesticVIP())
    calc.calculate(Order("domestic", "vip", 1.0))

    print("\n" + "=" * 60)
    print("🐍 Python 特色：函数作为策略")
    print("=" * 60)

    calc2 = ShippingCalculatorWithFunc(domestic_standard_func)
    calc2.calculate(Order("domestic", "normal", 1.0))

    calc2.set_strategy(overseas_vip_func)
    calc2.calculate(Order("overseas", "vip", 3.0))

    print("\n" + "=" * 60)
    print("🚀 Python 特色：lambda 即兴策略")
    print("=" * 60)

    calc3 = ShippingCalculatorWithFunc()
    calc3.set_strategy(lambda o: 999.0)  # 黑五免运费？不，黑五涨价！
    calc3.calculate(Order("domestic", "normal", 1.0))

    calc3.set_strategy(lambda o: 0.0 if o.member_level == "vip" else 20.0)
    calc3.calculate(Order("domestic", "vip", 1.0))
    calc3.calculate(Order("overseas", "normal", 2.0))


if __name__ == "__main__":
    test_strategy()


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 策略模式 vs 状态模式（State Pattern）有什么区别？
    A: 这是面试中最容易被混淆的一对模式。
       - 策略模式：客户端主动选择策略，策略之间平级、互相独立
         → 比如"我选顺丰还是圆通"——由我决定
       - 状态模式：状态的切换由对象内部决定，不同状态行为不同
         → 比如"订单已付款/已发货/已签收"——由订单状态自动流转
       - 核心区别：谁控制切换？
         策略：客户端（外部）控制
         状态：对象自身（内部）控制

Q2: 如果策略只有一种方法，是否可以用 lambda 替代？
    A: 可以。在 Python 中，函数是一等公民，
       当策略接口只有一个方法时，完全可以：
       - 用函数替代策略类（更简洁）
       - 用 lambda 表达式（最灵活）
       - 用 functools.partial（预绑定参数）
       但注意：如果策略需要维护内部状态，还是需要用类。

Q3: 策略模式有什么缺点？
    A: 1. 客户端必须了解不同策略的区别（否则不知道怎么选）
       2. 策略类数量会增多（每个算法一个类）
       3. 可以通过策略工厂 + 函数策略来缓解

Q4: 策略模式在 Python 标准库中有应用吗？
    A: 有！经典例子：
       1. sorted() 的 key 参数：传入一个函数作为排序策略
       2. functools.lru_cache 的 maxsize 参数
       3. re.compile 的 flags 参数
       4. threading.Thread 的 target 参数
       Python 的"函数式接口"天然支持策略模式。

Q5: 策略模式和工厂模式有什么区别？
    A: 策略模式关注"算法的选择与替换"（行为型）
       工厂模式关注"对象的创建"（创建型）
       两者常一起使用：工厂负责创建策略对象，策略负责执行算法。

💡 面试官变种题：
   如果我有 100 种运费策略，难道要创建 100 个类吗？
   思路：
     1. 参数化策略：同一个策略类通过不同参数区分
     2. 函数策略：直接用函数替代类
     3. 策略注册表 + 反射：通过配置动态加载策略
"""
