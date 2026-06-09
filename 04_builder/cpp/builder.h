/*
================================================================================
Lesson 4: Builder — C++ Builder 模式实现 [创建型]
================================================================================
  C++ 中实现 Builder 模式的两种方式：
  1. 外部 Builder 类（推荐，最常用）
  2. 内部 Builder 类（Java 风格，C++ 也可实现）

  本文件采用"外部 Builder 类"方式，展示 Fluent Interface（链式调用）。

  🔑 C++ 实现要点：
    - 产品类的构造函数设为 private（限制外部直接创建）
    - Builder 类设为产品类的友元（friend class）
    - Builder 返回 *this 实现链式调用
    - 禁止拷贝构造和赋值（C++11 delete）
================================================================================
*/

#ifndef BUILDER_H
#define BUILDER_H

#include <iostream>
#include <string>

// ============================================================================
// 前向声明
// ============================================================================

class ComputerBuilder;  // Builder 类的前向声明


// ============================================================================
// 产品类：Computer（电脑）
// ============================================================================

class Computer {
    /*
     * 🎯 最终产品——构建完成后不可变
     *
     * 设计要点：
     * 1. 构造函数是 private——只能通过 Builder 创建
     * 2. 没有 setter——创建后不可修改
     * 3. 有 getter 用于读取属性
     * 4. Builder 是友元，可以访问私有构造函数
     */

private:
    // --- 私有成员变量 ---
    std::string cpu_;
    std::string ram_;
    std::string storage_;
    std::string gpu_;
    std::string os_;
    bool has_wifi_;
    bool has_bluetooth_;
    std::string keyboard_;
    std::string mouse_;

    // 构造函数设为私有——只有友元类可以调用
    friend class ComputerBuilder;  // Builder 是友元

    // 私有构造函数，只能通过 Builder 创建
    Computer()
        : gpu_("集成显卡"), os_("无"),
          has_wifi_(false), has_bluetooth_(false),
          keyboard_("标准键盘"), mouse_("标准鼠标") {}

public:
    // 禁止拷贝和赋值
    Computer(const Computer&) = delete;
    Computer& operator=(const Computer&) = delete;

    // 允许移动构造和移动赋值（C++11）
    Computer(Computer&& other) noexcept
        : cpu_(std::move(other.cpu_)),
          ram_(std::move(other.ram_)),
          storage_(std::move(other.storage_)),
          gpu_(std::move(other.gpu_)),
          os_(std::move(other.os_)),
          has_wifi_(other.has_wifi_),
          has_bluetooth_(other.has_bluetooth_),
          keyboard_(std::move(other.keyboard_)),
          mouse_(std::move(other.mouse_)) {}

    Computer& operator=(Computer&& other) noexcept {
        if (this != &other) {
            cpu_ = std::move(other.cpu_);
            ram_ = std::move(other.ram_);
            storage_ = std::move(other.storage_);
            gpu_ = std::move(other.gpu_);
            os_ = std::move(other.os_);
            has_wifi_ = other.has_wifi_;
            has_bluetooth_ = other.has_bluetooth_;
            keyboard_ = std::move(other.keyboard_);
            mouse_ = std::move(other.mouse_);
        }
        return *this;
    }

    // --- Getter 方法（只读）---
    const std::string& cpu() const { return cpu_; }
    const std::string& ram() const { return ram_; }
    const std::string& storage() const { return storage_; }
    const std::string& gpu() const { return gpu_; }
    const std::string& os() const { return os_; }
    bool has_wifi() const { return has_wifi_; }
    bool has_bluetooth() const { return has_bluetooth_; }
    const std::string& keyboard() const { return keyboard_; }
    const std::string& mouse() const { return mouse_; }

    // 显示配置信息
    void display() const {
        std::cout << "┌─ 电脑配置 ────────────────────────┐\n"
                  << "  CPU    : " << cpu_ << "\n"
                  << "  内存   : " << ram_ << "\n"
                  << "  硬盘   : " << storage_ << "\n"
                  << "  显卡   : " << gpu_ << "\n"
                  << "  系统   : " << os_ << "\n"
                  << "  WiFi   : " << (has_wifi_ ? "✓" : "✗") << "\n"
                  << "  蓝牙   : " << (has_bluetooth_ ? "✓" : "✗") << "\n"
                  << "  键盘   : " << keyboard_ << "\n"
                  << "  鼠标   : " << mouse_ << "\n"
                  << "└────────────────────────────────────┘\n";
    }
};


// ============================================================================
// Builder 类：ComputerBuilder
// ============================================================================

