"""
================================================================================
 Lesson 3: Abstract Factory — 抽象工厂模式（模式实现）
================================================================================
  上节课的 bad_abstract_factory.py 我们看到了 if-else 创建产品族的问题，
  现在来看看设计模式怎么解决。

 📐 设计模式定义：
   抽象工厂模式(Abstract Factory)提供一个创建一系列相关或相互依赖
   对象的接口，而无需指定它们具体的类。

 🎯 解决的问题：
   - 创建"产品族"（一组相关对象）时，保证它们之间的兼容性
   - 客户端代码与具体产品的创建解耦
   - 方便切换整个产品族

 💡 核心思想：
   把"创建一组相关产品"的接口抽象出来，
   每个具体工厂负责创建一个完整的产品族。

   关键角色：
   1. AbstractFactory（抽象工厂）— 声明创建产品的接口
   2. ConcreteFactory（具体工厂）— 实现创建具体产品族的方法
   3. AbstractProduct（抽象产品）— 产品接口
   4. ConcreteProduct（具体产品）— 产品实现
   5. Client（客户端）— 只依赖抽象工厂和抽象产品

 📊 对比工厂方法：
   - 工厂方法：一个工厂创建一种产品（一对一）
   - 抽象工厂：一个工厂创建一组产品（一对多）
   - 抽象工厂通常用工厂方法来实现每个产品的创建
================================================================================
"""

from abc import ABC, abstractmethod


# ============================================================================
# 1. 抽象产品 (AbstractProduct)
# ============================================================================

class Button(ABC):
    """按钮抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> str:
        pass


class Input(ABC):
    """输入框抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def get_value(self) -> str:
        pass


