/*
================================================================================
Lesson 11: Command — C++ 反模式：硬编码遥控器
================================================================================
  和 Python 版一样，展示 RemoteControl 中硬编码的控制逻辑。

  😱 问题：新增家电就要改 RemoteControl 的 if-else 判断！
================================================================================
*/

#include <iostream>
#include <string>

// ============================================================================
// 家电类
// ============================================================================

class Light {
public:
    void on() { std::cout << "  💡 灯打开了\n"; }
    void off() { std::cout << "  💡 灯关闭了\n"; }
};

class Fan {
public:
    void on() { std::cout << "  🌀 风扇打开了\n"; }
    void off() { std::cout << "  🌀 风扇关闭了\n"; }
};

class Stereo {
public:
    void on() { std::cout << "  🔊 音响打开了\n"; }
    void off() { std::cout << "  🔊 音响关闭了\n"; }
    void setVolume(int vol) { std::cout << "  🔊 音量设置为 " << vol << "\n"; }
};

// ============================================================================
// 反模式：硬编码遥控器
// ============================================================================

class RemoteControl {
    /*
     * 😱 每个按钮对应一个 if-else 分支
     * 新增家电就要修改这个类的代码！
     * 无法撤销！无法组合！
     */
private:
    Light light_;
    Fan fan_;
    Stereo stereo_;

public:
    void onButtonPressed(const std::string& btn) {
        if (btn == "light_on") {
            light_.on();
        } else if (btn == "light_off") {
            light_.off();
        } else if (btn == "fan_on") {
            fan_.on();
        } else if (btn == "fan_off") {
            fan_.off();
        } else if (btn == "stereo_on") {
            stereo_.on();
        } else if (btn == "stereo_off") {
            stereo_.off();
        } else {
            std::cout << "  ❌ 未知按钮: " << btn << "\n";
        }
    }
};

int main() {
    std::cout << "========================================\n";
    std::cout << "🎮 C++ 反模式：硬编码遥控器\n";
    std::cout << "========================================\n";

    RemoteControl remote;
    remote.onButtonPressed("light_on");
    remote.onButtonPressed("fan_on");
    remote.onButtonPressed("stereo_on");
    remote.onButtonPressed("ac_on");  // ❌ 未知按钮

    return 0;
}
