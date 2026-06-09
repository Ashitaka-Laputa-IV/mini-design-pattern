/*
================================================================================
 Lesson 3: Abstract Factory — C++ 演示代码
================================================================================
  compile & run:
    g++ -std=c++14 abstract_factory.cpp -o abstract_factory
    ./abstract_factory

  展示如何使用抽象工厂模式切换整个平台 UI 风格。
================================================================================
*/

#include "abstract_factory.h"
#include <memory>
#include <vector>

/*
 * 客户端 Application 类。
 *
 * 🔑 和 Python 版本一样，Application 只依赖抽象接口：
 *   - GUIFactory（抽象工厂）
 *   - Button, Input, Menu（抽象产品）
 *
 * Application 不知道具体是 Windows 还是 Mac 还是 Linux。
 * 切换平台 = 传入不同的 Factory 对象。
 */
class Application {
private:
    GUIFactory& factory_;
    std::unique_ptr<Button> button_;
    std::unique_ptr<Input> input_;
    std::unique_ptr<Menu> menu_;

public:
    /*
     * 通过依赖注入接收工厂。
     * 注意：这里传入的是引用，因为工厂对象由外部管理生命周期。
     */
    Application(GUIFactory& factory) : factory_(factory) {}

    void createUI() {
        std::cout << "\n  创建 UI...\n";
        button_ = factory_.createButton();
        input_ = factory_.createInput();
        menu_ = factory_.createMenu();
    }

    void renderUI() const {
        button_->render();
        input_->render();
        menu_->render();
    }

    void simulateInteraction() const {
        button_->onClick();
        std::cout << "  输入框值: " << input_->getValue() << "\n";
        menu_->selectItem(1);
    }
};

int main() {
    std::cout << "====== C++ 抽象工厂模式演示 ======\n\n";

    // 创建具体工厂
    WindowsFactory winFactory;
    MacFactory macFactory;
    LinuxFactory linuxFactory;

    // 用同一个 Application 类，传入不同的工厂
    // 一行代码切换整个 UI 风格！
    std::cout << "--- Windows 平台 ---";
    Application winApp(winFactory);
    winApp.createUI();
    winApp.renderUI();
    winApp.simulateInteraction();

    std::cout << "\n--- Mac 平台 ---";
    Application macApp(macFactory);
    macApp.createUI();
    macApp.renderUI();
    macApp.simulateInteraction();

    std::cout << "\n--- Linux 平台 ---";
    Application linuxApp(linuxFactory);
    linuxApp.createUI();
    linuxApp.renderUI();
    linuxApp.simulateInteraction();

    std::cout << "\n========================================\n";
    std::cout << "✅ 添加 Android 平台只需：\n";
    std::cout << "   1. 新建 AndroidButton, AndroidInput, AndroidMenu 类\n";
    std::cout << "   2. 新建 AndroidFactory 类继承 GUIFactory\n";
    std::cout << "   3. 客户端创建 Application(androidFactory)\n";
    std::cout << "   ✅ 不需要修改任何已有代码！\n";

    return 0;
}
