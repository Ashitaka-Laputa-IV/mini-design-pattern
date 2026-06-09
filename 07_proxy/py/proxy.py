"""
================================================================================
Lesson 7: Proxy (代理模式) — 模式实现篇
================================================================================
  Proxy 模式为另一个对象提供一个"替身"或"占位符"，
  以控制对这个对象的访问。

  核心思想：代理和被代理对象实现同一接口，
  客户端不需要知道它操作的是代理还是真实对象。

  三种常见类型：
    1. 虚拟代理 (Virtual Proxy) — 延迟加载，需要时才创建真实对象
    2. 保护代理 (Protection Proxy) — 控制访问权限
    3. 远程代理 (Remote Proxy) — 代表远程对象（如 RPC）

  角色：
    - Subject (抽象主题) — 定义真实对象和代理的共同接口
    - RealSubject (真实主题) — 真正的业务逻辑对象
    - Proxy (代理) — 持有 RealSubject 引用，控制对其访问

  场景：图片查看器
    - 虚拟代理：缩略图点击后才加载原图
    - 保护代理：某些图片需要权限才能查看
================================================================================
"""

from abc import ABC, abstractmethod
import time


# ==============================================================================
# 1. Subject (抽象主题) — 共同接口
# ==============================================================================

class Image(ABC):
    """图片接口：代理和真实图片实现同一接口"""

    @abstractmethod
    def display(self):
        """显示图片"""
        pass

    @abstractmethod
    def get_filename(self) -> str:
        """获取文件名"""
        pass


# ==============================================================================
# 2. RealSubject (真实主题) — 真正的图片
# ==============================================================================

class HighResolutionImage(Image):
    """
    高分辨率图片 — 真正的业务对象
    加载代价高昂（需要从磁盘读取、占用大量内存）
    """

    def __init__(self, filename: str):
        self._filename = filename
        self._image_data = None  # 真实图片数据

    def load_from_disk(self):
        """从磁盘加载图片（耗时操作）"""
        if self._image_data is not None:
            return  # 已经加载过
        print(f"    [加载] {self._filename} 从磁盘加载中... (10MB)", end="")
        time.sleep(0.5)  # 模拟 IO 延迟
        self._image_data = bytearray(10 * 1024 * 1024)  # 模拟 10MB
        print(" ✅ 完成")

    def display(self):
        """显示原图"""
        if self._image_data is None:
            print(f"  ⚠ {self._filename} 未加载！")
            return
        print(f"  [显示原图] {self._filename} ({self._image_data.__len__() / 1024 / 1024:.0f}MB)")

    def get_filename(self) -> str:
        return self._filename


# ==============================================================================
# 3. Virtual Proxy (虚拟代理) — 延迟加载
# ==============================================================================

class ProxyImage(Image):
    """
    图片虚拟代理 — ⭐ 核心实现

    工作原理：
    1. 创建时代理很轻量，只保存文件名
    2. 只有调用 display() 时，才创建并加载真实图片
    3. 一旦加载过，后续调用复用已加载的图片
    """

    def __init__(self, filename: str):
        self._filename = filename
        self._real_image: HighResolutionImage | None = None  # ⭐ 延迟创建！

    def display(self):
        """显示图片 — 触发延迟加载"""
        # ⭐ 真正需要时才加载！
        if self._real_image is None:
            print(f"  [代理] 首次访问 {self._filename}，开始加载...")
            self._real_image = HighResolutionImage(self._filename)
            self._real_image.load_from_disk()
        else:
            print(f"  [代理] {self._filename} 已加载，直接显示")

        self._real_image.display()

    def get_filename(self) -> str:
        return self._filename


# ==============================================================================
# 4. Protection Proxy (保护代理) — 权限控制
# ==============================================================================

class ProtectedImage(Image):
    """
    图片保护代理 — 控制访问权限

    除了延迟加载，还增加了权限校验：
    - 普通用户：只能看缩略图，不能看原图
    - VIP 用户：可以看原图
    """

    def __init__(self, filename: str, required_role: str = "vip"):
        self._filename = filename
        self._required_role = required_role  # 需要什么角色才能查看
        self._real_image: HighResolutionImage | None = None

    def display(self, user_role: str = "normal"):
        """带权限校验的显示"""
        # ⭐ 权限检查
        if user_role != self._required_role and user_role != "admin":
            print(f"  [代理] ❌ 权限不足！需要 '{self._required_role}' 角色才能查看 {self._filename}")
            return False

        # 权限通过，延迟加载
        if self._real_image is None:
            print(f"  [代理] 权限验证通过，开始加载 {self._filename}...")
            self._real_image = HighResolutionImage(self._filename)
            self._real_image.load_from_disk()

        self._real_image.display()
        return True

    def display(self):
        """覆盖父类 display（简化版本用默认角色）"""
        return self.display_with_role("normal")

    def display_with_role(self, user_role: str) -> bool:
        """带角色参数的显示"""
        return self._display_with_role(user_role)

    def _display_with_role(self, user_role: str) -> bool:
        if user_role != self._required_role and user_role != "admin":
            print(f"  [代理] ❌ 权限不足！需要 '{self._required_role}' 角色")
            return False

        if self._real_image is None:
            print(f"  [代理] 权限验证通过，开始加载 {self._filename}...")
            self._real_image = HighResolutionImage(self._filename)
            self._real_image.load_from_disk()

        self._real_image.display()
        return True

    def get_filename(self) -> str:
        return self._filename


