/*
================================================================================
Lesson 7: Proxy (代理模式) — C++ 实现
================================================================================
  展示 C++ 中如何使用基类指针实现虚拟代理和保护代理。

  要点：
  - 纯虚函数定义接口
  - 虚析构函数确保正确释放
  - 智能指针管理资源
  - 延迟加载 + 缓存机制

  compile & run:
    g++ -std=c++11 main.cpp -o proxy
    ./proxy
================================================================================
*/

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <thread>
#include <chrono>

class Image {
public:
    virtual ~Image() = default;
    virtual void display() = 0;
    virtual std::string getFilename() const = 0;
};


// =============================================================================
// 2. RealSubject (真实主题)
// =============================================================================

class HighResolutionImage : public Image {
public:
    explicit HighResolutionImage(const std::string& filename)
        : _filename(filename), _imageData(nullptr) {
        // ⚠ 注意：真实对象不再在构造时加载
    }

    void loadFromDisk() {
        if (_imageData != nullptr) {
            return;  // 已加载
        }
        std::cout << "    [加载] " << _filename << " 从磁盘加载中... (10MB)";
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        _imageData = new char[10 * 1024 * 1024];  // 模拟 10MB
        std::cout << " OK" << std::endl;
    }

    void display() override {
        if (_imageData == nullptr) {
            std::cout << "  [警告] " << _filename << " 未加载！" << std::endl;
            return;
        }
        std::cout << "  [显示原图] " << _filename << " (10MB)" << std::endl;
    }

    std::string getFilename() const override {
        return _filename;
    }

    ~HighResolutionImage() override {
        delete[] _imageData;
    }

private:
    std::string _filename;
    char* _imageData;
};


// =============================================================================
// 3. Virtual Proxy (虚拟代理)
// =============================================================================

class ProxyImage : public Image {
public:
    explicit ProxyImage(const std::string& filename)
        : _filename(filename), _realImage(nullptr) {
        // ⭐ 构造时只保存文件名，不加载图片
    }

    void display() override {
        // ⭐ 首次访问时延迟加载
        if (_realImage == nullptr) {
            std::cout << "  [代理] 首次访问 " << _filename << "，开始加载..." << std::endl;
            _realImage = std::make_unique<HighResolutionImage>(_filename);
            _realImage->loadFromDisk();
        } else {
            std::cout << "  [代理] " << _filename << " 已加载，直接显示" << std::endl;
        }
        _realImage->display();
    }

    std::string getFilename() const override {
        return _filename;
    }

private:
    std::string _filename;
    std::unique_ptr<HighResolutionImage> _realImage;  // ⭐ 延迟创建
};


// =============================================================================
// 4. Protection Proxy (保护代理)
// =============================================================================

class ProtectedImage : public Image {
public:
    ProtectedImage(const std::string& filename, const std::string& requiredRole)
        : _filename(filename), _requiredRole(requiredRole), _realImage(nullptr) {}

    void display() override {
        // 默认：普通用户
        displayWithRole("normal");
    }

    bool displayWithRole(const std::string& userRole) {
        // ⭐ 权限检查
        if (userRole != _requiredRole && userRole != "admin") {
            std::cout << "  [代理] 权限不足！需要 '" << _requiredRole
                      << "' 角色才能查看 " << _filename << std::endl;
            return false;
        }

        // 权限通过，延迟加载
        if (_realImage == nullptr) {
            std::cout << "  [代理] 权限验证通过，开始加载 " << _filename << "..." << std::endl;
            _realImage = std::make_unique<HighResolutionImage>(_filename);
            _realImage->loadFromDisk();
        }

        _realImage->display();
        return true;
    }

    std::string getFilename() const override {
        return _filename;
    }

private:
    std::string _filename;
    std::string _requiredRole;
    std::unique_ptr<HighResolutionImage> _realImage;
};


// =============================================================================
// 5. 测试
// =============================================================================

void demoVirtualProxy() {
    std::cout << "==========================================" << std::endl;
    std::cout << "场景 1: 虚拟代理 — 延迟加载" << std::endl;
    std::cout << "==========================================" << std::endl;

    // 创建代理（极快，不加载图片）
    std::vector<std::unique_ptr<Image>> images;
    for (int i = 1; i <= 5; ++i) {
        images.push_back(std::make_unique<ProxyImage>(
            "photo_" + std::to_string(i) + ".jpg"
        ));
    }
    std::cout << "创建 5 个代理对象完成（内存占用极小）" << std::endl;

    // 查看缩略图（不触发加载）
    std::cout << "\n查看缩略图（代理不触发加载）:" << std::endl;
    for (const auto& img : images) {
        std::cout << "  缩略图: " << img->getFilename() << std::endl;
    }

    // 打开第 3 张图片（触发延迟加载）
    std::cout << "\n打开第 3 张图片（首次加载）:" << std::endl;
    images[2]->display();

    // 再次打开（缓存）
    std::cout << "\n再次打开第 3 张图片（缓存）:" << std::endl;
    images[2]->display();
}

void demoProtectionProxy() {
    std::cout << "\n==========================================" << std::endl;
    std::cout << "场景 2: 保护代理 — 权限控制" << std::endl;
    std::cout << "==========================================" << std::endl;

    ProtectedImage publicImg("public_photo.jpg", "normal");
    ProtectedImage vipImg("vip_photo.jpg", "vip");

    std::cout << "\n普通用户尝试查看公共图片:" << std::endl;
    publicImg.displayWithRole("normal");

    std::cout << "\n普通用户尝试查看 VIP 图片:" << std::endl;
    vipImg.displayWithRole("normal");  // 被拒绝

    std::cout << "\nVIP 用户查看 VIP 图片:" << std::endl;
    vipImg.displayWithRole("vip");  // 通过
}

int main() {
    demoVirtualProxy();
    demoProtectionProxy();
    return 0;
}
