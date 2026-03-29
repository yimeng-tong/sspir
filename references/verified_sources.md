# 已核对来源清单

生成时间：2026-03-27

本文件只记录当前已经核对到的正式论文来源、可访问入口和对应代码线索。`Deep research` 文件仅作为线索索引，不直接作为引用来源。

## 核心参考文献

### 1. Retinex 理论起点

- 文献：Land E. H. The Retinex Theory of Color Vision. *Scientific American*, 1977, 237(6): 108-128.
- DOI：`10.1038/scientificamerican1277-108`
- 正式入口：
  - `https://doi.org/10.1038/scientificamerican1277-108`
  - `https://www.scientificamerican.com/article/the-retinex-theory-of-color-vision/`
- 用途：第二章 Retinex 理论来源；第三章 `I = R ⊙ L` 的物理动机。
- 备注：适合用于理论起点，不承担现代网络结构细节的论证任务。

### 2. GAN 类 LLIE 基线

- 文献：Jiang Y, Gong X, Liu D, et al. EnlightenGAN: Deep Light Enhancement without Paired Supervision. *IEEE Transactions on Image Processing*, 2021, 30: 2340-2349.
- DOI：`10.1109/TIP.2021.3051462`
- 正式入口：
  - `https://doi.org/10.1109/TIP.2021.3051462`
  - `https://arxiv.org/abs/1906.06972`
- 代码：
  - `https://github.com/VITA-Group/EnlightenGAN`
- 用途：第一章和第四章中的 GAN 基线；说明判别式/对抗式增强在真实感和伪影之间的权衡。

### 3. 扩散模型基础

- 文献：Ho J, Jain A, Abbeel P. Denoising Diffusion Probabilistic Models. *Advances in Neural Information Processing Systems*, 2020, 33: 6840-6851.
- 正式入口：
  - `https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html`
  - `https://proceedings.neurips.cc/paper_files/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf`
  - `https://arxiv.org/abs/2006.11239`
- 用途：第二章 2.2.1 的 DDPM 基础引用；第四章方法实现背景。

### 4. 语义与结构先验扩散恢复

- 文献：Zhang Y, Zhang H, Cheng Z, et al. SSP-IR: Semantic and Structure Priors for Diffusion-based Realistic Image Restoration. *IEEE Transactions on Circuits and Systems for Video Technology*, 2025.
- DOI：`10.1109/TCSVT.2025.3538772`
- 正式入口：
  - `https://doi.org/10.1109/TCSVT.2025.3538772`
  - `https://arxiv.org/abs/2407.03635`
  - `https://zyhrainbow.github.io/projects/SSP-IR/`
- 代码：
  - `https://github.com/zyhrainbow/SSP-IR`
- 用途：第三章和第四章的直接主参考；语义先验、结构先验、ControlNet 注入与扩散主干冻结范式。

### 5. Retinex 深度展开方法

- 文献：Wu W, Weng J, Zhang P, et al. URetinex-Net: Retinex-Based Deep Unfolding Network for Low-Light Image Enhancement. In: *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2022: 5901-5910.
- 正式入口：
  - `https://openaccess.thecvf.com/content/CVPR2022/html/Wu_URetinex-Net_Retinex-Based_Deep_Unfolding_Network_for_Low-Light_Image_Enhancement_CVPR_2022_paper.html`
  - `https://openaccess.thecvf.com/content/CVPR2022/papers/Wu_URetinex-Net_Retinex-Based_Deep_Unfolding_Network_for_Low-Light_Image_Enhancement_CVPR_2022_paper.pdf`
- 代码：
  - `https://github.com/SZU-AdvTech-2023/262-URetinex-Net-Retinex-based-Deep-Unfolding-Network-for-Low-light-Image-Enhancement`
- 用途：第二章 Retinex 深度方法综述；第四章 Retinex 判别式强基线。

### 6. 扩散恢复综述

