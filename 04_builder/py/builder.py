"""
================================================================================
Lesson 4: Builder — 构建器模式（模式实现篇）[创建型]
================================================================================
  上一节的 bad_builder.py 我们看到了 Telescoping Constructor 的问题，
  现在来看看 Builder 模式如何优雅地解决这些问题。

  📐 设计模式定义：
    Builder 模式将一个复杂对象的构建与它的表示分离，
    使得同样的构建过程可以创建不同的表示。

  🎯 解决的问题：
    - 构造函数参数过多（>3-4个）
    - 参数顺序容易搞错
    - 需要创建不同配置的相似对象
    - 希望创建不可变对象（Builder 完成后产品不可变）

  💡 核心思想：
    把"对象构造"和"对象表示"分开。
    Builder 负责一步步构造，Director 负责编排构建步骤。

  🆚 Builder vs 工厂模式：
    - 工厂：一步创建完整对象，适合简单创建
    - Builder：分步创建，对构造过程有精细控制，适合复杂对象
================================================================================
"""


# ============================================================================
# 核心产品类：Computer（电脑）
# ============================================================================

class Computer:
    """
    🎯 最终产品——构建完成后不可变（Immutable）

    注意：构造函数是私有的（用 _ 表示），客户端只能通过 Builder 创建。
    所有属性只读（不提供 setter），保证对象创建后不被修改。
    """

    def __init__(self):
        """
        使用私有构造函数，通过 Builder 来创建。
        ⚠️ 不直接暴露给客户端，客户端用 ComputerBuilder 创建。
        """
        # 所有属性设为私有，只提供 getter
        self._cpu = None
        self._ram = None
        self._storage = None
        self._gpu = "集成显卡"
        self._os = "无"
        self._has_wifi = False
        self._has_bluetooth = False
        self._keyboard = "标准键盘"
        self._mouse = "标准鼠标"

    # --- 只读属性（没有 setter！）---
    @property
    def cpu(self):
        return self._cpu

    @property
    def ram(self):
        return self._ram

    @property
    def storage(self):
        return self._storage

    @property
    def gpu(self):
        return self._gpu

    @property
    def os(self):
        return self._os

    @property
    def has_wifi(self):
        return self._has_wifi

    @property
    def has_bluetooth(self):
        return self._has_bluetooth

    @property
    def keyboard(self):
        return self._keyboard

    @property
    def mouse(self):
        return self._mouse

    def __str__(self) -> str:
        """显示完整配置"""
        lines = [
            "┌─ 电脑配置 ─────────────────────────┐",
            f"  CPU        : {self._cpu}",
            f"  内存       : {self._ram}",
            f"  硬盘       : {self._storage}",
            f"  显卡       : {self._gpu}",
            f"  操作系统   : {self._os}",
            f"  WiFi       : {'✓' if self._has_wifi else '✗'}",
            f"  蓝牙       : {'✓' if self._has_bluetooth else '✗'}",
            f"  键盘       : {self._keyboard}",
            f"  鼠标       : {self._mouse}",
            "└──────────────────────────────────────┘",
        ]
        return "\n".join(lines)


# ============================================================================
# Builder：电脑构建器
# ============================================================================

