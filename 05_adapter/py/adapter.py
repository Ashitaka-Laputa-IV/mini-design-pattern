"""
================================================================================
Lesson 5: Adapter — 适配器模式（模式实现篇）[结构型]
================================================================================
  上一节的 bad_adapter.py 我们看到了散装转换和修改第三方库的问题，
  现在来看看 Adapter 模式如何优雅地解决这些兼容性问题。

  📐 设计模式定义：
    适配器模式（Adapter）将一个类的接口转换成客户期望的另一个接口。
    让原本不兼容的类可以一起工作。

  🎯 解决的问题：
    - 接口不兼容：现有接口（XML）和客户期望接口（JSON）不匹配
    - 无法修改第三方代码：不能改 Adaptee 的源码
    - 不想大范围修改：不想把系统所有接口从 XML 改成 JSON

  💡 核心思想：
    在中间加一层"适配器"：它实现目标接口（Target），
    内部调用被适配者（Adaptee）的接口做转换。

  🔑 两种实现方式：
    1. 对象适配器（Object Adapter）—— 使用组合（推荐）
    2. 类适配器（Class Adapter）—— 使用多重继承（C++ 特有）
================================================================================
"""

import json
import re
from typing import Any, Dict, List


# ============================================================================
# Adaptee（被适配者）：旧系统的 XML 接口
# ============================================================================

class OldEmployeeAPI:
    """
    🏢 Adaptee（被适配者）
    公司现有的老系统——所有接口返回 XML 格式。
    我们不能修改这个类，它已经被几百个模块依赖。
    """

    def get_employee_xml(self) -> str:
        """获取所有员工信息（XML 格式）"""
        return """<?xml version="1.0"?>
<employees>
    <employee>
        <name>张三</name>
        <age>28</age>
        <dept>技术部</dept>
        <salary>15000</salary>
    </employee>
    <employee>
        <name>李四</name>
        <age>35</age>
        <dept>产品部</dept>
        <salary>18000</salary>
    </employee>
    <employee>
        <name>王五</name>
        <age>42</age>
        <dept>技术部</dept>
        <salary>22000</salary>
    </employee>
    <employee>
        <name>赵六</name>
        <age>26</age>
        <dept>市场部</dept>
        <salary>13000</salary>
    </employee>
</employees>"""

    def get_employee_by_id_xml(self, emp_id: int) -> str:
        """按 ID 查询（XML 格式）"""
        return f"""<?xml version="1.0"?>
<employee>
    <id>{emp_id}</id>
    <name>张三</name>
    <age>28</age>
    <dept>技术部</dept>
    <salary>15000</salary>
</employee>"""


# ============================================================================
# Target（目标接口）：新系统需要的 JSON 接口
# ============================================================================

class EmployeeTarget:
    """
    🎯 Target（目标接口）

    这是客户（新系统）期望的接口。
    在 Python 中，我们用抽象基类来定义"契约"。
    """

    def get_employees(self) -> List[Dict[str, Any]]:
        """
        获取所有员工信息（返回 JSON 兼容的 dict 列表）
        子类必须实现此方法。
        """
        raise NotImplementedError("子类必须实现 get_employees()")

    def get_employee_by_id(self, emp_id: int) -> Dict[str, Any]:
        """
        按 ID 查询员工（返回 dict）
        """
        raise NotImplementedError("子类必须实现 get_employee_by_id()")


# ============================================================================
# Adaptee（被适配者）：新第三方库的 JSON 分析器
# ============================================================================

