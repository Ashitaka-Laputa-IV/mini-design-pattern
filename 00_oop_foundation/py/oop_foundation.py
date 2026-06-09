"""
================================================================================
 Lesson 0: OOP Foundation — 面向对象编程基础
================================================================================
  ⚠ 先修课：在学设计模式之前，必须理解 OOP 的核心概念。
  设计模式的本质就是 "如何用 OOP 特性优雅地解决问题"。

  本课覆盖：
    1. 封装 (Encapsulation) — 数据隐藏，暴露接口
    2. 继承 (Inheritance) — 代码复用，is-a 关系
    3. 多态 (Polymorphism) — 同一接口，不同行为
    4. 抽象类/接口 (Abstract/Interface) — 约定规范
    5. 组合优于继承 (Composition > Inheritance) — has-a 关系

  学习方式：先看反模式（坏的味道），再看正确写法。
  每段代码都有详细注释，请一行行读过去。
================================================================================
"""

# ============================================================================
# 1. 封装 (Encapsulation)
# ============================================================================
"""
▸ 概念：把数据和操作数据的方法捆绑在一起，对外隐藏内部细节。
▸ 反模式（坏味道）：直接暴露内部数据，任何人都可以随意修改。
"""

# ---------- 反模式：裸数据 ----------
class BadBankAccount:
    """❌ 坏味道：余额直接暴露，谁都能改"""

    def __init__(self, owner: str, balance: float):
        self.owner = owner  # 公开属性
        self.balance = balance  # 公开属性


# 任何人都可以直接操作内部数据
account = BadBankAccount("Alice", 1000)
account.balance = -500  # ⚠ 可以随意设为负数！不合逻辑
account.balance = account.balance - 2000  # 直接操作，没有任何校验
print(f"[反模式] {account.owner} 余额: {account.balance}")  # 输出 -500，不合理


# ---------- 模式：封装 ----------
class GoodBankAccount:
    """✅ 封装：私有属性 + 公开方法控制访问"""

    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance  # ❗ 单下划线：约定"请别直接访问我"
        # __（双下划线）会触发名称改写 (name mangling)，Python 特有的机制

    # ---- property：Python 风格的 getter/setter ----
    @property
    def balance(self) -> float:
        """getter：只读访问余额（外部不能直接赋值）"""
        return self._balance

    def deposit(self, amount: float):
        """存款：有业务逻辑校验"""
        if amount <= 0:
            raise ValueError("存款金额必须为正数")
        self._balance += amount

    def withdraw(self, amount: float):
        """取款：有业务逻辑校验"""
        if amount <= 0:
            raise ValueError("取款金额必须为正数")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount

    def __str__(self) -> str:
        return f"{self.owner} 余额: ¥{self._balance:.2f}"


# 测试封装
account = GoodBankAccount("Alice", 1000)
account.deposit(500)       # 存入 500
account.withdraw(200)      # 取出 200
print(f"[封装] {account}")  # 输出：Alice 余额: ¥1300.00

# account.balance = 9999    # ❌ 会报错！@property 没有 setter
# account._balance = 9999   # ❌ 技术上可以但不要这么做！约定就是协议


# ============================================================================
# 2. 继承 (Inheritance)
# ============================================================================
"""
▸ 概念：子类自动拥有父类的所有属性和方法，可以扩展或重写。
▸ 反模式：过度使用继承，导致类层次太深、代码僵化。
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."


# ---------- 继承的正确用法 ----------
class Dog(Animal):
    def speak(self) -> str:
        return "汪汪！"


class Cat(Animal):
    def speak(self) -> str:
        return "喵～"


# ---------- 继承 vs 组合的对比 ----------
"""
💡 关键原则："优先使用组合而非继承" (Favor composition over inheritance)
   - 继承：is-a 关系  (Dog is an Animal)
   - 组合：has-a 关系  (Car has an Engine)

