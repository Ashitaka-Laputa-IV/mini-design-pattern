/*
================================================================================
 Lesson 9: Observer — 观察者模式 [行为型] · C++ 反模式
================================================================================
  和 Python 版本一样的场景：天气站系统。

  同事在 WeatherStation 中硬编码了所有面板的更新调用，
  每次新增面板都要改核心代码。

  🧠 在 C++ 中，这种硬编码通知更危险：
    - 编译型语言，改完后需要重新编译整个模块
    - 头文件依赖可能导致级联重新编译
    - 耦合度高导致单元测试困难
================================================================================
*/

#include <iostream>
#include <string>
#include <vector>

// ============================================================================
// 反模式：硬编码通知
// ============================================================================

class CurrentConditionsDisplay {
public:
    void update(double temperature, double humidity, double pressure) {
        std::cout << "  [当前天气] " << temperature << "°C, "
                  << humidity << "%, " << pressure << "hPa\n";
    }
};

class StatsDisplay {
private:
    std::vector<double> temps_;

public:
    void update(double temperature, double humidity, double pressure) {
        temps_.push_back(temperature);
        double sum = 0;
        for (double t : temps_) sum += t;
        double avg = sum / temps_.size();

        double max_temp = temps_[0], min_temp = temps_[0];
        for (double t : temps_) {
            if (t > max_temp) max_temp = t;
            if (t < min_temp) min_temp = t;
        }

        std::cout << "  [统计面板] 最高=" << max_temp << "°C, "
                  << "最低=" << min_temp << "°C, "
                  << "平均=" << avg << "°C (" << temps_.size() << " 次采样)\n";
    }
};

class ForecastDisplay {
private:
    double lastPressure_ = 0.0;

public:
    void update(double temperature, double humidity, double pressure) {
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

class WeatherStation {
    /*
     * ❌ 反模式：硬编码通知
     *
     * 问题分析：
     *   1. WeatherStation 直接依赖三个具体面板类
     *   2. 新增面板必须修改 setMeasurements 方法
     *   3. 删除面板也必须修改 WeatherStation
     *   4. 无法运行时动态增减面板
     */
private:
    double temperature_;
    double humidity_;
    double pressure_;

    // 硬编码的面板对象
    CurrentConditionsDisplay currentDisplay_;
    StatsDisplay statsDisplay_;
    ForecastDisplay forecastDisplay_;

public:
    WeatherStation() : temperature_(0.0), humidity_(0.0), pressure_(0.0) {}

    void setMeasurements(double temperature, double humidity, double pressure) {
        temperature_ = temperature;
        humidity_ = humidity;
        pressure_ = pressure;

        std::cout << "\n  [WeatherStation] 新数据: "
                  << temperature << "°C, " << humidity << "%, " << pressure << "hPa\n";
        std::cout << "  [通知] 开始通知所有面板...\n";

        // ❌ 硬编码的通知列表——每加一个面板就要改这里！
        currentDisplay_.update(temperature, humidity, pressure);
        statsDisplay_.update(temperature, humidity, pressure);
        forecastDisplay_.update(temperature, humidity, pressure);
        // 如果加一个 AirQualityDisplay:
        // airQualityDisplay_.update(temperature, humidity, pressure);

        std::cout << "  [通知] 所有面板通知完毕\n";
    }
};

int main() {
    std::cout << "====== C++ 反模式：硬编码通知 天气站系统 ======\n\n";

    WeatherStation station;
    station.setMeasurements(25.0, 65, 1012);
    station.setMeasurements(26.5, 70, 1008);
    station.setMeasurements(24.0, 80, 1005);

    std::cout << "\n🤔 思考：如果新增'空气质量面板'，\n"
              << "   你需要修改 WeatherStation 的三个地方：\n"
              << "     1. 包含新面板的头文件\n"
              << "     2. 声明新面板的成员变量\n"
              << "     3. 在 setMeasurements 中添加 update 调用\n"
              << "   每次改动都可能导致编译级联和潜在 bug。\n";

    return 0;
}
