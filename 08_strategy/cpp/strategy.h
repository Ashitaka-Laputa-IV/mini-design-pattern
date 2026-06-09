/*
================================================================================
 Lesson 8: Strategy — 策略模式 [行为型] · C++ 实现
================================================================================
  C++ 策略模式实现要点：
    1. 抽象基类（接口）定义策略协议
    2. 具体策略类继承基类实现算法
    3. Context 类通过指针/引用持有策略对象
    4. 运行时通过多态切换策略

  🔑 面试要点：
    - C++ 策略模式的关键是"虚函数 + 指针/引用"实现多态
    - 可以用 std::function 替代虚函数（类似 Python 的函数策略）
    - 注意策略对象的生命周期管理（裸指针 vs unique_ptr vs shared_ptr）
================================================================================
*/

#ifndef STRATEGY_H
#define STRATEGY_H

#include <iostream>
#include <string>
#include <memory>
#include <functional>

// ============================================================================
// 数据类：订单
// ============================================================================

struct Order {
    /*
     * 订单数据——只负责数据，不关心运费怎么算。
     * 使用 struct 简化，成员直接公开。
     */
    std::string region;
    std::string member_level;
    double total_weight;

    Order(const std::string& r, const std::string& m, double w)
        : region(r), member_level(m), total_weight(w) {}
};

// ============================================================================
// 策略接口（抽象基类）
// ============================================================================

class ShippingStrategy {
    /*
     * 🧩 策略接口
     *
     * C++ 中通过抽象基类定义接口：
     *   - virtual ~ShippingStrategy()：虚析构函数（重要！）
     *   - virtual double calculate(...) = 0：纯虚函数
     *
     * 面试题：为什么策略基类需要虚析构函数？
     *   → 如果通过基类指针删除派生类对象，没有虚析构会导致未定义行为。
     */
public:
    virtual ~ShippingStrategy() = default;

    // 纯虚函数：所有子类必须实现
    virtual double calculate(const Order& order) const = 0;

    // 非虚函数：获取策略名称（所有子类共享此实现）
    virtual std::string name() const {
        return "ShippingStrategy";
    }
};

// ============================================================================
// 具体策略类
// ============================================================================

class DomesticStandard : public ShippingStrategy {
    /*
     * 国内普通：固定 10 元
     */
public:
    double calculate(const Order& order) const override {
        return 10.0;
    }

    std::string name() const override {
        return "DomesticStandard";
    }
};

class DomesticVIP : public ShippingStrategy {
    /*
     * 国内 VIP：免运费
     */
public:
    double calculate(const Order& order) const override {
        return 0.0;
    }

    std::string name() const override {
        return "DomesticVIP";
    }
};

class OverseasStandard : public ShippingStrategy {
    /*
     * 海外普通：重量 × 15 元/kg
     */
public:
    double calculate(const Order& order) const override {
        return order.total_weight * 15.0;
    }

    std::string name() const override {
        return "OverseasStandard";
    }
};

class OverseasVIP : public ShippingStrategy {
    /*
     * 海外 VIP：重量 × 10 元/kg
     */
public:
    double calculate(const Order& order) const override {
        return order.total_weight * 10.0;
    }

    std::string name() const override {
        return "OverseasVIP";
    }
};

// ============================================================================
// Context：策略持有者
// ============================================================================

class ShippingCalculator {
    /*
     * 🎯 Context
     *
     * 持有策略的指针，运行时可以切换策略。
     *
     * 生命周期管理选择：
     *   - 这里使用 std::unique_ptr（独占所有权）
     *   - 也可以使用裸指针（不拥有，由外部管理）
     *   - 面试官可能会问"用 shared_ptr 可不可以？"
     *     → 可以，但需要共享所有权时再用，否则 unique_ptr 更轻量
     */
private:
    std::unique_ptr<ShippingStrategy> strategy_;

public:
    // 构造函数：传入初始策略
    explicit ShippingCalculator(std::unique_ptr<ShippingStrategy> strategy = nullptr)
        : strategy_(std::move(strategy)) {}

    // 禁止拷贝（unique_ptr 不可拷贝）
    ShippingCalculator(const ShippingCalculator&) = delete;
    ShippingCalculator& operator=(const ShippingCalculator&) = delete;

    // 允许移动
    ShippingCalculator(ShippingCalculator&&) = default;
    ShippingCalculator& operator=(ShippingCalculator&&) = default;

    // 运行时切换策略
    void setStrategy(std::unique_ptr<ShippingStrategy> new_strategy) {
        if (strategy_) {
            std::cout << "  [切换策略] " << strategy_->name()
                      << " → " << new_strategy->name() << "\n";
        } else {
            std::cout << "  [设置策略] " << new_strategy->name() << "\n";
        }
        strategy_ = std::move(new_strategy);
    }

    double calculate(const Order& order) const {
        if (!strategy_) {
            throw std::runtime_error("请先设置运费策略！");
        }
        double cost = strategy_->calculate(order);
        std::cout << "  [策略] " << strategy_->name() << " → 运费: " << cost << " 元\n";
        return cost;
    }
};

// ============================================================================
// C++11 进阶：使用 std::function 替代虚函数
// ============================================================================

/*
 * C++ 中也可以用 std::function 实现"函数即策略"。
 * 效果类似于 Python 的函数策略模式。
 *
 * 适用场景：
 *   - 策略逻辑简单
 *   - 不需要策略类层次结构
 *   - 希望减少类数量
 */

using ShippingFunc = std::function<double(const Order&)>;

class ShippingCalculatorWithFunc {
    /*
     * 函数策略版本的 Context。
     * 直接持有 std::function，不需要策略类层次。
     */
private:
    ShippingFunc strategy_;

public:
    explicit ShippingCalculatorWithFunc(ShippingFunc strategy = nullptr)
        : strategy_(std::move(strategy)) {}

    void setStrategy(ShippingFunc strategy) {
        strategy_ = std::move(strategy);
    }

    double calculate(const Order& order) const {
        if (!strategy_) {
            throw std::runtime_error("请先设置运费策略！");
        }
        double cost = strategy_(order);
        std::cout << "  [函数策略] → 运费: " << cost << " 元\n";
        return cost;
    }
};

#endif // STRATEGY_H
