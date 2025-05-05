---
title: 让 Qwen3-32B 模型来生成：esp32+oled 天气时钟
weight: 11
prev: /docs/esp32-microPython/10ws2812
next: /docs/esp32-microPython/
sidebar:
  open: true
---

## 一、背景介绍
今天的目的是让 Qwen3-32B 本地模型来生成一个 esp32 的小项目，前天看到 Qwen3 的发布，能力提升非常大，所以也在本地使用了一下这个模型。

这里使用一个比较小的项目来测试验证：在前面我也有一个[esp32+oled 天气时钟](/docs/esp32-microPython/08weatheroled)，这个是我自己参考网上项目来实现的，花费了不少时间，今天我就想是不是可以使用大模型来辅助，看能不能加快实现过程。

## 二、大模型环境
使用了 lm-studio，下载模型是：lmstudio-community/Qwen3-32B-GGUF/Qwen3-32B-Q4_K_M.gguf，模型大小：19.76 GB。

## 三、硬件测试环境
### 1. 软硬件系统
1. thonny软件
2. ESP32开发板
3. 0.96寸OLED显示屏12864屏模块带矩阵4个按键接口 键盘IIC SSD1306。

### 2. 实验接线：
硬件连接参考[OLED显示屏12864屏IIC SSD1306使用](../04oled1306)。

## 四、大模型提示词
我是用的提示词如下：
```
使用 esp32+0.96寸OLED显示屏，开发一个天气时钟，使用 python 开发，天气获取和时间获取显示要分成 2 个线程进行。
```

## 五、大模型思考过程
```
Thoughts: Thought for 58.97 seconds

好的，用户现在想要在ESP32上用MicroPython开发一个天气时钟，并且要求将天气获取和时间获取显示分成两个线程处理。之前已经帮助他开发了基于电子墨水屏的日历和OLED的天气时钟，现在需要进一步优化结构为多线程。

首先，用户提到要使用线程，但MicroPython的threading模块功能有限，特别是在ESP32上可能存在的限制需要注意。例如，由于ESP32的硬件资源有限，创建多个线程可能会遇到内存或调度问题。此外，MicroPython的GIL（全局解释器锁）可能影响多线程的并行执行效果。

接下来需要考虑如何将天气获取和时间显示分离到两个任务中，并确保它们能够并发运行。可能使用MicroPython中的_thread模块来实现低级线程，但需要注意同步问题和资源共享。例如，OLED屏幕作为共享资源，需要防止多个线程同时写入导致冲突。

另外，用户之前已经实现了定时刷新天气和时间的逻辑，现在改为多线程后，可能需要调整计时器或循环结构。比如一个线程负责每分钟更新时间显示，另一个线程负责每隔一定时间获取天气数据，并将结果保存到共享变量中供时间线程使用。

同时还需要处理可能出现的问题，例如线程安全、资源竞争等。可以使用锁机制来保护对OLED屏幕的访问和共享数据结构的操作。此外，需要确保两个任务之间的协作不会导致程序崩溃或显示异常。

另外，用户可能希望代码结构更清晰，模块化程度更高，所以需要将不同功能分解到不同的函数中，并在多线程环境下正确调用它们。例如，一个线程循环获取天气数据并存储结果，另一个线程不断检查当前时间和天气数据，更新屏幕显示。

最后，测试和调试也是关键步骤。由于涉及并发操作，可能出现难以复现的竞态条件或死锁问题，需要仔细验证代码逻辑是否正确处理了这些情况。
```

## 六、大模型输出

### 1. 设计思路
1. 线程 1：时间更新线程
    1. 负责每秒/分钟更新当前时间和显示到 OLED。

2. 线程 2：天气获取线程
    1. 每隔一定时间（如 5 分钟）调用 API 获取天气信息，并将结果写入共享内存。

3. 资源共享管理
    1. 使用 thread.allocate_lock() 管理对 OLED 的访问，避免并发冲突。
    2. 共享变量存储天气数据，供两个线程使用。