# ==============================================================================
# 5. 图片查看器（使用 Proxy 的版本）
# ==============================================================================

class PhotoViewer:
    """
    图片查看器 — 使用虚拟代理

    创建时只创建轻量级 Proxy，不加载真实图片
    """

    def __init__(self, filenames: list):
        print("\n" + "=" * 60)
        print("✅ 使用 Virtual Proxy：启动极快，内存占用极小")
        print("=" * 60)
        start = time.time()

        # ⭐ 只创建代理，不加载真实图片！
        self._images = [ProxyImage(f) for f in filenames]

        elapsed = time.time() - start
        print(f"创建 {len(filenames)} 个代理对象，耗时 {elapsed:.3f}s")
        print(f"内存占用 ≈ 极小（只有文件名和引用）")

    def show_thumbnails(self):
        """显示所有缩略图"""
        print("\n[缩略图模式] 显示所有图片缩略图...")
        for img in self._images:
            # ⭐ 代理对象不会触发加载！
            print(f"  📋 缩略图: {img.get_filename()}")

    def open_image(self, index: int):
        """打开指定图片 — ⭐ 只有此时才加载！"""
        if 0 <= index < len(self._images):
            self._images[index].display()
        else:
            print("索引超出范围")


# ==============================================================================
# 6. 测试
# ==============================================================================

def main():
    print("=" * 60)
    print("✅ Proxy 模式：虚拟代理 + 保护代理")
    print("=" * 60)

    photos = [f"photo_{i}.jpg" for i in range(1, 6)]

    # ---- 虚拟代理测试 ----
    print("\n" + "-" * 40)
    print("场景 1: 虚拟代理 — 延迟加载")
    print("-" * 40)

    viewer = PhotoViewer(photos)

    print("\n用户操作：查看缩略图（不会触发加载）")
    viewer.show_thumbnails()

    print("\n用户操作：打开第 3 张图片（首次加载）")
    viewer.open_image(2)

    print("\n用户操作：再次打开第 3 张图片（缓存，无需加载）")
    viewer.open_image(2)

    print("\n用户操作：打开第 1 张图片（新加载）")
    viewer.open_image(0)

    # ---- 保护代理测试 ----
    print("\n" + "-" * 40)
    print("场景 2: 保护代理 — 权限控制")
    print("-" * 40)

    # 普通图片（所有人可看）
    public_img = ProtectedImage("public_photo.jpg", required_role="normal")
    # VIP 图片（需要 VIP 权限）
    vip_img = ProtectedImage("vip_photo.jpg", required_role="vip")

    print("\n普通用户尝试查看公共图片：")
    public_img.display_with_role("normal")

    print("\n普通用户尝试查看 VIP 图片：")
    vip_img.display_with_role("normal")  # ❌ 被拒绝

    print("\nVIP 用户查看 VIP 图片：")
    vip_img.display_with_role("vip")  # ✅ 通过

    print("\n" + "=" * 60)
    print("🎯 对比：代理 vs 装饰器")
    print("=" * 60)
    print("""
  代理模式 (Proxy)：                装饰器模式 (Decorator)：
  ─────────────────────────         ─────────────────────────
  控制对对象的访问                  为对象添加新行为
  延迟加载、权限控制                动态添加功能
  代理和真实对象接口完全一致        装饰器和被装饰者接口完全一致
  代理通常自己创建真实对象          装饰器接收外部传入的对象
  客户端可能不知道代理的存在        客户端知道装饰过程
  典型：图片懒加载、RPC 代理       典型：Java I/O 流包装

  一句话总结：
  Proxy 控制"能不能用"（访问控制）
  Decorator 控制"怎么用"（功能增强）
  """)


# ==============================================================================
# 面试高频追问 🔥
# ==============================================================================
"""
  1. 代理模式和装饰器模式的区别？
     结构非常相似，但意图完全不同：
     - Proxy: 控制访问（延迟加载、权限控制、日志记录）
     - Decorator: 添加行为（动态增强功能）
     Proxy 创建自己的真实对象，Decorator 接收外部传入的对象。

  2. 虚拟代理和懒加载的关系？
     虚拟代理是懒加载(Lazy Loading)的一种实现方式。
     还有其他懒加载方式：Lazy Initialization、Value Holder 等。
     虚拟代理的优点是客户端完全无感知——接口一致。

  3. 动态代理是什么？
     动态代理在运行时动态创建代理类，不需要手动编写代理类。
     Python 可以用 __getattr__ 实现动态代理，Java 用 java.lang.reflect.Proxy。
     动态代理的优点是通用性强，一个代理类可以代理多种类型。

  4. 保护代理和访问者模式的区别？
     保护代理控制"谁能访问"（权限前置判断）
     访问者模式定义"对对象的操作"（操作分离）
     前者是结构型模式，后者是行为型模式。

  5. 代理模式的缺点？
     - 增加系统复杂度（多一层间接访问）
     - 可能影响性能（代理层增加调用开销）
     - 如果真实对象和代理接口不一致，需要适配
"""


if __name__ == "__main__":
    main()
