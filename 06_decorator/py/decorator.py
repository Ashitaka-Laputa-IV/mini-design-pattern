"""
================================================================================
Lesson 6: Decorator (装饰器模式) — 模式实现篇
================================================================================
  Decorator 模式通过"组合"而不是"继承"来解决类爆炸问题。

  ▸ 核心思想：装饰器和被装饰者实现同一接口
  ▸ 装饰器"包装"被装饰者，在调用前后添加额外行为
  ▸ 可以多层包装，形成"装饰链"

  角色：
    1. Component (抽象组件) — 定义统一接口
    2. ConcreteComponent (具体组件) — 被装饰的基础对象
    3. Decorator (抽象装饰器) — 持有 Component 引用，实现接口转发
    4. ConcreteDecorator (具体装饰器) — 添加额外行为

  场景：咖啡订单系统
    - 不再为每种组合创建新类
    - 基础饮料 + 一层层"包装"配料装饰器
================================================================================
"""

from abc import ABC, abstractmethod


# ==============================================================================
# 1. Component (抽象组件) — 定义统一接口
# ==============================================================================

class Beverage(ABC):
    """饮料抽象类：所有饮料和装饰器的共同接口"""

    def __init__(self):
        self._description = "未知饮料"

    def get_description(self) -> str:
        return self._description

    @abstractmethod
    def cost(self) -> float:
        pass


# ==============================================================================
# 2. ConcreteComponent (具体组件) — 基础饮料
# ==============================================================================

class Espresso(Beverage):
    """浓缩咖啡 — 基础组件"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡"

    def cost(self) -> float:
        return 10.0


class Americano(Beverage):
    """美式咖啡 — 基础组件"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡"

    def cost(self) -> float:
        return 8.0


# ==============================================================================
# 3. Decorator (抽象装饰器) — 关键！
# ==============================================================================
"""
  ⭐ Decorator 和 Beverage 实现同一接口（继承自 Beverage）
  ⭐ Decorator 持有 Beverage 引用（组合关系）
  这就是"继承接口 + 组合行为"的典型应用。
"""


class CondimentDecorator(Beverage):
    """配料抽象装饰器：继承接口，组合行为"""

    def __init__(self, beverage: Beverage):
        """
        :param beverage: 被装饰的饮料对象
        """
        super().__init__()
        self._beverage = beverage  # ⭐ 持有被装饰者的引用（组合）

    @abstractmethod
    def get_description(self) -> str:
        """子类必须实现：在原有描述后追加配料名"""
        pass


# ==============================================================================
# 4. ConcreteDecorator (具体装饰器)
# ==============================================================================

class Milk(CondimentDecorator):
    """牛奶配料装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        # 委托给被装饰者，再追加自己的描述
        return self._beverage.get_description() + " + 牛奶"

    def cost(self) -> float:
        # 委托给被装饰者，再追加自己的价格
        return self._beverage.cost() + 2.0


class Sugar(CondimentDecorator):
    """糖配料装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return self._beverage.get_description() + " + 糖"

    def cost(self) -> float:
        return self._beverage.cost() + 1.0


class Whip(CondimentDecorator):
    """奶油配料装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return self._beverage.get_description() + " + 奶油"

    def cost(self) -> float:
        return self._beverage.cost() + 3.0


# ==============================================================================
# 5. Python @ 语法糖 — 函数装饰器
# ==============================================================================
"""
  Python 语言本身也有 @decorator 语法（函数装饰器），
  和 Decorator 设计模式思想一致，但应用在函数级别。

  @decorator 本质是：func = decorator(func)
  和设计模式的"包装"思想完全一致！
"""


def log_cost(func):
    """函数装饰器：记录每次 cost() 调用"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"  [日志] cost() 返回: ¥{result}")
        return result

    return wrapper


# 我们可以把函数装饰器应用到类的方法上
class LoggedEspresso(Espresso):
    """带日志功能的浓缩咖啡"""

    @log_cost  # ⭐ cost = log_cost(cost)
    def cost(self) -> float:
        return super().cost()


# ==============================================================================
# 测试：装饰器模式解决类爆炸
# ==============================================================================

