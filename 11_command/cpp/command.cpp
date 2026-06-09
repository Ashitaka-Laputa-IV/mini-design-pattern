/*
================================================================================
Lesson 11: Command — C++ 命令模式演示
================================================================================
  compile & run:
    g++ -std=c++11 command.cpp -o command
    ./command
================================================================================
*/

#include "command.h"

int main() {
    std::cout << "====== C++ 命令模式演示 ======\n\n";

    // ---- 创建接收者 ----
    Light livingRoomLight;
    Fan ceilingFan;

    // ---- 创建命令 ----
    auto lightOn = std::make_unique<LightOnCommand>(&livingRoomLight);
    auto lightOff = std::make_unique<LightOffCommand>(&livingRoomLight);
    auto fanHigh = std::make_unique<FanSetSpeedCommand>(&ceilingFan, Fan::HIGH);
    auto fanOff = std::make_unique<FanSetSpeedCommand>(&ceilingFan, Fan::OFF);

    // ---- 设置遥控器 ----
    RemoteControl remote;
    remote.setCommand(0, std::move(lightOn), std::move(lightOff));
    remote.setCommand(1, std::move(fanHigh), std::move(fanOff));

    // ---- 用户操作 ----
    remote.onButtonPressed(0);    // 开灯
    remote.offButtonPressed(0);   // 关灯
    remote.undoButtonPressed();   // 撤销关灯 → 灯又亮了

    remote.onButtonPressed(1);    // 风扇高速
    remote.offButtonPressed(1);   // 风扇关闭
    remote.undoButtonPressed();   // 撤销关风扇 → 恢复到高速

    std::cout << "\n====== 总结 ======\n";
    std::cout << "✅ 遥控器(Invoker)不需要知道具体操作\n";
    std::cout << "✅ 添加新设备只需创建新的命令类\n";
    std::cout << "✅ 撤销功能通过历史记录自动支持\n";
    std::cout << "✅ 可以实现宏命令(组合多个命令)\n";

    return 0;
}
