"""
================================================================================
Lesson 4: Builder — 构建器模式（反模式篇）[创建型]
================================================================================
 📖 本课采用"反模式驱动"方式：
    先看坏代码长什么样，感受痛点，再引入设计模式解决问题。

 🔑 面试频率：★★★★☆（中高频）
================================================================================
"""

"""
===============================================================================
 🎬 场景：你们团队在做一个"电脑配置系统"

  需求：用户可以在线自定义电脑配置，选择 CPU、内存、硬盘、显卡、操作系统等。

  同事小明写了一个 Computer 类：

      computer = Computer("Intel i7", "16GB", "1TB", "RTX 3060",
                          "Windows 11", true, true, "机械键盘", "RGB鼠标")

  😕 你觉得哪里不对劲？先想想再看下面的分析。

  典型的 Telescoping Constructor（伸缩构造函数）反模式！
===============================================================================
"""


# ============================================================================
# 反模式：Telescoping Constructor（伸缩构造函数）
# ============================================================================

class Computer:
    """
    ❌ 坏味道：Telescoping Constructor（伸缩构造函数）

    问题分析：
    1. 参数过多——构造函数的参数多达 9 个
    2. 参数顺序容易搞错——CPU 和 内存的顺序写反了也不知道
    3. 可选参数导致大量重载——不同配置需要不同数量的参数
    4. 可读性极差——Computer(True, False, True) 谁知道这些 bool 什么意思？
    5. 客户端代码难以阅读和维护
    """

    def __init__(
        self,
        cpu: str,
        ram: str,
        storage: str,
        gpu: str = "集成显卡",
        os: str = "无",
        has_wifi: bool = False,
        has_bluetooth: bool = False,
        keyboard: str = "标准键盘",
        mouse: str = "标准鼠标",
    ):
        """
        参数列表（已按必选→可选排列，但仍然太多）：

        📌 必选参数：
            cpu     — CPU 型号（如 "Intel i7"）
            ram     — 内存大小（如 "16GB"）
            storage — 硬盘大小（如 "1TB"）

        📌 可选参数（默认值）：
            gpu         — 显卡（默认 "集成显卡"）
            os          — 操作系统（默认 "无"）
            has_wifi    — 是否支持 WiFi
            has_bluetooth — 是否支持蓝牙
            keyboard    — 键盘类型
            mouse       — 鼠标类型

        ❗ 问题：如果我想配一台只有 cpu、ram、storage 的电脑，
            但想要蓝牙，必须传 has_wifi=False, has_bluetooth=True！
        """
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.os = os
        self.has_wifi = has_wifi
        self.has_bluetooth = has_bluetooth
        self.keyboard = keyboard
        self.mouse = mouse

    def __str__(self) -> str:
        """显示电脑配置"""
        parts = [
            f"CPU: {self.cpu}",
            f"内存: {self.ram}",
            f"硬盘: {self.storage}",
            f"显卡: {self.gpu}",
            f"系统: {self.os}",
            f"WiFi: {'有' if self.has_wifi else '无'}",
            f"蓝牙: {'有' if self.has_bluetooth else '无'}",
            f"键盘: {self.keyboard}",
            f"鼠标: {self.mouse}",
        ]
        return " | ".join(parts)


# ============================================================================
# 🧪 演示反模式的问题
# ============================================================================

