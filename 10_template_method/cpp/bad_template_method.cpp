/*
================================================================================
Lesson 10: Template Method — C++ 反模式：代码重复
================================================================================
  和 Python 版一样，展示 Tea 和 Coffee 类中的大量重复代码。

  😱 问题：boilWater() 和 pourInCup() 在两个类中完全一样！
================================================================================
*/

#include <iostream>

// ============================================================================
// 反模式：CTRL+C/V 式重复
// ============================================================================

class Tea {
    /*
     * 茶类——冲泡茶叶
     * 问题：和 Coffee 大量重复代码
     */
public:
    void prepareRecipe() {
        boilWater();
        steepTeaBag();
        pourInCup();
        addLemon();
    }

    void boilWater() {
        std::cout << "  1. 把水烧开\n";
    }

    void steepTeaBag() {
        std::cout << "  2. 把茶叶放入水中浸泡 3 分钟\n";
    }

    void pourInCup() {
        std::cout << "  3. 把饮料倒入杯子\n";
    }

    void addLemon() {
        std::cout << "  4. 加柠檬片\n";
    }
};

class Coffee {
    /*
     * 咖啡类——冲泡咖啡
     * 😱 boilWater() 和 pourInCup() 和 Tea 完全一样！
     */
public:
    void prepareRecipe() {
        boilWater();
        brewCoffeeGrounds();
        pourInCup();
        addSugarAndMilk();
    }

    void boilWater() {
        std::cout << "  1. 把水烧开\n";   // 重复！
    }

    void brewCoffeeGrounds() {
        std::cout << "  2. 用热水冲泡咖啡粉\n";
    }

    void pourInCup() {
        std::cout << "  3. 把饮料倒入杯子\n";  // 重复！
    }

    void addSugarAndMilk() {
        std::cout << "  4. 加糖和牛奶\n";
    }
};

int main() {
    std::cout << "========================================\n";
    std::cout << "☕ 冲泡茶\n";
    std::cout << "========================================\n";
    Tea tea;
    tea.prepareRecipe();

    std::cout << "\n========================================\n";
    std::cout << "☕ 冲泡咖啡\n";
    std::cout << "========================================\n";
    Coffee coffee;
    coffee.prepareRecipe();

    return 0;
}
