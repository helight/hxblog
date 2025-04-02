---
title: esp32做一个声音播放器
weight: 9
prev: /docs/esp32-microPython/02Esp32DevKit32E
next: /docs/esp32-microPython/
sidebar:
  open: true
---

## 硬件连接
草稿中。
​ESP32与MAX98357接线​（参考）：

| ​ESP32引脚 | ​MAX98357引脚 |​​功能 |
| ------  | ----------- | ----------- |
|​GPIO15	|​BCLK	|​位时钟|​
|​GPIO16	|​LRCLK	|​左/右声道时钟|​
|​GPIO7	|​DIN	|​数字音频输入|​
|​3.3V	|​VIN	|​电源输入|​
|​GND	|​GND|​	接地|​

​音频输出：`MAX98357` 的 `Audio+` 和 `Audio-` 接喇叭正负极（需根据模块标识确认）。

1. ​环境配置

安装 ​MicroPython固件 到ESP32。
通过 upip 安装音频解码库（如 micropython-mp3）：
```python
import upip
upip.install('micropython-mp3')
```
2. ​I2S初始化
``` python
from machine import I2S, Pin
import audioio
import ulab as np

# 配置I2S输出（参考[1,2](@ref)）
i2s = I2S(
    mode=I2S.STEREO,          # 立体声模式
    sck=15,                  # BCLK引脚
    ws=16,                  # LRCLK引脚
    sd=7,                   # DIN引脚
    rate=48000,             # 采样率（需与MP3文件匹配）
    bits=16,                # 位深
    format=I2S.MSB,         # 数据格式
    channels=2              # 双声道
)

# 初始化音频输出
dac = audioio.AudioOut(i2s)
```

3. WAV格式：使用 ulab 库直接处理WAV文件（无需解码）：

``` python
import ulab as np
with open("test.wav", "rb") as f:
    wav = np.frombuffer(f.read(), dtype=np.int16)
    dac.write(wav.tobytes())
```

调试建议

​验证I2S通信：
```python
while True:
    dac.write(b'\x00' * 1024)  # 播放静音测试
    print("I2S输出正常")
```
​检查内存使用：
```python
import gc
print(gc.mem_free())  # 确保剩余内存>100KB
```