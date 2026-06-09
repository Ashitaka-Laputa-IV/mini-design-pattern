/*
================================================================================
Lesson 4: Builder — C++ 演示代码 [创建型]
================================================================================
  compile & run:
    g++ -std=c++11 builder.cpp -o builder
    ./builder
================================================================================
*/

#include "builder.h"
#include <iostream>
#include <stdexcept>

// ============================================================================
// 辅助函数：展示 Builder 模式的各种用法
// ============================================================================

void demo_builder_pattern() {
    /*
     * 展示 Builder 模式的各种用法，与 Python 版本一一对应。
     */

    std::cout << "====== C++ Builder 模式演示 ======\n\n";

    // ---- 1. 自由搭配：链式调用 ----
    std::cout << "1️⃣  自由搭配（链式调用）\n";
    std::cout << "-----------------------------\n\n";

    Computer gaming_rig = ComputerBuilder()
        .set_cpu("AMD Ryzen 7 7800X3D")
        .set_ram("32GB DDR5")
        .set_storage("1TB NVMe SSD")
        .set_gpu("NVIDIA RTX 4070 Ti")
        .set_os("Windows 11")
        .enable_wifi()
        .enable_bluetooth()
        .set_keyboard("机械键盘")
        .set_mouse("游戏鼠标")
        .build();

    std::cout << "  自定游戏配置:\n";
    gaming_rig.display();

    // ---- 2. 只设置必填项 ----
    std::cout << "2️⃣  只配置核心部件（其他用默认值）\n";
    std::cout << "-----------------------------\n\n";

    Computer basic_pc = ComputerBuilder()
        .set_cpu("Intel i3-12100")
        .set_ram("8GB DDR4")
        .set_storage("256GB SSD")
        .build();

    std::cout << "  基础配置:\n";
    basic_pc.display();

    // ---- 3. 使用 Director 预设 ----
    std::cout << "3️⃣  Director 预设方案\n";
    std::cout << "-----------------------------\n\n";

    std::cout << "💼 办公电脑:\n";
    ComputerDirector::create_office_pc().display();

    std::cout << "🎮 游戏电脑:\n";
    ComputerDirector::create_gaming_pc().display();

    std::cout << "👨‍💻 程序员电脑:\n";
    ComputerDirector::create_programmer_pc().display();

    std::cout << "🖥️  服务器:\n";
    ComputerDirector::create_minimal_server().display();

    // ---- 4. 校验错误演示 ----
    std::cout << "4️⃣  必填参数校验\n";
    std::cout << "-----------------------------\n\n";

    try {
        // 忘记设置必填项
        Computer incomplete = ComputerBuilder()
            .set_cpu("Intel i5")
            // 忘记设置 ram 和 storage
            .build();
    } catch (const std::runtime_error& e) {
        std::cout << "  ✅ build() 时校验: " << e.what() << "\n\n";
    }

    // ---- 5. 参数顺序无关 ----
    std::cout << "5️⃣  参数顺序无关——再也不怕传错了！\n";
    std::cout << "-----------------------------\n\n";

    Computer pc_a = ComputerBuilder()
        .set_ram("16GB")       // 先设内存
        .set_cpu("Intel i7")   // 再设 CPU
        .set_storage("1TB")
        .build();

    Computer pc_b = ComputerBuilder()
        .set_cpu("Intel i7")   // 先设 CPU
        .set_storage("1TB")    // 再设硬盘
        .set_ram("16GB")       // 最后设内存
        .build();

    std::cout << "  pc_a: CPU=" << pc_a.cpu()
              << ", RAM=" << pc_a.ram() << "\n";
    std::cout << "  pc_b: CPU=" << pc_b.cpu()
              << ", RAM=" << pc_b.ram() << "\n";
    std::cout << "  顺序不影响结果 ✓\n";
}


// ============================================================================
// 对比展示：反模式 vs Builder 模式
// ============================================================================

void comparison() {
    std::cout << "\n====== 对比：反模式 vs Builder 模式 ======\n\n";

    std::cout << R"(
    ┌──────────────────────────────────────────────────────────────┐
    │           反模式 (Telescoping Constructor)                   │
    ├──────────────────────────────────────────────────────────────┤
    │  Computer("Intel i7", "16GB", "1TB", "RTX 3060",            │
    │           "Windows 11", true, true, "机械键盘", "游戏鼠标") │
    │                                                              │
    │  ❌ 9 个位置参数，记不住顺序                                  │
    │  ❌ true, true 是什么意思？WiFi？蓝牙？                       │
    │  ❌ C++ 编译不会报类型错误（都是 string/bool）                │
    └──────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────┐
    │           ✅ Builder 模式                                    │
    ├──────────────────────────────────────────────────────────────┤
    │  ComputerBuilder()                                           │
    │      .set_cpu("Intel i7")      ← 方法名说明含义              │
    │      .set_ram("16GB")                                       │
    │      .set_storage("1TB")                                    │
    │      .set_gpu("RTX 3060")                                   │
    │      .set_os("Windows 11")                                  │
    │      .enable_wifi()           ← 没有 true/false 歧义         │
    │      .enable_bluetooth()                                    │
    │      .set_keyboard("机械键盘")                               │
    │      .set_mouse("游戏鼠标")                                  │
    │      .build()                ← 最后一步构建不可变对象        │
    │                                                              │
    │  ✅ 方法名说明参数含义                                        │
    │  ✅ 顺序任意                                                │
    │  ✅ build() 时校验必填项                                     │
    └──────────────────────────────────────────────────────────────┘
    )" << "\n";
}


int main() {
    demo_builder_pattern();
    comparison();

    std::cout << "\n====== 小结 ======\n";
    std::cout << "什么时候用 Builder？\n";
    std::cout << "  - 构造函数参数 > 3-4 个\n";
    std::cout << "  - 对象有大量可选属性\n";
    std::cout << "  - 需要创建不同配置的相似对象\n";
    std::cout << "  - 希望创建不可变对象\n";
    std::cout << "  - C++ 中尤其有用（无命名参数）\n";

    return 0;
}
