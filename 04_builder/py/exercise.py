"""
================================================================================
Lesson 4: Builder — 构建器模式（练习题）
================================================================================
"""


# ============================================================================
# 题目 1：实现 PizzaBuilder（基础）
# ============================================================================
# 实现 PizzaBuilder，支持链式调用：
# - set_dough() — 设置面团类型
# - set_sauce() — 设置酱料
# - add_topping() — 添加配料
# - build() — 构建 Pizza 对象
# Pizza 类有 __str__() 返回披萨描述
# ============================================================================

class Pizza:
    """披萨产品类"""

    def __init__(self):
        self._dough = None
        self._sauce = None
        self._toppings = []

    def __str__(self) -> str:
        """返回披萨的描述字符串"""
        # TODO: 返回格式如 "面团: 薄脆, 酱料: 番茄, 配料: 芝士, 蘑菇"
        pass


class PizzaBuilder:
    """披萨构建器"""

    def __init__(self):
        # TODO: 初始化 Pizza 实例
        pass

    def set_dough(self, dough: str) -> "PizzaBuilder":
        """设置面团类型"""
        # TODO: 设置面团并返回 self
        pass

    def set_sauce(self, sauce: str) -> "PizzaBuilder":
        """设置酱料"""
        # TODO: 设置酱料并返回 self
        pass

    def add_topping(self, topping: str) -> "PizzaBuilder":
        """添加配料"""
        # TODO: 添加配料并返回 self
        pass

    def build(self) -> Pizza:
        """构建并返回 Pizza 对象"""
        # TODO: 校验必填项（dough 和 sauce），返回 Pizza
        pass


# ============================================================================
# 题目 2：实现 HTTPRequestBuilder（综合）
# ============================================================================
# 实现 HTTPRequestBuilder，支持链式调用：
# - set_url() — 设置 URL
# - set_method() — 设置 HTTP 方法（GET/POST/PUT/DELETE）
# - add_header() — 添加请求头
# - set_body() — 设置请求体
# - build() — 构建 HTTPRequest 对象
# HTTPRequest 有 send() 方法返回描述字符串
# ============================================================================

class HTTPRequest:
    """HTTP 请求类"""

    def __init__(self):
        self._url = None
        self._method = "GET"
        self._headers = {}
        self._body = None

    def send(self) -> str:
        """发送请求，返回描述字符串"""
        # TODO: 返回如 "发送 GET 请求到 https://api.example.com，请求头: {...}，请求体: {...}"
        pass


class HTTPRequestBuilder:
    """HTTP 请求构建器"""

    def __init__(self):
        # TODO: 初始化 HTTPRequest 实例
        pass

    def set_url(self, url: str) -> "HTTPRequestBuilder":
        """设置 URL"""
        # TODO: 设置 URL 并返回 self
        pass

    def set_method(self, method: str) -> "HTTPRequestBuilder":
        """设置 HTTP 方法"""
        # TODO: 设置方法并返回 self
        pass

    def add_header(self, key: str, value: str) -> "HTTPRequestBuilder":
        """添加请求头"""
        # TODO: 添加请求头并返回 self
        pass

    def set_body(self, body: str) -> "HTTPRequestBuilder":
        """设置请求体"""
        # TODO: 设置请求体并返回 self
        pass

    def build(self) -> HTTPRequest:
        """构建并返回 HTTPRequest 对象"""
        # TODO: 校验必填项（url），返回 HTTPRequest
        pass


# ============================================================================
# 题目 3：实现 Director 和 QueryBuilder（拓展）
# ============================================================================
# 实现一个 QueryBuilder（SQL 查询构建器），支持：
# - select() — 指定查询字段
# - from_() — 指定表名
# - where() — 添加条件
# - order_by() — 排序
# - build() — 生成 SQL 字符串
# 同时实现 Director，提供常用查询预设
# ============================================================================

class QueryBuilder:
    """SQL 查询构建器"""

    def __init__(self):
        # TODO: 初始化字段、表名、条件、排序等
        pass

    def select(self, *fields: str) -> "QueryBuilder":
        """指定查询字段"""
        # TODO: 设置字段并返回 self
        pass

    def from_(self, table: str) -> "QueryBuilder":
        """指定表名"""
        # TODO: 设置表名并返回 self
        pass

    def where(self, condition: str) -> "QueryBuilder":
        """添加 WHERE 条件"""
        # TODO: 添加条件并返回 self
        pass

    def order_by(self, field: str, direction: str = "ASC") -> "QueryBuilder":
        """添加 ORDER BY 排序"""
        # TODO: 设置排序并返回 self
        pass

    def build(self) -> str:
        """生成 SQL 查询字符串"""
        # TODO: 校验必填项（select 和 from_），生成并返回 SQL
        pass


class QueryDirector:
    """SQL 查询导演者，提供常用查询预设"""

    @staticmethod
    def select_all_users() -> str:
        """查询所有用户"""
        # TODO: 使用 QueryBuilder 构建 "SELECT * FROM users"
        pass

    @staticmethod
    def select_active_users() -> str:
        """查询所有活跃用户"""
        # TODO: 使用 QueryBuilder 构建 "SELECT * FROM users WHERE status='active'"
        pass

    @staticmethod
    def select_recent_orders(limit: int = 10) -> str:
        """查询最近的订单"""
        # TODO: 使用 QueryBuilder 构建 "SELECT * FROM orders ORDER BY created_at DESC"
        pass
