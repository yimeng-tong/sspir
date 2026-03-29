# Remote Assets Policy

This repository is designed to support collaboration between local writing, Colab execution, and GitHub versioning.

## Versioned In GitHub

- thesis drafts
- experiment planning documents
- verified reference notes
- Colab notebooks and scripts
- configuration templates
- lightweight metadata and summary tables

## Kept Outside GitHub

- datasets
- model weights
- downloaded paper PDFs
- raw prediction images
- large logs and intermediate artifacts
- cloned third-party repositories

## Why

- GitHub repositories are not a good storage layer for large binary assets.
- Large files increase clone time and make iteration slower.
- Some downloaded papers and pretrained weights have redistribution constraints.

## Where To Put External Assets

Recommended location:

```text
Google Drive / thesis_llie_l4/
  datasets/
  weights/
  runs/
```

## What To Sync Back To GitHub

After experiments finish, only sync back:

- aggregated metric tables
- lightweight representative figures
- updated chapter text
- updated configuration files
- notes about reproducibility issues
