"""
================================================================================
Lesson 4: Builder — 构建器模式（测试）
================================================================================
"""

import pytest
from exercise import (
    Pizza,
    PizzaBuilder,
    HTTPRequest,
    HTTPRequestBuilder,
    QueryBuilder,
    QueryDirector,
)


class TestBuilderExercise:
    """测试 Builder 练习题"""

    # ========================================================================
    # 题目 1：基础测试 — PizzaBuilder
    # ========================================================================

    def test_pizza_builder_chain(self):
        """测试 PizzaBuilder 链式调用"""
        pizza = (
            PizzaBuilder()
            .set_dough("薄脆")
            .set_sauce("番茄")
            .add_topping("芝士")
            .add_topping("蘑菇")
            .build()
        )
        assert isinstance(pizza, Pizza), "build() 应返回 Pizza 实例"

    def test_pizza_str_contains_info(self):
        """测试 Pizza.__str__() 包含披萨信息"""
        pizza = (
            PizzaBuilder()
            .set_dough("薄脆")
            .set_sauce("番茄")
            .add_topping("芝士")
            .add_topping("蘑菇")
            .build()
        )
        result = str(pizza)
        assert "薄脆" in result, "__str__() 应包含面团信息"
        assert "番茄" in result, "__str__() 应包含酱料信息"
        assert "芝士" in result or "蘑菇" in result, "__str__() 应包含配料信息"

    def test_pizza_builder_missing_required(self):
        """测试 PizzaBuilder 缺少必填项时抛出异常"""
        builder = PizzaBuilder()
        # 只添加配料，不设置面团和酱料
        builder.add_topping("芝士")
        with pytest.raises(ValueError, match=".*面团.*|.*酱料.*|.*必填.*"):
            builder.build()

    def test_pizza_builder_no_toppings(self):
        """测试 PizzaBuilder 不加配料也能构建"""
        pizza = (
            PizzaBuilder()
            .set_dough("厚底")
            .set_sauce("BBQ")
            .build()
        )
        assert isinstance(pizza, Pizza), "不添加配料也应能构建"

    # ========================================================================
    # 题目 2：综合测试 — HTTPRequestBuilder
    # ========================================================================

    def test_http_builder_chain(self):
        """测试 HTTPRequestBuilder 链式调用"""
        request = (
            HTTPRequestBuilder()
            .set_url("https://api.example.com/users")
            .set_method("GET")
            .add_header("Authorization", "Bearer token123")
            .add_header("Content-Type", "application/json")
            .build()
        )
        assert isinstance(request, HTTPRequest), "build() 应返回 HTTPRequest 实例"

    def test_http_send_contains_info(self):
        """测试 HTTPRequest.send() 包含请求信息"""
        request = (
            HTTPRequestBuilder()
            .set_url("https://api.example.com/users")
            .set_method("POST")
            .add_header("Content-Type", "application/json")
            .set_body('{"name": "test"}')
            .build()
        )
        result = request.send()
        assert "https://api.example.com/users" in result, \
            "send() 应包含 URL"
        assert "POST" in result, "send() 应包含 HTTP 方法"

    def test_http_builder_missing_url(self):
        """测试 HTTPRequestBuilder 缺少 URL 时抛出异常"""
        builder = HTTPRequestBuilder()
        builder.set_method("GET")
        with pytest.raises(ValueError, match=".*URL.*|.*必填.*"):
            builder.build()

    def test_http_builder_default_method(self):
        """测试 HTTPRequestBuilder 默认方法为 GET"""
        request = (
            HTTPRequestBuilder()
            .set_url("https://api.example.com/test")
            .build()
        )
        result = request.send()
        assert "GET" in result, "默认方法应为 GET"

    # ========================================================================
    # 题目 3：拓展测试 — QueryBuilder 和 Director
    # ========================================================================

    def test_query_builder_basic(self):
        """测试 QueryBuilder 基本 SQL 生成"""
        sql = (
            QueryBuilder()
            .select("id", "name", "email")
            .from_("users")
            .build()
        )
        assert "SELECT" in sql, "SQL 应包含 SELECT"
        assert "id" in sql, "SQL 应包含字段 id"
        assert "name" in sql, "SQL 应包含字段 name"
        assert "FROM" in sql, "SQL 应包含 FROM"
        assert "users" in sql, "SQL 应包含表名 users"

    def test_query_builder_with_where(self):
        """测试 QueryBuilder 带 WHERE 条件"""
        sql = (
            QueryBuilder()
            .select("*")
            .from_("users")
            .where("age > 18")
            .build()
        )
        assert "WHERE" in sql, "SQL 应包含 WHERE"
        assert "age > 18" in sql, "SQL 应包含条件"

    def test_query_builder_with_order_by(self):
        """测试 QueryBuilder 带 ORDER BY"""
        sql = (
            QueryBuilder()
            .select("*")
            .from_("products")
            .order_by("price", "DESC")
            .build()
        )
        assert "ORDER BY" in sql, "SQL 应包含 ORDER BY"
        assert "DESC" in sql, "SQL 应包含排序方向"

    def test_query_builder_missing_select(self):
        """测试 QueryBuilder 缺少 select 时抛出异常"""
        builder = QueryBuilder()
        builder.from_("users")
        with pytest.raises(ValueError, match=".*SELECT.*|.*字段.*|.*必填.*"):
            builder.build()

    def test_query_builder_missing_from(self):
        """测试 QueryBuilder 缺少 from_ 时抛出异常"""
        builder = QueryBuilder()
        builder.select("*")
        with pytest.raises(ValueError, match=".*FROM.*|.*表名.*|.*必填.*"):
            builder.build()

    def test_query_director_select_all_users(self):
        """测试 QueryDirector 预设：查询所有用户"""
        sql = QueryDirector.select_all_users()
        assert "SELECT" in sql and "FROM" in sql, "应为有效 SQL"
        assert "users" in sql, "应查询 users 表"

    def test_query_director_select_active_users(self):
        """测试 QueryDirector 预设：查询活跃用户"""
        sql = QueryDirector.select_active_users()
        assert "WHERE" in sql, "应包含 WHERE 条件"
        assert "active" in sql or "status" in sql, "应包含状态条件"

    def test_query_director_select_recent_orders(self):
        """测试 QueryDirector 预设：查询最近订单"""
        sql = QueryDirector.select_recent_orders()
        assert "ORDER BY" in sql, "应包含 ORDER BY"
        assert "orders" in sql, "应查询 orders 表"
