"""
================================================================================
 Lesson 01: Singleton — 单例模式练习
================================================================================
 本文件包含 3 道练习题，难度递进：
    练习1：基础单例 — 用 __new__ 方式实现 AppConfig
    练习2：线程安全单例 — 用元类方式实现 DBConnectionPool
    练习3：思考题 — 多例模式 Multiton

 说明：
   - 所有 TODO 处需要你补全代码
   - 完成练习后，运行 test_exercise.py 验证正确性
================================================================================
"""

import threading
from abc import ABC, abstractmethod


# ============================================================================
# 练习1：基础单例 — __new__ 方式
# ============================================================================
# 实现 AppConfig 类，要求：
#   1. 用 __new__ 方式确保只有一个实例
#   2. 从 dict 加载配置（通过 __init__ 传入）
#   3. get(key, default=None) 方法获取配置值
# ============================================================================

class AppConfig:
    """应用配置类 — 单例模式（__new__ 方式）

    用法：
        config = AppConfig({"db_host": "localhost", "debug": True})
        config.get("db_host")  # => "localhost"
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # TODO: 实现单例逻辑
        # 1. 第一次检查 _instance 是否为 None
        # 2. 加锁
        # 3. 第二次检查 _instance
        # 4. 如果仍为 None，调用 super().__new__(cls)
        # 5. 返回 _instance
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: dict = None):
        # TODO: 实现初始化逻辑，确保只初始化一次
        # 提示：用 _initialized 标志位避免重复初始化
        if self._initialized:
            return
        self._config = config or {}
        self._initialized = True

    def get(self, key: str, default=None):
        """获取配置值"""
        # TODO: 返回 key 对应的值，不存在则返回 default
        return self._config.get(key, default)


# ============================================================================
# 练习2：线程安全单例 — 元类方式
# ============================================================================
# 实现 DBConnectionPool，要求：
#   1. 用元类 SingletonMeta 保证单例
#   2. acquire() — 获取一个连接（限制最多 3 个连接）
#   3. release(conn) — 释放一个连接
#   4. 线程安全
# ============================================================================

class SingletonMeta(type):
    """单例元类 — 线程安全"""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # TODO: 实现元类单例逻辑（双重检查锁定）
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DBConnectionPool(metaclass=SingletonMeta):
    """数据库连接池 — 线程安全单例

    管理最多 3 个数据库连接。
    """

    MAX_CONNECTIONS = 3

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._available = [f"conn_{i+1}" for i in range(self.MAX_CONNECTIONS)]
        self._in_use = set()
        self._lock = threading.Lock()
        self._initialized = True

    def acquire(self) -> str:
        """获取一个数据库连接

        Returns:
            连接标识字符串

        Raises:
            RuntimeError: 如果没有可用连接
        """
        # TODO: 实现连接获取逻辑
        # 1. 加锁
        # 2. 从 _available 取出一个连接
        # 3. 加入 _in_use
        # 4. 返回连接标识
        # 5. 如果无可用连接，抛出 RuntimeError
        with self._lock:
            if not self._available:
                raise RuntimeError("无可用连接")
            conn = self._available.pop()
            self._in_use.add(conn)
            return conn

    def release(self, conn: str) -> None:
        """释放一个数据库连接

        Args:
            conn: 要释放的连接标识

        Raises:
            ValueError: 如果该连接不属于此连接池
        """
        # TODO: 实现连接释放逻辑
        # 1. 加锁
        # 2. 验证 conn 在 _in_use 中
        # 3. 从 _in_use 移除
        # 4. 放回 _available
        with self._lock:
            if conn not in self._in_use:
                raise ValueError(f"连接 {conn} 不属于此连接池")
            self._in_use.remove(conn)
            self._available.append(conn)

    @property
    def available_count(self) -> int:
        """当前可用连接数"""
        return len(self._available)

    @property
    def in_use_count(self) -> int:
        """当前使用中的连接数"""
        return len(self._in_use)


# ============================================================================
# 练习3：思考题 — 多例模式 (Multiton)
# ============================================================================
# 实现 Multiton 模式，按名称创建有限实例：
#   1. PoolManager(max_instances=3) — 最多管理 3 个命名实例
#   2. get_instance(name) — 按名称获取或创建实例
#   3. 达到最大实例数后不能再创建新命名实例
# ============================================================================

class PoolManager:
    """多例模式 (Multiton) — 按名称创建有限实例

    用法：
        pm = PoolManager(max_instances=3)
        inst_a = pm.get_instance("a")  # 创建新实例
        inst_b = pm.get_instance("b")  # 创建新实例
        inst_a2 = pm.get_instance("a") # 返回已有实例
        inst_a is inst_a2  # => True
    """

    def __init__(self, max_instances: int = 3):
        self._max_instances = max_instances
        self._instances = {}
        self._lock = threading.Lock()

    def get_instance(self, name: str) -> object:
        """按名称获取或创建实例

        Args:
            name: 实例名称

        Returns:
            指定名称的实例对象

        Raises:
            RuntimeError: 如果已达到最大实例数且名称为新名称
        """
        # TODO: 实现多例逻辑
        # 1. 检查 name 是否已有实例
        # 2. 如果有，直接返回
        # 3. 如果没有，检查是否已达到 max_instances
        # 4. 如果未达到，创建新实例并保存
        # 5. 如果已达到，抛出 RuntimeError
        with self._lock:
            if name in self._instances:
                return self._instances[name]
            if len(self._instances) >= self._max_instances:
                raise RuntimeError(
                    f"已达到最大实例数 ({self._max_instances})，无法创建新实例 '{name}'"
                )
            instance = object()
            self._instances[name] = instance
            return instance

    @property
    def instance_count(self) -> int:
        """当前实例数量"""
        return len(self._instances)

    @property
    def max_instances(self) -> int:
        """最大实例数量"""
        return self._max_instances
