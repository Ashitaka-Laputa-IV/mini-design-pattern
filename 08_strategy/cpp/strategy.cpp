/*
================================================================================
 Lesson 8: Strategy — 策略模式 · C++ 演示代码
================================================================================
  compile & run:
    g++ -std=c++11 strategy.cpp -o strategy
    ./strategy
================================================================================
*/

#include "strategy.h"

int main() {
    std::cout << "====== C++ 策略模式演示 ======\n\n";

    // 创建订单
    Order order1("domestic", "normal", 5.0);
    Order order2("domestic", "vip", 5.0);
    Order order3("overseas", "normal", 2.0);
    Order order4("overseas", "vip", 3.0);

    // ---- 1. 经典策略模式 ----
    std::cout << "--- 1. 经典策略模式 ---\n";

    ShippingCalculator calc;

    calc.setStrategy(std::make_unique<DomesticStandard>());
    calc.calculate(order1);

    calc.setStrategy(std::make_unique<DomesticVIP>());
    calc.calculate(order2);

    calc.setStrategy(std::make_unique<OverseasStandard>());
    calc.calculate(order3);

    calc.setStrategy(std::make_unique<OverseasVIP>());
    calc.calculate(order4);

    // ---- 2. std::function 函数策略 ----
    std::cout << "\n--- 2. std::function 函数策略 ---\n";

    // 用 lambda 表达式作为策略（类似 Python 的 lambda）
    auto domesticNormalFunc = [](const Order&) -> double {
        return 10.0;
    };

    auto overseasVIPFunc = [](const Order& o) -> double {
        return o.total_weight * 10.0;
    };

    ShippingCalculatorWithFunc funcCalc(domesticNormalFunc);
    funcCalc.calculate(order1);

    funcCalc.setStrategy(overseasVIPFunc);
    funcCalc.calculate(order4);

    // 更灵活的 lambda：即兴策略
    funcCalc.setStrategy([](const Order& o) -> double {
        return (o.member_level == "vip") ? 0.0 : 20.0;
    });
    funcCalc.calculate(order2);  // VIP -> 0
    funcCalc.calculate(order1);  // normal -> 20

    /*
     * 💡 C++ vs Python 策略模式对比：
     *
     *   Python:
     *     - 函数是一等公民，直接传函数/lambda
     *     - 鸭子类型，不需要显式接口
     *     - 更简洁，但运行时才能发现类型错误
     *
     *   C++:
     *     - 传统方式用虚函数 + 继承（编译期类型安全）
     *     - C++11 后也可以用 std::function + lambda
     *     - 性能更好（虚函数表 vs 函数指针）
     *     - 需要手动管理生命周期（unique_ptr / shared_ptr）
     */

    return 0;
}
