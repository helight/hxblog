---
title: tts
weight: 2
prev: /docs/aillm/01cline
next: /docs/aillm/
sidebar:
  open: true
---

## F5-TTS介绍
1. ​特点：基于E2-TTS改进，2秒音频即可复刻音色，推理速度优于阿里CosyVoice，支持多音色克隆和情绪风格调整（如Shouting）。
2. ​部署体验：通过ModelScope可在线测试，本地部署需Hugging Face模型下载，显存占用较低，适合生产环境。
3。 ​适用场景：有声读物、多角色播客。
项目地址：[GitHub](https://github.com/SWivid/F5-TTS)

<!--more-->

## mac 上安装部署
2. Local editable (if also do training, finetuning)
``` sh
git clone https://github.com/SWivid/F5-TTS.git
cd F5-TTS
# git submodule update --init --recursive  # (optional, if need > bigvgan)
pip install -e .
```
## 启动
``` sh
# Launch a Gradio app (web interface)
f5-tts_infer-gradio

# Specify the port/host
f5-tts_infer-gradio --port 7860 --host 0.0.0.0

# Launch a share link
f5-tts_infer-gradio --share
```

我们使用 webui 来启动使用f5-tts，使用"f5-tts_infer-gradio"启动后如下：
``` sh
(base) helightxu•~/F5-TTS(main)» f5-tts_infer-gradio 
The cache for model files in Transformers v4.22.0 has been updated. Migrating your old cache. This is a one-time only operation. You can interrupt this and resume the migration later on by calling `transformers.utils.move_cache()`.
0it [00:00, ?it/s]
Download Vocos from huggingface charactr/vocos-mel-24khz

vocab :  /Users/helightxu/F5-TTS/src/f5_tts/infer/examples/vocab.txt
token :  custom
model :  /Users/helightxu/.cache/huggingface/hub/models--SWivid--F5-TTS/snapshots/84e5a410d9cead4de2f847e7c9369a6440bdfaca/F5TTS_v1_Base/model_1250000.safetensors

/opt/anaconda3/lib/python3.12/site-packages/gradio/components/chatbot.py:282: UserWarning: You have not specified a value for the `type` parameter. Defaulting to the 'tuples' format for chatbot messages, but this is deprecated and will be removed in a future version of Gradio. Please set type='messages' instead, which uses openai-style dictionaries with 'role' and 'content' keys.
  warnings.warn(
Starting app...
* Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
```
启动后界面如下：
![](01f5-tts-imgs/1.png)