class Menu(ABC):
    """菜单抽象接口"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def select_item(self, index: int) -> str:
        pass


# ============================================================================
# 2. 具体产品 (ConcreteProduct) — Windows 风格
# ============================================================================

class WindowsButton(Button):
    def render(self) -> str:
        return "渲染 [Windows 按钮] — 圆角、蓝色背景"

    def on_click(self) -> str:
        return "Windows 按钮被点击"


class WindowsInput(Input):
    def render(self) -> str:
        return "渲染 [Windows 输入框] — 带边框、白色背景"

    def get_value(self) -> str:
        return "Windows 输入框的内容"


class WindowsMenu(Menu):
    def render(self) -> str:
        return "渲染 [Windows 菜单] — 下拉式、带图标"

    def select_item(self, index: int) -> str:
        return f"Windows 菜单选中第 {index} 项"


# ============================================================================
# 3. 具体产品 (ConcreteProduct) — Mac 风格
# ============================================================================

class MacButton(Button):
    def render(self) -> str:
        return "渲染 [Mac 按钮] — 毛玻璃效果、圆润"

    def on_click(self) -> str:
        return "Mac 按钮被点击"


class MacInput(Input):
    def render(self) -> str:
        return "渲染 [Mac 输入框] — 搜索框风格、无边框"

    def get_value(self) -> str:
        return "Mac 输入框的内容"


class MacMenu(Menu):
    def render(self) -> str:
        return "渲染 [Mac 菜单] — 顶部菜单栏、全局"

    def select_item(self, index: int) -> str:
        return f"Mac 菜单选中第 {index} 项"


# ============================================================================
# 4. 具体产品 (ConcreteProduct) — Linux 风格
# ============================================================================

class LinuxButton(Button):
    def render(self) -> str:
        return "渲染 [Linux 按钮] — 扁平、极简风格"

    def on_click(self) -> str:
        return "Linux 按钮被点击"


class LinuxInput(Input):
    def render(self) -> str:
        return "渲染 [Linux 输入框] — 简洁、灰色边框"

    def get_value(self) -> str:
        return "Linux 输入框的内容"


class LinuxMenu(Menu):
    def render(self) -> str:
        return "渲染 [Linux 菜单] — 传统下拉、右键菜单"

    def select_item(self, index: int) -> str:
        return f"Linux 菜单选中第 {index} 项"


# ============================================================================
# 5. 抽象工厂 (AbstractFactory) — 核心！
# ============================================================================

class GUIFactory(ABC):
    """
    抽象工厂：定义创建一组相关产品的接口。

    🧠 这就是"抽象工厂"名字的来源：
      它本身是"抽象的"（不能直接使用），
      它"生产"的不是一种产品，而是"一组"（一个产品族）。

    📌 每个方法看起来都像"工厂方法"！
      没错！抽象工厂内部通常用工厂方法来实现。
      抽象工厂 = 一组工厂方法的组合。
    """

    @abstractmethod
    def create_button(self) -> Button:
        """创建按钮（看起来像工厂方法，对吧？）"""
        pass

    @abstractmethod
    def create_input(self) -> Input:
        """创建输入框"""
        pass

    @abstractmethod
    def create_menu(self) -> Menu:
        """创建菜单"""
        pass

    def create_all_components(self):
        """
        一次创建所有组件——方便批量创建。

        🔑 这个方法的威力：
          不管是什么平台，调用这个方法就能获得一整套兼容的组件。
          客户端不需要知道具体平台，只需要调用 create_all_components()。
        """
        return {
            "button": self.create_button(),
            "input": self.create_input(),
            "menu": self.create_menu(),
        }


# ============================================================================
# 6. 具体工厂 (ConcreteFactory)
# ============================================================================
# 每个具体工厂负责创建一个完整的产品族。

class WindowsFactory(GUIFactory):
    """Windows 产品族工厂"""

    def create_button(self) -> Button:
        return WindowsButton()

    def create_input(self) -> Input:
        return WindowsInput()

    def create_menu(self) -> Menu:
        return WindowsMenu()


class MacFactory(GUIFactory):
    """Mac 产品族工厂"""

    def create_button(self) -> Button:
        return MacButton()

    def create_input(self) -> Input:
        return MacInput()

    def create_menu(self) -> Menu:
        return MacMenu()


class LinuxFactory(GUIFactory):
    """Linux 产品族工厂"""

    def create_button(self) -> Button:
        return LinuxButton()

    def create_input(self) -> Input:
        return LinuxInput()

    def create_menu(self) -> Menu:
        return LinuxMenu()


# ============================================================================
# 7. 客户端代码
# ============================================================================

class Application:
    """
    客户端应用程序。

    🔑 关键设计：Application 只依赖 GUIFactory（抽象）和
    Button/Input/Menu（抽象），完全不知道具体平台。

    这就是"依赖倒置原则"的极致体现：
      1. 高层模块（Application）不依赖低层模块（WindowsButton 等）
      2. 两者都依赖抽象（GUIFactory, Button, Input, Menu）

    💡 好处：
      - 切换平台只需换一个 Factory 对象
      - 新增平台只需新增 Factory 类 + 产品类
      - 不会出现"Windows 按钮 + Mac 菜单"这种不兼容组合
    """

    def __init__(self, factory: GUIFactory):
        # 通过依赖注入(Dependency Injection)接收工厂
        # Application 不知道具体是哪个平台！
        self._factory = factory
        self._button: Button = None
        self._input: Input = None
        self._menu: Menu = None

    def create_ui(self):
        """创建 UI——通过工厂方法，不依赖具体平台"""
        print(f"\n  使用 {self._factory.__class__.__name__} 创建 UI...")
        self._button = self._factory.create_button()
        self._input = self._factory.create_input()
        self._menu = self._factory.create_menu()

    def render_ui(self):
        """渲染所有组件"""
        print(f"  {self._button.render()}")
        print(f"  {self._input.render()}")
        print(f"  {self._menu.render()}")

    def simulate_interaction(self):
        """模拟用户交互"""
        print(f"  交互: {self._button.on_click()}")
        print(f"  交互: {self._input.get_value()}")
        print(f"  交互: {self._menu.select_item(1)}")


# ============================================================================
# 🧪 测试抽象工厂
# ============================================================================

def test_abstract_factory():
    print("=" * 60)
    print("✅ 抽象工厂模式")
    print("=" * 60)

    # 客户端只需要切换 Factory，整个 UI 风格就变了！
    factories = {
        "Windows": WindowsFactory(),
        "Mac": MacFactory(),
        "Linux": LinuxFactory(),
    }

    for platform_name, factory in factories.items():
        print(f"\n--- {platform_name} 平台 ---")
        app = Application(factory)
        app.create_ui()
        app.render_ui()
        app.simulate_interaction()

    print("\n" + "=" * 60)
    print("✅ 现在想加 Android 平台：")
    print("   1. 新建 AndroidButton, AndroidInput, AndroidMenu 类")
    print("   2. 新建 AndroidFactory 继承 GUIFactory")
    print("   3. 客户端创建 Application(AndroidFactory())")
    print("   ✅ 不需要修改任何已有代码！")


# ============================================================================
# 进阶：通过配置选择工厂
# ============================================================================
"""
实际项目中，通常通过配置文件或环境变量来选择工厂：

    def get_factory_for_platform(platform: str) -> GUIFactory:
        factories = {
            "windows": WindowsFactory(),
            "mac": MacFactory(),
            "linux": LinuxFactory(),
        }
        factory = factories.get(platform.lower())
        if factory is None:
            raise ValueError(f"不支持的平台: {platform}")
        return factory

    # 一行代码切换平台：
    # factory = get_factory_for_platform(os.environ.get("PLATFORM", "windows"))
    # app = Application(factory)