- 文献：Li J, Wang H, Li Y, et al. A Comprehensive Review of Image Restoration Research Based on Diffusion Models. *Mathematics*, 2025, 13(13): 2079.
- DOI：`10.3390/math13132079`
- 正式入口：
  - `https://doi.org/10.3390/math13132079`
  - `https://www.mdpi.com/2227-7390/13/13/2079`
- 用途：第二章综述背景、扩散图像恢复分类法与研究趋势。
- 备注：综述文献，只用于概览，不替代原始方法论文。

### 7. MLLM 介入图像恢复

- 文献：Jin X, Shi Y, Xia B, et al. LLMRA: Multi-modal Large Language Model based Restoration Assistant. *arXiv preprint*, 2024.
- arXiv：`2401.11401`
- 正式入口：
  - `https://arxiv.org/abs/2401.11401`
  - `https://arxiv.org/pdf/2401.11401`
- 用途：第二章 MLLM 与图像恢复关系综述；第三章语义先验净化动机。
- 备注：本轮检索未确认到官方公开代码仓库，引用时以 arXiv 论文为准。

### 8. 近期 Retinex 判别式方法

- 文献：Yin M, Yang J. ILR-Net: Low-light image enhancement network based on the combination of iterative learning mechanism and Retinex theory. *PLOS ONE*, 2025, 20(2): e0314541.
- DOI：`10.1371/journal.pone.0314541`
- 正式入口：
  - `https://doi.org/10.1371/journal.pone.0314541`
  - `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314541`
- 代码：
  - `https://github.com/Yinmohan2000/ILR-Net`
- 用途：第四章可作为近期 Retinex 判别式对比方法补充。

### 9. Retinex + Diffusion 代表方法一

- 文献：Yi X, Xu H, Zhang H, et al. Diff-Retinex: Rethinking Low-light Image Enhancement with A Generative Diffusion Model. In: *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 2023: 12302-12311.
- 正式入口：
  - `https://openaccess.thecvf.com/content/ICCV2023/html/Yi_Diff-Retinex_Rethinking_Low-light_Image_Enhancement_with_A_Generative_Diffusion_Model_ICCV_2023_paper.html`
  - `https://openaccess.thecvf.com/content/ICCV2023/papers/Yi_Diff-Retinex_Rethinking_Low-light_Image_Enhancement_with_A_Generative_Diffusion_Model_ICCV_2023_paper.pdf`
- 代码：
  - `https://github.com/XunpengYi/Diff-Retinex`
- 用途：第四章中最重要的 Retinex + Diffusion 可比对象之一。

### 10. Retinex + Latent Diffusion 代表方法二

- 文献：He C, Fang C, Zhang Y, et al. Reti-Diff: Illumination Degradation Image Restoration with Retinex-based Latent Diffusion Model. *ICLR*, 2025.
- 正式入口：
  - `https://arxiv.org/abs/2311.11638`
  - `https://github.com/ChunmingHe/Reti-Diff`
- 用途：第四章中与“Retinex 引导扩散”最接近的现成对比对象。

## 与深度频域约束相关的辅助文献

### 11. 频域生成与结构频率线索

- 文献：Frequency Generation for Real-World Image Super-Resolution.
- 当前已识别正式信息：*IEEE Transactions on Circuits and Systems for Video Technology*, 34(8): 7029-7040, 2024.
- DOI：`10.1109/TCSVT.2024.3367876`
- 当前可用入口：
  - `https://doi.org/10.1109/TCSVT.2024.3367876`
  - `https://www.researchgate.net/publication/378345105_Frequency_Generation_for_Real-World_Image_Super-Resolution`
- 用途：第三章频域先验设计的旁证材料。
- 备注：正式引用时不要引用 `ResearchGate` 页面本身。

## 当前来源使用原则

- 可以直接引用：正式论文页、DOI、arXiv、CVF Open Access、PLOS、期刊官网、项目页、官方代码仓库。
- 不可直接引用：`Deep research` 文档正文、ResearchGate 页面、Emergent Mind 页面、博客、二手中文解读。
- 写作时应优先回到“原始方法论文 + 官方代码仓库”这一对组合来确认方法与实验细节。
