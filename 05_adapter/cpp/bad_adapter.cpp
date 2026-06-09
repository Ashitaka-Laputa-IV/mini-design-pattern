/*
================================================================================
Lesson 5: Adapter — C++ 反模式示例 [结构型]
================================================================================
  C++ 中的接口不兼容问题更常见：
  - 不同库用不同的数据格式
  - 旧系统的接口不能改，新系统接口不能动
  - 第三方库只有二进制，无法修改源码

  🎬 场景和 Python 版本一致：旧系统返回 XML，新库需要 JSON。
================================================================================*/

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>

// ============================================================================
// 被适配者：旧系统的 XML 接口
// ============================================================================

class OldEmployeeAPI {
    /*
     * 🏢 公司现有的老系统——所有接口返回 XML 格式。
     * 不能修改这个类！
     */
public:
    std::string getEmployeeXML() const {
        return
            "<?xml version=\"1.0\"?>"
            "<employees>"
            "<employee><name>张三</name><age>28</age><dept>技术部</dept></employee>"
            "<employee><name>李四</name><age>35</age><dept>产品部</dept></employee>"
            "<employee><name>王五</name><age>42</age><dept>技术部</dept></employee>"
            "</employees>";
    }

    std::string getEmployeeByIDXML(int emp_id) const {
        std::ostringstream xml;
        xml << "<?xml version=\"1.0\"?>"
            << "<employee>"
            << "<id>" << emp_id << "</id>"
            << "<name>张三</name><age>28</age><dept>技术部</dept>"
            << "</employee>";
        return xml.str();
    }
};


// ============================================================================
// 第三方库：只接受 JSON 的分析器
// ============================================================================

class NewDataAnalyzer {
    /*
     * 📦 新引入的第三方数据分析库——只接受 JSON。
     * 不能修改这个类！
     */
public:
    struct AnalysisResult {
        int total_employees;
        double average_age;
        std::map<std::string, int> department_distribution;
    };

    /*
     * 分析员工数据。
     * 参数用简单的数据结构模拟 JSON。
     */
    AnalysisResult analyze(const std::vector<std::map<std::string, std::string>>& employees) const {
        AnalysisResult result;
        result.total_employees = static_cast<int>(employees.size());
        result.average_age = 0.0;

        if (employees.empty()) return result;

        int total_age = 0;
        for (const auto& emp : employees) {
            auto it = emp.find("age");
            if (it != emp.end()) {
                total_age += std::stoi(it->second);
            }

            auto dept_it = emp.find("dept");
            if (dept_it != emp.end()) {
                result.department_distribution[dept_it->second]++;
            }
        }

        result.average_age = static_cast<double>(total_age) / employees.size();
        return result;
    }
};


// ============================================================================
// ❌ 反模式：在客户端代码中到处做转换
// ============================================================================

/*
 * 问题：
 * 1. 每个使用处都要写 XML→JSON 转换代码
 * 2. 转换逻辑散落在各模块中，维护困难
 * 3. XML 格式变化时，所有地方都要改
 */

// 非常粗糙的 XML 解析（仅用于演示反模式问题）
std::vector<std::map<std::string, std::string>> parseXML_antipattern(
    const std::string& xml) {

    std::vector<std::map<std::string, std::string>> result;
    std::map<std::string, std::string> current;

    // 简单的标签提取（仅供演示）
    auto extract = [](const std::string& str, const std::string& tag) -> std::string {
        std::string open = "<" + tag + ">";
        std::string close = "</" + tag + ">";
        auto start = str.find(open);
        if (start == std::string::npos) return "";
        start += open.length();
        auto end = str.find(close, start);
        if (end == std::string::npos) return "";
        return str.substr(start, end - start);
    };

    // 提取每个 employee 块
    size_t pos = 0;
    while (true) {
        std::string open = "<employee>";
        std::string close = "</employee>";
        auto start = xml.find(open, pos);
        if (start == std::string::npos) break;
        start += open.length();
        auto end = xml.find(close, start);
        if (end == std::string::npos) break;

        std::string block = xml.substr(start, end - start);
        current["name"] = extract(block, "name");
        current["age"] = extract(block, "age");
        current["dept"] = extract(block, "dept");

        result.push_back(current);
        pos = end + close.length();
    }

    return result;
}


int main() {
    std::cout << "====== C++ 反模式：散装的接口转换 ======\n\n";

    OldEmployeeAPI old_api;
    NewDataAnalyzer analyzer;

    // ---- 散装转换的问题 ----
    std::cout << "1️⃣  模块 A：自己写转换\n";
    std::cout << "-----------------------------\n\n";

    std::string xml1 = old_api.getEmployeeXML();
    // 模块 A 自己写了转换
    auto data1 = parseXML_antipattern(xml1);
    auto result1 = analyzer.analyze(data1);

    std::cout << "  模块 A 分析结果:\n";
    std::cout << "    总人数: " << result1.total_employees << "\n";
    std::cout << "    平均年龄: " << result1.average_age << "\n";

    // ---- 另一个模块又写一次 ----
    std::cout << "\n2️⃣  模块 B：又写了一遍相同的转换！\n";
    std::cout << "-----------------------------\n\n";

    std::string xml2 = old_api.getEmployeeXML();
    auto data2 = parseXML_antipattern(xml2);  // 完全相同的代码！
    auto result2 = analyzer.analyze(data2);

    std::cout << "  模块 B 分析结果:\n";
    std::cout << "    总人数: " << result2.total_employees << "\n";

    // ---- 如果直接修改第三方库 ----
    std::cout << "\n3️⃣  直接修改第三方库的问题\n";
    std::cout << "-----------------------------\n\n";

    std::cout << "  ❌ 如果改 ThirdPartyAnalyzer:\n";
    std::cout << "     - 库升级时修改被覆盖\n";
    std::cout << "     - 许可证可能不允许修改\n";
    std::cout << "     - 其他项目也受影响\n";

    std::cout << "\n====== 结论 ======\n";
    std::cout << "C++ 中接口不兼容问题更常见（不同库的字符串格式、二进制格式等）\n";
    std::cout << "推荐使用 Adapter 模式解决。\n";

    return 0;
}
