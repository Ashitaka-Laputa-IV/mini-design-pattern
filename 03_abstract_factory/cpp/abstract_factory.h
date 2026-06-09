/*
================================================================================
 Lesson 3: Abstract Factory — C++ 抽象工厂模式实现
================================================================================
  C++ 中抽象工厂的实现要点：
    1. 每个产品类型一个抽象基类（带虚析构函数）
    2. 每个平台一套具体产品类
    3. 抽象工厂基类定义创建所有产品的接口
    4. 每个平台一个具体工厂类
    5. 使用 std::unique_ptr 管理对象生命周期

  🔑 面试要点：
    - C++ 的抽象工厂比 Python 更"重"——每个产品都需要虚基类
    - 抽象工厂通常结合工厂方法使用
    - 新增产品种类（如 Checkbox）需要修改抽象工厂接口
    - 这是抽象工厂在 C++ 中的主要局限
================================================================================
*/

#ifndef ABSTRACT_FACTORY_H
#define ABSTRACT_FACTORY_H

#include <iostream>
#include <memory>
#include <string>

// ============================================================================
// 1. 抽象产品 (AbstractProduct)
// ============================================================================

class Button {
public:
    virtual ~Button() = default;
    virtual void render() const = 0;
    virtual void onClick() const = 0;
};

class Input {
public:
    virtual ~Input() = default;
    virtual void render() const = 0;
    virtual std::string getValue() const = 0;
};

class Menu {
public:
    virtual ~Menu() = default;
    virtual void render() const = 0;
    virtual void selectItem(int index) const = 0;
};


// ============================================================================
// 2. 具体产品 — Windows 风格
// ============================================================================

class WindowsButton : public Button {
public:
    void render() const override {
        std::cout << "渲染 [Windows 按钮] — 圆角、蓝色背景\n";
    }
    void onClick() const override {
        std::cout << "Windows 按钮被点击\n";
    }
};

class WindowsInput : public Input {
public:
    void render() const override {
        std::cout << "渲染 [Windows 输入框] — 带边框、白色背景\n";
    }
    std::string getValue() const override {
        return "Windows 输入框的内容";
    }
};

class WindowsMenu : public Menu {
public:
    void render() const override {
        std::cout << "渲染 [Windows 菜单] — 下拉式、带图标\n";
    }
    void selectItem(int index) const override {
        std::cout << "Windows 菜单选中第 " << index << " 项\n";
    }
};


// ============================================================================
// 3. 具体产品 — Mac 风格
// ============================================================================

class MacButton : public Button {
public:
    void render() const override {
        std::cout << "渲染 [Mac 按钮] — 毛玻璃效果、圆润\n";
    }
    void onClick() const override {
        std::cout << "Mac 按钮被点击\n";
    }
};

class MacInput : public Input {
public:
    void render() const override {
        std::cout << "渲染 [Mac 输入框] — 搜索框风格、无边框\n";
    }
    std::string getValue() const override {
        return "Mac 输入框的内容";
    }
};

class MacMenu : public Menu {
public:
    void render() const override {
        std::cout << "渲染 [Mac 菜单] — 顶部菜单栏、全局\n";
    }
    void selectItem(int index) const override {
        std::cout << "Mac 菜单选中第 " << index << " 项\n";
    }
};


// ============================================================================
// 4. 具体产品 — Linux 风格
// ============================================================================

class LinuxButton : public Button {
public:
    void render() const override {
        std::cout << "渲染 [Linux 按钮] — 扁平、极简风格\n";
    }
    void onClick() const override {
        std::cout << "Linux 按钮被点击\n";
    }
};

class LinuxInput : public Input {
public:
    void render() const override {
        std::cout << "渲染 [Linux 输入框] — 简洁、灰色边框\n";
    }
    std::string getValue() const override {
        return "Linux 输入框的内容";
    }
};

class LinuxMenu : public Menu {
public:
    void render() const override {
        std::cout << "渲染 [Linux 菜单] — 传统下拉、右键菜单\n";
    }
    void selectItem(int index) const override {
        std::cout << "Linux 菜单选中第 " << index << " 项\n";
    }
};


// ============================================================================
// 5. 抽象工厂 (AbstractFactory)
// ============================================================================

/*
 * GUIFactory 是抽象工厂的核心接口。
 *
 * 🧠 注意：每个 createXXX 方法都返回 unique_ptr<XXX>，
 * 这其实就是一个"工厂方法"。
 * 所以抽象工厂 = 多个工厂方法的组合。
 *
 * 📌 限制：如果要新增一种产品（如 Checkbox），
 * 必须在这里添加 createCheckbox() 方法，
 * 然后所有具体工厂都要实现它。
 * 这就是抽象工厂"扩展产品种类困难"的体现。
 */
class GUIFactory {
public:
    virtual ~GUIFactory() = default;

    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<Input> createInput() = 0;
    virtual std::unique_ptr<Menu> createMenu() = 0;
};


// ============================================================================
// 6. 具体工厂 (ConcreteFactory)
// ============================================================================

class WindowsFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<Input> createInput() override {
        return std::make_unique<WindowsInput>();
    }
    std::unique_ptr<Menu> createMenu() override {
        return std::make_unique<WindowsMenu>();
    }
};

class MacFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<MacButton>();
    }
    std::unique_ptr<Input> createInput() override {
        return std::make_unique<MacInput>();
    }
    std::unique_ptr<Menu> createMenu() override {
        return std::make_unique<MacMenu>();
    }
};

class LinuxFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<LinuxButton>();
    }
    std::unique_ptr<Input> createInput() override {
        return std::make_unique<LinuxInput>();
    }
    std::unique_ptr<Menu> createMenu() override {
        return std::make_unique<LinuxMenu>();
    }
};

#endif // ABSTRACT_FACTORY_H
