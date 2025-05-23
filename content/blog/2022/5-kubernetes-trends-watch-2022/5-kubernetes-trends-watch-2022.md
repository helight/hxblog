---
title: "2022 年 kubernetes 的 5 个发展趋势"
date: 2022-03-01T08:45:20+08:00
tags: ["云原生"]
categories: ["云原生", "微服务"]
banner: "/images/banners/kubernetes.jpeg"
author: "helight"
authorlink: "http://helight.cn"
summary: ""
keywords: ["云原生", "微服务", "DevOps"]
draft: false
---

本文译自 [5 Kubernetes trends to watch in 2022](https://enterprisersproject.com/article/2022/1/5-kubernetes-trends-watch-2022)。
作者：[Kevin Casey](https://twitter.com/kevinrcasey)，
译者：[helight](http://helight.cn/)。

原文地址：https://enterprisersproject.com/article/2022/1/5-kubernetes-trends-watch-2022

## 前言

随着企业云基础设施的不断发展，Kubernetes 的使用量也有望继续增长。从基本采用到安全使用，这里有 5 个方面需要关注。

Kubernetes 还在继续发展 - 这是针对所有使用 Kubernetes 的团队都是一样的。

这些早期的采用的同学现在正在在他们自己的领域中，基于积累的经验和云原生生态系统的增长，以新的方式来扩展 Kubernetes 的核心能力。

Liberty Mutual 的高级架构师 Eric ​​Drobisewski 这样说到：“我们会继续把 Kubernetes 用在我们业务所需要解决混合云，多云场景中。就如和我们看到的一样，Kubernetes 提供的申明式 API 和强循环调度对于我们建立统一的无论是私有云还是公有云环境下的资产管理都非常关键，对我们持续实现如何定义，管理和安全管理数字资产非常重要。”

100 强公广泛司在混合云和多云基础设施上加速使用 Kubernetes 作为他们的平台了，这样是反应 Kubernetes 在产业界的使用影响力趋势之一。

## Kubernetes 发展的 5 个关键趋势

另外一个大的趋势：大量的公司才正在开始使用 Kubernetes。并且在他们上云之路的任何阶段，学多的 IT 负责人希望在生产中运行更多的容器化应用 - 使用 Kubernetes 是他们最普遍的做法。 

“Gartner 预测，到 2022年，超过 75% 的全球组织会在他们的生产中运行容器化的应用，而这一数据在 2020 年才不到 30%。” Red Hat 的高级执行产品  Brian Gracely 说。

这和 Red Hat 2021 年企业开源状态报告一致，72% 的 IT 负责人说他们预期在他们的组织中容器使用会增加。他们几乎普遍都认为（85%）Kubernetes 是云原生中的关键。

这对 Kubernetes 的能力，使用场景，使用技巧和其他领域都产生了连续的影响。

伴随着其他新技术的发展，Kubernetes 在技术和学习曲线尚都逐步成熟。

考虑到这些，在新年伊始，这里总结了了 Kubernetes 发展的 5 个关键趋势。

## 1. Kubernetes 成为所有服务的平台？
Kubernetes 和容器是分不开的。这点不会改变，至少不会在 2022 年出现。在 2022 年和未来会继续发展的是基于 Kubernetes 的平台的管理应用的类型。

在早期，用户都是自己在机器上构建 Kubernetes 平台，并且只是部署简单的一组应用，但是现在 Kubernetes 已经很稳定了，使用模式也显著的成熟了。

多数早期应用在 Kubernetes 上是以无状态的方式运行的，曾经 Kubernetes 被看作是对状态服务是不适合的，但是现在已经不成问题了。

当我们已经看到很多各种各样的应用使用容器运行，我们开始看到越来越多的组织也把他们的关键能力和状态应用放到了 Kubernetes 上。数据库，事件驱动消息和关键任务应用都希望可以迁移到 Kubernetes 上，来使用 Kubernetes 上的优势：扩展性，安全和便于迁移。

同样，Kubernetes 主要更多的还是仅仅作为一个容器编排工具，到目前为止还是这样的，但是 Kubernetes 的控制面已经变成一个多云和混合云操作的通用骨架。

Kubernetes 提供了超过容器编排的能力，如声明式 API，控制循环和强壮的基于角色的访问控制（RBAC），来满足多数组织对多云，混合云的需求。这种进化将会围绕控制面，通过扩展 Kubernetes API 系统来对任何资源或基础设施进行定义，管理，生命周期和安全防护，即便是这些资源和基础设施没有原生的链接到 Kubernetes 的运行中。

数据库，时间驱动消息和关键任务应用程序都期望能迁移到 Kubernetes 上，可以利用 Kubernetes 的伸缩性，安全性和可移植能力。同时也期望更多有经验的团队可以使用新的方式 包括使用 Kubernetes Operators，继续发展 Kubernetes 的成熟应用能力。

各种组织在他们 DevOps 应用过程的下一个环节就是使用 Kubernetes operator 框架。我们将会看到许多自服务的能力扩展，都会基于 Kubernetes 来构建，这些能扩展能力从基本的自动管理和生命周期管理发展到了全面自动管理模式，使用更底层的数据驱动来发展自动推荐和自我修复能力，让他们管理的服务可以动态的适应 workload 的要求。

## 2. Kubernetes 和 AI/ML 成为了明星组合
Kubernetes 的成熟和处理不断增加的复杂场景能力可能是它在 AI 和机器学习上的最好证据。Kubernetes 成为在生产环境中服务人工智能和机器学习的选择。

这是一个强大的组合，在未来的几年中会产生巨大的商业影响。

当数据科学变成每个公司的一个关键角色的时候，需要改进并增强许多类型应用能力的需求也在增加。从改进用户交互以利用数据做更好的决策，比如自动驾驶汽车的应用，AI/ML 影线了几乎现在商业的各个角落。

就像容器化的好处一样，在生产中管理所有的也需要一种方式，所以 AI/ML 也明显需要一种坚固的 IT 基础设施来管理。

Kubernetes 为 AI/ML 带来了一个非常好的平台能力 - 伸缩性，访问 GPU，workload 迁移等等。我们可以看到有组织在使用 Kubernetes 做了很厉害的 AI/ML 方面的事情，我们期望下一代的应用可以彻底改变工业产业。

## 3. 唯一比 Kubernetes 更热的东西？Kubernetes 人才

我们知道，没人真想听到说“人才短缺”

但是在可见的未来，对 Kubernetes 技能人才（包括云原生能力）的需求还是很热的。目前很难有可信的数据来说明，但是可以确定的是 2022 年依然是需求大于供给。

目前 Kubernetes 和云原生技术的使用趋势还没有放缓的趋势。我希望可以看到更多的组织持续上云，并且增加微服务，serverless 和其他云原生技术的使用。更重要的是，我们希望更多的组织在意识到 Kubernetes, Linux, 和 DevOps 之间的关系。

人才短缺会在几个方面表现出来。首先，通过云原生全景图可以很自然的引导很多人进行自己学习，也就会让大家掌握很好的技能。

全球多元化和开放工程社区在加速发展，它帮忙建立一个充满活力的云原生生态。人们在寻求构建 Kubernetes 和云原生生态的知识和技能的趋势也在持续发展，还有各种规模的组织对具备这些技能的工程师的需求，都在帮助这方面的人才有更好的发展。

其次，公司和招聘管理者必须要更加积极主动。如果放缓或是搁置关键的 IT 人才等招聘？那就等着吧。

在 2022 年各个公司会继续愿意投入在新老雇员或者未来要雇佣的员工身上，培训他们 Kubernetes 和其他云相关技术（例如 Linux），真金白银的投入而不是说说。在 Kubernetes 认证上 Linux 基金会是最大的一个参与者。

但是这个趋势这里不只是说认证。更多的说这是一种员工本身的思想转变，不是说一种漂亮的方式宣传说是一种职业发展，而实际上是他们自身愿意投入时间去学习。管理者如果想我招你来工作的不是来学习的，那么那就基本是招不到人的，除非他能忽悠。公司进行培训并且对有工作经验的员工进行云原生培训实践，就持续找到一大批愿意学习的人员的。

## 4. Kubernetes 商业化管理服务业将蓬勃发展

商业 Kubernetes 平台，像 Red Hat 的 OpenShift，实在开源项目智商构建的，已经是企业 Kubernetes 采用和使用的主流方式。随着越来越多成功的案例出现，其他的组织自然要去寻找相似的商业产品。但是并不是所有的公司都需要从头构建能力来运行他们自己的平台。

多数时候，他们不想在运营和管理维护 Kubernetes 上投入，只想使用而已。这就是我们看到快速发展的 Kubernetes 管理云服务。比如 OpenShift。

Kubernetes 管理服务的增长实在公有云上（除了可以运行在任何云上一些商业平台），这就意味着很多组织是不需要或者不想自己来运维管理 Kubernetes 的。

译者注：我也是这么看的，未来中小企业使用云来优化自己内部的资源问题，场景适配问题是核心，而 Kubernetes 以及底层资源的运维管理不是核心，完全可以托管。

## 5. Kubernetes 社区将继续优先考虑安全问题

Kubernetes 内置了重要的安全特性，只需要配置 ok 即可。它繁荣的生态也非常重视平台的安全性，在 OperatorHub.io 上有 29 中不同的安全 app，这也是一个可以侧面反应对安全重视的指标。

2022 年，企业组织剋使用这些可用的工具和服务来加强他们的云和云原生安全。例如，我们会看到企业如何使用管理应用入口上的变化。

我们会看到基于策略的部署管理的增长，比如使用 OPA Gatekeeper, Kyverno, 和 Argo CD 等。

总的来说，预计整个社区都会继续投入 Kubernetes 的安全性，尤其是在简化（而不是降低）团队安全性方面，并通过将其嵌入到他们用来管理集群的工具中来减少其预算。

Kubernetes 发行版将开始在发行版中直接添加更多安全功能。这将有助于增强分发的整体安全性，并有助于降低 Kubernetes 安全部署的成本。

## 后记
整体来说这篇文章还是有点东西的，几个趋势应该也是今后 Kubernetes 的重要发展趋势。这些趋势目前确实也是我们在实际场景终于到的，比如 KaaS 的提出，人才的招聘难度，现在招聘 golang 开发在国内都比较紧张。还有 Kubernetes 在 AI 上的结合，确实 AI 重在应用，而 Kubernetes 重在底层调度，Kubernetes 的调度扩展特性也设计的非常好。

但是我认为分析的不够深入，缺乏一些数据支持。所以在翻译过程中有些内容我也进行了删减。

<center>
看完本文有收获？请分享给更多人

关注「黑光技术」，关注大数据+微服务

![](/images/qrcode_helight_tech.jpg)

</center>