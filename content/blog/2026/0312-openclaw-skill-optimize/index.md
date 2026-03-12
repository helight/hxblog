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

### 4.1 tech-news-fetcher

#### 问题分析

这个 Skill 的问题看起来不大，但实际上有两处隐性错误会悄悄影响 Agent 的判断质量。

**第一个问题：description 信息过期。** 原版 description 里明确列出了10个新闻源，其中包括「CSDN」。但在开发早期，CSDN 的 RSS 接口返回 HTTP 401，已经替换为「IT之家」。description 是 Agent 判断"这个 Skill 能干什么"的唯一依据——如果 description 和实际行为不一致，Agent 在推理时会产生一个微妙的认知偏差：它以为自己会抓 CSDN，结果没有，但又不知道原因。

更深层的问题是：description 里把10个来源全部罗列出来，显得像是一份"功能清单"而非"触发说明"。触发一个 Skill 的关键信息应该是**什么场景下用它**，而不是它内部包含哪些资源。

**第二个问题：主要用法没有体现在 SKILL.md 里。** 随着使用深入，Hugo Blog 模式已经成为主要用途（直接生成博客内容并提交 PR），但原版 SKILL.md 只写了 Obsidian 模式。Agent 每次执行时，要么需要用户额外说明，要么凭"记忆"推断——这两种情况都不可靠。

#### 改造内容

- description 删掉来源清单，改为场景触发词为主，并加入"生成今日新闻博客"这类 Hugo 触发词
- SKILL.md 重构为"Hugo 模式优先，Obsidian 模式次之"，主用法第一眼就能看到
- FAQ（某些源抓不到怎么办、图片慢怎么办）和反封禁机制细节（UA 轮换逻辑、请求间隔参数）→ 新建 `references/usage.md`，这些是偶发场景才需要查的内容

```markdown
## 主要用法（Hugo Blog 模式）
python3 scripts/fetch_news.py --hugo-blog /projects/hxblog --date 2026-03-10

## Obsidian 模式
python3 scripts/fetch_news.py --output-dir ~/Documents/Obsidian/科技新闻
```

**结果：** 76 行 → 40 行，↓47%。更重要的是，description 和实际行为重新对齐，Agent 的 Skill 选择判断准确率会提升。

---

### 4.2 blog-writer

#### 问题分析

`blog-writer` 的问题集中在两个层面：**信息结构错位**和**可复用性缺陷**。

**第一个问题：步骤中嵌入了规格说明。** Step 2.5（生成 Banner）这一步写成这样：

```markdown
**Banner 设计规范（312×240）：**
- 手绘 sketch 风，米白底，炭笔线条
- 左侧：标题 + 副标题 + 关键词彩色胶囊
- 右侧：1~2 个手绘卡通图标（自动根据关键词选取）
  - 机器人 → AI / Agent / LLM 主题
  - 盾牌 → 安全 / 风险主题
  - 放大镜 → 搜索 / 分析主题
  - 灯泡 → 创新 / 思考主题
  - 齿轮 → 工程 / 架构主题
- 多留白，不堆砌元素
```

这段内容的性质是**脚本规格说明**，描述的是 `gen_banner.py` 的内部设计逻辑，而不是"怎么执行这一步"的操作指令。Agent 每次执行博客生成流程，都会把这段塞进上下文——但实际上，除非用户要求定制 banner 风格，否则这段内容从来不会被用到。**每次白白占用几十个 token，换来的是零收益。**

**第二个问题：description 里硬编码了个人信息。** 原版 description 写的是"帮助 helight 写技术博客文章"。这在功能上没问题，但一旦把这个 Skill 分享给其他人，触发逻辑就会歧义：Agent 会认为这个 Skill 是专属于 helight 的，在其他用户的语境下可能不触发，或者触发后产生奇怪的行为（比如在文章里自动填写 helight 的信息）。好的 Skill 应该在 description 里描述**任务类型**，不应该绑定具体的使用者身份。

**第三个问题：流程有缺漏。** PR merge 后需要同步推送到 Gitee，但原版 Step 5 没有这一步。这不是"细节问题"，而是实际执行时每次都要额外补一条命令——说明 SKILL.md 的工作流描述与实际操作存在断层。

