"""
================================================================================
Lesson 7: Proxy (代理模式) — 练习测试
================================================================================
"""

import time
import pytest
from exercise import (
    RealVideo,
    VideoProxy,
    BankAccount,
    BankAccountProxy,
    SlowAPI,
    APICacheProxy,
)


# ==============================================================================
# 第1题测试：虚拟代理（延迟加载）
# ==============================================================================

class TestVideoProxy:
    """测试虚拟代理的延迟加载"""

    def test_real_video_loading_time(self):
        """验证 RealVideo 创建时确实耗时"""
        start = time.time()
        video = RealVideo("Test Movie")
        elapsed = time.time() - start
        assert elapsed >= 0.3, f"RealVideo 加载耗时 {elapsed:.3f}s，预期 >= 0.3s"
        assert video.get_title() == "Test Movie"

    def test_proxy_creation_is_fast(self):
        """验证 VideoProxy 创建时非常快（不加载真实视频）"""
        start = time.time()
        proxy = VideoProxy("Fast Movie")
        elapsed = time.time() - start
        assert elapsed < 0.1, f"VideoProxy 创建耗时 {elapsed:.3f}s，预期很快"
        assert proxy.get_title() == "Fast Movie"

    def test_proxy_lazy_load_on_play(self):
        """验证代理在 play() 时才延迟加载"""
        proxy = VideoProxy("Lazy Movie")

        # 创建后立即检查 get_title（应极快，不触发加载）
        start = time.time()
        title = proxy.get_title()
        elapsed = time.time() - start
        assert elapsed < 0.1, f"get_title 不应触发加载，耗时 {elapsed:.3f}s"
        assert title == "Lazy Movie"

        # 首次 play 应触发加载
        start = time.time()
        result = proxy.play()
        elapsed = time.time() - start
        assert elapsed >= 0.3, f"首次 play 应触发加载，耗时 {elapsed:.3f}s"
        assert "正在播放: Lazy Movie" in result

    def test_proxy_reuses_loaded_video(self):
        """验证代理复用已加载的视频"""
        proxy = VideoProxy("Reuse Movie")

        # 首次播放 — 加载
        proxy.play()

        # 第二次播放 — 应直接从缓存播放，不加载
        start = time.time()
        result = proxy.play()
        elapsed = time.time() - start
        assert elapsed < 0.1, f"第二次 play 不应加载，耗时 {elapsed:.3f}s"
        assert "正在播放: Reuse Movie" in result

    def test_multiple_proxies_independent(self):
        """验证多个代理实例互不影响"""
        proxy1 = VideoProxy("Movie A")
        proxy2 = VideoProxy("Movie B")

        # 只播放第一个
        result1 = proxy1.play()
        assert "Movie A" in result1

        # 第二个还没加载，get_title 应快速返回
        start = time.time()
        title2 = proxy2.get_title()
        elapsed = time.time() - start
        assert elapsed < 0.1, f"未加载的代理 get_title 应很快，耗时 {elapsed:.3f}s"
        assert title2 == "Movie B"


# ==============================================================================
# 第2题测试：保护代理（权限控制）
# ==============================================================================

