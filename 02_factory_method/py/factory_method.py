"""
================================================================================
 Lesson 2: Factory Method — 工厂方法模式（模式实现）
================================================================================
  上节课的 bad_factory_method.py 我们看到了 if-else 创建对象的问题，
  现在来看看设计模式怎么解决。

 📐 设计模式定义：
   工厂方法模式(Factory Method)定义一个创建对象的接口，
   但让子类决定实例化哪个类。工厂方法使一个类的实例化延迟到子类。

 🎯 解决的问题：
   - 对象创建逻辑与使用逻辑耦合（违反单一职责）
   - 新增产品类型需要修改已有代码（违反开闭原则）

 💡 核心思想：
   把"创建对象"这个行为抽象成一个方法，让子类去决定创建什么。
   父类只定义"如何创建"的接口，不关心"创建什么"。

   关键角色：
   1. Product（产品接口）— 定义产品共有的行为
   2. ConcreteProduct（具体产品）— 实现产品接口
   3. Creator（创建者接口）— 声明工厂方法
   4. ConcreteCreator（具体创建者）— 实现工厂方法，创建具体产品
================================================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================================
# 1. 定义产品接口 (Product)
# ============================================================================

class Logger(ABC):
    """
    抽象产品：所有日志类型的共同接口。

    🎯 工厂方法模式的核心就是"依赖抽象，不依赖具体"。
    客户端代码只依赖 Logger 这个抽象接口，
    不管具体是 ConsoleLogger 还是 FileLogger。
    """

    @abstractmethod
    def log(self, message: str):
        """输出日志"""
        pass

    @abstractmethod
    def get_type_name(self) -> str:
        """返回日志类型名称（用于展示）"""
        pass


# ============================================================================
# 2. 具体产品 (ConcreteProduct)
# ============================================================================

class ConsoleLogger(Logger):
    """控制台日志"""

    def log(self, message: str):
        print(f"[控制台 {datetime.now()}] {message}")

    def get_type_name(self) -> str:
        return "控制台"


class FileLogger(Logger):
    """文件日志"""

    def __init__(self):
        self._file = "app.log"
        print("  [FileLogger] 打开文件: app.log")

    def log(self, message: str):
        print(f"[文件 {self._file} {datetime.now()}] {message}")

    def get_type_name(self) -> str:
        return "文件"


class NetworkLogger(Logger):
    """网络日志"""

    def __init__(self):
        self._endpoint = "https://logs.example.com/api"
        self._connection = self._establish_connection()

    def _establish_connection(self):
        """模拟建立网络连接"""
        print(f"  [NetworkLogger] 建立连接到 {self._endpoint}")
        return True

    def log(self, message: str):
        print(f"[网络 {self._endpoint} {datetime.now()}] {message}")

    def get_type_name(self) -> str:
        return "网络"


# ============================================================================
# 3. 创建者接口 / 抽象工厂 (Creator)
# ============================================================================

class LoggerCreator(ABC):
    """
    抽象创建者：定义工厂方法。

    🧠 这就是工厂方法模式的核心——"工厂方法"本身。

    所谓"工厂方法"就是：
      1. 定义一个抽象方法 create_logger() 来创建对象
      2. 子类负责实现这个方法来创建具体的产品
      3. 父类中的其他方法（比如 write_log）使用这个工厂方法
         创建对象，但不知道具体创建的是什么类型

    💡 好处：
      - 客户端代码只依赖 LoggerCreator 和 Logger 这两个抽象
      - 新增一种日志类型 = 新增一个 Creator 子类 + 一个 Product 子类
      - 不需要修改任何已有的代码！
    """

    @abstractmethod
    def create_logger(self) -> Logger:
        """
        工厂方法：子类实现此方法来创建具体的 Logger。

        ⚡ 这就是"工厂方法"的名字来源：
        这个方法本身就是一个"工厂"，专门生产 Logger 对象。
        """
        pass

    def write_log(self, message: str):
        """
        使用工厂方法的业务方法。

        🔑 注意：这个方法并不知道具体使用的是哪种 Logger！
        它只通过抽象接口 Logger 来操作。
        这就是"依赖倒置原则"(Dependency Inversion Principle)的体现：
          高层模块（write_log）不依赖低层模块（具体 Logger），
          两者都依赖抽象（Logger 接口）。
        """
        logger = self.create_logger()  # 调用工厂方法
        print(f"  [LoggerCreator] 使用 {logger.get_type_name()}Logger...")
        logger.log(message)


# ============================================================================
# 4. 具体创建者 (ConcreteCreator)
# ============================================================================
# 每个具体创建者只负责创建一种具体产品。

class ConsoleLoggerCreator(LoggerCreator):
    """具体创建者：负责创建 ConsoleLogger"""

    def create_logger(self) -> Logger:
        return ConsoleLogger()


class FileLoggerCreator(LoggerCreator):
    """具体创建者：负责创建 FileLogger"""

    def create_logger(self) -> Logger:
        return FileLogger()


class NetworkLoggerCreator(LoggerCreator):
    """具体创建者：负责创建 NetworkLogger"""

    def create_logger(self) -> Logger:
        return NetworkLogger()


# ============================================================================
# 5. 客户端代码
# ============================================================================

def test_factory_method():
    print("=" * 60)
    print("✅ 工厂方法模式")
    print("=" * 60)

    # 客户端只需要知道有哪些 Creator，选择需要的即可
    # 不需要知道具体 Logger 的创建细节

    creators = [
        ConsoleLoggerCreator(),
        FileLoggerCreator(),
        NetworkLoggerCreator(),
    ]

    for creator in creators:
        creator.write_log("这是一条测试日志")
        print()

    print("--- 现在想加 DatabaseLogger ---")
    print("   1. 新建 DatabaseLogger 类实现 Logger 接口")
    print("   2. 新建 DatabaseLoggerCreator 类继承 LoggerCreator")
    print("   3. 客户端选择 DatabaseLoggerCreator")
    print("   ✅ 不需要修改任何已有代码！")


# ============================================================================
# 进阶：带参数的工厂方法
# ============================================================================
"""
在实际项目中，工厂方法可能更灵活。例如：

    class ConfigurableFileLoggerCreator(LoggerCreator):
        def __init__(self, file_path: str):
            self._file_path = file_path

        def create_logger(self) -> Logger:
            return FileLogger(self._file_path)  # 传入参数

