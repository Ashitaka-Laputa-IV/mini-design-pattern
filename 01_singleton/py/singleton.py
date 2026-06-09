"""
================================================================================
 Lesson 1: Singleton — 单例模式（模式实现）
================================================================================
  上节课的 bad_singleton.py 我们看到了问题，
  现在来看看设计模式怎么解决。
================================================================================

  📐 设计模式定义：
    单例模式(Singleton)确保一个类只有一个实例，并提供一个全局访问点。

  🎯 解决的问题：
    - 控制实例数量：有些对象只需一个（配置、日志、线程池、数据库连接池）
    - 提供全局访问点：避免全局变量污染命名空间

  💡 实现要点：
    1. 把构造函数设为私有（限制外部 new）
    2. 类自己保存唯一实例
    3. 通过静态方法/类方法提供全局访问
    4. ⚠ 线程安全！（面试高频考点）
"""

import threading


# ============================================================================
# 实现 1：经典单例（线程安全）
# ============================================================================

class SingletonMeta(type):
    """
    🧠 元类(Metaclass)方式实现单例——面试加分项

    原理：元类是"类的类"，控制类的创建过程。
    当 SingletonMeta 被用作类的 metaclass 时，
    每次 new 该类都会先走 __call__ 方法。
    Python 中 __call__ 控制的是 "ClassName()" 这个行为。
    """

    _instances = {}       # 类字典：{类名: 实例}
    _lock = threading.Lock()  # 线程锁

    def __call__(cls, *args, **kwargs):
        """
        重写 __call__：控制"类被调用实例化"的行为。

        流程：
          1. 先检查字典里有没有这个类的实例
          2. 如果没有，加锁再检查一次（双重检查锁定 Double-checked Locking）
          3. 创建实例并保存
          4. 返回实例
        """
        # 第一次检查：避免每次调用都加锁（性能优化）
        if cls not in cls._instances:
            with cls._lock:
                # 第二次检查：防止两个线程同时通过第一次检查
                if cls not in cls._instances:
                    print(f"  [创建] {cls.__name__} 唯一实例")
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    """
    使用 SingletonMeta 元类后，ConfigManager() 永远返回同一个对象。
    不需要任何额外代码！
    """

    def __init__(self):
        """注意：__init__ 在单例模式下会多次调用！
        需要确保初始化逻辑只执行一次。
        """
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._config = self._load_config()
        self._initialized = True

    def _load_config(self):
        # 模拟加载配置文件
        print("  [加载] 读取配置文件 config.json...")
        return {"db_host": "localhost", "db_port": 3306, "debug": True}

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def set(self, key: str, value):
        """更新配置，所有模块立即可见"""
        self._config[key] = value

    def __str__(self):
        return f"ConfigManager@{id(self)}: {self._config}"


# ============================================================================
# 实现 2：装饰器方式（Pythonic 风格）
# ============================================================================

