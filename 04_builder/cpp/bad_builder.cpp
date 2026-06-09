/*
================================================================================
Lesson 4: Builder — C++ 反模式示例 [创建型]
================================================================================
  C++ 中 Telescoping Constructor（伸缩构造函数）问题更严重：
  因为 C++ 没有默认参数的重载灵活性（虽然支持默认参数，但顺序限制严格）。

  🎬 场景和 Python 版本一致：构建一台"电脑"对象。
================================================================================
*/

#include <iostream>
#include <string>

// ============================================================================
// 反模式：Telescoping Constructor（伸缩构造函数）
// ============================================================================

class Computer {
    /*
     * ❌ 坏味道：Telescoping Constructor
     *
     * C++ 中这个问题比 Python 更严重：
     * 1. 没有命名参数（keyword arguments）
     * 2. 默认参数只能在末尾
     * 3. 同类型参数相邻时，传参顺序错了编译器不会警告！
     *
     * 以下有 9 个参数，前 3 个必选，后 6 个可选。
     * 但 C++ 默认参数必须从右到左连续排列。
     */

private:
    std::string cpu_;
    std::string ram_;
    std::string storage_;
    std::string gpu_;
    std::string os_;
    bool has_wifi_;
    bool has_bluetooth_;
    std::string keyboard_;
    std::string mouse_;

public:
    /*
     * 构造函数——参数列表长得可怕！
     *
     * C++ 没有默认参数跳过语法，如果我想设 has_bluetooth=true，
     * 必须把 has_wifi 也传上。
     */
    Computer(
        const std::string& cpu,
        const std::string& ram,
        const std::string& storage,
        const std::string& gpu = "集成显卡",
        const std::string& os = "无",
        bool has_wifi = false,
        bool has_bluetooth = false,
        const std::string& keyboard = "标准键盘",
        const std::string& mouse = "标准鼠标"
    )
        : cpu_(cpu), ram_(ram), storage_(storage),
          gpu_(gpu), os_(os),
          has_wifi_(has_wifi), has_bluetooth_(has_bluetooth),
          keyboard_(keyboard), mouse_(mouse) {
        std::cout << "  [Computer 构造] 9个参数已接收\n";
    }

    void display() const {
        /*
         * 显示电脑配置信息。
         * const 保证不修改成员变量。
         */
        std::cout << "  CPU    : " << cpu_ << "\n"
                  << "  内存   : " << ram_ << "\n"
                  << "  硬盘   : " << storage_ << "\n"
                  << "  显卡   : " << gpu_ << "\n"
                  << "  系统   : " << os_ << "\n"
                  << "  WiFi   : " << (has_wifi_ ? "有" : "无") << "\n"
                  << "  蓝牙   : " << (has_bluetooth_ ? "有" : "无") << "\n"
                  << "  键盘   : " << keyboard_ << "\n"
                  << "  鼠标   : " << mouse_ << "\n";
    }
};


// ============================================================================
// 反模式 2：C++ 中另一种常见的坏做法——用 struct 裸传
// ============================================================================

struct ComputerConfig {
    /*
     * 另一种 C++ 常见反模式：用 struct 传参
     *
     * 这比直接传 9 个参数好一点，但：
     * 1. struct 的字段仍然可以被随意修改
     * 2. 仍然需要记住哪些字段是必填的
     * 3. 需要手动保证所有字段被正确初始化
     */
    std::string cpu;
    std::string ram;
    std::string storage;
    std::string gpu = "集成显卡";
    std::string os = "无";
    bool has_wifi = false;
    bool has_bluetooth = false;
    std::string keyboard = "标准键盘";
    std::string mouse = "标准鼠标";
};

class ComputerWithConfig {
    /*
     * 用 struct 替代长参数列表——略好，但仍有问题
     */
private:
    std::string cpu_;
    std::string ram_;
    std::string storage_;
    std::string gpu_;
    std::string os_;
    bool has_wifi_;
    bool has_bluetooth_;
    std::string keyboard_;
    std::string mouse_;

public:
    explicit ComputerWithConfig(const ComputerConfig& cfg)
        : cpu_(cfg.cpu), ram_(cfg.ram), storage_(cfg.storage),
          gpu_(cfg.gpu), os_(cfg.os),
          has_wifi_(cfg.has_wifi), has_bluetooth_(cfg.has_bluetooth),
          keyboard_(cfg.keyboard), mouse_(cfg.mouse) {}

    void display() const {
        std::cout << "  CPU    : " << cpu_ << "\n"
                  << "  内存   : " << ram_ << "\n"
                  << "  硬盘   : " << storage_ << "\n"
                  << "  显卡   : " << gpu_ << "\n"
                  << "  系统   : " << os_ << "\n"
                  << "  WiFi   : " << (has_wifi_ ? "有" : "无") << "\n"
                  << "  蓝牙   : " << (has_bluetooth_ ? "有" : "无") << "\n"
                  << "  键盘   : " << keyboard_ << "\n"
                  << "  鼠标   : " << mouse_ << "\n";
    }
};


int main() {
    std::cout << "====== C++ 反模式：Telescoping Constructor ======\n\n";

    // ---- 问题 1：参数顺序容易搞错 ----
    std::cout << "1️⃣  参数顺序错误的风险\n\n";

    // 正确顺序
    Computer pc1("Intel i7", "16GB", "1TB", "RTX 3060", "Windows 11");
    std::cout << "  ✅ 正确顺序:\n";
    pc1.display();

    // 错误顺序：CPU 和 内存传反了
    // C++ 编译不会报错！都是 std::string 类型
    Computer pc2("16GB", "Intel i7", "1TB", "RTX 3060", "Windows 11");
    std::cout << "\n  ❌ 顺序传反了（编译不报错！）:\n";
    pc2.display();

    // ---- 问题 2：可选参数必须按顺序填充 ----
    std::cout << "\n2️⃣  可选参数必须填充中间值\n\n";

    // 我只想设置 has_bluetooth=true，但 has_wifi 在前面
    // C++ 没有 Python 的关键字参数语法，必须显式传 has_wifi
    Computer pc3("AMD Ryzen 7", "32GB", "2TB",
                 "RTX 4070", "Ubuntu",
                 false,   // ← 必须显式传 has_wifi
                 true);   // ← 才能传到 has_bluetooth
    std::cout << "  😤 为了设蓝牙，必须传WiFi:\n";
    pc3.display();

    // ---- 问题 3：使用 struct 方式 ----
    std::cout << "\n3️⃣  struct 传参方式（略好，仍有问题）\n\n";

    ComputerConfig cfg;
    cfg.cpu = "Intel i5";
    cfg.ram = "16GB";
    cfg.storage = "512GB";
    // 忘记设置 os，但编译不会报错！
    // cfg.os 会是默认值 "无"

    ComputerWithConfig pc4(cfg);
    std::cout << "  😱 忘记设置操作系统，但没人提醒:\n";
    pc4.display();

    std::cout << "\n====== 结论 ======\n";
    std::cout << "C++ 中参数过多的构造函数问题更严重！\n";
    std::cout << "推荐使用 Builder 模式解决。\n";

    return 0;
}