### 2. 开发步骤
1. 初始化硬件和网络
``` python
import network, ntptime, time
from machine import I2C, Pin
import ssd1306

# Wi-Fi 连接
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect("WiFi名称", "WiFi密码")
        while not wlan.isconnected():
            pass
    print("Connected:", wlan.ifconfig())

# 初始化 OLED 屏幕 (I2C 默认地址 0x3c)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # 根据你的引脚定义修改
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 同步时间（UTC）
connect_wifi()
ntptime.settime()  # 同步 UTC 时间

```
2. 多线程逻辑分离

线程共享状态（全局变量 + 锁）
``` python
from _thread import allocate_lock, start_new_thread
import urequests, ujson

# 共享变量：存储天气数据
weather_data = {"temp": None, "description": "Updating..."}
weather_lock = allocate_lock()  # 控制对共享变量的访问

# OLED 显示锁（防止两个线程同时更新）
oled_lock = allocate_lock()

```
线程 A：每分钟更新一次当前时间显示
``` python
fdef update_time_display():
    while True:
        with oled_lock:  # 加锁确保只一个线程写 OLED
            oled.fill(0)
            
            # 获取本地时间 (UTC+8)
            _, month, day, _, hour, minute, second, _ = time.localtime(time.time() + 8 * 3600)
            current_time = f"{hour:02d}:{minute:02d}"
            oled.text(current_time, 45, 10)

            # 显示天气信息（从共享变量中读取）
            with weather_lock:
                temp_text = "N/A" if weather_data["temp"] is None else f"{weather_data['temp']} C"
                desc_text = weather_data["description"]
            oled.text(f"Temp: {temp_text}", 0, 40)
            oled.text(desc_text, 0, 55)
            
            oled.show()

        time.sleep(1)  # 每秒更新一次
```
线程 B：每分钟调用 API 更新天气信息
``` python
def fetch_weather():
    api_key = "你的OpenWeatherMapAPIKey"
    city_id = 1816670  # 替换为城市 ID

    while True:
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"

        try:
            with weather_lock:  # 加锁确保共享变量操作安全
                response = urequests.get(url)
                data = ujson.loads(response.text)
                
                temperature = round(data["main"]["temp"] - 273.15, 1)
                description = data["weather"][0]["description"].title()
                weather_data["temp"] = temperature
                weather_data["description"] = description
        except Exception as e:
            print("Fetch error:", e)

        time.sleep(60)  # 每分钟更新一次天气

```
3. 启动两个线程（主程序入口）
``` python
if __name__ == "__main__":
    start_new_thread(update_time_display, ())  # 线程 A：时间显示主线程
    fetch_weather()                            # 主线程运行 B：天气获取

    while True:
        time.sleep(1)  # 防止主进程退出，让子线程持续执行

```

### 3. 调试与注意事项
线程安全建议
1. 所有对 OLED 屏幕和共享变量的访问必须使用锁（oled_lock, weather_lock）。
2. 两个线程间的数据流向：
    1. 天气线程 → 共享数据 → 时间线程 → OLED 显示。

限制与建议
| 项目	| 建议 |
| --- | --- |
|硬件资源	|ESP32 内存有限，避免创建太多线程或使用大变量。|
|API 频率	|OpenWeatherMap 免费版每分钟最多调用 60 次，建议设置 sleep(30) 至少。|
|OLED 显示刷新率 | 不要过于频繁更新（如每秒刷新），可降低为每分钟一次。|

### 4. 最终效果
1. 线程 A：持续在屏幕上显示当前时间。
2. 线程 B：定期从 OpenWeatherMap API 获取天气数据，并写入共享变量中。
3. 两个任务并发运行，互不干扰。

如果需要进一步扩展（如添加图标、报警闹钟等），可以基于此多线程结构进行功能模块化。

## 七、总结

从整体的实现思路、实现过程和最终给出的代码来看，质量还是非常不错的，不过我没有集成测试，看代码还是可以的。

首先实现思路是没有大问题的，要考虑的线程安全等问题都考虑的还是比较好的，这些问题，在我之前写的测试程序中都没有考虑到位的，但是他这里考虑的还是比较全面的。

实现的代码逻辑上来看也没有什么问题。思考+实现输出大概不到 2 分钟。还是非常给力的。

后面开发这类简单项目，大模型的服务能力应该是非常有帮助的。