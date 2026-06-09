/*
================================================================================
 Lesson 1: Singleton — C++ 单例模式实现
================================================================================
  C++ 面试中 Singleton 是最高频考点之一。

  实现方式（从坏到好）：
    1. ❌ 懒汉式（直接判断指针，非线程安全）
    2. ❌ 饿汉式（静态全局初始化，有初始化顺序问题）
    3. ❌ 双检锁 DCLP（有指令重排问题）
    4. ✅ Meyers' Singleton (C++11 静态局部变量，线程安全)
    5. ✅ std::call_once + 静态指针

  🔑 面试要点：
    C++11 标准保证：静态局部变量的初始化是线程安全的！
    所以 Meyers' Singleton 是最简洁且正确的实现。
================================================================================
*/

#ifndef SINGLETON_H
#define SINGLETON_H

#include <iostream>
#include <string>
#include <unordered_map>
#include <mutex>
#include <memory>

// ============================================================================
// 实现 1：Meyers' Singleton (C++11 推荐方式)
// ============================================================================

class ConfigManager {
    /*
     * ✅ 最佳实践：Meyers' Singleton
     *
     * 原理：
     *   在 getInstance() 中定义 static 局部变量。
     *   C++11 及之后保证：static 局部变量的初始化在多线程中是安全的。
     *   只有第一次调用 getInstance() 时才构造，称为"懒汉式"。
     *
     * 优点：
     *   - 代码极简
     *   - 线程安全（C++11 保证）
     *   - 懒加载（按需初始化）
     *   - 无内存泄露风险（程序结束时自动析构）
     */
private:
    std::unordered_map<std::string, std::string> config_;
    bool initialized_ = false;

    // 把构造函数设为 private，禁止外部创建
    ConfigManager() {
        loadConfig();
    }

    void loadConfig() {
        if (initialized_) return;
        std::cout << "  [Meyers] 读取配置文件...\n";
        config_["db_host"] = "localhost";
        config_["db_port"] = "3306";
        config_["debug"] = "true";
        initialized_ = true;
    }

public:
    // 禁止拷贝和赋值（C++11 delete 语法）
    ConfigManager(const ConfigManager&) = delete;
    ConfigManager& operator=(const ConfigManager&) = delete;

    // 全局访问点
    static ConfigManager& getInstance() {
        /*
         * 🎯 C++11 保证：static 局部变量在第一次使用时
         * 以线程安全的方式初始化。
         * 编译器会自动加入锁机制。
         */
        static ConfigManager instance;
        return instance;
    }

    std::string get(const std::string& key, const std::string& default_val = "") {
        auto it = config_.find(key);
        return (it != config_.end()) ? it->second : default_val;
    }

    void set(const std::string& key, const std::string& value) {
        config_[key] = value;
    }

    void display() const {
        std::cout << "  ConfigManager 内容:\n";
        for (const auto& [key, value] : config_) {
            std::cout << "    " << key << " = " << value << "\n";
        }
    }
};


// ============================================================================
// 实现 2：std::call_once 方式（适用于更复杂的初始化场景）
// ============================================================================

class Logger {
    /*
     * call_once 方式：当你需要在单例初始化时做更多控制时使用。
     *
     * 适用场景：
     *   - 初始化需要更多参数
     *   - 需要处理初始化失败的情况
     *   - 需要在程序运行过程中重新初始化
     */
private:
    static std::unique_ptr<Logger> instance_;
    static std::once_flag initFlag_;

    Logger() {
        std::cout << "  [call_once] 初始化 Logger...\n";
    }

    static void init() {
        instance_.reset(new Logger());
    }

public:
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    ~Logger() = default;

    static Logger& getInstance() {
        /*
         * std::call_once 保证 init() 只会被调用一次，
         * 即使在多线程环境下。
         */
        std::call_once(initFlag_, init);
        return *instance_;
    }

    void log(const std::string& msg) {
        std::cout << "  [LOG] " << msg << "\n";
    }
};


// ============================================================================
// 实现 3：对比展示——非线程安全的懒汉式（面试常考"错在哪里"）
// ============================================================================

class BadLazySingleton {
    /*
     * ❌ 错误的懒汉式实现 —— 面试官会让你指出问题
     *
     * 问题：
     *   1. instance_ 是裸指针，谁负责 delete？
     *   2. if (instance_ == nullptr) 存在竞态条件
     *      (Race Condition)：两个线程同时进入 if 判断
     *   3. 没有处理内存泄漏
     */
private:
    static BadLazySingleton* instance_;

    BadLazySingleton() = default;

public:
    BadLazySingleton(const BadLazySingleton&) = delete;
    BadLazySingleton& operator=(const BadLazySingleton&) = delete;

    static BadLazySingleton* getInstance() {
        if (instance_ == nullptr) {  // ❌ 竞态条件！
            instance_ = new BadLazySingleton();
        }
        return instance_;
    }
};

#endif // SINGLETON_H
