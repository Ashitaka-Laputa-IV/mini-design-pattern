/*
================================================================================
 Lesson 0: OOP Foundation (C++ — 演示代码入口)
================================================================================
  compile & run:
    g++ -std=c++11 oop_foundation.cpp -o oop_foundation
    ./oop_foundation
================================================================================
*/

#include "oop_foundation.h"

int main() {
    std::cout << "====== OOP 基础演示 (C++) ======\n\n";

    // ---- 1. 封装 ----
    std::cout << "--- 1. 封装 ---\n";
    GoodBankAccount account("Alice", 1000);
    account.deposit(500);
    account.withdraw(200);
    account.display();

    // ❌ 以下代码编译报错，因为 balance_ 是 private
    // account.balance_ = 9999;

    // ---- 2. 多态 ----
    std::cout << "\n--- 2. 多态 ---\n";
    /*
     * 🎯 关键知识点：C++ 运行时多态通过 基类指针/引用 + 虚函数 实现。
     *    如果用值而不是指针/引用，会发生"对象切片"(Object Slicing)。
     *    e.g. std::vector<Animal> 会丢失派生类信息！
     */
    std::vector<std::unique_ptr<Animal>> animals;
    animals.push_back(std::make_unique<Dog>("旺财"));
    animals.push_back(std::make_unique<Cat>("咪咪"));

    for (const auto& a : animals) {
        std::cout << a->name_ << "说: " << a->speak() << "\n";
    }

    // ---- 3. 抽象类 ----
    std::cout << "\n--- 3. 抽象类 ---\n";
    std::unique_ptr<Shape> c = std::make_unique<Circle>(5);
    std::unique_ptr<Shape> r = std::make_unique<Rectangle>(3, 4);
    // Shape s;  // ❌ 编译错误！不能实例化抽象类

    std::cout << c->description() << "\n";
    std::cout << r->description() << "\n";

    // ---- 4. 组合 ----
    std::cout << "\n--- 4. 组合优于继承 ---\n";
    GoodCar car;
    std::cout << car.drive() << "\n";

    return 0;
}
