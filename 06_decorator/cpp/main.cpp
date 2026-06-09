/*
================================================================================
Lesson 6: Decorator (装饰器模式) — C++ 实现
================================================================================
  展示 C++ 中如何使用基类指针实现装饰链。

  要点：
  - 虚函数 + 纯虚函数实现多态接口
  - 基类指针实现运行时多态
  - unique_ptr 管理内存（C++11 智能指针）

  compile & run:
    g++ -std=c++11 main.cpp -o decorator
    ./decorator
================================================================================
*/

#include <iostream>
#include <memory>
#include <string>

class Beverage {
public:
    Beverage() : _description("未知饮料") {}
    virtual ~Beverage() = default;

    virtual std::string getDescription() const {
        return _description;
    }

    // 纯虚函数：计算价格
    virtual double cost() const = 0;

protected:
    std::string _description;
};


// =============================================================================
// 2. ConcreteComponent (具体组件)
// =============================================================================

class Espresso : public Beverage {
public:
    Espresso() {
        _description = "浓缩咖啡";
    }

    double cost() const override {
        return 10.0;
    }
};


class Americano : public Beverage {
public:
    Americano() {
        _description = "美式咖啡";
    }

    double cost() const override {
        return 8.0;
    }
};


// =============================================================================
// 3. Decorator (抽象装饰器)
// =============================================================================
/*
  ⭐ 关键点：
    - CondimentDecorator 继承 Beverage（接口一致）
    - CondimentDecorator 持有 Beverage*（组合）
  这样装饰器可以包装任何 Beverage 子类。
*/

class CondimentDecorator : public Beverage {
public:
    explicit CondimentDecorator(std::unique_ptr<Beverage> beverage)
        : _beverage(std::move(beverage)) {}

    std::string getDescription() const override = 0;

protected:
    std::unique_ptr<Beverage> _beverage;  // ⭐ 持有被装饰者的引用
};


// =============================================================================
// 4. ConcreteDecorator (具体装饰器)
// =============================================================================

class Milk : public CondimentDecorator {
public:
    explicit Milk(std::unique_ptr<Beverage> beverage)
        : CondimentDecorator(std::move(beverage)) {}

    std::string getDescription() const override {
        return _beverage->getDescription() + " + 牛奶";
    }

    double cost() const override {
        return _beverage->cost() + 2.0;
    }
};


class Sugar : public CondimentDecorator {
public:
    explicit Sugar(std::unique_ptr<Beverage> beverage)
        : CondimentDecorator(std::move(beverage)) {}

    std::string getDescription() const override {
        return _beverage->getDescription() + " + 糖";
    }

    double cost() const override {
        return _beverage->cost() + 1.0;
    }
};


class Whip : public CondimentDecorator {
public:
    explicit Whip(std::unique_ptr<Beverage> beverage)
        : CondimentDecorator(std::move(beverage)) {}

    std::string getDescription() const override {
        return _beverage->getDescription() + " + 奶油";
    }

    double cost() const override {
        return _beverage->cost() + 3.0;
    }
};


// =============================================================================
// 5. 测试
// =============================================================================

int main() {
    std::cout << "==========================================" << std::endl;
    std::cout << "C++ Decorator 模式" << std::endl;
    std::cout << "==========================================" << std::endl;

    // 基础饮料
    auto espresso = std::make_unique<Espresso>();
    std::cout << "基础: " << espresso->getDescription()
              << " -> $" << espresso->cost() << std::endl;

    // 装饰链：浓缩咖啡 + 牛奶
    auto e_milk = std::make_unique<Milk>(std::make_unique<Espresso>());
    std::cout << "装饰: " << e_milk->getDescription()
              << " -> $" << e_milk->cost() << std::endl;

    // 装饰链：浓缩咖啡 + 牛奶 + 糖
    auto e_milk_sugar = std::make_unique<Sugar>(
        std::make_unique<Milk>(std::make_unique<Espresso>())
    );
    std::cout << "装饰: " << e_milk_sugar->getDescription()
              << " -> $" << e_milk_sugar->cost() << std::endl;

    // 装饰链：浓缩咖啡 + 牛奶 + 糖 + 奶油
    auto e_all = std::make_unique<Whip>(
        std::make_unique<Sugar>(
            std::make_unique<Milk>(std::make_unique<Espresso>())
        )
    );
    std::cout << "装饰: " << e_all->getDescription()
              << " -> $" << e_all->cost() << std::endl;

    // 美式咖啡 + 奶油
    auto a_whip = std::make_unique<Whip>(std::make_unique<Americano>());
    std::cout << "装饰: " << a_whip->getDescription()
              << " -> $" << a_whip->cost() << std::endl;

    return 0;
}