这样"选择工厂"的逻辑也独立出来了，不会污染 Application 类。
"""


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 工厂方法模式和抽象工厂模式有什么区别？
A:   核心区别在于"产品数量"和"产品族"：
    - 工厂方法：一个工厂创建一种产品
      - 适用于"产品等级结构"（如：各种 Logger）
    - 抽象工厂：一个工厂创建一组相关产品（产品族）
      - 适用于"产品族"（如：同一平台的 Button + Input + Menu）
    - 关系：抽象工厂内部通常用工厂方法来实现每个产品的创建

   记忆口诀：
   工厂方法 = 一种产品，多种实现
   抽象工厂 = 一组产品（产品族），多种实现族

Q2: 什么是"产品族"(Product Family)？
A:   产品族是指"一组相关或相互依赖的产品"。
   例如 Windows 平台的 Button、Input、Menu 就构成一个产品族。
   它们之间的约束是：必须一起使用，不能混用跨平台的组件。

   产品族 vs 产品等级结构：
   - 产品等级结构：Button -> WindowsButton, MacButton, LinuxButton
   - 产品族：Windows(Button, Input, Menu) vs Mac(Button, Input, Menu)

Q3: 抽象工厂的优缺点？
A:   优点：
     - 保证产品族内产品的兼容性
     - 客户端与具体产品解耦
     - 符合开闭原则：新增产品族容易
     - 方便切换整个产品族
   缺点：
     - 扩展产品种类困难（新增一种产品，所有工厂都要改）
     - 系统复杂度增加

Q4: 什么时候用抽象工厂？
A:   适合的场景：
     - 系统需要独立于产品的创建、组合和表示
     - 系统需要配置多个产品族中的一个
     - 产品族内的产品必须一起使用
     - 想要提供产品类库，只想暴露接口，不暴露实现

Q5: 抽象工厂在现实框架中的应用？
A:   经典例子：
     - Java 的 AWT/Swing 工具包：不同 Look and Feel 对应不同工厂
     - Qt 框架的 QStyle：不同平台风格
     - 数据库访问层：不同数据库（MySQL, PostgreSQL, SQLite）有不同的
       连接、命令、事务实现——这正是抽象工厂的经典应用
     - 游戏开发：不同关卡/场景需要不同种类的敌人、道具、背景

💡 面试官变种题：
   如果新增一种组件（比如 Checkbox），抽象工厂模式有什么问题？
   答：需要修改抽象工厂接口（新增 create_checkbox()），
   然后所有具体工厂都要实现这个方法——这就是"扩展产品种类困难"的体现。
   解决方案：使用"扩展接口"或"默认实现"来缓解。
"""
