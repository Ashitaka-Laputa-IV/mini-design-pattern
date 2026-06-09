/*
================================================================================
 Lesson 3: Abstract Factory — C++ 反模式示例
================================================================================
  🎬 场景：和 Python 版本一样——跨平台 GUI 库。

  C++ 中的"坏味道"：
    - 用 if-else 或 switch-case 创建不同平台的产品
    - 所有平台的创建逻辑耦合在一个类中
    - 新增平台需要修改多处代码
    - 返回裸指针，内存管理混乱

  🧠 思考：这段代码有哪些问题？
================================================================================
*/

#include <iostream>
#include <string>

// ============================================================================
// 各种平台的组件
// ============================================================================

// ---- Windows ----
class WindowsButton {
public:
    void render() { std::cout << "渲染 [Windows 按钮] — 圆角、蓝色背景\n"; }
};

class WindowsInput {
public:
    void render() { std::cout << "渲染 [Windows 输入框] — 带边框、白色背景\n"; }
};

// ---- Mac ----
class MacButton {
public:
    void render() { std::cout << "渲染 [Mac 按钮] — 毛玻璃效果、圆润\n"; }
};

class MacInput {
public:
    void render() { std::cout << "渲染 [Mac 输入框] — 搜索框风格、无边框\n"; }
};

// ---- Linux ----
class LinuxButton {
public:
    void render() { std::cout << "渲染 [Linux 按钮] — 扁平、极简风格\n"; }
};

class LinuxInput {
public:
    void render() { std::cout << "渲染 [Linux 输入框] — 简洁、灰色边框\n"; }
};

// ============================================================================
// ❌ 反模式：用 if-else 创建所有平台的所有组件
// ============================================================================

/*
 * ❌ 问题分析：
 *   1. 所有平台的创建逻辑都耦合在 GUIFactory 中
 *   2. 每次新增平台，每个方法都要加一个 else if
 *   3. 方法返回 void*，不是类型安全的
 *   4. 调用者需要手动 delete，容易内存泄漏
 *   5. 如果混用了不同平台的组件，编译不会报错
 */
class GUIFactory {
public:
    static void* createButton(const std::string& platform) {
        if (platform == "windows") {
            return new WindowsButton();
        } else if (platform == "mac") {
            return new MacButton();
        } else if (platform == "linux") {
            return new LinuxButton();
        }
        return nullptr;
    }

    static void* createInput(const std::string& platform) {
        if (platform == "windows") {
            return new WindowsInput();
        } else if (platform == "mac") {
            return new MacInput();
        } else if (platform == "linux") {
            return new LinuxInput();
        }
        return nullptr;
    }
};

int main() {
    std::cout << "====== C++ 反模式：if-else 创建产品族 ======\n\n";

    std::string platforms[] = {"windows", "mac", "linux"};

    for (const auto& platform : platforms) {
        std::cout << "--- " << platform << " ---\n";

        void* btn = GUIFactory::createButton(platform);
        void* inp = GUIFactory::createInput(platform);

        // ⚠ 类型转换：如果写错了类型，编译不报错，运行时报错！
        static_cast<WindowsButton*>(btn)->render();
        static_cast<WindowsInput*>(inp)->render();

        // ⚠ 手动 delete：容易忘记或重复删除
        delete static_cast<WindowsButton*>(btn);
        delete static_cast<WindowsInput*>(inp);

        std::cout << "\n";
    }

    std::cout << "⚠  如果加 Android 平台，必须修改 GUIFactory 的两个方法！\n";

    return 0;
}
