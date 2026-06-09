/*
================================================================================
 Lesson 2: Factory Method — C++ 反模式示例
================================================================================
  🎬 场景：和 Python 版本一样——一个日志系统需要支持不同格式的输出。

  在 C++ 中，常见的"坏味道"是：
    - 用 if-else 或 switch-case 创建不同对象
    - 所有创建逻辑集中在一个函数/类中
    - 新增类型需要修改已有代码

  🧠 思考：这个代码的问题在哪？
================================================================================
*/

#include <iostream>
#include <string>
#include <memory>

// ============================================================================
// 产品类：各种 Logger
// ============================================================================

class ConsoleLogger {
public:
    void log(const std::string& message) {
        std::cout << "[控制台] " << message << "\n";
    }
};

class FileLogger {
public:
    FileLogger() {
        std::cout << "  [FileLogger] 打开文件: app.log\n";
    }

    void log(const std::string& message) {
        std::cout << "[文件 app.log] " << message << "\n";
    }
};

class NetworkLogger {
public:
    NetworkLogger() {
        std::cout << "  [NetworkLogger] 建立连接到 https://logs.example.com/api\n";
    }

    void log(const std::string& message) {
        std::cout << "[网络] " << message << "\n";
    }
};

// ============================================================================
// ❌ 反模式：用 if-else 创建对象
// ============================================================================

/*
 * 问题分析（和 Python 版本一样）：
 *   1. 每次增加新的日志类型，都要加一个 else if
 *   2. 违反了"开闭原则"——对扩展开放，对修改封闭
 *   3. 所有创建逻辑耦合在一起
 *   4. 返回裸指针，谁负责 delete？
 *      （这里故意用裸指针来展示问题）
 */
class LoggerFactory {
public:
    /*
     * ❌ 问题方法：根据字符串类型创建不同的 Logger
     *
     * 每次加新类型都要改这个函数！
     * 而且返回 void* 不是类型安全的
     */
    static void* createLogger(const std::string& type) {
        std::cout << "  [工厂] 正在创建 " << type << " 日志...\n";

        if (type == "console") {
            return new ConsoleLogger();
        } else if (type == "file") {
            return new FileLogger();
        } else if (type == "network") {
            return new NetworkLogger();
        }
        // 如果要加 DatabaseLogger:
        // else if (type == "database") {
        //     return new DatabaseLogger();  // 又要改这个函数！
        // }
        else {
            std::cerr << "不支持的日志类型: " << type << "\n";
            return nullptr;
        }
    }
};

int main() {
    std::cout << "====== C++ 反模式：if-else 工厂方法 ======\n\n";

    /*
     * ❌ 反模式的使用方式：
     *   - 调用者必须知道返回的是什么类型，然后做类型转换
     *   - 转换错了就出 bug
     *   - 还要手动 delete，容易内存泄漏
     */
    std::cout << "--- 反模式使用 ---\n";

    void* obj = LoggerFactory::createLogger("console");
    if (obj) {
        // 需要手动转回具体类型
        static_cast<ConsoleLogger*>(obj)->log("这是一条控制台日志");
        delete static_cast<ConsoleLogger*>(obj);
    }

    obj = LoggerFactory::createLogger("file");
    if (obj) {
        static_cast<FileLogger*>(obj)->log("这是一条文件日志");
        delete static_cast<FileLogger*>(obj);
    }

    std::cout << "\n⚠  如果再加 DatabaseLogger，必须修改 LoggerFactory！\n";
    std::cout << "   这就是"开闭原则"被违反的典型案例。\n";

    return 0;
}