class ComputerBuilder {
    /*
     * 🎯 Builder 类——负责一步步构建 Computer 对象
     *
     * 核心设计（Fluent Interface / 链式调用）：
     * 每个 setter 方法返回 ComputerBuilder&（*this 的引用）
     * 这样客户端可以连续调用：builder.setX().setY().build()
     *
     * 为什么返回引用而不是值？
     * 返回引用避免拷贝，保持操作的是同一个 builder 对象。
     */

private:
    Computer computer_;  // 内部持有的正在构建的产品

public:
    ComputerBuilder() = default;

    // --- 链式 Setter 方法 ---
    // 每个方法返回 ComputerBuilder& 以实现链式调用

    ComputerBuilder& set_cpu(const std::string& cpu) {
        computer_.cpu_ = cpu;
        return *this;
    }

    ComputerBuilder& set_ram(const std::string& ram) {
        computer_.ram_ = ram;
        return *this;
    }

    ComputerBuilder& set_storage(const std::string& storage) {
        computer_.storage_ = storage;
        return *this;
    }

    ComputerBuilder& set_gpu(const std::string& gpu) {
        computer_.gpu_ = gpu;
        return *this;
    }

    ComputerBuilder& set_os(const std::string& os) {
        computer_.os_ = os;
        return *this;
    }

    ComputerBuilder& enable_wifi() {
        computer_.has_wifi_ = true;
        return *this;
    }

    ComputerBuilder& enable_bluetooth() {
        computer_.has_bluetooth_ = true;
        return *this;
    }

    ComputerBuilder& set_keyboard(const std::string& keyboard) {
        computer_.keyboard_ = keyboard;
        return *this;
    }

    ComputerBuilder& set_mouse(const std::string& mouse) {
        computer_.mouse_ = mouse;
        return *this;
    }

    /*
     * build() —— 构建最终产品
     *
     * 在 build() 中做校验，确保必填项已设置。
     * 使用 std::move 转移所有权，避免拷贝。
     *
     * build() 之后，当前 Builder 对象不再有效。
     */
    Computer build() {
        // 校验必填参数
        if (computer_.cpu_.empty()) {
            throw std::runtime_error("CPU 是必填项！");
        }
        if (computer_.ram_.empty()) {
            throw std::runtime_error("内存是必填项！");
        }
        if (computer_.storage_.empty()) {
            throw std::runtime_error("硬盘是必填项！");
        }
        // 转移所有权，返回构建好的 Computer
        return std::move(computer_);
    }
};


// ============================================================================
// Director 类：ComputerDirector（可选组件）
// ============================================================================

class ComputerDirector {
    /*
     * 🎯 Director（导演者）——提供常用预设配置
     *
     * Director 封装了"构建步骤的编排"。
     * 相当于快餐店的"套餐"——帮你搭配好了常见的配置组合。
     */

public:
    // 💼 办公电脑预设
    static Computer create_office_pc() {
        return ComputerBuilder()
            .set_cpu("Intel i5-13400")
            .set_ram("16GB DDR4")
            .set_storage("512GB SSD")
            .set_gpu("集成显卡")
            .set_os("Windows 11 家庭版")
            .enable_wifi()
            .enable_bluetooth()
            .set_keyboard("标准键盘")
            .set_mouse("标准鼠标")
            .build();
    }

    // 🎮 游戏电脑预设
    static Computer create_gaming_pc() {
        return ComputerBuilder()
            .set_cpu("Intel i9-14900K")
            .set_ram("64GB DDR5")
            .set_storage("2TB NVMe SSD")
            .set_gpu("NVIDIA RTX 4090")
            .set_os("Windows 11 Pro")
            .enable_wifi()
            .enable_bluetooth()
            .set_keyboard("机械键盘 (青轴)")
            .set_mouse("游戏鼠标 (6400DPI)")
            .build();
    }

    // 👨‍💻 程序员电脑预设
    static Computer create_programmer_pc() {
        return ComputerBuilder()
            .set_cpu("AMD Ryzen 9 7950X")
            .set_ram("128GB DDR5")
            .set_storage("2TB NVMe SSD")
            .set_gpu("集成显卡")
            .set_os("Ubuntu 24.04 LTS")
            .enable_wifi()
            .set_keyboard("静音键盘")
            .set_mouse("人体工学鼠标")
            .build();
    }

    // 🖥️ 最小化服务器预设
    static Computer create_minimal_server() {
        return ComputerBuilder()
            .set_cpu("Intel Xeon E-2388G")
            .set_ram("32GB ECC DDR4")
            .set_storage("1TB NVMe SSD")
            .set_gpu("集成显卡")
            .set_os("CentOS Stream 9")
            .build();
    }
};

#endif // BUILDER_H