def singleton(cls):
    """
    装饰器实现单例——最简洁的 Python 风格

    原理：用一个字典保存类名→实例的映射，
    每次调用类时直接返回已有实例。
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    print(f"  [创建·装饰器] {cls.__name__} 唯一实例")
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    """
    用 @singleton 装饰器实现的日志类。

    💡 Logger 是最常见的单例使用场景之一。
    """

    def __init__(self):
        self.logs = []

    def info(self, msg: str):
        self.logs.append(f"[INFO] {msg}")

    def error(self, msg: str):
        self.logs.append(f"[ERROR] {msg}")

    def show(self):
        for log in self.logs:
            print(log)

    # ❗注意：使用装饰器方式后，Logger() 返回的是 get_instance 函数
    # 所以 isinstance(Logger(), Logger) 会报错
    # 面试时提到这个局限性可以加分！


# ============================================================================
# 实现 3：模块级单例（Python 最推荐的方式）
# ============================================================================

class _DatabasePool:
    """
    模块级单例：利用 Python 模块导入是单例的这一特性。

    原理：Python 模块在第一次 import 时被加载并缓存，
    之后再次 import 返回的是同一个模块对象。
    """

    def __init__(self):
        self._connections = []
        print("  [创建·模块级] DatabasePool 唯一实例")

    def acquire(self):
        print("  获取数据库连接")
        return "conn_1"

    def release(self, conn):
        print(f"  释放连接: {conn}")


# 在模块级别创建实例——这才是 Python 中最推荐的单例方式！
# 外部使用: from singleton import db_pool
db_pool = _DatabasePool()


# ============================================================================
# 实现 4：__new__ 方法（经典 Python 方式）
# ============================================================================

class ThreadSafeSingleton:
    """
    __new__ 方式实现单例——面试最常被问到的写法

    __new__ vs __init__:
      - __new__：创建对象（静态方法），在 __init__ 之前调用
      - __init__：初始化对象
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print(f"  [创建·__new__] {cls.__name__} 唯一实例")
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """避免重复初始化"""
        if self._initialized:
            return
        print("  [初始化] 执行一次性初始化工作")
        self._initialized = True


# ============================================================================
# 🧪 测试所有单例实现
# ============================================================================

def test_singletons():
    print("\n" + "=" * 50)
    print("1️⃣  元类方式 Singleton (线程安全)")
    print("=" * 50)

    def create_config():
        c = ConfigManager()
        print(f"    线程内获取: {id(c)}")

    threads = []
    for i in range(3):
        t = threading.Thread(target=create_config, name=f"T{i}")
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    c1 = ConfigManager()
    c2 = ConfigManager()
    print(f"\n  c1 is c2? {c1 is c2}")
    print(f"  c1 == c2? {c1 == c2}")
    c1.set("debug", False)
    print(f"  c1 修改后 c2 也变了: {c2.get('debug')}")  # False

    print("\n" + "=" * 50)
    print("2️⃣  装饰器方式 Singleton")
    print("=" * 50)

    log1 = Logger()
    log2 = Logger()
    log1.info("第一条日志")
    log2.info("第二条日志")
    print("  log1 和 log2 的日志在一起: ")
    log1.show()  # 两条日志都在

    print("\n" + "=" * 50)
    print("3️⃣  模块级 Singleton")
    print("=" * 50)

    # 模拟多次 import 得到同一个对象
    from singleton import db_pool as pool1
    from singleton import db_pool as pool2
    print(f"  pool1 is pool2? {pool1 is pool2}")

    print("\n" + "=" * 50)
    print("4️⃣  __new__ 方式 Singleton")
    print("=" * 50)

    s1 = ThreadSafeSingleton()
    s2 = ThreadSafeSingleton()
    print(f"  s1 is s2? {s1 is s2}")  # True


if __name__ == "__main__":
    test_singletons()


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 单例模式的缺点？
    - 全局状态，不利于测试（单元测试需要隔离）
    - 违反单一职责原则（既管理实例，又做业务）
    - 多线程环境需要额外处理

Q2: Python 中实现单例有哪几种方式？
    ① 元类 (metaclass) —— 面试最喜欢问
    ② 装饰器 (@singleton)
    ③ 模块级单例 —— Python 中最推荐的
    ④ __new__ 方法
    ⑤ 共享状态 (Monostate / Borg 模式)

Q3: 单例和全局变量有什么区别？
    全局变量：只是变量，没有"唯一性约束"
    单例模式：通过封装保证"唯一实例"

Q4: C++ 中如何实现线程安全的单例？
    C++11 之后推荐 Meyers' Singleton：
        static Singleton& getInstance() {
            static Singleton instance;  // C++11 保证线程安全
            return instance;
        }

💡 面试官变种题：如果让你写一个"多例模式"呢？
    比如数据库连接池，有固定数量的连接。
    思路：把 _instances 从单个改为固定大小的列表，用轮询或队列分配。
"""
