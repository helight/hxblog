---
title: "OpenClaw Skills 优化实践：用 Progressive Disclosure 原则压缩 AI Agent 的上下文开销"
date: 2026-03-12T08:45:20+08:00
tags: ["AI", "应用"]
categories: ["AI", "应用"]
banner: "/blog/2026/0312-openclaw-skill-optimize/imgs/banner.jpg"
author: "helight"
authorlink: "http://helight.cn"
summary: ""
keywords: ["OpenClaw", "AI Agent", "Skill", "Context Window", "Progressive Disclosure"]
draft: false
---

最近在用 OpenClaw（一款基于 Claude 的 AI Agent 工具）为自己的工作流开发了几个自动化 Skill，跑了一段时间后发现一个问题：随着 Skill 越写越详细，响应质量反而开始下降，有时候 Agent 会忽略某些关键步骤，或者混淆不同 Skill 的指令。

排查一圈后发现根本原因：**SKILL.md 写得太长，把无关细节都塞进了上下文窗口，产生了认知噪音。**

这篇文章记录我把三个 Skill 从"事无巨细"优化为"按需加载"的全过程，以及背后的设计原理。

## 一、OpenClaw Skill 是什么

OpenClaw 的 Skill 系统可以理解为"给 AI Agent 的专项说明书"。每个 Skill 是一个目录，包含：

```
skill-name/
├── SKILL.md          # 核心指令（必须）
├── scripts/          # 可执行脚本
├── references/       # 参考文档（按需加载）
└── assets/           # 模板/图片等资产
```

Agent 在每次对话时，会把所有 Skill 的 **frontmatter**（name + description，约 100 词）常驻在上下文里。当用户的请求命中某个 Skill 时，才加载它的 SKILL.md 正文。`references/` 里的文件则由 Agent 在需要时自行读取，不会自动进入上下文。

这个"三级加载"机制就是 **Progressive Disclosure（渐进式披露）**：

```
Level 1：Metadata（name + description）  → 始终在上下文，~100 词
Level 2：SKILL.md body                   → Skill 触发时加载，建议 <500 行
Level 3：references/ 文件               → Agent 按需读取，无大小限制
```

## 二、问题：Skills 越写越臃肿

我开发的三个主要 Skill：

| Skill | 功能 | 优化前 SKILL.md 行数 |
|-------|------|---------------------|
| `tech-news-fetcher` | 抓取10个 RSS 源生成科技新闻日报 | 76 行 |
| `blog-writer` | 生成 Hugo 博客文章并提交 PR | 120 行 |
| `file-manager` | 分析和整理开发项目文件结构 | **531 行** |

`file-manager` 是重灾区。531 行里混杂着：常见场景举例、最佳实践清单、故障排查手册、高级用法、批量处理脚本……全部堆在 SKILL.md，一旦触发就全部进入上下文。

另外发现几个具体问题：

**1. frontmatter description 信息失真**

`tech-news-fetcher` 的 description 里写着「CSDN」作为新闻源，但早已替换为 IT之家——触发词和实际行为对不上，影响 Agent 的 Skill 选择判断。

**2. 细节与流程混在一起**

`blog-writer` 的 SKILL.md 里，Step 2.5（生成 Banner）这一节嵌入了大段图标映射规则，像这样：

```markdown
- 机器人 → AI / Agent / LLM 主题
- 盾牌 → 安全 / 风险主题
- 放大镜 → 搜索 / 分析主题
- 灯泡 → 创新 / 思考主题
- 齿轮 → 工程 / 架构主题
```

这些细节在每次博客流程中几乎不需要查阅——它们本应是脚本内部逻辑，放进 SKILL.md 只会增加噪音。

**3. 角色定位写死了个人信息**

`blog-writer` 的 description 里硬编码了 "helight"，技术上这个 Skill 若被分享出去，触发逻辑会产生歧义。

## 三、优化原则：只放"不在这里就找不到"的内容

新版 skill-creator 的核心指导思想总结成一句话：

> **Default assumption: Claude is already very smart. Only add context Claude doesn't already have.**

每加一行内容，都要问自己：

