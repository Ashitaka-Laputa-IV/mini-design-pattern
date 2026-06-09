# Mini Design Pattern — 设计模式迷你课程

一个面向 **面试准备** 的设计模式课程，以 **反模式/坏味道驱动** 的方式学习。

> **语言**: 主学 Python，C++ 对照参考
> **方式**: 先看坏代码 → 分析痛点 → 引入设计模式 → 面试追问

---

## 课程总览

| # | 类型 | 模式 | 关键词 | 反模式 |
|---|------|------|--------|--------|
| **00** | 🏁 先修 | OOP 基础 | 封装/继承/多态/抽象/组合 | 裸数据、if-else 判断类型 |
| **01** | 创建型 | Singleton | 唯一实例、全局访问点、线程安全 | 全局变量滥用 |
| **02** | 创建型 | Factory Method | 创建逻辑延迟到子类、开闭原则 | if-else 创建扩散 |
| **03** | 创建型 | Abstract Factory | 产品族、跨平台、一致性 | 产品族耦合 |
| **04** | 创建型 | Builder | 分步构建、链式调用、不可变对象 | 构造函数参数过长 |
| **05** | 结构型 | Adapter | 接口转换、兼容旧系统、开闭原则 | 强行修改已有代码 |
| **06** | 结构型 | Decorator | 组合替代继承、类爆炸、装饰链 | 子类爆炸 |
| **07** | 结构型 | Proxy | 延迟加载、访问控制、缓存 | 急加载、无权限控制 |
| **08** | 行为型 | Strategy | 算法族可替换、运行时切换 | if-else 策略分支 |
| **09** | 行为型 | Observer | 一对多通知、松耦合、事件驱动 | 轮询/硬编码通知 |
| **10** | 行为型 | Template Method | 固定算法骨架、钩子方法、好莱坞原则 | 重复的算法结构 |
| **11** | 行为型 | Command | 请求封装、撤销/重做、命令队列 | 请求收发紧耦合 |

---

## 每节课的文件结构

```
XX_模式名/
├── py/                          ← 主学语言：Python
│   ├── bad_xxx.py               ← 反模式：先感受痛点
│   ├── xxx.py                   ← 模式实现 + 面试高频追问
│   ├── exercise.py              ← 练习题（含 TODO 标记）
│   └── test_exercise.py         ← pytest 单元测试
└── cpp/                         ← 对照语言：C++
    ├── bad_xxx.cpp              ← C++ 版反模式
    ├── xxx.h                    ← 模式头文件
    └── xxx.cpp                  ← 演示代码（可编译运行）
```

---

## 如何使用

### 学习路径

```
先修课 → 创建型 → 结构型 → 行为型
 00        01-04     05-07     08-11
```

### 每节课的标准流程

```bash
# 1. 先看反模式，感受痛点
cd 08_strategy/py
cat bad_strategy.py

# 2. 学习模式实现
cat strategy.py

# 3. 做练习（填充 TODO）
#    打开 exercise.py 完成 3 道题

# 4. 运行测试验证
pytest test_exercise.py -v
```

### 运行 Python 代码

```bash
cd 01_singleton/py
python singleton.py      # 运行模式演示
python bad_singleton.py  # 运行反模式
pytest test_exercise.py -v  # 运行练习测试
```

### 编译运行 C++ 代码

```bash
cd 01_singleton/cpp
g++ -std=c++11 -pthread singleton.cpp -o singleton
./singleton
```

---

## 练习题说明

每课的 `exercise.py` 包含 3 道难度递进的题目：

1. **基础** — 实现模式的核心机制
2. **综合** — 在真实场景中应用模式
3. **拓展** — 模式的变体或进阶用法

每道题都有中文 `# TODO` 注释指导思路。完成后用 pytest 验证：

```bash
# 验证所有课的练习
cd 08_strategy/py
pytest test_exercise.py -v

# 预期输出类似：
# test_exercise.py::TestSortStrategy::test_bubble_sort PASSED
# test_exercise.py::TestDiscountStrategy::test_percentage_discount PASSED
# ...
```

---

## 前置要求

- **Python**: 3.6+（需要 `pytest` 库）
- **C++**: 支持 C++11 的编译器（g++ / clang++ / MSVC）
- **pytest**: `pip install pytest`

---

## 面试重点

每个模式的 `.py` 文件末尾都有 **"面试高频追问"** 章节，覆盖该模式在面试中最常见的提问：

- 该模式解决了什么问题？
- 和相似模式有什么区别？（如 Strategy vs State, Decorator vs Proxy）
- Python 和 C++ 的实现差异
- 该模式的缺点和适用场景
- 变种题（面试官会怎么改题）

---

## 参考

- GoF《设计模式：可复用面向对象软件的基础》
- Head First 设计模式（中文版）
- Python 3 官方文档 — `abc` 模块
- C++11 标准 — `static` 局部变量线程安全保证
