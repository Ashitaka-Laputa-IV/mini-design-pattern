/*
================================================================================
 Lesson 1: Singleton — C++ 反模式示例
================================================================================
  和 Python 版本一样的场景：全局配置管理器。

  🎬 场景：
    你和同事做一个应用，需要一个全局配置对象。
    同事写了一个 ConfigManager 类，但每次 new 都重新加载文件。
    多个模块之间无法共享同一份配置数据。

  🧠 在 C++ 中，常见的"坏味道"是什么？
    - 全局变量（global variable）
    - 静态成员变量直接公开
    - 不同模块各自创建实例
================================================================================
*/

#include <iostream>
#include <string>
#include <unordered_map>

// ============================================================================
// 反模式 1：全局变量
// ============================================================================

std::unordered_map<std::string, std::string> g_config;  // 全局变量

void initConfig() {
    /*
     * ❌ 问题：
     *   - 全局变量可以被任何函数修改
     *   - 没有封装，没有访问控制
     *   - 多线程环境需要额外加锁（但谁也没加）
     *   - 测试困难：所有测试共享同一份数据
     */
    g_config["db_host"] = "localhost";
    g_config["db_port"] = "3306";
    g_config["debug"] = "true";
}

// ============================================================================
// 反模式 2：类本身可以被随意构造
// ============================================================================

class BadConfigManager {
    /*
     * ❌ 问题：
     *   - 构造函数是 public，任何人都可以 new
     *   - 每次 new 都重新加载配置，浪费 IO
     *   - 不同地方 new 出来的不是同一个对象
     */
public:
    std::unordered_map<std::string, std::string> config;

    BadConfigManager() {
        std::cout << "  [加载] 读取配置文件... (每次 new 都执行！)\n";
        config["db_host"] = "localhost";
        config["db_port"] = "3306";
    }

    std::string get(const std::string& key) {
        return config[key];
    }
};

int main() {
    std::cout << "====== C++ 反模式：全局配置管理 ======\n\n";

    // 反模式 1：全局变量
    initConfig();
    std::cout << "[反模式1] db_host = " << g_config["db_host"] << "\n";
    g_config["db_host"] = "hacker.com";  // 谁都能改！
    std::cout << "[反模式1] 被篡改后 db_host = " << g_config["db_host"] << "\n";

    // 反模式 2：多个实例
    std::cout << "\n[反模式2] 每次 new 都重新加载:\n";
    BadConfigManager b1;
    BadConfigManager b2;
    // b1 和 b2 不是同一个对象，修改 b1 不影响 b2
    b1.config["debug"] = "false";
    std::cout << "  b1.debug = " << b1.config["debug"] << "\n";
    std::cout << "  b2.debug = " << b2.config["debug"] << "\n";  // 还是 "true"!

    return 0;
}
