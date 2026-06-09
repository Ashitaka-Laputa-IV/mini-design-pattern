/*
================================================================================
Lesson 5: Adapter — C++ 适配器模式 [结构型]
================================================================================
  解决"接口不兼容"的问题——不改旧代码，不加新转换，用适配器桥接。

  C++ 中有两种适配器：
    1. 类适配器 (Class Adapter)：通过多重继承，适配Target和Adaptee
    2. 对象适配器 (Object Adapter)：通过组合，持有Adaptee对象

  ✅ 推荐使用对象适配器，更灵活（C++多重继承会增加复杂性）
================================================================================
*/

#ifndef ADAPTER_H
#define ADAPTER_H

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>

// ============================================================================
// Adaptee (被适配者) — 旧系统的 XML 接口
// ============================================================================

class OldEmployeeAPI {
public:
    std::string getEmployeeXML() const {
        return
            "<?xml version=\"1.0\"?>"
            "<employees>"
            "<employee><name>张三</name><age>28</age><dept>技术部</dept></employee>"
            "<employee><name>李四</name><age>35</age><dept>产品部</dept></employee>"
            "</employees>";
    }
};


// ============================================================================
// Target (目标接口) — 新系统需要的 JSON 接口
// ============================================================================

struct Employee {
    std::string name;
    int age;
    std::string dept;
};

// 新数据分析器的目标接口
class IEmployeeAnalyzer {
public:
    virtual ~IEmployeeAnalyzer() = default;
    virtual void analyze() = 0;
};


// ============================================================================
// Adaptee 的包装：对象适配器 (Object Adapter)
// ============================================================================
/*
 * 🎯 核心思想：
 *   适配器继承 Target 接口，组合 Adaptee 对象，
 *   在中间完成转换工作。
 *
 *   Client → [Target接口] → Adapter → [Adaptee]
 *                                 ↕
 *                           数据格式转换
 */

class EmployeeAnalyzerAdapter : public IEmployeeAnalyzer {
private:
    OldEmployeeAPI* oldApi_;           // 持有 Adaptee（组合）
    std::vector<Employee> employees_;  // 转换后的数据

    // ⭐ 适配的核心：XML → 内部数据结构
    std::vector<Employee> convertXMLToEmployees(const std::string& xml) const {
        std::vector<Employee> result;

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
            Employee emp;
            emp.name = extract(block, "name");
            emp.age = std::stoi(extract(block, "age"));
            emp.dept = extract(block, "dept");
            result.push_back(emp);
            pos = end + close.length();
        }
        return result;
    }

public:
    explicit EmployeeAnalyzerAdapter(OldEmployeeAPI* api)
        : oldApi_(api) {}

    // ⭐ 统一的 analyze 接口——Client 不需要知道底层是 XML
    void analyze() override {
        std::string xml = oldApi_->getEmployeeXML();
        employees_ = convertXMLToEmployees(xml);

        std::cout << "  [适配器] 员工数据分析结果:\n";
        std::cout << "    总人数: " << employees_.size() << "\n";

        int totalAge = 0;
        for (const auto& emp : employees_) {
            totalAge += emp.age;
        }
        std::cout << "    平均年龄: " << (totalAge / employees_.size()) << "\n";

        // 部门分布
        std::map<std::string, int> deptCount;
        for (const auto& emp : employees_) {
            deptCount[emp.dept]++;
        }
        std::cout << "    部门分布:\n";
        for (const auto& [dept, count] : deptCount) {
            std::cout << "      " << dept << ": " << count << "人\n";
        }
    }
};


// ============================================================================
// 类适配器示例（Class Adapter）— 使用多重继承
// ============================================================================
/*
 * 类适配器同时继承 Target 和 Adaptee。
 * 优点：不需要组合对象，可以直接调用 Adaptee 的方法
 * 缺点：需要多重继承，在某些语言(C++没问题)和场景下不灵活
 */

class ClassAdapter : public IEmployeeAnalyzer,
                     private OldEmployeeAPI {  // private 继承隐藏细节
public:
    void analyze() override {
        // 直接使用 Adaptee 的方法
        std::string xml = getEmployeeXML();
        std::cout << "  [类适配器] XML 数据长度: " << xml.length() << "\n";
        std::cout << "  [类适配器] 已转换并分析完成\n";
    }
};

#endif // ADAPTER_H
