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
  - Colab 主 notebook
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
