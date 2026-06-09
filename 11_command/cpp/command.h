/*
================================================================================
Lesson 11: Command — C++ 命令模式 [行为型]
================================================================================
  将"请求"封装成对象，支持参数化、队列化、可撤销。

  核心角色：
    1. Command (命令接口) — 声明 execute() 和 undo()
    2. ConcreteCommand (具体命令) — 绑定 Receiver 和具体动作
    3. Invoker (调用者) — 持有命令对象，触发执行
    4. Receiver (接收者) — 真正执行操作的对象
    5. Client (客户端) — 创建具体命令并设置给 Invoker
================================================================================
*/

#ifndef COMMAND_H
#define COMMAND_H

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <stack>

// ============================================================================
// Receiver (接收者) — 真正干活的类
// ============================================================================

class Light {
    /*
     * 🔌 灯：开/关两个操作
     */
public:
    void on()  { std::cout << "  💡 灯开了\n";  state_ = 1; }
    void off() { std::cout << "  💡 灯关了\n";  state_ = 0; }
    int state() const { return state_; }
private:
    int state_ = 0;
};

class Fan {
    /*
     * 🔄 风扇：多档位，支持加速/减速/开关
     */
public:
    enum Speed { OFF = 0, LOW = 1, MEDIUM = 2, HIGH = 3 };

    void turnOn() {
        speed_ = LOW;
        std::cout << "  🌀 风扇开启 (低速)\n";
    }

    void turnOff() {
        speed_ = OFF;
        std::cout << "  🌀 风扇关闭\n";
    }

    void setSpeed(Speed s) {
        speed_ = s;
        static const char* names[] = {"关闭", "低速", "中速", "高速"};
        std::cout << "  🌀 风扇 -> " << names[speed_] << "\n";
    }

    Speed getSpeed() const { return speed_; }

private:
    Speed speed_ = OFF;
};


// ============================================================================
// Command (命令接口)
// ============================================================================

class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};


// ============================================================================
// ConcreteCommand (具体命令)
// ============================================================================

class LightOnCommand : public Command {
private:
    Light* light_;

public:
    explicit LightOnCommand(Light* light) : light_(light) {}

    void execute() override {
        std::cout << "  [命令] 执行开灯\n";
        light_->on();
    }

    void undo() override {
        std::cout << "  [命令] 撤销开灯\n";
        light_->off();
    }
};

class LightOffCommand : public Command {
private:
    Light* light_;

public:
    explicit LightOffCommand(Light* light) : light_(light) {}

    void execute() override {
        std::cout << "  [命令] 执行关灯\n";
        light_->off();
    }

    void undo() override {
        std::cout << "  [命令] 撤销关灯\n";
        light_->on();
    }
};

// 无操作命令 (Null Object 模式的应用)
class NoCommand : public Command {
public:
    void execute() override { /* 什么也不做 */ }
    void undo() override {}
};


// ============================================================================
// 带状态保存的风扇命令（实现撤销的关键）
// ============================================================================

class FanSetSpeedCommand : public Command {
private:
    Fan* fan_;
    Fan::Speed previousSpeed_;
    Fan::Speed newSpeed_;

public:
    FanSetSpeedCommand(Fan* fan, Fan::Speed speed)
        : fan_(fan), newSpeed_(speed) {}

    void execute() override {
        previousSpeed_ = fan_->getSpeed();  // ⭐ 保存撤销所需的状态
        std::cout << "  [命令] 设置风扇速度\n";
        fan_->setSpeed(newSpeed_);
    }

    void undo() override {
        std::cout << "  [命令] 恢复风扇到之前的速度\n";
        fan_->setSpeed(previousSpeed_);
    }
};


// ============================================================================
// Invoker (调用者) — 遥控器
// ============================================================================

class RemoteControl {
    /*
     * 🎮 万能遥控器
     * - 支持多个按钮
     * - 每个按钮可以分配不同的命令
     * - 支持一键撤销
     */
private:
    std::vector<std::unique_ptr<Command>> onCommands_;
    std::vector<std::unique_ptr<Command>> offCommands_;
    std::stack<Command*> history_;  // ⭐ 命令历史记录（用于撤销）

public:
    static const int SLOTS = 4;

    RemoteControl() {
        // 初始化所有槽位为无操作命令
        for (int i = 0; i < SLOTS; ++i) {
            onCommands_.push_back(std::make_unique<NoCommand>());
            offCommands_.push_back(std::make_unique<NoCommand>());
        }
    }

    void setCommand(int slot,
                    std::unique_ptr<Command> onCmd,
                    std::unique_ptr<Command> offCmd) {
        if (slot < 0 || slot >= SLOTS) return;
        onCommands_[slot] = std::move(onCmd);
        offCommands_[slot] = std::move(offCmd);
    }

    void onButtonPressed(int slot) {
        std::cout << "\n--- 按下了第 " << (slot + 1) << " 个开按钮 ---\n";
        if (slot < 0 || slot >= SLOTS) return;
        onCommands_[slot]->execute();
        history_.push(onCommands_[slot].get());  // ⭐ 记录历史
    }

    void offButtonPressed(int slot) {
        std::cout << "\n--- 按下了第 " << (slot + 1) << " 个关按钮 ---\n";
        if (slot < 0 || slot >= SLOTS) return;
        offCommands_[slot]->execute();
        history_.push(offCommands_[slot].get());
    }

    void undoButtonPressed() {
        std::cout << "\n--- 按下了撤销按钮 ---\n";
        if (history_.empty()) {
            std::cout << "  没有操作可以撤销\n";
            return;
        }
        Command* lastCmd = history_.top();
        history_.pop();
        lastCmd->undo();
    }
};

#endif // COMMAND_H
