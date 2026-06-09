/*
================================================================================
 Lesson 9: Observer — 观察者模式 · C++ 演示代码
================================================================================
  compile & run:
    g++ -std=c++11 -pthread observer.cpp -o observer
    ./observer
================================================================================
*/

#include "observer.h"

int main() {
    std::cout << "====== C++ 观察者模式演示 ======\n\n";

    // ---- 1. 经典观察者模式 ----
    std::cout << "--- 1. 经典观察者模式 ---\n";

    WeatherData weatherData;

    CurrentConditionsDisplay current;
    StatsDisplay stats;
    ForecastDisplay forecast;

    // 注册观察者
    weatherData.registerObserver(&current);
    weatherData.registerObserver(&stats);
    weatherData.registerObserver(&forecast);

    // 模拟数据更新
    weatherData.setMeasurements(25.0, 65, 1012);
    weatherData.setMeasurements(26.5, 70, 1008);
    weatherData.setMeasurements(24.0, 80, 1005);

    // ---- 2. 动态注册/注销 ----
    std::cout << "\n--- 2. 动态注册/注销演示 ---\n";

    weatherData.removeObserver(&forecast);   // 关闭预报面板
    weatherData.setMeasurements(22.0, 60, 1018);  // 只有 current 和 stats 收到

    weatherData.registerObserver(&forecast);  // 重新开启
    weatherData.setMeasurements(28.0, 55, 1010);  // 三个面板都收到

    // ---- 3. std::function 回调方式 ----
    std::cout << "\n--- 3. std::function 回调方式 ---\n";

    CallbackWeatherData cbWeather;

    // 用 lambda 作为观察者
    cbWeather.registerCallback([](double t, double h, double p) {
        std::cout << "  [lambda面板] 温度=" << t << "°C\n";
    });

    cbWeather.registerCallback([](double t, double h, double p) {
        std::cout << "  [lambda面板] 湿度=" << h << "%"
                  << (h > 75 ? " 偏高" : " 正常") << "\n";
    });

    cbWeather.setMeasurements(28.0, 80, 1015);

    /*
     * 💡 C++ vs Python 观察者模式对比：
     *
     *   Python:
     *     - 鸭子类型，观察者不需要继承接口
     *     - __call__ 或直接传函数/lambda
     *     - 不需要手动管理生命周期（GC 自动处理）
     *     - 弱引用（weakref）可解决内存泄漏
     *
     *   C++:
     *     - 传统方式用虚函数 + 继承（类型安全）
     *     - C++11 后也可以用 std::function + lambda
     *     - 必须手动管理观察者生命周期（谁负责 delete?）
     *     - 多线程安全需要显式加锁
     *     - 迭代器失效问题需要小心处理
     */

    return 0;
}
