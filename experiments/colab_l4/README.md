# Colab L4 Workflow

这套材料用于在 Colab `L4 GPU` 上完成低光照增强论文的第一轮实验复现，目标是：

1. 跑通主要基线推理。
2. 自动记录运行状态、耗时和日志。
3. 自动计算核心指标并汇总成第四章可用表格。

## 当前支持的方法

- `uretinex`
- `diff-retinex`
- `reti-diff`

## 当前不默认纳入第一轮 Colab 流程的方法

- `ssp-ir`

原因：

- 当前本地仓库中的 `SSP-IR/test.py` 版本不完整。
- 该方法还依赖额外的 LLaVA / Stable Diffusion / RAM 权重与更重的环境。
- 论文第一轮主表更适合先用 `URetinex-Net + Diff-Retinex + Reti-Diff` 搭起来。

## 文件说明

- `llie_l4_pipeline.ipynb`
  - Colab 主 notebook，兼容两种代码来源
  - 优先推荐直接从 GitHub 克隆整个 `sspir` 仓库后运行
  - 也兼容把 `experiments/colab_l4` 整个目录上传到 Drive 后运行
  - 在 VSCode 插件连接的 Colab 远端环境里，如果 `/content/sspir` 不存在，第一格会自动克隆仓库
- `config/run_config.example.json`
  - 路径配置模板
- `scripts/progress_utils.py`
  - 状态记录与命令执行封装
- `scripts/run_baseline.py`
  - 基线推理执行器
- `scripts/compute_metrics.py`
  - 指标计算器
- `scripts/aggregate_results.py`
  - 汇总多个结果为 markdown/csv 表格

## 建议的 Drive 目录结构

```text
MyDrive/
  thesis/
    experiments/
      colab_l4/
        # 只有在你选择“代码也放 Drive”时才需要
  thesis_llie_l4/
    datasets/
      LOL/
        eval15/
          low/
          high/
      LOLv2/
        Real_captured/
          Test/
            Low/
            Normal/
        Synthetic/
          Test/
            Low/
            Normal/
    weights/
      diff_retinex/
        checkpoint_LOL_Diff_TDN.pth
        Diff_RDA_best.pth
        Diff_IDA_best.pth
      reti_diff/
        llie_real.pth
        llie_syn.pth
        retinex_decomnet.pth
    runs/
```

## 推荐运行模式

优先推荐：

1. 在 Colab/VSCode 远程环境里把 GitHub 仓库克隆到 `/content/sspir`
2. 直接打开 `/content/sspir/experiments/colab_l4/llie_l4_pipeline.ipynb`
3. 只把数据集、权重和 `runs/` 放在 Google Drive

这种模式的好处是：

- 代码更新直接通过 `git pull` 同步
- 不需要每次把 notebook 和脚本重新上传到 Drive
- 我们后续协作时，仓库里的 notebook 输出和脚本改动都更容易对齐

如果你不想用 GitHub 克隆模式，仍然可以把 `experiments/colab_l4` 整个目录上传到：

- `MyDrive/thesis/experiments/colab_l4/`

当前 notebook 会自动尝试识别这两种路径。

如果你是通过 VSCode 的 Colab/Jupyter 插件连接远端运行环境，通常直接打开仓库里的 notebook 并运行第一格即可，不需要你先手动执行 `git clone`。

## 推荐执行顺序

1. 先跑 `uretinex`，验证数据与指标链路通畅。
2. 再跑 `diff-retinex`，注意默认关闭 `GT-means`。
3. 再跑 `reti-diff`，分别跑 `real` 与 `syn`。
4. 最后统一算指标并汇总。

## 结果落盘

每次运行都会在 `output_root/<method>/<dataset>/<run_name>/` 下生成：

- `status.json`
- `run.log`
- `predictions/` 或方法对应输出目录
- `metrics/per_image.csv`
- `metrics/summary.json`

## 与第四章的对应关系

- `summary.json` 中的均值指标可直接转为第四章主表。
- `per_image.csv` 可用于挑选可视化案例。
- `run.log` 和 `status.json` 可用于补写实验环境与运行代价。
