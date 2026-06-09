/*
================================================================================
 Lesson 9: Observer — 观察者模式 [行为型] · C++ 实现
================================================================================
  C++ 观察者模式实现要点：
    1. 抽象基类定义 Observer 和 Subject 接口
    2. 使用 std::vector 存储观察者列表
    3. 主题通过虚函数多态通知所有观察者
    4. ⚠ 线程安全：多线程环境下需要加锁

  🔑 面试要点：
    - 虚析构函数的重要性（基类指针删除派生类对象）
    - 遍历观察者列表时删除观察者的问题（迭代器失效）
    - 线程安全的通知机制
================================================================================
*/

#ifndef OBSERVER_H
#define OBSERVER_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <mutex>
#include <memory>

// ============================================================================
// 观察者接口
// ============================================================================

class Observer {
    /*
     * 👁 观察者接口
     *
     * 所有观察者必须继承此类并实现 update()。
     * 注意：基类需要虚析构函数！
     */
public:
    virtual ~Observer() = default;

    // 观察者接收主题推送的数据（Push 模式）
    virtual void update(double temperature, double humidity, double pressure) = 0;

    // 可选的标识（方便调试）
    virtual std::string name() const {
        return "Observer";
    }
};

// ============================================================================
// 主题接口
// ============================================================================

class Subject {
public:
    virtual ~Subject() = default;

    virtual void registerObserver(Observer* observer) = 0;
    virtual void removeObserver(Observer* observer) = 0;
    virtual void notifyObservers() = 0;
};

// ============================================================================
// 具体主题：天气数据（带线程安全）
// ============================================================================

class WeatherData : public Subject {
    /*
     * ☀️ 具体主题：天气数据
     *
     * ⚠ 线程安全：
     *   使用 std::mutex 保护观察者列表的操作。
     *   notifyObservers 时也加锁，防止在通知过程中列表被修改。
     *
     * 面试题：为什么要在通知时也加锁？
     *   → 如果线程 A 正在通知观察者，线程 B 同时注册/注销观察者，
     *     可能导致迭代器失效或通知遗漏。
     */
private:
    std::vector<Observer*> observers_;  // 观察者列表（裸指针，不拥有对象）
    double temperature_ = 0.0;
    double humidity_ = 0.0;
    double pressure_ = 0.0;
    mutable std::mutex mutex_;  // 互斥锁（mutable 允许在 const 方法中加锁）

public:
    void registerObserver(Observer* observer) override {
        /*
         * 注册观察者。
         * 注意：使用裸指针，不管理观察者的生命周期。
         * 观察者由外部创建和管理。
         */
        std::lock_guard<std::mutex> lock(mutex_);
        if (std::find(observers_.begin(), observers_.end(), observer) == observers_.end()) {
            observers_.push_back(observer);
            std::cout << "  [注册] " << observer->name() << " 已加入订阅\n";
        }
    }

    void removeObserver(Observer* observer) override {
        /*
         * 注销观察者。
         *
         * 面试题：如果在 notifyObservers 过程中调用了 removeObserver 怎么办？
         *   → 一个解决方案是：先拷贝观察者列表，在拷贝上通知
         *   → 另一个方案：标记为"待删除"，通知结束后再统一删除
         */
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = std::find(observers_.begin(), observers_.end(), observer);
        if (it != observers_.end()) {
            observers_.erase(it);
            std::cout << "  [注销] " << observer->name() << " 已取消订阅\n";
        }
    }

    void notifyObservers() override {
        /*
         * 通知所有观察者（Push 方式）。
         *
         * 这里在锁的保护下遍历观察者列表。
         * 实际项目中可能会先拷贝列表再遍历，以减少锁的持有时间。
         */
        std::lock_guard<std::mutex> lock(mutex_);
        std::cout << "  [通知] 向 " << observers_.size() << " 个观察者推送数据...\n";
        for (Observer* observer : observers_) {
            observer->update(temperature_, humidity_, pressure_);
        }
    }

    void setMeasurements(double temperature, double humidity, double pressure) {
        /*
         * 设置新数据并自动通知所有观察者。
         */
        temperature_ = temperature;
        humidity_ = humidity;
        pressure_ = pressure;

        std::cout << "\n  [WeatherData] 新测量值: "
                  << temperature << "°C, " << humidity << "%, " << pressure << "hPa\n";
        notifyObservers();
    }
};

// ============================================================================
// 具体观察者
// ============================================================================

class CurrentConditionsDisplay : public Observer {
public:
    std::string name() const override {
        return "CurrentConditionsDisplay";
    }

    void update(double temperature, double humidity, double pressure) override {
        std::cout << "  [当前天气] " << temperature << "°C, "
                  << humidity << "%, " << pressure << "hPa\n";
    }
};

class StatsDisplay : public Observer {
private:
    std::vector<double> temperatures_;

public:
    std::string name() const override {
        return "StatsDisplay";
    }

    void update(double temperature, double humidity, double pressure) override {
        temperatures_.push_back(temperature);

        double sum = 0;
        for (double t : temperatures_) sum += t;
        double avg = sum / temperatures_.size();

        double max_temp = temperatures_[0];
        double min_temp = temperatures_[0];
        for (double t : temperatures_) {
            if (t > max_temp) max_temp = t;
            if (t < min_temp) min_temp = t;
        }

        std::cout << "  [统计面板] 最高=" << max_temp << "°C, "
                  << "最低=" << min_temp << "°C, "
                  << "平均=" << avg << "°C ("
                  << temperatures_.size() << " 次采样)\n";
    }
};

class ForecastDisplay : public Observer {
private:
    double lastPressure_ = 0.0;

public:
    std::string name() const override {
        return "ForecastDisplay";
    }

    void update(double temperature, double humidity, double pressure) override {
        std::string forecast;
        if (lastPressure_ == 0.0) {
            forecast = "数据不足，无法预报";
        } else if (pressure > lastPressure_) {
            forecast = "天气转好";
        } else if (pressure < lastPressure_) {
            forecast = "注意：可能有雨";
        } else {
            forecast = "天气稳定";
        }
        lastPressure_ = pressure;
        std::cout << "  [预报面板] " << forecast << "\n";
    }
};

// ============================================================================
// C++11 进阶：使用 std::function 实现轻量级观察者
// ============================================================================

/*
 * 类似 Python 的 Callable 方式，C++ 可以用 std::function 实现轻量级观察者。
 * 观察者可以是 lambda、函数指针、或 std::function 对象。
 */

#include <functional>

class CallbackWeatherData {
private:
    std::vector<std::function<void(double, double, double)>> callbacks_;
    double temperature_ = 0.0;
    double humidity_ = 0.0;
    double pressure_ = 0.0;
    mutable std::mutex mutex_;

public:
    void registerCallback(std::function<void(double, double, double)> callback) {
        std::lock_guard<std::mutex> lock(mutex_);
        callbacks_.push_back(std::move(callback));
    }

    void setMeasurements(double temperature, double humidity, double pressure) {
        temperature_ = temperature;
        humidity_ = humidity;
        pressure_ = pressure;

        std::cout << "\n  [CallbackWeatherData] 新数据: "
                  << temperature << "°C, " << humidity << "%, " << pressure << "hPa\n";

        std::lock_guard<std::mutex> lock(mutex_);
        for (const auto& cb : callbacks_) {
            cb(temperature_, humidity_, pressure_);
        }
    }
};

#endif // OBSERVER_H
