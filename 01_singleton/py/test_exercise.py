"""
================================================================================
 Lesson 01: Singleton — 单元测试
================================================================================
 运行方式：pytest test_exercise.py -v
================================================================================
"""

import threading
import pytest
from exercise import AppConfig, DBConnectionPool, PoolManager


# ============================================================================
# 测试练习1：基础单例 (__new__ 方式)
# ============================================================================

class TestAppConfig:
    """测试 AppConfig 单例"""

    def test_singleton_uniqueness(self):
        """测试单例唯一性：多次创建返回同一实例"""
        c1 = AppConfig({"key": "value"})
        c2 = AppConfig({"other": "data"})
        assert c1 is c2

    def test_singleton_same_object(self):
        """测试单例是同一个对象"""
        c1 = AppConfig({"debug": True})
        c2 = AppConfig()
        assert id(c1) == id(c2)

    def test_get_existing_key(self):
        """测试获取已存在的配置项"""
        config = AppConfig({"db_host": "localhost", "db_port": 3306})
        assert config.get("db_host") == "localhost"
        assert config.get("db_port") == 3306

    def test_get_non_existing_key(self):
        """测试获取不存在的配置项返回默认值"""
        config = AppConfig({"debug": True})
        assert config.get("nonexistent") is None
        assert config.get("nonexistent", "default") == "default"

    def test_singleton_config_shared(self):
        """测试单例配置在所有引用间共享"""
        c1 = AppConfig({"theme": "dark"})
        c2 = AppConfig()
        # c2 获取时 c1 已经初始化，c2 应该看到 c1 的配置
        assert c2.get("theme") == "dark"

    def test_singleton_thread_safety(self):
        """测试多线程环境下单例唯一性"""
        instances = []

        def create_config():
            c = AppConfig({"thread": threading.current_thread().name})
            instances.append(c)

        threads = [threading.Thread(target=create_config) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 所有线程获取到的应该是同一个实例
        for inst in instances:
            assert inst is instances[0]


# ============================================================================
# 测试练习2：线程安全单例 (元类方式)
# ============================================================================

class TestDBConnectionPool:
    """测试 DBConnectionPool 单例"""

    def test_singleton_uniqueness(self):
        """测试连接池单例唯一性"""
        p1 = DBConnectionPool()
        p2 = DBConnectionPool()
        assert p1 is p2

    def test_acquire_connection(self):
        """测试获取连接"""
        pool = DBConnectionPool()
        conn = pool.acquire()
        assert conn.startswith("conn_")
        assert pool.available_count == 2
        assert pool.in_use_count == 1

    def test_acquire_and_release(self):
        """测试获取和释放连接"""
        pool = DBConnectionPool()
        conn = pool.acquire()
        pool.release(conn)
        assert pool.available_count == 3
        assert pool.in_use_count == 0

    def test_acquire_all_connections(self):
        """测试获取全部 3 个连接"""
        pool = DBConnectionPool()
        conns = [pool.acquire() for _ in range(3)]
        assert pool.available_count == 0
        assert pool.in_use_count == 3

    def test_acquire_exhausted(self):
        """测试连接耗尽时抛出异常"""
        pool = DBConnectionPool()
        for _ in range(3):
            pool.acquire()
        with pytest.raises(RuntimeError, match="无可用连接"):
            pool.acquire()

    def test_release_invalid_connection(self):
        """测试释放无效连接时抛出异常"""
        pool = DBConnectionPool()
        with pytest.raises(ValueError, match="不属于此连接池"):
            pool.release("invalid_conn")

    def test_release_and_reacquire(self):
        """测试释放后可以重新获取"""
        pool = DBConnectionPool()
        conn1 = pool.acquire()
        pool.release(conn1)
        conn2 = pool.acquire()
        assert conn1 == conn2  # 释放后应该能重新获取到同一个连接

    def test_thread_safety(self):
        """测试多线程环境下的连接获取"""
        pool = DBConnectionPool()
        acquired = []
        errors = []

        def worker():
            try:
                conn = pool.acquire()
                acquired.append(conn)
            except Exception as e:
                errors.append(e)

        # 启动 6 个线程竞争 3 个连接
        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 最多只能成功获取 3 个连接
        assert len(acquired) <= 3
        # 应该有一些线程获取失败
        assert len(errors) >= 3

        # 清理：释放所有成功获取的连接
        for conn in acquired:
            pool.release(conn)


# ============================================================================
# 测试练习3：多例模式 (Multiton)
# ============================================================================

class TestPoolManager:
    """测试 PoolManager 多例模式"""

    def test_get_instance_by_name(self):
        """测试按名称获取实例"""
        pm = PoolManager(max_instances=3)
        inst = pm.get_instance("a")
        assert inst is not None
        assert pm.instance_count == 1

    def test_same_name_same_instance(self):
        """测试相同名称返回相同实例"""
        pm = PoolManager(max_instances=3)
        inst1 = pm.get_instance("a")
        inst2 = pm.get_instance("a")
        assert inst1 is inst2

    def test_different_name_different_instance(self):
        """测试不同名称返回不同实例"""
        pm = PoolManager(max_instances=3)
        inst_a = pm.get_instance("a")
        inst_b = pm.get_instance("b")
        assert inst_a is not inst_b
        assert pm.instance_count == 2

    def test_max_instances_limit(self):
        """测试达到最大实例数后不能创建新实例"""
        pm = PoolManager(max_instances=3)
        pm.get_instance("a")
        pm.get_instance("b")
        pm.get_instance("c")
        assert pm.instance_count == 3
        with pytest.raises(RuntimeError, match="已达到最大实例数"):
            pm.get_instance("d")

    def test_existing_name_after_limit(self):
        """测试达到上限后仍可获取已有名称的实例"""
        pm = PoolManager(max_instances=2)
        pm.get_instance("a")
        pm.get_instance("b")
        # 获取已有名称应该仍然成功
        inst = pm.get_instance("a")
        assert inst is not None

    def test_max_instances_one(self):
        """测试 max_instances=1 时的行为"""
        pm = PoolManager(max_instances=1)
        pm.get_instance("only")
        with pytest.raises(RuntimeError):
            pm.get_instance("another")

    def test_max_instances_default(self):
        """测试默认 max_instances 为 3"""
        pm = PoolManager()
        assert pm.max_instances == 3

    def test_thread_safety(self):
        """测试多线程环境下的多例"""
        pm = PoolManager(max_instances=5)
        results = {}

        def worker(name):
            try:
                inst = pm.get_instance(name)
                results[name] = inst
            except Exception as e:
                results[name] = e

        threads = [threading.Thread(target=worker, args=(f"t{i}",)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 前 5 个应成功，后 3 个应失败
        success_count = sum(1 for v in results.values() if not isinstance(v, Exception))
        fail_count = sum(1 for v in results.values() if isinstance(v, Exception))
        assert success_count == 5
        assert fail_count >= 3