def demonstrate_anti_pattern():
    """
    展示 Telescoping Constructor 的各种问题。
    运行这段代码，看看实际使用中的痛点。
    """

    print("=" * 60)
    print("❌ 反模式：Telescoping Constructor（伸缩构造函数）")
    print("=" * 60)

    # ---- 问题 1：参数顺序容易搞错 ----
    print("\n1️⃣  参数顺序错误的风险")

    # 正确的顺序
    pc1 = Computer("Intel i7", "16GB", "1TB", "RTX 3060", "Windows 11")
    print(f"  ✅ 正确: {pc1}")

    # 容易犯的错误：CPU 和 内存顺序写反
    pc2 = Computer("16GB", "Intel i7", "1TB", "RTX 3060", "Windows 11")
    #                                    ↑ 编译不会报错！运行时才发现问题
    print(f"  ❌ 顺序错: {pc2}")
    print(f"     意图是 CPU=i7, 内存=16GB")
    print(f"     实际变成 CPU=16GB, 内存=i7 ← 荒谬但不会报错！")

    # ---- 问题 2：可选参数需要填充中间值 ----
    print("\n2️⃣  可选参数需要填充中间值")

    # 我只想要 CPU、内存、硬盘、蓝牙（不想要 WiFi）
    # 但蓝牙在 has_wifi 后面，必须显式传 has_wifi 的默认值
    pc3 = Computer(
        "AMD Ryzen 7",
        "32GB",
        "2TB",
        gpu="RTX 4070",
        os="Ubuntu",
        has_wifi=False,  # ← 必须显式写 False，否则传不到 has_bluetooth
        has_bluetooth=True,
    )
    print(f"  😤 中间参数必须填充: {pc3}")
    print(f"     为了设置 has_bluetooth=True，不得不传 has_wifi=False")

    # ---- 问题 3：Bool 参数含义不明 ----
    print("\n3️⃣  Bool 参数含义不明")

    # 不看构造函数定义，你能猜出下面这些 True/False 是什么意思吗？
    pc4 = Computer("Intel i5", "8GB", "512GB", os="Windows 11", True, False)
    #                                                                  ↑  ↑
    #                                                          has_wifi? 蓝牙?
    print(f"  🤔 谁能看懂 True, False 什么意思？")
    print(f"     结果: CPU=i5, 8GB, 512GB, Win11, WiFi有, 蓝牙无")

    # ---- 问题 4：大量重载（Python 通过默认参数解决，但可读性差） ----
    print("\n4️⃣  可读性差")

    # 实际项目中，这种代码非常常见：
    pc5 = Computer(
        "Intel Core i9-13900K",
        "64GB DDR5",
        "2TB NVMe SSD",
        "NVIDIA RTX 4090",
        "Windows 11 Pro",
        True,
        True,
        "机械键盘",
        "游戏鼠标",
    )
    print(f"  😵 这 9 个参数真的能一眼看懂吗？")
    print(f"     尤其是中间那几个 True/True... 什么意思来着？")

    print("\n" + "=" * 60)
    print("💡 结论：当构造函数的参数超过 3-4 个时，")
    print("   就应该考虑使用 Builder 模式了！")
    print("=" * 60)


# ============================================================================
# 另一个反模式：JavaBean 模式（先构造后设值）
# ============================================================================

class ComputerJavaBean:
    """
    ❌ 另一种反模式：JavaBean 模式（先 new 空对象，再逐个 set）

    有的人会说："那我不用长参数列表，我用无参构造 + setter 不就好了？"

    问题：
    1. 对象在构造过程中处于不一致状态（部分属性已设，部分未设）
    2. 无法创建不可变对象（所有属性都需要 setter）
    3. 容易忘记设置某些必填属性
    """

    def __init__(self):
        # 先创建一个空壳子
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = "集成显卡"
        self.os = "无"
        self.has_wifi = False
        self.has_bluetooth = False
        self.keyboard = "标准键盘"
        self.mouse = "标准鼠标"

    def set_cpu(self, cpu: str):
        self.cpu = cpu

    def set_ram(self, ram: str):
        self.ram = ram

    # ... 更多的 setter 方法 ...
    # (省略，因为这种模式本身就有问题)


def demonstrate_javabean_antipattern():
    """展示 JavaBean 模式的问题"""

    print("\n" + "=" * 60)
    print("❌ 另一种反模式：JavaBean（先构造后设值）")
    print("=" * 60)

    pc = ComputerJavaBean()
    # 此时 pc 对象处于"半构造"状态
    pc.set_cpu("Intel i7")
    # 如果在多线程环境中，另一个线程可能在这里读取 pc
    # 此时 ram 还是 None！—— 对象状态不一致！
    pc.set_ram("16GB")

    print(f"  ⚠️ 对象在构造过程中处于不一致状态")
    print(f"     cpu={pc.cpu}, ram={pc.ram}")  # 假设在 set_cpu 和 set_ram 之间被读取

    # 而且无法保证必填参数被设置了
    pc2 = ComputerJavaBean()
    pc2.set_cpu("Intel i7")
    # 忘记设置 ram 和 storage！
    print(f"  😱 必填属性可能被遗漏: cpu={pc2.cpu}, ram={pc2.ram}, storage={pc2.storage}")


if __name__ == "__main__":
    demonstrate_anti_pattern()
    demonstrate_javabean_antipattern()

    print("\n" + "=" * 60)
    print("👉 请继续看 builder.py，看看 Builder 模式如何解决这些问题！")
    print("=" * 60)


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 除了 Telescoping Constructor，还有哪些"坏味道"？
    - 过多的参数（>3-4个）
    - 多个同类型参数相邻（容易传反）
    - bool 参数含义不明确
    - 方法/构造函数中有大段"参数赋值"样板代码

Q2: 为什么不用 JavaBean 模式替代？
    - 对象状态不一致：构造过程中可能被其他线程读取
    - 不可变性丧失：需要 setter 就不能做不可变对象
    - 必填属性无法强制：容易忘记设置关键属性

Q3: Python 中怎么处理多个参数？
    - 可以用 **kwargs 字典，但失去了类型提示和 IDE 自动补全
    - 可以用 dataclass，但创建时参数列表仍然长
    - 推荐：参数少用普通构造，参数多用 Builder
"""
