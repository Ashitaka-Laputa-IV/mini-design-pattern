/*
================================================================================
 Lesson 1: Singleton — C++ 演示代码
================================================================================
  compile & run:
    g++ -std=c++11 -pthread singleton.cpp -o singleton
    ./singleton
================================================================================
*/

#include "singleton.h"

// 静态成员变量定义（必须在 .cpp 中定义）
BadLazySingleton* BadLazySingleton::instance_ = nullptr;
std::unique_ptr<Logger> Logger::instance_ = nullptr;
std::once_flag Logger::initFlag_;

int main() {
    std::cout << "====== C++ 单例模式演示 ======\n\n";

    // ---- 1. Meyers' Singleton ----
    std::cout << "--- 1. Meyers' Singleton ---\n";

    ConfigManager& c1 = ConfigManager::getInstance();
    ConfigManager& c2 = ConfigManager::getInstance();

    std::cout << "  c1 地址: " << &c1 << "\n";
    std::cout << "  c2 地址: " << &c2 << "\n";
    std::cout << "  是否同一个: " << (&c1 == &c2 ? "true" : "false") << "\n";

    c1.set("debug", "false");
    std::cout << "  c2.get(\"debug\") = " << c2.get("debug") << "\n";

    // c1 和 c2 是同一个对象，修改 c1 就是修改 c2

    // ---- 2. call_once Singleton ----
    std::cout << "\n--- 2. call_once Singleton ---\n";

    Logger& log1 = Logger::getInstance();
    Logger& log2 = Logger::getInstance();
    log1.log("第一条日志");
    log2.log("第二条日志（同一对象）");

    // ---- 3. ConfigManager 内容展示 ----
    std::cout << "\n--- 配置内容 ---\n";
    c1.display();

    /*
     * 💡 为什么 Singleton 的析构函数不是问题？
     * Meyers' Singleton 的 static 局部变量在 main() 结束后自动析构。
     * 但注意：如果其他 static 对象的析构函数调用了 Singleton，
     * 可能出现"静态初始化顺序失败"(Static Initialization Order Fiasco)。
     * 解决方案：Meyers' Singleton 本身能避免这个问题。
     */

    return 0;
}
