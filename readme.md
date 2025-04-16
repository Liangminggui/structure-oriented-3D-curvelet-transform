

## 📁 Reproducibility Overview

This repository contains four datasets, each located in a separate folder.
Each folder includes a `code` subdirectory that reproduces the corresponding results presented in the paper.

### ⚙️ Environment Setup

The 3D structure-oriented curvelet transform is implemented based on the [Curvelop](https://github.com/curvelop/curvelop) library. It depends on:

- Python 3.8  
- CurveLab 2.1.3  
- FFTW 2.1.5  

An `environment.yml` file is included to help set up the conda environment with the required Python packages.  
> **Note:** `CurveLab 2.1.3` and `FFTW 2.1.5` must be installed manually by following the [Curvelop installation guide](https://github.com/curvelop/curvelop#installation).

You can create the environment with:

```bash
conda env create -f environment.yml
conda activate curvelet
