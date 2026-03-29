# 论文工作约定

## 1. 课题定位

- 当前拟定题目：基于 Retinex 分解与多模态语义-频域双重引导的低光照图像增强研究
- 研究方向：低光照图像增强（LLIE）
- 核心路线：Retinex 分解 + 多模态语义先验 + 频域结构约束 + 扩散生成
- 当前默认框架名：`SSP-IR`
- 术语约定：除非引用原文标题，否则统一使用 `SSP-IR`、Retinex、Reflectance/Illumination、低光照图像增强（LLIE）等表述，避免 `sspir` / `SSP` / `SSP-IR` 混用

## 2. 目录用途

- `chapters/`：各章正文、提纲与修订稿
- `notes/`：文献笔记、推导草稿、写作备忘
- `figures/`：论文插图、框架图、结果图
- `tables/`：实验表格、对比表格、消融表格
- `references/`：`.bib`、引文映射、引用核验记录
- `papers/`：论文原文、论文摘要整理、文献入口
- `experiments/`：实验设置、日志、指标、消融记录
- `assets/`：模板、封面素材、答辩辅助材料

## 3. 引用与证据规则

- 引用必须准确，作者、题目、年份、期刊/会议、页码、DOI 或可访问链接都要逐项核对。
- 每一条正文中的关键论断，都应能追溯到真实存在且可访问的原始论文或官方页面。
- 优先引用一级来源：期刊官网、会议官网、`doi.org`、`arXiv`、`dblp`、出版社页面。
- `ResearchGate` 只可作为检索入口或下载镜像，不作为正式引用来源。
- `papers/` 中凡是以 `Deep research` 开头的文件，一律视为二级综述材料，禁止直接作为论文引用来源。
- 如果某个观点、结论、实验数字来自 `Deep research` 文件，必须反向定位到它对应的真实原始论文，再决定是否引用。
- 综述类论文只能用于综述、分类法、研究趋势总结；具体方法细节、损失函数、实验指标，优先回到原始方法论文。
- 不能编造引用，不能补不存在的 DOI、页码、作者顺序或实验结果。
- 当来源不确定、链接失效、信息冲突时，正文中先标记 `TODO`，不得强行写入正式论述。
- 当引用实验指标时，必须同时核对数据集、评价指标、是否为有参考/无参考设置，以及是否是作者原文报告值。

## 4. 已知文献入口与使用边界

以下链接已作为当前课题的已知入口记录，但实际写入论文前仍需逐条复核引用格式。

- `Diffusion Models for Low-Light Image Enhancement: A Multi-Perspective Taxonomy and Performance Analysis`
  - 入口：`https://arxiv.org/html/2510.05976v1`
  - 类型：综述
  - 用途：可用于第二章综述、分类法、研究挑战与趋势描述
  - 限制：不直接替代原始方法论文

- `Frequency Generation for Real-World Image Super-Resolution`
  - 已识别正式信息：IEEE Transactions on Circuits and Systems for Video Technology, 34(8): 7029-7040, 2024
  - DOI：`10.1109/TCSVT.2024.3367876`
  - 现有入口：`https://www.researchgate.net/publication/378345105_Frequency_Generation_for_Real-World_Image_Super-Resolution`
  - 用途：可用于频域生成、结构频率约束相关论述
  - 限制：正式引用时不要引用 `ResearchGate` 页面本身，应改用 DOI、出版社或 `dblp` 核验后的信息

- `ILR-Net: Low-light image enhancement network based on the combination of iterative learning mechanism and Retinex theory`
  - 入口：`https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314541`
  - DOI：`10.1371/journal.pone.0314541`
  - 类型：期刊论文
  - 用途：可用于 Retinex 类 LLIE 方法综述和相关工作比较

- `Unifying Image Processing as Visual Prompting Question Answering`
  - 入口：`https://arxiv.org/html/2310.10513v2`
  - arXiv：`2310.10513`
  - 类型：方法论文
  - 用途：可用于统一图像处理、视觉提示范式、多任务图像处理相关表述

## 5. Deep Research 文件规则

- 当前路径：
  - `papers/Deep research: Advanced Integration of Multi-Modal Semantic Priors and Structural Frequency Constraints in Low-Light Image Restoration: A Comprehensive Analysis of the SSP-IR Framework and Retinex-Based Generative Models.MD`