class NewDataAnalyzer:
    """
    📦 新引入的第三方数据分析库。
    它只接受 JSON（Python dict），但功能很强大。

    注意：我们不能修改这个类。
    """

    def analyze_employees(self, employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析员工数据。

        参数:
            employees: List[dict]，员工列表
                每个元素格式: {"name": str, "age": int, "dept": str, "salary": int}

        返回:
            dict: 分析结果
        """
        total = len(employees)
        if total == 0:
            return {"total": 0, "average_age": 0, "average_salary": 0}

        avg_age = sum(e["age"] for e in employees) / total
        avg_salary = sum(e["salary"] for e in employees) / total
        dept_count = {}
        for e in employees:
            d = e["dept"]
            dept_count[d] = dept_count.get(d, 0) + 1

        return {
            "total_employees": total,
            "average_age": round(avg_age, 1),
            "average_salary": round(avg_salary, 1),
            "department_distribution": dept_count,
        }


# ============================================================================
# ✅ 对象适配器（Object Adapter）—— 使用组合
# ============================================================================

class EmployeeAdapter(EmployeeTarget):
    """
    ✅ Adapter（适配器）—— 对象适配器（推荐方式）

    工作原理：
      1. 实现 Target 接口（get_employees, get_employee_by_id）
      2. 内部持有 Adaptee（OldEmployeeAPI）的引用
      3. 在 Target 方法的实现中调用 Adaptee 并做格式转换

    🎯 优点：
      - 使用组合，灵活度高
      - 可以适配 Adaptee 及其所有子类
      - 不需要修改 Adaptee 的代码
      - 转换逻辑集中在一个类中，方便维护

    💡 类比现实：
      就像一个"USB-C 转 HDMI 转换器"——
      你的电脑只有 USB-C（Target），显示器只接受 HDMI（Adaptee），
      转换器（Adapter）在中间做信号转换。
    """

    def __init__(self, old_api: OldEmployeeAPI):
        """
        持有 Adaptee 的引用（组合关系）。

        参数:
            old_api: OldEmployeeAPI 实例
        """
        self._old_api = old_api  # 持有被适配者的引用

    def get_employees(self) -> List[Dict[str, Any]]:
        """
        实现 Target 接口：获取员工列表（JSON 格式）

        内部流程：
          1. 调用 Adaptee 获取 XML
          2. 将 XML 解析为 dict（JSON 格式）
          3. 返回客户端期望的格式
        """
        # 1. 从旧系统获取 XML 数据
        xml_data = self._old_api.get_employee_xml()

        # 2. 将 XML 转换为 JSON（dict）
        employees = self._parse_employees_xml(xml_data)

        return employees

    def get_employee_by_id(self, emp_id: int) -> Dict[str, Any]:
        """
        实现 Target 接口：按 ID 查询（JSON 格式）
        """
        xml_data = self._old_api.get_employee_by_id_xml(emp_id)
        employee = self._parse_single_employee_xml(xml_data)
        return employee

    # --- 私有转换方法（封装在 Adapter 内部）---

    def _parse_employees_xml(self, xml_str: str) -> List[Dict[str, Any]]:
        """
        解析员工列表 XML → JSON

        转换逻辑封装在 Adapter 内部，客户端不需要关心。
        如果 XML 格式变了，只需要改这一个地方！
        """
        employees = []

        # 用正则表达式提取每个员工块（实际项目应使用 xml.etree.ElementTree）
        employee_blocks = re.findall(
            r"<employee>(.*?)</employee>", xml_str, re.DOTALL
        )

        for block in employee_blocks:
            employee = self._parse_employee_block(block)
            employees.append(employee)

        return employees

    def _parse_single_employee_xml(self, xml_str: str) -> Dict[str, Any]:
        """解析单个员工 XML"""
        # 提取 employee 标签内的内容
        match = re.search(
            r"<employee>(.*?)</employee>", xml_str, re.DOTALL
        )
        if match:
            return self._parse_employee_block(match.group(1))
        return {}

    def _parse_employee_block(self, block: str) -> Dict[str, Any]:
        """
        解析单个员工信息块。

        从 XML:
            <name>张三</name>
            <age>28</age>
        转换为 dict:
            {"name": "张三", "age": 28}
        """
        name = self._extract_tag(block, "name")
        age = int(self._extract_tag(block, "age") or 0)
        dept = self._extract_tag(block, "dept")
        salary = int(self._extract_tag(block, "salary") or 0)

        return {
            "name": name,
            "age": age,
            "dept": dept,
            "salary": salary,
        }

    @staticmethod
    def _extract_tag(xml_block: str, tag: str) -> str:
        """提取 XML 标签中的文本内容"""
        match = re.search(f"<{tag}>(.*?)</{tag}>", xml_block)
        return match.group(1) if match else ""


# ============================================================================
# 🧪 演示 Adapter 模式
# ============================================================================

def test_adapter_pattern():
    """
    展示 Adapter 模式如何优雅地解决接口不兼容问题
    """

    print("=" * 60)
    print("✅ Adapter 模式演示")
    print("=" * 60)

    # 1. 创建被适配者（旧系统）
    old_api = OldEmployeeAPI()

    # 2. 创建适配器
    adapter = EmployeeAdapter(old_api)

    # 3. 通过适配器获取 JSON 数据
    print("\n1️⃣  通过 Adapter 获取员工数据（JSON）")
    print("-" * 40)

    employees = adapter.get_employees()
    print(f"  员工列表（JSON 格式）:")
    for emp in employees:
        print(f"    - {emp['name']} | {emp['age']}岁 | {emp['dept']} | {emp['salary']}元")
    print(f"\n  数据类型: {type(employees)}")  # list
    print(f"  元素类型: {type(employees[0])}")  # dict

    # 4. 使用第三方库分析数据
    print("\n2️⃣  使用第三方库分析数据（直接传入 dict）")
    print("-" * 40)

    analyzer = NewDataAnalyzer()
    result = analyzer.analyze_employees(employees)

    print(f"  分析结果:")
    print(f"    - 总人数: {result['total_employees']}")
    print(f"    - 平均年龄: {result['average_age']}")
    print(f"    - 平均薪资: {result['average_salary']}")
    print(f"    - 部门分布: {result['department_distribution']}")

    # 5. 按 ID 查询
    print("\n3️⃣  按 ID 查询员工")
    print("-" * 40)

    emp = adapter.get_employee_by_id(1001)
    print(f"  查询结果: {emp}")

    # 6. Adapter 的复用性
    print("\n4️⃣  Adapter 的复用性")
    print("-" * 40)

    # 多个地方使用同一个 Adapter
    module_a = EmployeeAdapter(old_api)
    module_b = EmployeeAdapter(old_api)

    data_a = module_a.get_employees()
    data_b = module_b.get_employees()

    print(f"  模块 A 获取的数据条数: {len(data_a)}")
    print(f"  模块 B 获取的数据条数: {len(data_b)}")
    print(f"  转换逻辑集中在 Adapter 中，各模块不需要重复写转换代码 ✓")


# ============================================================================
# 对比：反模式 vs Adapter 模式
# ============================================================================

def comparison():
    """直观对比反模式和 Adapter 模式的代码质量"""

    print("\n" + "=" * 60)
    print("📊 对比：反模式 vs Adapter 模式")
    print("=" * 60)

    print("""
    ┌──────────────────────────────────────────────────────────────────────┐
    │  ❌ 反模式：散装转换                                                │
    ├──────────────────────────────────────────────────────────────────────┤
    │  # 模块 A                                                          │
    │  xml_data = old_api.get_employee_xml()                             │
    │  json_data = my_convert(xml_data)    # 每个模块都写自己的转换       │
    │  analyzer.analyze(json_data)                                       │
    │                                                                     │
    │  # 模块 B（又写一遍！）                                            │
    │  xml_data = old_api.get_employee_xml()                             │
    │  json_data = my_convert(xml_data)    # 几乎一样的代码！            │
    │  analyzer.analyze(json_data)                                       │
    │                                                                     │
    │  ❌ 转换逻辑散落在 N 个模块中                                       │
    │  ❌ XML 格式一变，N 个模块都得改                                    │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │  ✅ Adapter 模式                                                   │
    ├──────────────────────────────────────────────────────────────────────┤
    │  # 适配器——转换逻辑只在这里                                        │
    │  adapter = EmployeeAdapter(old_api)                                 │
    │                                                                     │
    │  # 模块 A                                                          │
    │  employees = adapter.get_employees()  # 直接拿 JSON                 │
    │  analyzer.analyze(employees)                                       │
    │                                                                     │
    │  # 模块 B                                                          │
    │  employees = adapter.get_employees()  # 同样的调用方式              │
    │  analyzer.analyze(employees)                                       │
    │                                                                     │
    │  ✅ 转换逻辑集中在一个类                                            │
    │  ✅ XML 格式变了只改 Adapter 一个类                                 │
    │  ✅ 各模块不需要知道底层是 XML 还是 JSON                            │
    └──────────────────────────────────────────────────────────────────────┘
    """)


# ============================================================================
# 高级话题：双向适配器
# ============================================================================

class TwoWayAdapter:
    """
    💡 高级用法：双向适配器（Two-Way Adapter）

    有时候，适配器需要双向工作：
    - 新系统可以通过 Adapter 调用旧系统（XML→JSON）
    - 旧系统也可以通过 Adapter 调用新系统（JSON→XML）

    这展示了 Adapter 模式的灵活性。
    """

    def __init__(self, old_api: OldEmployeeAPI = None, analyzer: NewDataAnalyzer = None):
        self._old_api = old_api
        self._analyzer = analyzer

    # 方向 1：XML → JSON（旧系统适配到新系统）
    def get_employees_json(self) -> List[Dict[str, Any]]:
        adapter = EmployeeAdapter(self._old_api)
        return adapter.get_employees()

    # 方向 2：JSON → XML（新系统适配到旧系统）
    def get_employees_xml(self) -> str:
        """如果旧系统也需要消费新系统的数据"""
        employees = self.get_employees_json()
        # 转换为 XML
        xml_parts = ['<?xml version="1.0"?>', "<employees>"]
        for emp in employees:
            xml_parts.append("  <employee>")
            for key, value in emp.items():
                xml_parts.append(f"    <{key}>{value}</{key}>")
            xml_parts.append("  </employee>")
        xml_parts.append("</employees>")
        return "\n".join(xml_parts)


if __name__ == "__main__":
    test_adapter_pattern()
    comparison()

    print("\n" + "=" * 60)
    print("💡 小结：什么时候用 Adapter？")
    print("   - 系统接口不兼容，且双方都不方便修改")
    print("   - 需要使用第三方库，但其接口与你的系统不匹配")
    print("   - 想复用已有的类，但它的接口不是你需要的")
    print("   - 需要创建一个中间层来解耦双方")
    print("=" * 60)


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: Adapter 模式和 Facade（外观）模式有什么区别？
    ┌─────────────────────────────────────────────────────────────────────┐
    │      Adapter 模式          │      Facade 模式                      │
    ├─────────────────────────────────────────────────────────────────────┤
    │ 接口转换：A → B            │ 接口简化：提供更简单的接口             │
    │ 为了让两个系统协作          │ 为了让客户端更方便                    │
    │ 通常只适配一个类            │ 通常封装多个子系统                    │
    │ 目的是兼容性                │ 目的是易用性                          │
    │ 示例：XML↔JSON 转换器       │ 示例：一键关机的按钮（关灯+关空调+锁门）│
    └─────────────────────────────────────────────────────────────────────┘
    一句话：Adapter 是为了让不兼容的能一起工作，
           Facade 是为了让复杂的系统用起来简单。

Q2: 类适配器（Class Adapter）vs 对象适配器（Object Adapter）？
    ┌─────────────────────────────────────────────────────────────────────┐
    │  对象适配器（推荐）        │  类适配器                              │
    ├─────────────────────────────────────────────────────────────────────┤
    │ 使用组合                  │ 使用多重继承                            │
    │ 灵活：可适配任意子类       │ 局限：只能适配特定的父类                │
    │ Python 原生支持           │ C++ 可用，Python 也可（但少用）         │
    │ 推荐使用 ✅               │ 特定场景使用                            │
    └─────────────────────────────────────────────────────────────────────┘
    优先使用对象适配器，因为它更灵活（组合优于继承）。

Q3: Adapter 模式在现实中有哪些例子？
    - 电源转换器（美标插头 → 国标插座）
    - USB-C 转 HDMI 转接线
    - 读卡器（SD卡 → USB接口）
    - 翻译器（中文 → 英文）
    - Python 的 zipfile 模块就是各种压缩格式的适配器

Q4: 使用 Adapter 模式有什么代价？
    - 增加了一层间接性，略微降低性能（多一次函数调用和转换）
    - 如果适配的类很多，需要写很多 Adapter 类
    - 如果接口差异太大，Adapter 可能变得很复杂

Q5: 什么时候不应该用 Adapter？
    - 如果可以修改 Adaptee 的接口，直接改更简单
    - 如果接口差异太大，可能需要考虑 Bridge 模式
    - 如果只需要简化接口，考虑 Facade 模式
    - 过度使用会导致系统有很多"胶水代码"

💡 面试官变种题：
    如果同时有多个第三方库，每个库都有不同的接口格式，
    怎么办？（比如 JSON、XML、CSV、Protobuf）
    思路：定义一个统一的目标接口，为每种格式写一个 Adapter。
    这就是 Adapter + Strategy 的组合应用。
"""
