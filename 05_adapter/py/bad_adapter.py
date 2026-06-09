"""
================================================================================
Lesson 5: Adapter — 适配器模式（反模式篇）[结构型]
================================================================================
 📖 本课采用"反模式驱动"方式：
    先看坏代码长什么样，感受痛点，再引入设计模式解决问题。

 🔑 面试频率：★★★★☆（中高频）
================================================================================
"""

"""
===============================================================================
 🎬 场景：你的系统用 XML，第三方库只提供 JSON

  公司有一个老旧的"员工信息查询系统"，所有接口都返回 XML 格式的数据。
  现在老板说要用一个新的第三方数据分析库（只支持 JSON），
  让你把系统对接起来。

  系统现有接口：

      class OldEmployeeAPI:
          def get_employee_xml(self) -> str:
              # 返回 XML 格式的员工数据
              ...

  第三方库要求：

      class NewAnalyzer:
          def analyze(self, json_data: dict) -> dict:
              # 只接受 JSON (Python dict)
              ...

  你的同事提出了两个"方案"——都是典型的反模式！
===============================================================================
"""


# ============================================================================
# 反模式 1：直接修改第三方库代码
# ============================================================================

"""
❌ 方案一："直接把第三方库改成支持 XML 不就好了？"

问题：
  1. 第三方库可能有版本更新——改了之后没法升级
  2. 侵犯许可证（有的库不允许修改源码）
  3. 如果别人也在用这个库，你的修改会影响他们
  4. 第三方库可能很复杂，改一个地方牵一发动全身
  5. 不符合"开闭原则"（对扩展开放，对修改关闭）
"""

# 假设这是第三方库的源码（模拟）
class ThirdPartyAnalyzer:
    """
    📦 这是一个第三方数据分析库。
    注意：这是别人的代码，我们不建议修改它！
    """

    def analyze(self, json_data: dict) -> dict:
        """
        对员工数据进行分析。
        只接受 JSON 格式（Python dict）。

        参数:
            json_data: dict, 包含员工信息的 JSON 数据

        返回:
            dict, 分析结果
        """
        employees = json_data.get("employees", [])
        total = len(employees)
        avg_age = sum(e.get("age", 0) for e in employees) / max(total, 1)
        dept_count = {}
        for e in employees:
            dept = e.get("dept", "unknown")
            dept_count[dept] = dept_count.get(dept, 0) + 1

        return {
            "total_employees": total,
            "average_age": round(avg_age, 1),
            "department_distribution": dept_count,
        }


# ============================================================================
# 反模式 2：到处做 XML→JSON 转换（代码分散）
# ============================================================================

class OldEmployeeAPI:
    """
    🏢 公司现有的老系统——所有接口返回 XML 格式。

    这个系统已经运行了 10 年，有几百个模块依赖它。
    把所有接口改成 JSON 的代价太大了。
    """

    def get_employee_xml(self) -> str:
        """
        获取员工信息（XML 格式）。

        返回类似:
        <employees>
            <employee>
                <name>张三</name>
                <age>28</age>
                <dept>技术部</dept>
            </employee>
        </employees>
        """
        return """<?xml version="1.0"?>
<employees>
    <employee>
        <name>张三</name>
        <age>28</age>
        <dept>技术部</dept>
    </employee>
    <employee>
        <name>李四</name>
        <age>35</age>
        <dept>产品部</dept>
    </employee>
    <employee>
        <name>王五</name>
        <age>42</age>
        <dept>技术部</dept>
    </employee>
</employees>"""

    def get_department_xml(self, dept: str) -> str:
        """
        按部门查询员工（XML 格式）
        """
        return f"""<?xml version="1.0"?>
<employees>
    <employee>
        <name>张三</name>
        <age>28</age>
        <dept>{dept}</dept>
    </employee>
</employees>"""

    def get_employee_by_id_xml(self, emp_id: int) -> str:
        """
        按 ID 查询员工（XML 格式）
        """
        return f"""<?xml version="1.0"?>
<employee>
    <id>{emp_id}</id>
    <name>张三</name>
    <age>28</age>
    <dept>技术部</dept>
</employee>"""


# ============================================================================
# ❌ 反模式：到处做转换的散装代码
# ============================================================================

"""
❌ 方案二："在每个需要的地方手动转换 XML→JSON"

问题：
  1. 转换逻辑散落在各个业务模块中，重复代码多
  2. 如果 XML 格式变了，所有地方都要改（维护噩梦）
  3. 业务代码和转换逻辑耦合在一起，难以测试
  4. 新人来了不知道哪里做了转换，哪里没做
  5. 不符合"单一职责原则"
"""


