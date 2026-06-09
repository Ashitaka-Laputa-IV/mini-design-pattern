"""
================================================================================
Lesson 6: Decorator (装饰器模式) — 反模式篇
================================================================================
  ⚠ 本课展示"反模式"：用继承实现咖啡配料组合，导致"类爆炸"。

  场景：咖啡/饮料订单系统
  - 基础饮料：Espresso (浓缩咖啡)、Americano (美式咖啡)
  - 配料：Milk (牛奶)、Sugar (糖)、Whip (奶油)
  - 需求：客户可以任意组合基础饮料和配料

  问题：同事用继承来实现——每种组合都创建一个子类。
  如果有 2 种基础饮料 × 3 种配料，组合数量 = 2 × 2³ = 16 个类！
  如果再加 1 种基础饮料或 1 种配料，类数量会指数增长。

  这就是著名的"类爆炸"(Class Explosion) 问题，
  也是 Decorator 模式要解决的核心问题。
================================================================================
"""

# ==============================================================================
# 反模式：用继承实现咖啡配料
# ==============================================================================
"""
▸ 坏味道：每多一种配料组合，就要新建一个类。
▸ 后果：类数量呈指数增长，系统变得不可维护。
"""


class Beverage:
    """饮料基类"""

    def __init__(self, description: str):
        self._description = description

    def get_description(self) -> str:
        return self._description

    def cost(self) -> float:
        return 0.0


# ============ 基础饮料 ============

class Espresso(Beverage):
    """浓缩咖啡"""

    def __init__(self):
        super().__init__("浓缩咖啡")

    def cost(self) -> float:
        return 10.0


class Americano(Beverage):
    """美式咖啡"""

    def __init__(self):
        super().__init__("美式咖啡")

    def cost(self) -> float:
        return 8.0


# ============ ❌ 类爆炸开始 ============
# 每种配料组合都要创建一个新类！

class EspressoWithMilk(Espresso):
    """浓缩咖啡 + 牛奶"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 牛奶"

    def cost(self) -> float:
        return super().cost() + 2.0  # 牛奶 +2元


class EspressoWithSugar(Espresso):
    """浓缩咖啡 + 糖"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 糖"

    def cost(self) -> float:
        return super().cost() + 1.0  # 糖 +1元


class EspressoWithWhip(Espresso):
    """浓缩咖啡 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 奶油"

    def cost(self) -> float:
        return super().cost() + 3.0  # 奶油 +3元


class EspressoWithMilkAndSugar(Espresso):
    """浓缩咖啡 + 牛奶 + 糖"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 牛奶 + 糖"

    def cost(self) -> float:
        return super().cost() + 2.0 + 1.0


class EspressoWithMilkAndWhip(Espresso):
    """浓缩咖啡 + 牛奶 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 牛奶 + 奶油"

    def cost(self) -> float:
        return super().cost() + 2.0 + 3.0


class EspressoWithSugarAndWhip(Espresso):
    """浓缩咖啡 + 糖 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 糖 + 奶油"

    def cost(self) -> float:
        return super().cost() + 1.0 + 3.0


class EspressoWithMilkSugarAndWhip(Espresso):
    """浓缩咖啡 + 牛奶 + 糖 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "浓缩咖啡 + 牛奶 + 糖 + 奶油"

    def cost(self) -> float:
        return super().cost() + 2.0 + 1.0 + 3.0


# 美式咖啡的配料组合也要来一套...

class AmericanoWithMilk(Americano):
    """美式咖啡 + 牛奶"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 牛奶"

    def cost(self) -> float:
        return super().cost() + 2.0


class AmericanoWithSugar(Americano):
    """美式咖啡 + 糖"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 糖"

    def cost(self) -> float:
        return super().cost() + 1.0


class AmericanoWithWhip(Americano):
    """美式咖啡 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 奶油"

    def cost(self) -> float:
        return super().cost() + 3.0


class AmericanoWithMilkAndSugar(Americano):
    """美式咖啡 + 牛奶 + 糖"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 牛奶 + 糖"

    def cost(self) -> float:
        return super().cost() + 2.0 + 1.0


class AmericanoWithMilkAndWhip(Americano):
    """美式咖啡 + 牛奶 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 牛奶 + 奶油"

    def cost(self) -> float:
        return super().cost() + 2.0 + 3.0


class AmericanoWithSugarAndWhip(Americano):
    """美式咖啡 + 糖 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 糖 + 奶油"

    def cost(self) -> float:
        return super().cost() + 1.0 + 3.0


class AmericanoWithMilkSugarAndWhip(Americano):
    """美式咖啡 + 牛奶 + 糖 + 奶油"""

    def __init__(self):
        super().__init__()
        self._description = "美式咖啡 + 牛奶 + 糖 + 奶油"

    def cost(self) -> float:
        return super().cost() + 2.0 + 1.0 + 3.0


# ==============================================================================
# 测试：类爆炸的后果
# ==============================================================================

def main():
    print("=" * 50)
    print("❌ 反模式：用继承实现咖啡配料 — 类爆炸")
    print("=" * 50)

    # 基础饮料
    espresso = Espresso()
    print(f"{espresso.get_description()}: ¥{espresso.cost()}")

    americano = Americano()
    print(f"{americano.get_description()}: ¥{americano.cost()}")

    # 带配料的饮料
    e_milk = EspressoWithMilk()
    print(f"{e_milk.get_description()}: ¥{e_milk.cost()}")

    e_milk_sugar = EspressoWithMilkAndSugar()
    print(f"{e_milk_sugar.get_description()}: ¥{e_milk_sugar.cost()}")

    e_all = EspressoWithMilkSugarAndWhip()
    print(f"{e_all.get_description()}: ¥{e_all.cost()}")

    a_milk_whip = AmericanoWithMilkAndWhip()
    print(f"{a_milk_whip.get_description()}: ¥{a_milk_whip.cost()}")

    print("\n" + "=" * 50)
    print("💥 问题分析")
    print("=" * 50)
    print("""
  1. 类数量爆炸：2 种基础饮料 × 2³ 种配料组合 = 16 个类！
  2. 代码重复：每个类的 cost() 都在硬编码配料价格
  3. 难以扩展：加一种新配料 → 要为每个基础饮料都创建新子类
  4. 违反开闭原则：对修改没有关闭，加配料就要改现有代码

  如果再加 1 种基础饮料（如拿铁 Latte）：
    → 需要再创建 8 个新类（Latte + 每种配料组合）
  
  如果再加 1 种配料（如巧克力 Chocolate）：
    → 组合数翻倍！从 2 × 8 = 16 变成 2 × 16 = 32 个类！

  这就是为什么说继承会导致"类爆炸"——组合数 = M × 2ᴺ
  其中 M = 基础产品数，N = 配料种类数
  """)


if __name__ == "__main__":
    main()
