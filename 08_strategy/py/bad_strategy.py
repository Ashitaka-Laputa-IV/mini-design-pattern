"""
================================================================================
 Lesson 8: Strategy — 策略模式 [行为型] · 反模式
================================================================================
  📖 本课采用"反模式驱动"方式：
     先看一段糟糕的代码，分析问题，再引入设计模式。

 🔑 面试频率：★★★★☆（策略模式几乎是行为型模式中最常问的）
================================================================================
"""

"""
===============================================================================
 🎬 场景：电商系统的"运费计算"

  假设你在开发一个电商平台，不同地区、不同会员等级的运费不同。

  计算规则：
    国内普通：固定 10 元
    国内 VIP：固定 0 元（包邮）
    海外普通：重量 × 15 元/kg
    海外 VIP：重量 × 10 元/kg

  同事直接写了 if-else 处理所有情况，业务逻辑越堆越多……

  请你先停在这里想一想：
    1. 如果新增"海外超级VIP（免运费）"怎么改？
    2. 如果新增"港澳台地区"怎么改？
    3. 这些修改会影响到什么代码？
    .
    .
    .
    想好了吗？往下翻看"if-else 地狱" 👇
===============================================================================
"""


# ============================================================================
# 反模式：if-else 地狱
# ============================================================================

class Order:
    """
    订单类——本该只负责订单数据，结果被同事塞满了运费逻辑。
    """

    def __init__(self, region: str, member_level: str, total_weight: float):
        """
        :param region: 地区，如 "domestic" / "overseas"
        :param member_level: 会员等级，如 "normal" / "vip"
        :param total_weight: 总重量（kg）
        """
        self.region = region
        self.member_level = member_level
        self.total_weight = total_weight


def calculate_shipping(order: Order) -> float:
    """
    ❌ 反模式：if-else 地狱

    问题分析：
      1. 函数越来越长 —— 每增加一种策略，就要加一层 if-else
      2. 违反开闭原则 —— 新增策略必须修改现有代码
      3. 逻辑重复 —— 不同分支可能有相似的逻辑片段
      4. 难以测试 —— 分支组合爆炸
      5. 阅读困难 —— 嵌套层次深，很难一眼看出整体规则
    """
    print(f"  [计算运费] 地区={order.region}, 会员={order.member_level}, 重量={order.total_weight}kg")

    # ---------- 第一层：按地区 ----------
    if order.region == "domestic":
        # ---------- 第二层：按会员等级 ----------
        if order.member_level == "vip":
            # 国内 VIP：包邮
            shipping = 0.0
            print("  [规则] 国内 VIP → 免运费")

        elif order.member_level == "normal":
            # 国内普通：固定 10 元
            shipping = 10.0
            print("  [规则] 国内普通 → 固定 10 元")

        else:
            # 其他会员等级——但谁知道还有哪些？只好走默认
            print("  [⚠警告] 未知会员等级，使用默认规则")
            shipping = 10.0

    elif order.region == "overseas":
        # ---------- 第二层：按会员等级 ----------
        if order.member_level == "vip":
            # 海外 VIP：10 元/kg
            shipping = order.total_weight * 10.0
            print(f"  [规则] 海外 VIP → {order.total_weight}kg × 10 元 = {shipping} 元")

        elif order.member_level == "normal":
            # 海外普通：15 元/kg
            shipping = order.total_weight * 15.0
            print(f"  [规则] 海外普通 → {order.total_weight}kg × 15 元 = {shipping} 元")

        else:
            print("  [⚠警告] 未知会员等级，使用默认规则")
            shipping = order.total_weight * 15.0

    else:
        # 未知地区——抛异常还是给默认值？同事也不知道怎么处理
        print("  [⚠警告] 未知地区，使用海外普通规则")
        shipping = order.total_weight * 15.0

    return shipping


# ============================================================================
# 🧪 测试反模式代码
# ============================================================================

def test_bad_strategy():
    print("=" * 60)
    print("❌ 反模式：if-else 地狱 运费计算")
    print("=" * 60)

    orders = [
        Order("domestic", "normal", 5.0),
        Order("domestic", "vip", 5.0),
        Order("overseas", "normal", 2.0),
        Order("overseas", "vip", 3.0),
    ]

    for order in orders:
        cost = calculate_shipping(order)
        print(f"  >>> 运费: {cost} 元\n")

    print("\n" + "=" * 60)
    print("🤔 思考：如果现在要新增一个 'overseas_super_vip'（免运费），")
    print("   你需要修改 calculate_shipping 函数——改一处就够了？")
    print("   不！如果有 10 个模块都调用了这个函数呢？")
    print("   更糟的是：如果其他地方又写了重复的 if-else 判断呢？")
    print("=" * 60)


"""
===============================================================================
 反模式总结

 ❌ 存在的问题：
    1. 开闭原则违反：对修改开放，对扩展关闭
       → 新增策略 = 修改核心代码 = 可能引入 bug

    2. 代码膨胀：随着策略增加，函数越来越长
       → 国内/海外 × 普通/VIP/超级VIP = 6 种组合
       → 如果再加地区类型（港澳台、东南亚、欧美...）

    3. 条件判断散落各处：
       → 这个 if-else 可能出现在视图层、服务层、数据库层
       → 改规则时漏改一个地方就出 bug

    4. 复用困难：
       → 如果另一处也要运费计算，只能复制粘贴 if-else
       → 维护噩梦

 ✅ 解决思路：策略模式
   将"每种运费计算算法"封装成独立的策略类，
   让它们可以互相替换，客户端只需切换策略对象。

   翻到 strategy.py 看正解 👉
===============================================================================
"""


if __name__ == "__main__":
    test_bad_strategy()