- "这件事 Claude 不查这里也知道吗？" → 如果是，删掉
- "这个细节只在特定场景下用到吗？" → 如果是，移到 `references/`
- "这是步骤（How）还是背景（Why/What）？" → 步骤留 SKILL.md，背景移 references

### 三层内容分配原则

```
SKILL.md body（<500行）：
  ✅ 核心工作流（每次执行都要看的步骤）
  ✅ 关键命令（带最常用参数）
  ✅ 安全边界（必须注意的约束）
  ❌ FAQ 和常见问题
  ❌ 常见场景举例
  ❌ 细节参数说明

references/（按需加载）：
  ✅ 参数详细说明
  ✅ 常见场景与最佳实践
  ✅ 故障排查手册
  ✅ 领域模板/规则文档
```

## 四、三个 Skill 的实际改造

### tech-news-fetcher

**改动：**
- description 修正 CSDN → IT之家，补充 Hugo Blog 触发词
- SKILL.md 精简为核心两种用法（Hugo / Obsidian）+ 常用参数表
- FAQ + 反封禁机制细节 → 新建 `references/usage.md`

**结果：** 76 行 → 40 行，↓47%

新版 SKILL.md 的结构清晰多了，核心部分只有两段命令 + 一张参数表：

```markdown
## 主要用法（Hugo Blog 模式）
python3 scripts/fetch_news.py --hugo-blog /projects/hxblog --date 2026-03-10

## Obsidian 模式
python3 scripts/fetch_news.py --output-dir ~/Documents/Obsidian/科技新闻

## Agent 工作流
1. 确认日期和输出模式
2. 执行脚本（约 3~5 分钟）
3. Hugo 模式：验证 build → 创建 PR 分支 → 通知 PR 链接
```

### blog-writer

**改动：**
- description 去掉 "helight" 硬编码 → 通用描述
- Banner 设计规范（图标映射、配色规则）→ 新建 `references/banner-spec.md`
- Step 5 补充 Gitee 同步推送步骤（之前缺失）

**结果：** 120 行 → 60 行，↓50%

### file-manager

这个是改动最大的。531 行包含了大量"万一用户问到"的防御性文档，全部搬出去：

**移出内容：**
- 四个典型场景详解 → `references/scenarios.md`
- 定期维护建议 + 批量处理脚本 → `references/scenarios.md`
- 已知限制说明 → `references/scenarios.md`

**保留内容：**
- 四步工作流表格（一眼看出做什么）
- 每步一条核心命令
- 5 条安全规则
- 4 条故障排查（一行一条）

**结果：** 531 行 → 87 行，↓**84%**

重构后的 `file-manager` SKILL.md 核心部分长这样：

```markdown
## Workflow

| Step | When to use | Script |
|------|-------------|--------|
| 1. Analyze  | 首次/变更前  | file_analyzer.py   |
| 2. Plan     | 预览目标结构 | structure_planner.py |
| 3. Organize | 执行迁移    | file_organizer.py  |
| 4. Clean up | 清理冗余    | cleanup_manager.py |
```

四步、四个脚本、一目了然，细节全在 references 里等着被按需调用。

## 五、总结

这次优化让我重新理解了"给 AI 写文档"和"给人写文档"的本质区别：

**给人写文档**：越全越好，用户可以跳读，信息冗余有益无害。

**给 AI 写文档**：越精越好，上下文窗口是共享资源，每一行都有成本。塞进去的信息不是"备用知识"，而是会参与每次推理的"噪音候选"。

Progressive Disclosure 原则在 AI 场景里格外重要——不是因为 AI 读不懂复杂文档，而是因为**加载了不需要的内容会降低需要的内容的权重**。

三个 Skill 优化后的整体效果：

| Skill | 优化前 | 优化后 | 压缩率 |
|-------|--------|--------|--------|
| tech-news-fetcher | 76 行 | 40 行 | ↓47% |
| blog-writer | 120 行 | 60 行 | ↓50% |
| file-manager | 531 行 | 87 行 | ↓84% |

下一步计划把 references 文件也做结构化索引，让 Agent 能更精准地判断"什么情况下读哪个文件"，进一步减少不必要的文件加载。
