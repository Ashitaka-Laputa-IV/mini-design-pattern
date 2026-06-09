/*
================================================================================
 Lesson 2: Factory Method — C++ 演示代码
================================================================================
  compile & run:
    g++ -std=c++14 factory_method.cpp -o factory_method
    ./factory_method

  注意：使用 C++14 是因为 std::make_unique 是 C++14 引入的。
  如果只能用 C++11，可以用 std::unique_ptr<T>(new T()) 替代。
================================================================================
*/

#include "factory_method.h"
#include <memory>
#include <vector>

/*
 * 客户端代码示例。
 *
 * 展示如何使用工厂方法模式：
 *   - 客户端只依赖 LoggerCreator 和 Logger 这两个抽象类
 *   - 客户端不知道具体的 Logger 是如何创建的
 *   - 新增日志类型不需要修改客户端代码
 */
int main() {
    std::cout << "====== C++ 工厂方法模式演示 ======\n\n";

    // 创建各种 Creator（客户端选择需要哪种 Logger）
    std::vector<std::unique_ptr<LoggerCreator>> creators;
    creators.push_back(std::make_unique<ConsoleLoggerCreator>());
    creators.push_back(std::make_unique<FileLoggerCreator>());
    creators.push_back(std::make_unique<NetworkLoggerCreator>());

    // 通过统一的接口使用——完全不知道具体类型！
    for (auto& creator : creators) {
        creator->writeLog("这是一条测试日志");
        std::cout << "\n";
    }

    std::cout << "--- 现在想加 DatabaseLogger ---\n";
    std::cout << "   1. 新建 DatabaseLogger 类继承 Logger\n";
    std::cout << "   2. 新建 DatabaseLoggerCreator 类继承 LoggerCreator\n";
    std::cout << "   3. 客户端添加 DatabaseLoggerCreator\n";
    std::cout << "   ✅ 不需要修改任何已有的 Creator 或 Logger 代码！\n";

    /*
     * 💡 思考题：
     * 如果不用工厂方法，而是用 if-else，上面的扩展需要改哪些代码？
     *
     * 对比：
     *   工厂方法：新增 2 个类（Product + Creator），改 1 处（客户端添加新 Creator）
     *   if-else：改 1 处（工厂函数加 elif），但改的是已有代码（风险高）
     *
     * 核心区别：工厂方法是"扩展"(extend)，if-else 是"修改"(modify)。
     * 开闭原则说：对扩展开放，对修改封闭。
     */

    return 0;
}