这样每个 Creator 可以在创建时传入不同的配置参数。
"""


# ============================================================================
# 进阶：Python 风格的工厂方法（鸭子类型）
# ============================================================================
"""
Python 不强制使用 ABC，只要能响应 log() 方法即可（鸭子类型）。

甚至可以用函数代替类来实现工厂方法：

    def create_console_logger() -> Logger:
        return ConsoleLogger()

    def create_file_logger() -> Logger:
        return FileLogger()

    # 用字典代替 if-else
    LOGGER_CREATORS = {
        "console": create_console_logger,
        "file": create_file_logger,
    }

这其实就是"策略模式"(Strategy) + "工厂方法"的组合。
"""


# ============================================================================
# 面试高频追问 🔥
# ============================================================================
"""
Q1: 工厂方法模式和简单工厂模式有什么区别？
A:   - 简单工厂：一个类集中管理所有对象的创建，用 if-else 或 switch 分支
      - 违反开闭原则：加新类型要改工厂类
      - 所有创建逻辑耦合在一起
   - 工厂方法：把创建逻辑延迟到子类
      - 符合开闭原则：加新类型只要加新的子类
      - 每个子类只负责创建一种产品，职责单一
      - 但增加了系统复杂度（需要更多类）

Q2: 工厂方法解决了什么设计原则问题？
A:  主要解决了两个原则：
   1. 开闭原则 (Open-Closed Principle)：
      对扩展开放（可以新增 Creator 子类），
      对修改封闭（不需要修改已有的 Creator 代码）。
   2. 单一职责原则 (Single Responsibility Principle)：
      每个 Creator 子类只负责创建一种产品，职责明确。

Q3: 什么时候用工厂方法？什么时候直接用 new？
A:   用工厂方法：
     - 对象的创建逻辑复杂（需要读配置、查数据库等）
     - 需要根据条件创建不同的具体类型
     - 想把"创建"和"使用"解耦
   直接用 new：
     - 对象很简单，没有变化
     - 不会扩展出多个变体
     - 创建逻辑不会改变

Q4: 工厂方法在 Python 标准库中的应用？
A:   例子很多：
     - collections.defaultdict：传入 factory 参数
     - 各种 classmethod 替代构造函数（如 dict.fromkeys()）
     - Django REST Framework 的 Serializer 创建
     - unittest 的 TestLoader 加载测试用例

Q5: 工厂方法在 C++ 中有什么特别注意的？
A:   C++ 中工厂方法通常返回指针（裸指针或智能指针）。
    由于 C++ 的静态类型系统，工厂方法的返回值类型必须明确。
    推荐使用 unique_ptr 来管理工厂创建的对象生命周期。
    另外，C++ 需要虚析构函数来确保正确释放资源。

💡 面试官变种题：
   如果产品对象需要不同的参数怎么办？
   （例如 FileLogger 需要文件名，NetworkLogger 需要 URL）
   答：可以让工厂方法接收参数，或者让具体 Creator 持有配置。
   更优雅的方式是用 Builder 模式组合工厂方法。
"""
