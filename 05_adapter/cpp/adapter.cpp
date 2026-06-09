/*
================================================================================
Lesson 5: Adapter — C++ 适配器模式演示
================================================================================
  compile & run:
    g++ -std=c++11 adapter.cpp -o adapter
    ./adapter
================================================================================
*/

#include "adapter.h"

int main() {
    std::cout << "====== C++ 适配器模式演示 ======\n\n";

    // ---- 反模式回顾 ----
    std::cout << "--- [回顾] 之前的问题 ---\n";
    std::cout << " 每个模块自己写 XML → JSON 转换\n";
    std::cout << "  转换逻辑散落各处，XML 格式变化时到处要改\n\n";

    // ---- 对象适配器 ----
    std::cout << "--- 1. 对象适配器 (Object Adapter) ---\n";
    OldEmployeeAPI oldApi;
    EmployeeAnalyzerAdapter adapter(&oldApi);

    // Client 完全不知道底层是 XML！
    // 它只调用了 analyze() 这个统一接口
    adapter.analyze();

    // ---- 类适配器 ----
    std::cout << "\n--- 2. 类适配器 (Class Adapter) ---\n";
    ClassAdapter classAdapter;
    classAdapter.analyze();

    // ---- 适配器模式的优势 ----
    std::cout << "\n--- 优势总结 ---\n";
    std::cout << "  ✅ 不需要修改 OldEmployeeAPI（旧代码）\n";
    std::cout << "  ✅ 不需要修改 IEmployeeAnalyzer（新系统）\n";
    std::cout << "  ✅ 转换逻辑集中在一个地方\n";
    std::cout << "  ✅ 新增适配器不需要改已有代码（开闭原则）\n";

    return 0;
}
