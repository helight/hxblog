---
title: "【译】在 IT 系统的开发和运营中使用生成式人工智能的潜在好处"
date: 2023-05-30T08:45:20+08:00
tags: ["DevOps", "SRE"]
categories: ["DevOps", "SRE"]
banner: "/images/banners/kubernetes.jpeg"
author: "helight"
authorlink: "http://helight.cn"
summary: ""
keywords: ["DevOps", "SRE"]
draft: false
---

# 前言

很多团队正在试验如何使用生成性 AI 来开发和运营 IT 系统。

生成式 AI 可以自动生成 IT 系统中使用的代码或模型。这有助于加快开发过程并减少所需的人工劳动量。生成式人工智能还可以为 IT 系统创建人类开发人员可能没有考虑过的新设计或解决方案。

通过分析大量数据和识别模式，[生成式 AI](https://dzone.com/articles/the-exponential-growth-of-generative-ai-opportunit)可以为复杂问题开发新颖的解决方案。

生成式 AI[模型](https://dzone.com/articles/understanding-architecture-models-of-chatbot-and-r)学习大型数据集中的模式和特征，然后生成与这些模式和组件匹配的新内容。但是，它们无法创建训练数据中不存在的全新或原创内容。

虽然生成式 AI 模型可以产生逼真的内容，但必须注意它们不具备独立思考或创造力的能力。他们只能根据从训练数据中学到的知识生成新内容。

然而，值得注意的是，生成式 AI 仍处于早期阶段，许多挑战仍有待克服。例如，可能不太容易确保生成的代码或模型是高质量的并满足要求。此外，对于生成式 AI 中的偏见和公平性存在担忧，因为这些算法可能会受到它们所训练的数据中的现有偏见而把这种偏见永久化。

生成人工智能的一些案例已经可以在数周或数月内在企业内就可以实施。相比之下，其它案例可能需要更多的研究和开发才能在商业环境中有效使用。采用的时间表还取决于所解决问题的复杂性和组织可用的资源。因此，组织必须在投入资源开发和部署之前仔细评估生成式 AI 解决方案的可行性和潜在影响。

## **架构设计** 

[使用 AI](https://dzone.com/articles/artificial-intelligence-in-architecture)生成 IT 架构的好处之一是，与手动设计的系统相比，它可以设计更高效、可扩展和有弹性的系统。这是因为 AI[算法](https://dzone.com/articles/exploring-ai-algorithms)可以快速有效地搜索大量可能的设计，以找到最适合给定任务或问题的设计。

此外，生成式 AI 可以帮助组织快速且经济高效地设计和部署根据其特定需求定制的 IT 系统，从而减少手动设计和优化所需的时间和资源。

通过把设计和优化过程的某些方面自动化，生成式 AI 有可能显着增强基于模式的解决方案蓝图和系统架构文档的开发工作。

例如，生成式 AI 算法可以分析现有解决方案的大型数据集，并确定可应用于新解决方案的通用模式和设计原则。这有助于确定已经成功的最佳实践和设计模式，并使开发人员能够快速有效地将它们整合到新的解决方案中。

生成式 AI 还可以根据预定义的目标和约束自动生成和评估不同的设计选项，从而帮助优化系统架构。这有助于确定满足项目要求的最有效的系统架构。

此外，生成式 AI 可以根据已识别的模式和设计原则生成详细的图表、规范和其他支持文档，从而帮助自动化文档撰写过程。这有助于加快文档撰写过程并确保生成的文档准确且一致。

## **设计**

生成式 AI 还可用于帮助生成设计规范、基于行业模型的[API](https://dzone.com/articles/everything-you-should-know-about-apis)规范、框架/实用程序功能建议和数据库配置。

例如，生成式 AI 算法可以分析现有的设计模式、系统架构和代码库，以确定通用模式和最佳实践，并使用这些信息自动生成满足项目要求和约束的设计规范。

同样，生成式人工智能可以分析行业模型并生成针对特定行业的 API 规范，为特定于行业需求的 API 设计和开发提供标准化方法。

生成式 AI 还可以根据对现有代码库和开发趋势的分析，为最适合项目需求的框架和实用功能提供建议。这有助于减少手动研究和评估不同框架和实用程序所需的时间和精力，并使开发人员能够快速有效地确定最适合工作的工具。 

最后，生成式 AI 可以根据项目要求自动生成数据库设计和实施建议，从而协助数据库配置。这有助于确保数据库针对性能、可伸缩性和可靠性进行优化，并满足项目的需求。

## **测试**

生成式人工智能还可以为各种测试场景生成测试用例和测试数据，包括主要流程、备用路径、异常流程和错误处理。通过分析系统架构并识别常见模式和最佳实践，生成式人工智能可以生成涵盖广泛场景的测试用例和[测试数据](https://dzone.com/articles/what-is-test-data-why-is-data-driven-testing-neces)，确保系统得到全面测试，并识别和解决潜在问题。

除了生成测试用例和测试数据外，生成式 AI 还可以生成用于渗透、混沌和性能测试的测试配置文件。通过分析系统架构并识别潜在的漏洞和瓶颈，生成式人工智能可以生成模拟真实场景的测试配置文件，并提供对系统性能和弹性的宝贵见解。

生成式人工智能还可以帮助选择和优化测试框架和工具。通过分析现有代码库并确定常见的测试模式和最佳实践，生成式 AI 可以建议最适合项目要求和约束的测试框架和工具，帮助确保测试过程高效且有效。

## **部署**

生成式 AI 还可以生产协助打包和部署工件和数据现代化脚本。

生成式 AI 可以分析打包和部署工件的系统架构，并确定打包和部署软件系统的最佳实践和模式。基于这种分析，生成式 AI 可以生成部署脚本和模板，使部署过程自动化，并确保生成的工件是一致的、可靠的，并且针对目标环境进行了优化。

对于数据现代化脚本，生成式 AI 可以分析现有数据架构并确定数据现代化的常见模式和最佳实践。基于这种分析，生成式 AI 可以生成数据迁移脚本和模板，使数据现代化过程自动化，确保数据的转换和迁移高效且有效。

## **运营**

生成式 AI 还可用于协助事件分类和警报，以及服务管理的其他各个方面。

在事件分类和警报中，生成 AI 可以分析历史事件数据并识别模式和趋势，这些模式和趋势有助于根据事件的潜在影响和严重程度确定事件和警报的优先级。此外，通过分析类似的工单、问题类别、解决方案类别和根本原因，生成式 AI 可以提出潜在的解决方案和建议来解决事件和警报，并为问题和工单推荐运行手册以简化解决过程。

生成式 AI 还可以协助总结解决说明、根本原因和最终说明，提供事件的高级概述及其对开发、运营和客户使用价值流的影响。这有助于深入了解事件的根本原因以及事件对整体服务交付的影响。

除了事件管理，生成式人工智能还可用于为常见问题和标准操作程序生成自动化脚本，有助于简化解决流程并减少人工干预所需的时间和精力。

最后，生成式人工智能可以生成服务管理报告，为服务交付流程的绩效和有效性提供有价值的见解，包括事件量、解决时间和客户满意度等指标。通过分析这些报告，利益相关者可以深入了解服务交付流程的整体健康状况和绩效，并确定改进和优化的机会。

## **自治系统**

总有一天，生成式 AI 可用于创建自动化 IT 系统，这些系统能够在没有人为干预的情况下做出决策并采取行动。 

GitOps 是一种用于管理和自动化 IT 系统的方法，也可以与生成 AI 一起使用以提高 IT 系统的效率和可靠性。GitOps 使用 Git 等版本控制系统来管理和自动化 IT 操作。

生成式 AI 可用于创建可预测和预防潜在系统故障、识别性能瓶颈和优化资源利用率的模型。

通过将 GitOps 与生成式 AI 结合使用，组织可以自动化 IT 系统的部署和管理，同时确保在部署之前对变更进行充分的测试和审计。这有助于提高 IT 系统的可靠性和安全性，同时减少 IT 运营所需的时间和精力。

## **法律影响**

在开发 IT 系统时使用生成式 AI 会涉及法律问题。与任何技术一样，应考虑潜在风险和法律问题。

生成人工智能的主要法律问题之一是知识产权。例如，如果生成式 AI 系统创建了受版权保护的作品，则可能不清楚谁拥有该作品的权利。这可能导致所有权纠纷，甚至可能导致法律诉讼。

另一个问题与责任有关。如果生成式 AI 系统创造了造成伤害的产品或服务，那么可能会出现谁应对这种伤害负责的问题。例如，如果使用生成式 AI 开发的自动驾驶汽车发生事故，谁该承担责任：制造商、软件开发商还是 AI 系统本身？

隐私也是生成人工智能的一个重要法律问题。例如，如果系统根据用户数据生成内容，则可能存在有关如何收集、使用和存储该数据的问题。这可能会违反隐私法律和法规。

## **结论**

组织必须建立治理组织，以确保以合乎道德、负责任的方式使用生成人工智能，并遵守所有相关法律法规。这可能涉及制定政策和程序、建立监督和审查流程，以及培训员工正确使用技术。

原文：[https://dzone.com/articles/potential-benefits-of-using-generative-ai-in-the-d](https://dzone.com/articles/potential-benefits-of-using-generative-ai-in-the-d)