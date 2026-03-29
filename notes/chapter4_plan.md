# 第四章写作与实验执行方案

生成时间：2026-03-27

当前第四章标题：实验结果与分析

## 1. 第四章的核心目标

第四章不是泛泛证明“模型能增强图像”，而是要回答三个更具体的问题：

1. 引入 Retinex 前置分解后，是否比直接从低光图像提取先验更稳定。
2. 基于 `R` 图的语义净化，是否能减少语义漂移与不合理生成。
3. 加入 SNR 感知的双频域结构约束后，是否能在抑噪和结构保真之间取得更好的平衡。

## 2. 我建议的实验数据组织

### 主量化数据集

- `LOL-v1`
- `LOLv2-Real`
- `LOLv2-Synthetic`

理由：

- 这三套数据最容易和 `URetinex-Net`、`Diff-Retinex`、`Reti-Diff`、`ILR-Net` 等方法形成可比关系。
- `Reti-Diff` 和 `Diff-Retinex` 的公开实现都天然区分 real / synthetic，这和你第四章结构很契合。

### 辅助真实场景展示集

- `LIME`
- `NPE`
- `DICM`
- `MEF`
- `VV`

或替代为：

- `RealLR200`
- `MIT-Adobe FiveK` 的低光子集

理由：

- 这些集合更适合做真实场景可视化展示与无参考质量分析。
- 不建议把所有数据集都硬塞进量化表，第四章会变散。

## 3. 我建议的对比方法分组

### A. 传统 / GAN 类

- `EnlightenGAN`

### B. Retinex 判别式类

- `URetinex-Net`
- `ILR-Net`

### C. Retinex + Diffusion 类

- `Diff-Retinex`
- `Reti-Diff`

### D. 语义/先验引导扩散类

- `SSP-IR`

结论：

- 如果计算资源有限，第四章最少也要保证 `EnlightenGAN + URetinex-Net + Diff-Retinex + SSP-IR/或Reti-Diff` 这四类中每类至少一个方法。
- 如果只能做有限复现，我会优先保留：`URetinex-Net`、`Diff-Retinex`、`Reti-Diff`、`EnlightenGAN`。

## 4. 我建议的评价指标

### 有参考指标

- `PSNR`
- `SSIM`
- `LPIPS`

用途：

- `PSNR / SSIM` 用于量化重建保真。
- `LPIPS` 用于补充感知质量，避免只看像素指标。

### 无参考或真实场景指标

- `NIQE`
- 可选 `LOE`

建议：

- `FID` 在 LLIE 小规模数据上不一定稳定，除非样本量足够且复现链条清晰，否则不建议把它作为核心指标。
- 如果后续确实要写 `FID`，必须在第四章说明具体特征提取实现和样本数。

### 效率指标

- 单张推理时间
- 显存占用
- 扩散步数

理由：

- 你的方法本质上是“冻结主干 + 多先验受控生成”，计算代价会是论文中必须正面承认的点。

## 5. 我建议的第四章内部结构

### 4.1 实验环境与数据集准备

- 硬件环境、CUDA/PyTorch 版本
- 训练与推理分辨率
- 数据集划分与预处理方式
- 提示词离线生成流程

### 4.2 评估指标与对比算法

- 统一说明各方法类别
- 明确哪些结果来自官方权重复现，哪些来自论文引用
- 明确 paired / unpaired / real-world 的评估边界

### 4.3 对比实验结果分析

- 表 4-1：数据集与设置
- 表 4-2：LOL-v1 / LOLv2 定量对比
- 图 4-1：典型场景可视化对比
- 图 4-2：极暗区域、噪声区域、边缘区域局部放大对比

### 4.4 核心模块消融实验

- 去掉 Retinex 分解
- 用原始低光图直接生成 MLLM 提示
- 去掉 `L` 图隐式氛围分支
- 去掉 `SNR-aware mask`
- 把双频约束改回统一 FFT 约束

### 4.5 本章小结

- 总结：哪个模块提升结构，哪个模块抑制幻觉，哪个模块带来额外开销

## 6. 来自代码仓库的关键实验约束

### SSP-IR

- 仓库使用 `Stable Diffusion v1.5`
- 训练数据目录为 `gt / sr_bicubic / llm_caption`
- 推理脚本默认 `50` 步、`guidance_scale 7.5`、`process_size 512`
- 含义：你的第四章若要和它公平对比，扩散步数与输入尺度不能乱变

### SeeSR

- 使用 `SD-2-base`
- 训练依赖 `DAPE` 与标签文本
- README 给出 `50` 步标准推理和 `2` 步 turbo 变体
- 含义：它更适合给你提供“扩散+语义先验”实验组织方式，而不是直接作为 LLIE 定量主基线

### URetinex-Net

- 官方 README 的评估重点是 `LOL`
- 含义：它很适合作为 paired LLIE 基线，但不适合作为所有真实场景数据的统一比较对象

### Diff-Retinex

- 官方代码支持 `LOL`、`VE-LOL` 和 `LOLv2`
- `test_from_dataset.py` 明确提醒 `GT-means` 会显著影响 PSNR
- 含义：第四章必须单独说明是否开启 `GT-means`；我的建议是默认关闭，保证公平

### Reti-Diff

- 官方配置区分 `LLIE_real` 和 `LLIE_syn`
- 测试配置里 `timesteps` 为 `4`
- 含义：第四章最好把 real / synthetic 结果分表写，不要混在一起

### EnlightenGAN

- 训练是非配对的
- 测试集包含 `LIME / MEF / NPE / VV / DICP`
- 含义：它更适合作为真实场景视觉对比和经典方法代表，而不是 paired 数值最强基线

## 7. 我接下来实际会怎么做

1. 先把第四章锁定为“`LOL-v1 + LOLv2(real/syn)` 主量化，`LIME/DICM/NPE/MEF/VV` 辅助可视化”的双层结构。
2. 再把对比方法锁定为五类代表：`EnlightenGAN`、`URetinex-Net`、`ILR-Net`、`Diff-Retinex/Reti-Diff`、`SSP-IR`。
3. 接着把消融实验按你的真实创新点重排，避免出现“消融做了，但和创新点对不上”的问题。
4. 最后再反过来修第三章中的模块命名和损失定义，让第三章和第四章能一一对应。

## 8. 我的结论

第四章最稳妥的写法，不是把它写成一个泛化的“所有方法都比”，而是围绕下面这条主线展开：

`Retinex 前置净化` 负责让先验更可信，`R 图语义净化` 负责减少语义漂移，`SNR-aware 双频约束` 负责抑噪并守住结构。

如果后续实验资源有限，我会优先确保这条主线在 `LOL-v1` 和 `LOLv2` 上被证实，然后再补真实场景可视化和效率分析。