class ComputerBuilder:
    """
    🎯 Builder 类——负责一步步构建 Computer 对象

    核心设计：
    1. 链式调用（Fluent Interface）：每个 setter 都返回 self
    2. 必填参数在 build() 时校验
    3. build() 返回构造完成的不可变对象

    💡 链式调用的秘诀：每个 set_xxx() 方法 return self
    """

    def __init__(self):
        """初始化一个空的 Computer 实例"""
        self._computer = Computer()

    # --- 链式 setter 方法 ---

    def set_cpu(self, cpu: str) -> "ComputerBuilder":
        """
        设置 CPU
        返回 self 以支持链式调用
        """
        self._computer._cpu = cpu
        return self

    def set_ram(self, ram: str) -> "ComputerBuilder":
        """设置内存大小"""
        self._computer._ram = ram
        return self

    def set_storage(self, storage: str) -> "ComputerBuilder":
        """设置硬盘"""
        self._computer._storage = storage
        return self

    def set_gpu(self, gpu: str) -> "ComputerBuilder":
        """设置显卡"""
        self._computer._gpu = gpu
        return self

    def set_os(self, os: str) -> "ComputerBuilder":
        """设置操作系统"""
        self._computer._os = os
        return self

    def enable_wifi(self) -> "ComputerBuilder":
        """开启 WiFi"""
        self._computer._has_wifi = True
        return self

    def enable_bluetooth(self) -> "ComputerBuilder":
        """开启蓝牙"""
        self._computer._has_bluetooth = True
        return self

    def set_keyboard(self, keyboard: str) -> "ComputerBuilder":
        """设置键盘"""
        self._computer._keyboard = keyboard
        return self

    def set_mouse(self, mouse: str) -> "ComputerBuilder":
        """设置鼠标"""
        self._computer._mouse = mouse
        return self

    def build(self) -> Computer:
        """
        🚀 构建最终产品

        在 build() 中进行校验，确保必填项已设置。
        构建完成后，返回的 Computer 对象不再可变。
        """
        # 校验必填参数
        if not self._computer._cpu:
            raise ValueError("CPU 是必填项！")
        if not self._computer._ram:
            raise ValueError("内存是必填项！")
        if not self._computer._storage:
            raise ValueError("硬盘是必填项！")

        # 返回构建好的对象
        computer = self._computer
        # 清空 builder 中的引用，防止继续修改
        self._computer = None
        return computer


# ============================================================================
# Director：导演者（可选组件）
# ============================================================================

class ComputerDirector:
    """
    🎯 Director（导演者）——提供常用预设配置

    Director 不是 Builder 模式的必要组件，但它非常有用。
    作用：封装"构建步骤的顺序"，提供常用的预制方案。

    如果把 Builder 比作"菜单"（你能点什么菜），
    Director 就是"套餐"（帮你搭配好了）。
    """

    @staticmethod
    def create_office_pc() -> Computer:
        """
        💼 办公电脑预设
        特点：够用就行，性价比高
        """
        return (
            ComputerBuilder()
            .set_cpu("Intel i5-13400")
            .set_ram("16GB DDR4")
            .set_storage("512GB SSD")
            .set_gpu("集成显卡")  # 办公不需要独显
            .set_os("Windows 11 家庭版")
            .enable_wifi()
            .enable_bluetooth()
            .set_keyboard("标准键盘")
            .set_mouse("标准鼠标")
            .build()
        )

    @staticmethod
    def create_gaming_pc() -> Computer:
        """
        🎮 游戏电脑预设
        特点：高性能 CPU + 顶级显卡 + 大内存
        """
        return (
            ComputerBuilder()
            .set_cpu("Intel i9-14900K")
            .set_ram("64GB DDR5")
            .set_storage("2TB NVMe SSD")
            .set_gpu("NVIDIA RTX 4090")
            .set_os("Windows 11 Pro")
            .enable_wifi()
            .enable_bluetooth()
            .set_keyboard("机械键盘 (青轴)")
            .set_mouse("游戏鼠标 (6400DPI)")
            .build()
        )

    @staticmethod
    def create_programmer_pc() -> Computer:
        """
        👨‍💻 程序员电脑预设
        特点：大内存 + 多核心 + Linux
        """
        return (
            ComputerBuilder()
            .set_cpu("AMD Ryzen 9 7950X")
            .set_ram("128GB DDR5")
            .set_storage("2TB NVMe SSD + 4TB HDD")
            .set_gpu("集成显卡")  # 程序员不需要好显卡
            .set_os("Ubuntu 24.04 LTS")
            .enable_wifi()
            .set_keyboard("静音键盘")
            .set_mouse("人体工学鼠标")
            .build()
        )

    @staticmethod
    def create_minimal_server() -> Computer:
        """
        🖥️ 最小化服务器预设
        特点：不需要外设，不需要 GUI
        """
        return (
            ComputerBuilder()
            .set_cpu("Intel Xeon E-2388G")
            .set_ram("32GB ECC DDR4")
            .set_storage("1TB NVMe SSD")
            .set_gpu("集成显卡")  # 服务器不需要显卡
            .set_os("CentOS Stream 9")
            .build()
        )


# ============================================================================
# 🧪 演示 Builder 模式
# ============================================================================

