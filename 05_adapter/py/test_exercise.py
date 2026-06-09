"""
================================================================================
Lesson 5: Adapter — 适配器模式（测试）
================================================================================
"""

import pytest
from exercise import (
    OldWeatherAPI,
    WeatherAdapter,
    PaymentTarget,
    AlipayOld,
    WechatPayOld,
    AlipayAdapter,
    WechatPayAdapter,
    JSONToXMLAdapter,
    XMLToJSONAdapter,
)


class TestAdapterExercise:
    """测试适配器练习题"""

    # ========================================================================
    # 题目 1：基础测试 — 天气数据适配器
    # ========================================================================

    def test_weather_adapter_converts_f_to_c(self):
        """测试 WeatherAdapter 华氏度转摄氏度"""
        old_api = OldWeatherAPI()
        adapter = WeatherAdapter(old_api)

        # 77°F 约等于 25°C
        celsius = adapter.get_temperature_c()
        assert abs(celsius - 25.0) < 0.1, \
            f"77°F 应转换为约 25°C，实际得到 {celsius}"

    def test_weather_adapter_get_description(self):
        """测试 WeatherAdapter 获取天气描述"""
        old_api = OldWeatherAPI()
        adapter = WeatherAdapter(old_api)

        description = adapter.get_description()
        assert description == "晴天", \
            "get_description() 应返回正确的天气描述"

    def test_weather_adapter_celsius_is_float(self):
        """测试 WeatherAdapter 返回摄氏度类型正确"""
        old_api = OldWeatherAPI()
        adapter = WeatherAdapter(old_api)

        celsius = adapter.get_temperature_c()
        assert isinstance(celsius, float), \
            "get_temperature_c() 应返回 float 类型"

    # ========================================================================
    # 题目 2：综合测试 — 支付系统适配器
    # ========================================================================

    def test_alipay_adapter_implements_payment_target(self):
        """测试 AlipayAdapter 实现统一的支付接口"""
        old_alipay = AlipayOld()
        adapter = AlipayAdapter(old_alipay)

        assert isinstance(adapter, PaymentTarget), \
            "AlipayAdapter 应继承 PaymentTarget"

    def test_alipay_adapter_pay(self):
        """测试 AlipayAdapter 支付功能"""
        old_alipay = AlipayOld()
        adapter = AlipayAdapter(old_alipay)

        result = adapter.pay(100.0)
        assert "支付宝" in result, "支付结果应包含'支付宝'"
        assert "100" in result, "支付结果应包含金额"

    def test_wechat_pay_adapter_implements_payment_target(self):
        """测试 WechatPayAdapter 实现统一的支付接口"""
        old_wechat = WechatPayOld()
        adapter = WechatPayAdapter(old_wechat)

        assert isinstance(adapter, PaymentTarget), \
            "WechatPayAdapter 应继承 PaymentTarget"

    def test_wechat_pay_adapter_pay(self):
        """测试 WechatPayAdapter 支付功能"""
        old_wechat = WechatPayOld()
        adapter = WechatPayAdapter(old_wechat)

        result = adapter.pay(200.0)
        assert "微信" in result, "支付结果应包含'微信'"
        assert "200" in result, "支付结果应包含金额"

    def test_unified_payment_interface(self):
        """测试统一支付接口可以处理多种支付方式"""
        payments = [
            AlipayAdapter(AlipayOld()),
            WechatPayAdapter(WechatPayOld()),
        ]

        amounts = [99.9, 199.9]
        for i, payment in enumerate(payments):
            result = payment.pay(amounts[i])
            assert isinstance(result, str), "支付结果应为字符串"
            assert str(amounts[i]) in result, \
                "支付结果应包含正确的金额"

    # ========================================================================
    # 题目 3：拓展测试 — 双向适配器
    # ========================================================================

    def test_json_to_xml_conversion(self):
        """测试 JSON 转 XML"""
        adapter = JSONToXMLAdapter()
        json_data = {"name": "张三", "age": 28}

        xml_result = adapter.json_to_xml(json_data)

        assert "<name>" in xml_result, "XML 应包含 <name> 标签"
        assert "张三" in xml_result, "XML 应包含 name 的值"
        assert "<age>" in xml_result, "XML 应包含 <age> 标签"
        assert "28" in xml_result, "XML 应包含 age 的值"

    def test_xml_to_json_conversion(self):
        """测试 XML 转 JSON"""
        adapter = XMLToJSONAdapter()
        xml_str = "<root><name>张三</name><age>28</age></root>"

        json_result = adapter.xml_to_json(xml_str)

        assert isinstance(json_result, dict), "转换结果应为 dict"
        assert json_result.get("name") == "张三", \
            "应正确提取 name 字段"
        assert json_result.get("age") == "28", \
            "应正确提取 age 字段"

    def test_bidirectional_conversion_roundtrip(self):
        """测试双向转换的往返一致性"""
        json_adapter = JSONToXMLAdapter()
        xml_adapter = XMLToJSONAdapter()

        original = {"name": "李四", "age": 35, "city": "北京"}

        # JSON -> XML -> JSON
        xml_result = json_adapter.json_to_xml(original)
        back_to_json = xml_adapter.xml_to_json(xml_result)

        assert back_to_json["name"] == "李四", \
            "往返转换后 name 应保持不变"
        assert back_to_json["age"] == "35", \
            "往返转换后 age 应保持不变（XML 中均为字符串）"
