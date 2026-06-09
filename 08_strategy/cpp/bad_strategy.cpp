/*
================================================================================
 Lesson 8: Strategy — 策略模式 [行为型] · C++ 反模式
================================================================================
  和 Python 版本一样的场景：电商运费计算。

  同事用 if-else 处理所有地区的运费规则，
  每次新增一种规则就要改核心代码。

  🧠 在 C++ 中，这种 if-else 地狱更危险：
    - 编译型语言，改完后需要重新编译整个模块
    - if-else 分支多容易导致 CPU 分支预测失败（性能问题）
    - 多人协作时容易产生合并冲突
================================================================================
*/

#include <iostream>
#include <string>

// ============================================================================
// 反模式：if-else 地狱
// ============================================================================

struct Order {
    /*
     * 订单数据结构。
     * 在反模式中，运费计算逻辑完全写在外面的大函数里。
     */
    std::string region;
    std::string member_level;
    double total_weight;

    Order(const std::string& r, const std::string& m, double w)
        : region(r), member_level(m), total_weight(w) {}
};

double calculateShipping(const Order& order) {
    /*
     * ❌ 反模式：if-else 地狱
     *
     * 问题分析：
     *   1. 每增加一种策略，就要修改这个函数（违反开闭原则）
     *   2. 函数越来越长，难以维护
     *   3. 逻辑嵌套深，阅读困难
     *   4. 测试时分支组合爆炸
     *   5. 如果另一个地方也需要运费计算，只能复制粘贴
     */
    std::cout << "  [计算运费] 地区=" << order.region
              << ", 会员=" << order.member_level
              << ", 重量=" << order.total_weight << "kg\n";

    double shipping = 0.0;

    // 第一层：按地区
    if (order.region == "domestic") {
        // 第二层：按会员等级
        if (order.member_level == "vip") {
            shipping = 0.0;
            std::cout << "  [规则] 国内 VIP → 免运费\n";
        } else if (order.member_level == "normal") {
            shipping = 10.0;
            std::cout << "  [规则] 国内普通 → 固定 10 元\n";
        } else {
            std::cout << "  [⚠警告] 未知会员等级，使用默认规则\n";
            shipping = 10.0;
        }
    } else if (order.region == "overseas") {
        if (order.member_level == "vip") {
            shipping = order.total_weight * 10.0;
            std::cout << "  [规则] 海外 VIP → " << order.total_weight
                      << "kg × 10 元 = " << shipping << " 元\n";
        } else if (order.member_level == "normal") {
            shipping = order.total_weight * 15.0;
            std::cout << "  [规则] 海外普通 → " << order.total_weight
                      << "kg × 15 元 = " << shipping << " 元\n";
        } else {
            std::cout << "  [⚠警告] 未知会员等级，使用默认规则\n";
            shipping = order.total_weight * 15.0;
        }
    } else {
        std::cout << "  [⚠警告] 未知地区，使用海外普通规则\n";
        shipping = order.total_weight * 15.0;
    }

    return shipping;
}

int main() {
    std::cout << "====== C++ 反模式：if-else 地狱 运费计算 ======\n\n";

    Order orders[] = {
        Order("domestic", "normal", 5.0),
        Order("domestic", "vip", 5.0),
        Order("overseas", "normal", 2.0),
        Order("overseas", "vip", 3.0),
    };

    for (const auto& order : orders) {
        double cost = calculateShipping(order);
        std::cout << "  >>> 运费: " << cost << " 元\n\n";
    }

    std::cout << "🤔 思考：如果新增 '海外超级VIP（免运费）'，\n"
              << "   你需要修改 calculateShipping 函数——\n"
              << "   但如果有 10 处调用呢？搜索替换漏一处就出 bug。\n";

    return 0;
}