面试常问：什么时候用继承？什么时候用组合？
答：当关系是"是"(is-a) 时用继承；是"有"(has-a) 时用组合。
"""


# ============================================================================
# 3. 多态 (Polymorphism)
# ============================================================================
"""
▸ 概念：同一个方法名，不同对象有不同实现。
▸ 反模式：用 if-else 判断对象类型来执行不同行为。
"""


# ---------- 反模式：if-else 判断类型 ----------
def make_sound_bad(animal):
    """❌ 坏味道：每加一种新动物，就要改这个函数"""
    if isinstance(animal, Dog):
        print("汪汪！")
    elif isinstance(animal, Cat):
        print("喵～")
    else:
        print("???")


# ---------- 模式：利用多态 ----------
def make_sound_good(animal):
    """✅ 多态：不管什么动物，只要它有 speak() 方法就行"""
    print(animal.speak())


# 测试多态
animals = [Dog("旺财"), Cat("咪咪")]
for a in animals:
    make_sound_good(a)
# 输出：
# 汪汪！
# 喵～

"""
🔑 面试重点：Python 的多态是"鸭子类型"(Duck Typing)
   "如果它走路像鸭子，叫起来像鸭子，那它就是鸭子。"
   不需要显式继承，只要有相同的方法签名即可。
   这和 C++/Java 的静态类型多态完全不同，
   也是 Python 实现设计模式时更灵活的原因。
"""


# ============================================================================
# 4. 抽象类 / 接口 (Abstract Base Class)
# ============================================================================
"""
▸ 概念：定义一个"规范"，子类必须实现某些方法。
▸ Python 用 abc 模块实现，C++ 用纯虚函数实现。
"""

from abc import ABC, abstractmethod


class Shape(ABC):
    """抽象类：不能被实例化，只作为规范"""

    @abstractmethod
    def area(self) -> float:
        """子类必须实现此方法"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """子类必须实现此方法"""
        pass

    def description(self) -> str:
        """普通方法：所有子类共享"""
        return f"我是一个图形，面积={self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius * self.radius

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


# 测试
# s = Shape()          # ❌ TypeError: Can't instantiate abstract class
c = Circle(5)
r = Rectangle(3, 4)
print(f"[抽象类] 圆形: {c.description()}")     # 面积=78.54
print(f"[抽象类] 矩形: {r.description()}")     # 面积=12.00


# ============================================================================
# 5. 组合优于继承 (Composition over Inheritance)
# ============================================================================
"""
这个原则太重要了，很多设计模式（装饰器、策略、适配器等）
都建立在"组合"而不是"继承"之上。

让我们用一个经典例子来理解：
"""

# ---------- 反模式：滥用继承 ----------
class Engine:
    """发动机"""
    def start(self):
        return "发动机启动"

class Tires:
    """轮胎"""
    def inflate(self):
        return "轮胎充气"

class BadCar(Engine, Tires):
    """❌ 用继承实现"车有发动机和轮胎"——语义错误！
    Car is NOT an Engine, Car has an Engine!
    """
    def drive(self):
        return f"{self.start()}，开车！"


# ---------- 模式：组合 ----------
class GoodCar:
    """✅ 用组合：车"拥有"发动机和轮胎"""

    def __init__(self):
        self.engine = Engine()      # has-a 关系
        self.tires = [Tires() for _ in range(4)]  # has-a 关系

    def drive(self):
        result = self.engine.start()
        for t in self.tires:
            result += f", {t.inflate()}"
        return f"{result}，开车！"


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
1. Python 有真正的封装吗？
   没有。Python 靠"约定"（单下划线 _ 表示 protected，双下划线 __ 表示
   private 但实际是 name mangling），没有真正的访问控制。
   这和 C++ 的 private/protected/public 机制完全不同。

2. Python 支持多继承吗？
   支持！但存在菱形继承问题（Diamond Problem），Python 用 MRO
   (Method Resolution Order) 和 C3 线性化算法解决。

3. 抽象类和接口有什么区别？
   - Python 没有 interface 关键字，abc 模块既能模拟接口（全是抽象方法）
     也能模拟抽象类（有一些实现）
   - C++ 用纯虚函数实现接口，用有实现的虚函数做抽象类

4. 组合和继承什么时候选哪个？
   继承：子类是父类的一种 (is-a)，紧密耦合
   组合：对象拥有另一个对象 (has-a)，松散耦合
   💡 原则：能用组合就别用继承（除非确定是 is-a 关系）
"""


# ============================================================================
# 自测练习 🧪
# ============================================================================
"""
1. 把 BadBankAccount 改写成正确的封装
2. 用多态实现一个 "支付系统"：支付宝、微信支付、银行卡 都有 pay() 方法
3. 用组合实现一个 "电脑" 类：有 CPU、内存、硬盘
"""