def main():
    print("=" * 60)
    print("✅ Decorator 模式：用组合解决类爆炸")
    print("=" * 60)

    # ---- 基础饮料 ----
    espresso = Espresso()
    print(f"\n基础: {espresso.get_description()} → ¥{espresso.cost()}")

    # ---- 用装饰器动态添加配料 ----
    # 浓缩咖啡 + 牛奶
    e_milk: Beverage = Milk(espresso)  # ⭐ 用牛奶"包装"浓缩咖啡
    print(f"\n装饰链: {e_milk.get_description()} → ¥{e_milk.cost()}")
    # 调用链：Milk.cost() → Espresso.cost() + 2.0

    # 浓缩咖啡 + 牛奶 + 糖
    e_milk_sugar: Beverage = Sugar(Milk(espresso))  # ⭐ 两层包装！
    print(f"装饰链: {e_milk_sugar.get_description()} → ¥{e_milk_sugar.cost()}")
    # 调用链：Sugar.cost() → Milk.cost() → Espresso.cost() + 2.0 + 1.0

    # 浓缩咖啡 + 牛奶 + 糖 + 奶油
    e_all: Beverage = Whip(Sugar(Milk(espresso)))  # ⭐ 三层包装！
    print(f"装饰链: {e_all.get_description()} → ¥{e_all.cost()}")
    # 调用链：Whip → Sugar → Milk → Espresso → 10+2+1+3

    # 美式咖啡 + 奶油
    a_whip: Beverage = Whip(Americano())
    print(f"装饰链: {a_whip.get_description()} → ¥{a_whip.cost()}")

    # 美式咖啡 + 糖 + 牛奶
    a_sugar_milk: Beverage = Milk(Sugar(Americano()))
    print(f"装饰链: {a_sugar_milk.get_description()} → ¥{a_sugar_milk.cost()}")

    # ---- 对比反模式 ----
    print("\n" + "=" * 60)
    print("🎯 对比：装饰器 vs 继承")
    print("=" * 60)
    print("""
  继承方案：           装饰器方案：
  16 个类              4 个类（2 基础 + 3 配料装饰器）
  每种组合一个类       运行时动态组合
  加新配料 → 新建 N 个类  加新配料 → 新建 1 个类
  编译时确定           运行时灵活组装

  核心公式：
    继承方案需要的类数 = M × 2ᴺ  (M=基础数, N=配料数)
    装饰器方案需要的类数 = M + N  (线性增长！)
  
  当 M=5, N=10 时：
    继承方案 = 5 × 1024 = 5120 个类 ❌
    装饰器方案 = 5 + 10 = 15 个类 ✅
  """)

    # ---- Python 函数装饰器测试 ----
    print("=" * 60)
    print("🐍 Python @ 语法糖（函数装饰器）")
    print("=" * 60)
    logged = LoggedEspresso()
    print("调用 LoggedEspresso.cost():")
    logged.cost()


# ==============================================================================
# 面试高频追问 🔥
# ==============================================================================
"""
  1. Decorator 和继承的区别？
     继承是静态的（编译时确定），子类在编译期就决定了行为。
     装饰器是动态的（运行时组合），可以在运行时自由组装行为。
     "继承是白盒复用（子类知道父类细节），装饰器是黑盒复用（只知接口）"

  2. Decorator 和 Proxy（代理模式）的区别？
     - Decorator: 为对象"添加行为"（增强功能）
     - Proxy: 为对象"控制访问"（延迟加载、权限控制）
     - 结构相似，但意图不同！
     详见 Lesson 7: Proxy 模式。

  3. Python @wraps 的作用？
     functools.wraps 可以把被包装函数的元信息（__name__、__doc__ 等）
     复制到包装函数上。没有 @wraps 时，装饰后的函数会丢失原名和文档。
     例如：@wraps(func) 确保 wrapper.__name__ == func.__name__

  4. 多层装饰器的执行顺序？
     装饰顺序 = 从内到外执行（离被装饰函数近的先装饰）
     调用顺序 = 从外到内执行（离被装饰函数远的先执行）
     比如 @A @B @C def f() → f = A(B(C(f)))
     调用 f() 时：先执行 A 的外层，然后 B，然后 C，最后原始 f

  5. 装饰器模式的缺点？
     - 增加系统复杂度，多层包装时调试困难
     - 装饰器链中的某个装饰器出问题，整条链可能受影响
     - 如果装饰器过多，创建大量小对象增加内存开销
"""


if __name__ == "__main__":
    main()
