/*
================================================================================
 Lesson 2: Factory Method — C++ 工厂方法模式实现
================================================================================
  C++ 中的工厂方法模式实现要点：
    1. 抽象产品基类（带虚析构函数确保正确析构）
    2. 具体产品类继承抽象产品
    3. 抽象创建者基类（定义工厂方法接口）
    4. 具体创建者类实现工厂方法
    5. 使用 std::unique_ptr 管理对象生命周期

  🔑 面试要点：
    - C++ 中工厂方法通常返回智能指针（避免内存泄漏）
    - 虚析构函数是必须的（否则析构派生类时不会调用派生类的析构函数）
    - 对比 Python 的鸭子类型，C++ 是静态类型系统，接口更加严格
================================================================================
*/

#ifndef FACTORY_METHOD_H
#define FACTORY_METHOD_H

#include <iostream>
#include <memory>
#include <string>

// ============================================================================
// 1. 抽象产品 (Product)
// ============================================================================

/*
 * Logger 是所有日志类型的抽象基类。
 *
 * 在 C++ 中，抽象类通过"纯虚函数"（= 0）来定义接口。
 * 和 Python 的 ABC 类似，不能直接实例化。
 *
 * 🎯 注意虚析构函数：
 *   virtual ~Logger() = default;
 *   如果少了这行，delete 基类指针时不会调用派生类的析构函数，
 *   导致资源泄漏！这是 C++ 面试常考的点。
 */
class Logger {
public:
    virtual ~Logger() = default;

    // 纯虚函数：子类必须实现
    virtual void log(const std::string& message) = 0;
    virtual std::string getTypeName() const = 0;
};


// ============================================================================
// 2. 具体产品 (ConcreteProduct)
// ============================================================================

class ConsoleLogger : public Logger {
public:
    void log(const std::string& message) override {
        std::cout << "[控制台] " << message << "\n";
    }

    std::string getTypeName() const override {
        return "控制台";
    }
};


class FileLogger : public Logger {
public:
    FileLogger() {
        std::cout << "  [FileLogger] 打开文件: app.log\n";
    }

    void log(const std::string& message) override {
        std::cout << "[文件 app.log] " << message << "\n";
    }

    std::string getTypeName() const override {
        return "文件";
    }
};


class NetworkLogger : public Logger {
public:
    NetworkLogger() {
        std::cout << "  [NetworkLogger] 建立连接到 https://logs.example.com/api\n";
    }

    void log(const std::string& message) override {
        std::cout << "[网络] " << message << "\n";
    }

    std::string getTypeName() const override {
        return "网络";
    }
};


// ============================================================================
// 3. 抽象创建者 (Creator)
// ============================================================================

/*
 * LoggerCreator 是工厂方法模式的核心。
 *
 * 🧠 关键设计：
 *   1. createLogger() 是"工厂方法"——纯虚函数，子类实现
 *   2. writeLog() 是"模板方法"——调用工厂方法来完成业务逻辑
 *   3. 返回 unique_ptr——自动管理内存，不需要手动 delete
 *
 * 💡 unique_ptr 的好处：
 *   - 它是"独占所有权"的智能指针
 *   - 离开作用域自动释放
 *   - 不能拷贝，只能移动（明确所有权转移）
 *   - 在工厂方法中非常合适：工厂"生产"对象，把所有权交给调用者
 */
class LoggerCreator {
public:
    virtual ~LoggerCreator() = default;

    /*
     * 工厂方法：子类实现此方法创建具体的 Logger。
     *
     * 返回 unique_ptr<Logger> 而不是 Logger* 的原因：
     *   - 明确表示"我创建了一个对象，所有权交给你了"
     *   - 调用者不需要手动 delete
     *   - 避免内存泄漏
     */
    virtual std::unique_ptr<Logger> createLogger() = 0;

    /*
     * 模板方法：使用工厂方法创建 Logger 并写入日志。
     *
     * 🔑 这个函数并不知道具体用的是哪个 Logger 子类！
     * 它只通过 Logger 基类的接口来操作。
     * 这就是"依赖倒置原则"(DIP)的体现。
     */
    void writeLog(const std::string& message) {
        auto logger = createLogger();  // 多态调用！
        std::cout << "  [LoggerCreator] 使用 " << logger->getTypeName() << "Logger...\n";
        logger->log(message);
    }
};


// ============================================================================
// 4. 具体创建者 (ConcreteCreator)
// ============================================================================

class ConsoleLoggerCreator : public LoggerCreator {
public:
    std::unique_ptr<Logger> createLogger() override {
        return std::make_unique<ConsoleLogger>();
    }
};

class FileLoggerCreator : public LoggerCreator {
public:
    std::unique_ptr<Logger> createLogger() override {
        return std::make_unique<FileLogger>();
    }
};

class NetworkLoggerCreator : public LoggerCreator {
public:
    std::unique_ptr<Logger> createLogger() override {
        return std::make_unique<NetworkLogger>();
    }
};

#endif // FACTORY_METHOD_H
