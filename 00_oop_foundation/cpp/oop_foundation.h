/*
================================================================================
 Lesson 0: OOP Foundation (C++ Version)
================================================================================
  ⚠ 先修课：在学设计模式之前，必须理解 OOP 的核心概念。
  设计模式的本质就是 "如何用 OOP 特性优雅地解决问题"。

  本课覆盖：
    1. 封装 (Encapsulation) — private/protected/public
    2. 继承 (Inheritance) — is-a 关系，virtual 继承
    3. 多态 (Polymorphism) — 虚函数 + 运行时多态
    4. 抽象类 (Abstract Class) — 纯虚函数
    5. 组合 (Composition) — has-a 关系，对比继承

  🔑 Python vs C++ OOP 关键差异：
     - C++ 有编译时类型检查，Python 是鸭子类型
     - C++ 需要显式 virtual 关键字实现多态
     - C++ 有 RAII 和析构函数，Python 用上下文管理器
     - C++ 内存管理要小心，Python 有 GC
================================================================================
*/

#ifndef OOP_FOUNDATION_H
#define OOP_FOUNDATION_H

#include <iostream>
#include <string>
#include <memory>
#include <vector>
#include <cmath>
#include <stdexcept>

// ============================================================================
// 1. 封装 (Encapsulation)
// ============================================================================

// ---------- 反模式：裸数据 ----------
class BadBankAccount {
    /*
     * ❌ 坏味道：所有数据直接公开，没有任何保护。
     * public 成员可以被任何人随意修改。
     */
public:
    std::string owner;
    double balance;

    BadBankAccount(const std::string& owner, double balance)
        : owner(owner), balance(balance) {}
};

// ---------- 模式：封装 ----------
class GoodBankAccount {
    /*
     * ✅ 封装：
     *   - private 隐藏数据
     *   - public 方法提供受控访问
     *   - 可以在方法中添加业务逻辑校验
     */
private:
    std::string owner_;
    double balance_;

public:
    GoodBankAccount(const std::string& owner, double initial_balance = 0)
        : owner_(owner), balance_(initial_balance) {}

    // getter：允许读取但不允许直接修改
    double getBalance() const { return balance_; }
    std::string getOwner() const { return owner_; }

    // 带校验的存款
    void deposit(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("存款金额必须为正数");
        }
        balance_ += amount;
    }

    // 带校验的取款
    void withdraw(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("取款金额必须为正数");
        }
        if (amount > balance_) {
            throw std::invalid_argument("余额不足");
        }
        balance_ -= amount;
    }

    void display() const {
        std::cout << owner_ << " 余额: ¥" << balance_ << "\n";
    }
};


// ============================================================================
// 2. 继承 (Inheritance) + 多态 (Polymorphism)
// ============================================================================

class Animal {
    /*
     * 基类。virtual 析构函数是必须的：
     * 否则通过基类指针删除派生类对象时行为未定义。
     */
protected:
    std::string name_;

public:
    Animal(const std::string& name) : name_(name) {}
    virtual ~Animal() = default;

    // virtual 表示可以被子类重写
    virtual std::string speak() const {
        return "...";
    }
};

class Dog : public Animal {
public:
    using Animal::Animal;  // 继承构造函数 (C++11)

    // override 关键字（C++11）：明确表示重写基类虚函数
    // 编译器会检查是否真的重写了，没写对会报错
    std::string speak() const override {
        return "汪汪！";
    }
};

class Cat : public Animal {
public:
    using Animal::Animal;

    std::string speak() const override {
        return "喵～";
    }
};


// ============================================================================
// 3. 抽象类 (Abstract Class) — 纯虚函数
// ============================================================================

class Shape {
    /*
     * 抽象类：包含至少一个纯虚函数 (= 0)。
     * 不能实例化，只能作为基类。
     * 
     * Python 的 abc.ABC + @abstractmethod 等价于 C++ 的纯虚函数。
     */
public:
    virtual ~Shape() = default;

    // 纯虚函数 (Pure Virtual Function)
    virtual double area() const = 0;
    virtual double perimeter() const = 0;

    // 普通虚函数：有默认实现，子类可选重写
    virtual std::string description() const {
        return "我是一个图形，面积=" + std::to_string(area());
    }
};

class Circle : public Shape {
private:
    double radius_;

public:
    explicit Circle(double radius) : radius_(radius) {}

    double area() const override {
        return M_PI * radius_ * radius_;
    }

    double perimeter() const override {
        return 2 * M_PI * radius_;
    }
};

class Rectangle : public Shape {
private:
    double width_, height_;

public:
    Rectangle(double w, double h) : width_(w), height_(h) {}

    double area() const override {
        return width_ * height_;
    }

    double perimeter() const override {
        return 2 * (width_ + height_);
    }
};


// ============================================================================
// 4. 组合优于继承 (Composition over Inheritance)
// ============================================================================

class Engine {
public:
    std::string start() const { return "发动机启动"; }
};

class Tires {
public:
    std::string inflate() const { return "轮胎充气"; }
};

/*
 * ❌ 反模式：用继承实现 "车有发动机"
 * BadCar 不是一个 Engine，不应该继承它！
 */
class BadCar : public Engine, public Tires {
public:
    std::string drive() {
        return start() + "，开车！";
    }
};

/*
 * ✅ 模式：组合
 * Car 拥有 (has-a) Engine 和 Tires
 */
class GoodCar {
private:
    Engine engine_;
    std::vector<Tires> tires_;

public:
    GoodCar() : tires_(4) {}

    std::string drive() {
        std::string result = engine_.start();
        for (auto& t : tires_) {
            result += ", " + t.inflate();
        }
        return result + "，开车！";
    }
};

#endif // OOP_FOUNDATION_H
