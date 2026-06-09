/*
================================================================================
Lesson 7: Proxy — C++ 反模式示例
================================================================================
  🎬 场景：图片查看器。同事把所有图片在启动时全部加载到内存中。

  反模式：急加载 (Eager Loading) — 不管用不用，先加载再说。
  - 100 张图 × 10MB = 1GB 内存
  - 启动时间极长
  - 大部分图片用户根本不会点开看
================================================================================
*/

#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>

// ============================================================================
// ❌ 反模式：直接加载所有图片
// ============================================================================

class HighResolutionImage {
private:
    std::string filename_;
    char* imageData_;  // 模拟图片数据

public:
    explicit HighResolutionImage(const std::string& fname)
        : filename_(fname) {
        // ⚠ 构造时就加载！所有图片一次性进内存
        std::cout << "  [加载] " << filename_ << " 正在加载到内存...(10MB)\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(300));
        imageData_ = new char[10 * 1024 * 1024];  // 10MB
    }

    void display() const {
        std::cout << "  [显示] " << filename_ << " (10MB)\n";
    }

    std::string getFilename() const { return filename_; }

    ~HighResolutionImage() {
        delete[] imageData_;
    }
};

int main() {
    std::cout << "====== C++ 反模式：急加载图片 ======\n\n";

    // 模拟用户打开图片文件夹
    std::vector<std::string> filenames = {
        "photo_1.jpg", "photo_2.jpg", "photo_3.jpg",
        "photo_4.jpg", "photo_5.jpg"
    };

    std::cout << "1️⃣  用户打开文件夹，加载所有图片...(共" << filenames.size() << "张)\n\n";

    std::vector<HighResolutionImage> gallery;
    for (const auto& name : filenames) {
        gallery.emplace_back(name);  // 每张图都加载！
    }

    std::cout << "\n2️⃣  内存占用: " << (filenames.size() * 10) << "MB\n";
    std::cout << "    启动完成（但用户可能只看第3张）\n\n";

    // 用户只看第 3 张图
    std::cout << "3️⃣  用户查看第3张图:\n";
    gallery[2].display();

    std::cout << "\n❌ 问题总结:\n";
    std::cout << "  - 内存浪费：未查看的图片占用了大量内存\n";
    std::cout << "  - 启动慢：所有图加载完才能操作\n";
    std::cout << "  - 如果图库有1000张图，程序直接崩溃\n\n";

    std::cout << "✅ 解决方案：用 Proxy 代理模式做延迟加载\n";
    std::cout << "   查看 main.cpp 中的 ProxyImage 实现\n";

    return 0;
}
