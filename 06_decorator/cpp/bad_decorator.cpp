/*
================================================================================
Lesson 6: Decorator — C++ 反模式示例
================================================================================
  🎬 场景和 Python 版一样：咖啡订单系统。

  反模式：用继承实现"饮料+配料"组合 → 子类爆炸！

  举例：
    Espresso, EspressoWithMilk, EspressoWithSugar,
    EspressoWithMilkAndSugar, EspressoWithMilkAndSugarAndWhip,
    Americano, AmericanoWithMilk, AmericanoWithSugar...
    如果有 N 种饮料和 M 种配料，需要 N * 2^M 个子类！
================================================================================
*/

#include <iostream>
#include <string>

// ============================================================================
// ❌ 反模式：子类爆炸
// ============================================================================

class Beverage {
protected:
    std::string description_ = "未知饮料";
public:
    virtual std::string getDescription() const { return description_; }
    virtual double cost() const = 0;
    virtual ~Beverage() = default;
};

// 基础饮料
class Espresso : public Beverage {
public:
    Espresso() { description_ = "浓缩咖啡"; }
    double cost() const override { return 10.0; }
};

// 每种配料组合都需要一个单独的类！！
class EspressoWithMilk : public Beverage {
    // 重复了 Espresso 的价格逻辑
    double cost() const override { return 10.0 + 2.0; }
public:
    EspressoWithMilk() { description_ = "浓缩咖啡 + 牛奶"; }
};

class EspressoWithSugar : public Beverage {
    double cost() const override { return 10.0 + 1.0; }
public:
    EspressoWithSugar() { description_ = "浓缩咖啡 + 糖"; }
};

class EspressoWithMilkAndSugar : public Beverage {
    double cost() const override { return 10.0 + 2.0 + 1.0; }
public:
    EspressoWithMilkAndSugar() { description_ = "浓缩咖啡 + 牛奶 + 糖"; }
};

class Americano : public Beverage {
public:
    Americano() { description_ = "美式咖啡"; }
    double cost() const override { return 8.0; }
};

class AmericanoWithMilk : public Beverage {
    double cost() const override { return 8.0 + 2.0; }
public:
    AmericanoWithMilk() { description_ = "美式咖啡 + 牛奶"; }
};

// ... 以下省略另外 N * 2^M 个类 ...

int main() {
    std::cout << "====== C++ 反模式：子类爆炸 ======\n\n";

    Espresso e;
    EspressoWithMilk em;
    EspressoWithSugar es;
    EspressoWithMilkAndSugar ems;
    Americano a;
    AmericanoWithMilk am;

    std::cout << e.getDescription() << ": ¥" << e.cost() << "\n";
    std::cout << em.getDescription() << ": ¥" << em.cost() << "\n";
    std::cout << es.getDescription() << ": ¥" << es.cost() << "\n";
    std::cout << ems.getDescription() << ": ¥" << ems.cost() << "\n";
    std::cout << a.getDescription() << ": ¥" << a.cost() << "\n";
    std::cout << am.getDescription() << ": ¥" << am.cost() << "\n";

    std::cout << "\n❌ 问题：\n";
    std::cout << "  - 新增配料(如奶油)需要创建 N 个新类\n";
    std::cout << "  - 修改基础饮料价格需要更新所有组合类\n";
    std::cout << "  - 类数量 = N * 2^M，指数爆炸！\n";
    std::cout << "  - 如果再加大小杯选项就彻底失控了\n";

    // 看看用装饰器模式解决后的 main.cpp 吧！
    return 0;
}