- 该文件的定位：课题综述草稿或二级分析材料，不是正式引用源。
- 当前工作区核查结果：
  - 2026-03-26：该文件为空。
  - 2026-03-27：该文件已补充内容，可正常读取。
- 约束：
  - 不得直接从该文件复制引用到论文正文。
  - 如果后续该文件被补充内容，也只能把它作为线索索引，不能直接作为参考文献条目。
  - 如果需要使用其中提到的方法、数据集或结论，必须逐项回到原始论文核验。
  - 文件末尾包含混合质量来源，含 arXiv、项目页、代码仓库、ResearchGate、Emergent Mind 等；只有原始论文、官方页面和正式代码仓库可作为一手依据。

## 6. 当前论文结构状态

- 当前采用的正式结构为五章：
  - 第一章 绪论
  - 第二章 相关理论与技术综述
  - 第三章 面向低光照增强的 Retinex 物理启发与先验净化框架
  - 第四章 实验结果与分析
  - 第五章 总结与展望
- 附加部分：
  - 摘要
  - Abstract
  - 参考文献
  - 致谢
- 当前已提供较完整草稿的部分：
  - 第一章 绪论
  - 第二章 相关理论与技术综述
  - 第三章 面向低光照增强的 Retinex 物理启发与先验净化框架
- 第三章当前核心叙事：
  - `Retinex decomposition -> semantic prior purification -> SNR-aware dual-frequency constraint -> controlled diffusion generation`
  - Retinex 近似分解得到 `R` 与 `L`
  - 基于 `R` 图的 MLLM 显式语义净化
  - 基于 `L` 图的隐式氛围编码
  - 基于 `SNR-aware mask` 的双频域结构约束
  - 冻结扩散主干 + ControlNet / 注意力特征注入
- 当前创新点表述方向：
  - Retinex 前置分解驱动的先验净化策略
  - 基于 `R` 与 `L` 的解耦语义先验提取
  - 基于 SNR 感知掩码的双频域结构约束机制

## 7. 写作与修订规则

- 默认输出中文学术写作风格，保持客观、克制、可验证。
- 先保证逻辑自洽，再润色措辞；先保证证据链完整，再扩展创新表述。
- 对“首创”“显著优于”“彻底解决”等强结论保持谨慎，除非有充分实验支撑。
- 数学推导要说明变量含义、假设前提和使用边界。
- 方法章节中的模块命名要稳定，不要在不同段落中频繁改名。
- 当用户给出草稿时，优先保留原意，只改进结构、术语统一、学术表达与证据支撑。

## 8. 推荐执行顺序

1. 将当前目录草案和第三章草稿正式落盘到 `chapters/`。
2. 为第三章逐段建立“论断-来源”对应表，优先消除无来源或来源不稳的句子。
3. 在 `references/` 中建立文献清单与 `bib` 文件，固定标准引用格式。
4. 补写第二章相关工作，先写 Retinex、频域增强、扩散 LLIE、语义先验四条线。
5. 回到第一章，压实研究背景、问题定义、研究意义和创新点表述。
6. 最后再统一实验章节、摘要、结论和答辩材料。

## 9. 当前最重要的注意事项

- 不要直接引用任何 `Deep research` 文件。
- 不要把 `ResearchGate` 页面当作正式参考文献。
- 论文中的每个关键技术点都要回到原始论文核对。
- 第三章虽然已有较完整草稿，但在正式使用前必须完成逐段引文核验。

## 10. 当前已检查的代码线索

- 已本地保存并检查的相关仓库：
  - `experiments/repos/SSP-IR`
  - `experiments/repos/SeeSR`
  - `experiments/repos/URetinex-Net`
  - `experiments/repos/Diff-Retinex`
  - `experiments/repos/Reti-Diff`
  - `experiments/repos/EnlightenGAN`
  - `experiments/repos/ILR-Net`
- 这些仓库主要用于第四章实验设计、数据集选择、公平对比设置与可复现实验边界判断。
- 第四章写作时，优先依据仓库中的 `README`、训练/测试脚本、配置文件与官方论文页面来确定实验细节。
