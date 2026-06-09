/*
================================================================================
Lesson 10: Template Method — C++ 模板方法模式
================================================================================
  本文件演示 NVI（Non-Virtual Interface）惯用法。

  🎯 NVI 的核心思想：
    公有接口是非虚函数（Non-Virtual），
    虚函数设为 private 或 protected，
    用户通过公有接口调用，接口内部调用虚函数。

  这样做的好处：
    1. 基类可以在接口中加入"前置/后置"处理（如日志、锁）
    2. 精确控制子类可以重写哪些方法
    3. 分离"接口约定"和"实现细节"

  🔑 面试考点：NVI 是 C++ 特有的模板方法实现方式，
    面试官可能会问"为什么不用 virtual public 方法？"
================================================================================
*/

#ifndef TEMPLATE_METHOD_H
#define TEMPLATE_METHOD_H

#include <iostream>

// ============================================================================
// 抽象基类：CaffeineBeverage
// 使用 NVI 惯用法实现模板方法模式
// ============================================================================

class CaffeineBeverage {
    /*
     * 含咖啡因饮料——抽象基类
     *
     * NVI 惯用法的结构：
     *   public:    非虚接口（调用私有虚函数）
     *   protected: 可选实现（子类可重写）
     *   private:   纯虚函数（子类必须实现）
     */
public:
    // ========================================================================
    // 🎯 模板方法（Non-Virtual Interface）
    // ========================================================================
    /*
     * prepareRecipe() 是"模板方法"。
     * 它是非虚的（Non-Virtual），子类不能重写。
     * 它定义了算法的固定骨架：
     *   烧水 → 冲泡 → 倒杯 → 加料
     *
     * 💡 为什么设为非虚？
     *   因为骨架是固定的，不允许子类改变流程顺序。
     *   如果设为 virtual，子类可能不小心重写掉，破坏算法结构。
     */
    void prepareRecipe() {
        boilWater();
        brew();                    // 调用私有虚方法
        pourInCup();
        if (customerWantsCondiments()) {  // 钩子方法
            addCondiments();       // 调用私有虚方法
        }
    }

    // ========================================================================
    // 钩子方法（Hook）——虚函数，子类可选择重写
    // ========================================================================
    /*
     * customerWantsCondiments() 是一个"钩子"。
     * 基类提供默认实现（返回 true），
     * 子类可以覆盖它来控制流程分支。
     *
     * 这里设为 protected virtual，子类可见但外部用户不可见。
     */
protected:
    virtual bool customerWantsCondiments() const {
        return true;  // 默认加调料
    }

    // ========================================================================
    // 公共步骤：在基类实现，所有子类共享
    // ========================================================================
    /*
     * boilWater() 和 pourInCup() 是所有饮料共有的步骤，
     * 在基类中直接实现，子类不需要也不应该重写。
     * 它们是非虚的（Non-Virtual）。
     */
    void boilWater() const {
        std::cout << "  1. 把水烧开\n";
    }

    void pourInCup() const {
        std::cout << "  3. 把饮料倒入杯子\n";
    }

    // ========================================================================
    // 纯虚函数（Pure Virtual）——子类必须实现
    // ========================================================================
    /*
     * brew() 和 addCondiments() 是"可变步骤"，
     * 不同饮料的实现不同。
     *
     * 设为 private：
     *   - 子类必须实现它们（纯虚）
     *   - 外部用户不能直接调用它们
     *   - 只有模板方法 prepareRecipe() 可以调用它们
     *
     * ❗注意：C++ 允许派生类实现基类的 private 纯虚函数。
     *   这是 C++ 的特殊规则——访问权限和覆盖权限是分开的。
     */
private:
    virtual void brew() = 0;           // 冲泡方式（子类实现）
    virtual void addCondiments() = 0;  // 加调料方式（子类实现）

public:
    virtual ~CaffeineBeverage() = default;
};


// ============================================================================
// 具体子类：Tea
// ============================================================================

class Tea : public CaffeineBeverage {
    /*
     * 茶——实现 brew() 和 addCondiments()
     *
     * 注意：虽然基类把 brew() 设为 private，
     * 但 C++ 允许派生类覆盖它（只需在派生类中声明）。
     * 外部仍然不能通过 Tea 对象直接调用 brew()。
     */
private:
    void brew() override {
        std::cout << "  2. 把茶叶放入水中浸泡 3 分钟\n";
    }

    void addCondiments() override {
        std::cout << "  4. 加柠檬片\n";
    }
};


// ============================================================================
// 具体子类：Coffee
// ============================================================================

class Coffee : public CaffeineBeverage {
private:
    void brew() override {
        std::cout << "  2. 用热水冲泡咖啡粉\n";
    }

    void addCondiments() override {
        std::cout << "  4. 加糖和牛奶\n";
    }
};


// ============================================================================
// 具体子类：BlackTea（展示钩子方法）
// ============================================================================

class BlackTea : public CaffeineBeverage {
    /*
     * 清茶——顾客不想加调料
     * 重写钩子方法 customerWantsCondiments() 返回 false
     */
private:
    void brew() override {
        std::cout << "  2. 把茶叶放入水中浸泡 2 分钟\n";
    }

    void addCondiments() override {
        // 清茶不加任何调料，理论上不会执行到这里
        std::cout << "  4. （不加任何调料）\n";
    }

protected:
    /*
     * 重写钩子方法：跳过加调料步骤
     *
     * 注意：钩子方法是 protected，所以重写时也设为 protected。
     */
    bool customerWantsCondiments() const override {
        std::cout << "  4. （顾客选择了不加调料，跳过此步骤）\n";
        return false;
    }
};


// ============================================================================
// 扩展示例：HotChocolate
// ============================================================================

class HotChocolate : public CaffeineBeverage {
private:
    void brew() override {
        std::cout << "  2. 把巧克力粉加入热水中搅拌\n";
    }

    void addCondiments() override {
        std::cout << "  4. 加棉花糖和奶油\n";
    }
};

#endif // TEMPLATE_METHOD_H