#### 改造内容

- description 改为通用表述："帮助写技术博客文章并提交到 Hugo 博客仓库"，去掉 "helight" 的绑定
- Banner 规格说明（尺寸、图标映射、配色逻辑）→ 新建 `references/banner-spec.md`；Step 2.5 只保留执行命令
- Step 5 补充 `git push gitee main`，流程与实际操作完全对齐

**结果：** 120 行 → 60 行，↓50%。更重要的是，Skill 的可复用性提升，流程不再有缺漏。

---

### 4.3 file-manager

#### 问题分析

这是三个 Skill 里问题最严重的，也是最典型的反面教材——**把 Skill 写成了用户手册**。

531 行的 SKILL.md 包含了：
- 四步工作流（这是必要的）
- 每步详细说明，包括"What it does"逐条列举（大量冗余）
- 四个典型使用场景，每个场景都展开成完整的操作步骤（典型的防御性写作）
- 最佳实践清单：DO / DON'T 各5条（这是给人读的）
- 故障排查：4类问题 × 详细解决方案（偶发场景，不该常驻上下文）
- 高级用法：自定义配置、批量处理脚本（极低频需求）
- 限制说明：6条已知局限（这是写给读者看的，不是 Agent 执行时需要的）

**根本问题是：写这个 Skill 的时候，假设的受众是"人类用户在读文档"，而不是"AI Agent 在执行任务"。** 两者的信息需求截然不同：

- 人类读文档：需要背景、需要 Why、需要举例、需要边界说明，越完整越好
- AI Agent 执行任务：只需要 How、只需要当前步骤、需要约束条件，越精简越好

防御性写法（"万一用户问到场景X，这里有答案"）在人类文档里是美德，在 AI Skill 里是负担——因为 Agent 在处理 `file-manager` 相关请求时，会把全部 531 行一次性加载进上下文，不管当前任务用不用得到场景X的内容。

以"最佳实践"这节为例，原版是这样的：

```markdown
- ✅ DO: Always use dry-run first
- ✅ DO: Create backups before major changes
- ✅ DO: Commit to Git before reorganizing
- ✅ DO: Review reports before executing
- ✅ DO: Test project functionality after changes
- ❌ DON'T: Skip dry-run mode
- ❌ DON'T: Delete backups immediately
...
```

这10条里，有效信息只有两条核心约束（先 dry-run、先备份），其余都是这两条的变体或推论。Agent 其实完全能从"先 dry-run、先备份"推导出后面8条——重复写出来只是在消耗上下文配额。

#### 改造内容

**核心原则：每一行 SKILL.md 都必须是"执行时必看"的内容。**

移出到 `references/scenarios.md`：
- 四个典型场景的详细操作步骤（按需查阅，不是每次都需要）
- 定期维护建议（属于最佳实践，不是执行指令）
- 批量处理多个项目的脚本（高级用法，极低频）
- 已知限制说明（背景信息，不影响执行）

保留在 SKILL.md：
- 四步工作流表格（执行时必看，决策入口）
- 每步一条核心命令（执行时必须知道）
- 5 条安全规则（执行时必须遵守的约束）
- 4 条故障排查（一行一条，精简到只有原因+解法）

重构后核心部分：

```markdown
## Workflow

| Step | When to use          | Script               |
|------|---------------------|----------------------|
| 1. Analyze  | 首次/变更前  | file_analyzer.py     |
| 2. Plan     | 预览目标结构 | structure_planner.py |
| 3. Organize | 执行迁移     | file_organizer.py    |
| 4. Clean up | 清理冗余     | cleanup_manager.py   |
```

四步、四个脚本、决策标准，一目了然。需要了解某步骤的典型场景？读 `references/scenarios.md`。需要知道清理规则的细节？读 `references/cleanup_rules.md`。这些文件只在真正需要时才被加载。

**结果：** 531 行 → 87 行，↓**84%**。上下文开销减少了五分之四，而实际执行能力没有任何损失——因为所有细节都在 references 里待命。

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