def test_builder_pattern():
    """展示 Builder 模式的各种用法"""

    print("=" * 60)
    print("✅ Builder 模式演示")
    print("=" * 60)

    # ---- 1. 自由搭配：链式调用 ----
    print("\n1️⃣  自由搭配（链式调用）")
    print("-" * 40)

    gaming_rig = (
        ComputerBuilder()
        .set_cpu("AMD Ryzen 7 7800X3D")
        .set_ram("32GB DDR5")
        .set_storage("1TB NVMe SSD")
        .set_gpu("NVIDIA RTX 4070 Ti")
        .set_os("Windows 11")
        .enable_wifi()
        .enable_bluetooth()
        .set_keyboard("机械键盘")
        .set_mouse("游戏鼠标")
        .build()
    )
    print(gaming_rig)
    print(f"  📍 对象地址: {id(gaming_rig)}")

    # ---- 2. 只设置必填项 ----
    print("\n2️⃣  只配置核心部件（其他用默认值）")
    print("-" * 40)

    basic_pc = (
        ComputerBuilder()
        .set_cpu("Intel i3-12100")
        .set_ram("8GB DDR4")
        .set_storage("256GB SSD")
        .build()
    )
    print(basic_pc)

    # ---- 3. 使用 Director 预设 ----
    print("\n3️⃣  Director 预设方案")
    print("-" * 40)

    print("💼 办公电脑:")
    office = ComputerDirector.create_office_pc()
    print(office)

    print("\n🎮 游戏电脑:")
    gaming = ComputerDirector.create_gaming_pc()
    print(gaming)

    print("\n👨‍💻 程序员电脑:")
    programmer = ComputerDirector.create_programmer_pc()
    print(programmer)

    print("\n🖥️ 服务器:")
    server = ComputerDirector.create_minimal_server()
    print(server)

    # ---- 4. 不可变性验证 ----
    print("\n4️⃣  不可变性验证（无 setter）")
    print("-" * 40)

    try:
        # Computer 对象没有 setter，不能修改
        gaming_rig._cpu = "hacked CPU"  # 虽然 Python 没有真正私有，
        # 但按约定 _ 开头的属性不应该直接修改
        print(f"  ⚠️ 通过 _cpu 修改了: {gaming_rig.cpu}")
        print(f"  （Python 没有真正的私有，但 Builder 模式约定禁止这样做）")
    except AttributeError as e:
        print(f"  ✅ 不能修改: {e}")

    # ---- 5. 校验错误演示 ----
    print("\n5️⃣  必填参数校验")
    print("-" * 40)

    try:
        # 忘记设置必填项
        incomplete = (
            ComputerBuilder()
            .set_cpu("Intel i5")
            # 忘记设置 ram 和 storage
            .build()
        )
    except ValueError as e:
        print(f"  ✅ build() 时校验: {e}")

    # ---- 6. 参数顺序无关 ----
    print("\n6️⃣  参数顺序无关——再也不怕传错了！")
    print("-" * 40)

    # 调用顺序可以任意，因为每个 setter 都有明确的方法名
    pc_a = (
        ComputerBuilder()
        .set_ram("16GB")  # 先设内存
        .set_cpu("Intel i7")  # 再设 CPU
        .set_storage("1TB")
        .build()
    )
    pc_b = (
        ComputerBuilder()
        .set_cpu("Intel i7")  # 先设 CPU
        .set_storage("1TB")  # 再设硬盘
        .set_ram("16GB")  # 最后设内存
        .build()
    )
    print(f"  pc_a: CPU={pc_a.cpu}, RAM={pc_a.ram}")
    print(f"  pc_b: CPU={pc_b.cpu}, RAM={pc_b.ram}")
    print(f"  结果相同，顺序不影响最终产品")


# ============================================================================
# 对比：反模式 vs Builder 模式
# ============================================================================