class TestBankAccountProxy:
    """测试保护代理的权限控制"""

    def test_admin_can_withdraw(self):
        """测试 admin 可以取款"""
        proxy = BankAccountProxy("Alice", 1000.0)
        result = proxy.withdraw(500.0, "admin")
        assert result is True
        assert proxy.get_balance() == 500.0

    def test_non_admin_cannot_withdraw(self):
        """测试非 admin 不能取款"""
        proxy = BankAccountProxy("Alice", 1000.0)
        result = proxy.withdraw(500.0, "normal")
        assert result is False
        # 余额不变
        assert proxy.get_balance() == 1000.0

    def test_anyone_can_deposit(self):
        """测试任何人都可以存款"""
        proxy = BankAccountProxy("Alice", 1000.0)
        proxy.deposit(500.0)
        assert proxy.get_balance() == 1500.0

    def test_anyone_can_check_balance(self):
        """测试任何人都可以查看余额"""
        proxy = BankAccountProxy("Alice", 888.0)
        assert proxy.get_balance() == 888.0

    def test_withdraw_insufficient_funds_as_admin(self):
        """测试 admin 取款超过余额"""
        proxy = BankAccountProxy("Bob", 100.0)
        result = proxy.withdraw(200.0, "admin")
        assert result is False
        assert proxy.get_balance() == 100.0

    def test_multiple_admin_operations(self):
        """测试多次 admin 操作"""
        proxy = BankAccountProxy("Charlie", 1000.0)
        proxy.deposit(500.0)
        assert proxy.get_balance() == 1500.0
        proxy.withdraw(300.0, "admin")
        assert proxy.get_balance() == 1200.0
        proxy.withdraw(200.0, "admin")
        assert proxy.get_balance() == 1000.0

    def test_withdraw_negative_amount(self):
        """测试负数取款应抛出异常"""
        proxy = BankAccountProxy("Dave", 500.0)
        with pytest.raises(ValueError, match="正数"):
            proxy.withdraw(-100.0, "admin")


# ==============================================================================
# 第3题测试：缓存代理
# ==============================================================================

class TestAPICacheProxy:
    """测试缓存代理的缓存行为"""

    def test_first_call_misses_cache(self):
        """测试首次调用未命中缓存"""
        api = SlowAPI()
        proxy = APICacheProxy(api)

        start = time.time()
        data = proxy.get_data("key1")
        elapsed = time.time() - start

        assert data == "data_for_key1"
        assert elapsed >= 0.5, f"首次调用应耗时，实际 {elapsed:.3f}s"

        stats = proxy.get_cache_stats()
        assert stats["misses"] == 1
        assert stats["hits"] == 0
        assert stats["cache_size"] == 1

    def test_repeated_call_hits_cache(self):
        """测试重复调用命中缓存"""
        api = SlowAPI()
        proxy = APICacheProxy(api)

        # 首次调用
        proxy.get_data("key1")

        # 第二次调用 — 应命中缓存
        start = time.time()
        data = proxy.get_data("key1")
        elapsed = time.time() - start

        assert data == "data_for_key1"
        assert elapsed < 0.1, f"缓存命中应很快，实际 {elapsed:.3f}s"

        stats = proxy.get_cache_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1

    def test_different_keys_independent(self):
        """测试不同 key 独立缓存"""
        api = SlowAPI()
        proxy = APICacheProxy(api)

        # 两个不同的 key
        data1 = proxy.get_data("alpha")
        data2 = proxy.get_data("beta")

        assert data1 == "data_for_alpha"
        assert data2 == "data_for_beta"

        stats = proxy.get_cache_stats()
        assert stats["misses"] == 2
        assert stats["cache_size"] == 2

        # 再次获取，都应命中
        assert proxy.get_data("alpha") == "data_for_alpha"
        assert proxy.get_data("beta") == "data_for_beta"
        stats = proxy.get_cache_stats()
        assert stats["hits"] == 2

    def test_clear_cache(self):
        """测试清空缓存"""
        api = SlowAPI()
        proxy = APICacheProxy(api)

        proxy.get_data("key1")
        assert proxy.get_cache_stats()["cache_size"] == 1

        proxy.clear_cache()
        stats = proxy.get_cache_stats()
        assert stats["cache_size"] == 0
        assert stats["hits"] == 0
        assert stats["misses"] == 1

    def test_after_clear_cache_misses_again(self):
        """测试清空缓存后再次调用应未命中"""
        api = SlowAPI()
        proxy = APICacheProxy(api)

        proxy.get_data("key1")
        proxy.clear_cache()

        # 清空后再次请求 — 应重新调用真实 API
        start = time.time()
        data = proxy.get_data("key1")
        elapsed = time.time() - start

        assert data == "data_for_key1"
        assert elapsed >= 0.5, f"清空缓存后应重新加载，实际 {elapsed:.3f}s"

        stats = proxy.get_cache_stats()
        assert stats["misses"] == 2
