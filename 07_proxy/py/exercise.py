"""
================================================================================
Lesson 7: Proxy (代理模式) — 练习题
================================================================================
"""

from abc import ABC, abstractmethod
import time


# ==============================================================================
# 第1题：基础 — 虚拟代理（延迟加载）
# ==============================================================================

class Video(ABC):
    """视频接口"""

    @abstractmethod
    def play(self) -> str:
        """播放视频，返回播放信息"""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """获取视频标题"""
        pass


class RealVideo(Video):
    """
    真实视频 — 加载代价高昂（模拟从网络/磁盘加载）
    每次创建时都会"模拟加载"，需要耗时 0.3 秒
    """

    def __init__(self, title: str):
        self._title = title
        # 模拟加载视频的耗时操作
        self._load_video()

    def _load_video(self):
        """模拟从网络加载视频"""
        time.sleep(0.3)

    def play(self) -> str:
        return f"正在播放: {self._title}"

    def get_title(self) -> str:
        return self._title


# TODO: 实现 VideoProxy（虚拟代理）
#   1. 创建时只保存标题，不创建 RealVideo（轻量级）
#   2. 调用 play() 时，首次才创建 RealVideo 并播放
#   3. 后续再次调用 play()，复用已创建的 RealVideo
#   4. get_title() 直接返回标题，不需要加载
class VideoProxy(Video):
    def __init__(self, title: str):
        pass

    def play(self) -> str:
        pass

    def get_title(self) -> str:
        pass


# ==============================================================================
# 第2题：综合 — 保护代理（权限控制）
# ==============================================================================

class BankAccount:
    """
    银行账户 — 真实业务对象
    注意：withdraw 方法目前没有权限检查
    """

    def __init__(self, owner: str, balance: float = 0.0):
        self._owner = owner
        self._balance = balance

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("存款金额必须为正数")
        self._balance += amount

    def withdraw(self, amount: float, user_role: str = "admin") -> bool:
        """
        取款操作
        :param amount: 取款金额
        :param user_role: 用户角色
        :return: 是否成功
        """
        if amount <= 0:
            raise ValueError("取款金额必须为正数")
        if amount > self._balance:
            return False
        self._balance -= amount
        return True


# TODO: 实现 BankAccountProxy（保护代理）
#   1. 持有 BankAccount 的真实引用
#   2. deposit() 直接委托给真实账户（所有人可存款）
#   3. withdraw() 先检查 user_role 是否为 "admin"
#      - 如果不是 admin，返回 False 并拒绝操作
#      - 如果是 admin，委托给真实账户
#   4. get_balance() 直接委托给真实账户
class BankAccountProxy:
    def __init__(self, owner: str, balance: float = 0.0):
        pass

    def get_balance(self) -> float:
        pass

    def deposit(self, amount: float):
        pass

    def withdraw(self, amount: float, user_role: str = "normal") -> bool:
        pass


# ==============================================================================
# 第3题：拓展 — 缓存代理
# ==============================================================================

class SlowAPI:
    """
    一个模拟的慢速 API 服务
    每次调用 get_data(key) 都要耗时 0.5 秒
    """

    def get_data(self, key: str) -> str:
        """模拟从远程获取数据"""
        time.sleep(0.5)
        return f"data_for_{key}"


# TODO: 实现 APICacheProxy（缓存代理）
#   1. 包装 SlowAPI，对相同 key 的请求缓存结果
#   2. 首次调用 get_data(key) → 调用真实 API，缓存结果
#   3. 后续相同 key 的调用 → 直接从缓存返回，不调用真实 API
#   4. 提供一个 clear_cache() 方法清空缓存
#   5. 提供一个 get_cache_stats() 方法返回缓存统计信息
#      (返回 dict: {"hits": int, "misses": int, "cache_size": int})
class APICacheProxy:
    def __init__(self, api: SlowAPI):
        pass

    def get_data(self, key: str) -> str:
        pass

    def clear_cache(self):
        """清空所有缓存"""
        pass

    def get_cache_stats(self) -> dict:
        """返回缓存统计信息"""
        pass