def comparison():
    """直观对比 Telescoping Constructor 和 Builder 模式的代码质量"""

    print("\n" + "=" * 60)
    print("📊 对比：反模式 vs Builder 模式")
    print("=" * 60)

    print("""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     反模式（Telescoping）                          │
    ├─────────────────────────────────────────────────────────────────────┤
    │  Computer("Intel i7", "16GB", "1TB", "RTX 3060",                  │
    │           "Windows 11", True, True, "机械键盘", "游戏鼠标")        │
    │                                                                     │
    │  ❌ 9 个位置参数，谁记得住顺序？                                    │
    │  ❌ True, True 是什么意思？WiFi？蓝牙？                             │
    │  ❌ 少传一个参数就全乱了                                            │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                     ✅ Builder 模式                                │
    ├─────────────────────────────────────────────────────────────────────┤
    │  ComputerBuilder()                                                  │
    │      .set_cpu("Intel i7")         ← 方法名说明含义                  │
    │      .set_ram("16GB")                                               │
    │      .set_storage("1TB")                                            │
    │      .set_gpu("RTX 3060")                                           │
    │      .set_os("Windows 11")                                          │
    │      .enable_wifi()              ← 没有 True/False 歧义             │
    │      .enable_bluetooth()                                            │
    │      .set_keyboard("机械键盘")                                      │
    │      .set_mouse("游戏鼠标")                                         │
    │      .build()                   ← 最后一步，构建不可变对象          │
    │                                                                     │
    │  ✅ 每个方法名说明参数含义                                           │
    │  ✅ 顺序可以任意，不再担心传错                                       │
    │  ✅ 可选参数可以省略，用默认值                                       │
    │  ✅ build() 时校验必填项                                             │
    └─────────────────────────────────────────────────────────────────────┘
    """)


if __name__ == "__main__":
    test_builder_pattern()
    comparison()

    print("\n" + "=" * 60)
    print("💡 小结：什么时候用 Builder？")
    print("   - 构造函数参数 > 3-4 个")
    print("   - 对象有大量可选属性")
    print("   - 需要创建不同配置的相似对象")
    print("   - 希望创建不可变对象")
    print("=" * 60)


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: Builder 模式和工厂模式有什么区别？
    ┌─────────────────────────────────────────────────────────────────────┐
    │          工厂模式 (Factory)          │   Builder 模式               │
    ├─────────────────────────────────────────────────────────────────────┤
    │ 一步创建完整对象                      │ 分步构建，精细控制           │
    │ 适合简单对象的创建                    │ 适合复杂对象的创建           │
    │ 隐藏创建逻辑                          │ 暴露创建步骤                 │
    │ 产品通常是同一类型的变体              │ 产品内部结构可能差异很大     │
    │ 示例：createLogger(type="file")       │ 示例：builder.setX().setY()  │
    └─────────────────────────────────────────────────────────────────────┘
    简单说：工厂负责"做什么"，Builder 负责"怎么做"。

Q2: Builder 模式如何保证不可变（Immutable）？
    - 产品类的构造函数设为私有（Python 用 _ 约定）
    - 不提供 setter 方法
    - 所有属性在 build() 完成后固定
    - Builder 在 build() 后清空内部引用，防止继续修改

Q3: 什么是链式调用（Fluent Interface）？如何实现？
    链式调用让代码读起来像自然语言。
    实现关键：每个 setter 方法返回 self（或 this）。
    优点：代码可读性强，写起来流畅。
    缺点：调试时断点不好定位（都在一行）。

Q4: Director 是必要的吗？
    不是。Director 是可选组件，用于封装常见的构建步骤。
    没有 Director 时，客户端直接使用 Builder 即可。
    Director 相当于"预定义的套餐"。

Q5: Python 中有什么替代方案？
    - @dataclass：适合简单的数据容器，但参数列表仍然长
    - dict / **kwargs：失去类型提示和 IDE 支持
    - namedtuple：不可变，但参数列表问题仍在
    - Builder 模式在参数多时仍然是最佳选择

Q6: Builder 模式的缺点？
    - 代码量增加（需要多写一个 Builder 类）
    - 如果对象不复杂，用 Builder 反而过度设计
    - 创建对象需要先创建 Builder（额外开销）

💡 面试官变种题：
    如果一个对象有 20+ 个属性，但很多属性之间有依赖关系怎么办？
    （比如选了 "机械键盘" 就自动选择 "游戏鼠标"）
    思路：在 set_keyboard() 中自动调用 set_mouse()，或者用 Director 封装规则。
"""
