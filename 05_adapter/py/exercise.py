"""
================================================================================
Lesson 5: Adapter — 适配器模式（练习题）
================================================================================
"""


# ============================================================================
# 题目 1：天气数据适配器（基础）
# ============================================================================
# 有一个旧类 OldWeatherAPI 返回华氏度（get_temperature_f()），
# 新系统需要摄氏度。请实现 WeatherAdapter 包装旧接口。
# ============================================================================

class OldWeatherAPI:
    """旧的天气 API，返回华氏度"""

    def get_temperature_f(self) -> float:
        """返回华氏度温度"""
        return 77.0  # 约 25°C

    def get_weather_description(self) -> str:
        """返回天气描述"""
        return "晴天"


class WeatherAdapter:
    """天气适配器：将华氏度转换为摄氏度"""

    def __init__(self, old_api: OldWeatherAPI):
        # TODO: 持有旧 API 的引用
        pass

    def get_temperature_c(self) -> float:
        """返回摄氏度温度"""
        # TODO: 调用旧 API 获取华氏度，转换为摄氏度并返回
        # 公式: C = (F - 32) * 5 / 9
        pass

    def get_description(self) -> str:
        """返回天气描述"""
        # TODO: 调用旧 API 获取描述
        pass


# ============================================================================
# 题目 2：支付系统适配器（综合）
# ============================================================================
# 旧接口 AlipayOld 有 .pay_alipay(amount)，
# 新系统需要统一的 .pay(amount) 接口。
# 实现 AlipayAdapter 适配旧接口到统一支付接口。
# 同时实现 WechatPayOld 和对应的 WechatPayAdapter。
# ============================================================================

class PaymentTarget:
    """统一的支付目标接口"""

    def pay(self, amount: float) -> str:
        """支付接口"""
        raise NotImplementedError("子类必须实现 pay()")


class AlipayOld:
    """旧的支付宝接口"""

    def pay_alipay(self, amount: float) -> str:
        """旧支付宝支付方法"""
        return f"支付宝支付 {amount} 元成功"


class WechatPayOld:
    """旧的微信支付接口"""

    def pay_wechat(self, amount: float) -> str:
        """旧微信支付方法"""
        return f"微信支付 {amount} 元成功"


class AlipayAdapter(PaymentTarget):
    """支付宝适配器"""

    def __init__(self, alipay: AlipayOld):
        # TODO: 持有旧支付宝接口的引用
        pass

    def pay(self, amount: float) -> str:
        # TODO: 调用旧接口的 pay_alipay 方法
        pass


class WechatPayAdapter(PaymentTarget):
    """微信支付适配器"""

    def __init__(self, wechat: WechatPayOld):
        # TODO: 持有旧微信接口的引用
        pass

    def pay(self, amount: float) -> str:
        # TODO: 调用旧接口的 pay_wechat 方法
        pass


# ============================================================================
# 题目 3：双向适配器（拓展）
# ============================================================================
# 实现 JSONToXMLAdapter 和 XMLToJSONAdapter，
# 支持 JSON <-> XML 的双向转换。
# ============================================================================

class JSONToXMLAdapter:
    """JSON 转 XML 适配器"""

    def json_to_xml(self, json_data: dict) -> str:
        """将 JSON (dict) 转换为 XML 字符串"""
        # TODO: 实现转换
        # 输入: {"name": "张三", "age": 28}
        # 输出: "<root><name>张三</name><age>28</age></root>"
        pass


class XMLToJSONAdapter:
    """XML 转 JSON 适配器"""

    def xml_to_json(self, xml_str: str) -> dict:
        """将 XML 字符串转换为 JSON (dict)"""
        # TODO: 实现转换
        # 输入: "<root><name>张三</name><age>28</age></root>"
        # 输出: {"name": "张三", "age": 28}
        pass
