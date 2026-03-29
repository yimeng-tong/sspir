# SSPIR Thesis Workspace

This repository contains the writing, experiment planning, and Colab workflow for an undergraduate thesis on low-light image enhancement based on Retinex decomposition and multi-modal / frequency-domain prior guidance.

## What Is In This Repo

- `chapters/`: thesis chapter drafts
- `notes/`: experiment plans, resource notes, and working memos
- `references/`: verified source lists and reading notes
- `experiments/colab_l4/`: Colab L4 workflow, scripts, and configuration templates
- `papers/`: literature notes and metadata files

## What Is Not Stored In This Repo

To keep the repository lightweight and collaboration-friendly, the following are intentionally not committed:

- large model weights
- datasets
- raw experiment outputs
- third-party cloned repositories
- downloaded paper PDFs

Those assets should live in Google Drive or another external storage location.

## Recommended External Storage Layout

```text
MyDrive/
  thesis_llie_l4/
    datasets/
    weights/
    runs/
```

## Main Entry Points

- Thesis outline: [chapters/00_outline.md](/home/tong123/thesis/chapters/00_outline.md)
- Chapter 1: [chapters/01_introduction.md](/home/tong123/thesis/chapters/01_introduction.md)
- Chapter 2: [chapters/02_related_theory.md](/home/tong123/thesis/chapters/02_related_theory.md)
- Chapter 3: [chapters/03_method.md](/home/tong123/thesis/chapters/03_method.md)
- Chapter 4 draft: [chapters/04_experiments.md](/home/tong123/thesis/chapters/04_experiments.md)
- Verified references: [references/verified_sources.md](/home/tong123/thesis/references/verified_sources.md)
- Colab workflow: [experiments/colab_l4/README.md](/home/tong123/thesis/experiments/colab_l4/README.md)

## Current Experiment Strategy

The current first-round reproducibility target on Colab L4 is:

- `URetinex-Net`
- `Diff-Retinex`
- `Reti-Diff`

`SSP-IR` is not yet in the default first-round flow because the local test entry is incomplete and would slow down the main experiment path.