def xml_to_json_basic(xml_str: str) -> dict:
    """
    一个简单的 XML→JSON 转换函数。
    （实际项目中应该用 xml.etree.ElementTree，这里模拟）

    注意：这个函数可能会在很多地方被调用——如果 XML 格式变了，
    所有调用处都得检查是否需要更新！
    """
    # 模拟解析 XML
    # 在实际项目中，转换逻辑可能散落在 10+ 个模块中
    if "<employee>" in xml_str and "<name>" in xml_str:
        # 非常粗糙的解析——只是为了演示
        import re
        names = re.findall(r"<name>(.*?)</name>", xml_str)
        ages = re.findall(r"<age>(.*?)</age>", xml_str)
        depts = re.findall(r"<dept>(.*?)</dept>", xml_str)

        employees = []
        for i in range(len(names)):
            employees.append({
                "name": names[i] if i < len(names) else "",
                "age": int(ages[i]) if i < len(ages) else 0,
                "dept": depts[i] if i < len(depts) else "",
            })

        return {"employees": employees}
    return {}


def show_anti_pattern_problems():
    """
    展示散装转换的各种问题
    """

    print("=" * 60)
    print("❌ 反模式：散装的 XML→JSON 转换")
    print("=" * 60)

    api = OldEmployeeAPI()

    # ---- 场景 1：模块 A 做了一次转换 ----
    print("\n1️⃣  模块 A：员工分析功能")
    print("-" * 40)

    xml_data = api.get_employee_xml()
    # 模块 A 自己写了一个转换
    json_data = xml_to_json_basic(xml_data)

    analyzer = ThirdPartyAnalyzer()
    result = analyzer.analyze(json_data)
    print(f"  分析结果: {result}")

    # ---- 场景 2：模块 B 又做了一次相同的转换 ----
    print("\n2️⃣  模块 B：另一个地方重复的转换代码")
    print("-" * 40)

    xml_data2 = api.get_employee_xml()
    # 模块 B 写了几乎一样的转换代码！
    json_data2 = xml_to_json_basic(xml_data2)
    print(f"  模块 B 也做了一遍转换: {json_data2}")

    # ---- 场景 3：XML 格式变化 ----
    print("\n3️⃣  如果 XML 格式变了……")
    print("-" * 40)

    # 假设有一天 XML 的 <name> 改成了 <full_name>
    # 那么所有调用 xml_to_json_basic 的地方都要修改！
    print("""
    😱 灾难场景：
    某天 XML 格式升级，<name> 改为 <full_name>：
    
    你需要找到所有写 xml_to_json_basic() 的地方……
        - module_a.py 第 42 行
        - module_b.py 第 78 行
        - module_c.py 第 15 行
        - ...
        - module_z.py 第 103 行
    
    漏改一个就出 Bug！这就是"散装转换"的噩梦。
    """)

    # ---- 场景 4：如果有人直接修改了第三方库…… ----
    print("\n4️⃣  如果直接修改第三方库……")
    print("-" * 40)

    print("""
    假设你同事把 ThirdPartyAnalyzer 改成了支持 XML：
    
    class ThirdPartyAnalyzer:
        def analyze(self, data) -> dict:
            if isinstance(data, str):  # 加了 XML 支持
                data = xml_to_json(data)
            ...
    
    问题：
    1. 库升级时，你的修改会被覆盖
    2. 其他项目如果也用这个库，升级就受影响
    3. 如果库是 pip install 安装的，改源码更不现实
    """)


if __name__ == "__main__":
    show_anti_pattern_problems()

    print("\n" + "=" * 60)
    print("👉 请继续看 adapter.py，看看 Adapter 模式如何解决这些问题！")
    print("=" * 60)


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 什么时候应该考虑使用适配器模式？
    - 你想使用一个已有的类，但它的接口与你的代码不兼容
    - 你想创建一个可复用的类，与不相关的类或不可预见的类协作
    - （对象适配器）你需要使用多个现有子类，但通过适配它们父类的接口来统一

Q2: 直接修改第三方库有什么风险？
    - 版本更新冲突：你的修改会被新版本覆盖
    - 许可证风险：某些开源协议不允许修改
    - 影响范围不可控：其他使用该库的项目也会受影响
    - 开闭原则违反：应该对扩展开放，对修改关闭

Q3: 为什么不用"到处手动转换"的方式？
    - 重复代码：每个使用处都要写转换逻辑
    - 维护困难：格式变化时到处都要改
    - 关注点混杂：业务代码中混入转换逻辑
    - 可测试性差：很难单独测试转换逻辑
"""
