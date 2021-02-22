# Introduction

This repository contains all the code and behavioral data necessary to completely replicate the figures found in Guest and Oxenham (2021). The codebase is a mixture of Python and R, with Python mostly being used to conduct neural simulations and R mostly being used to analyze behavioral data and create figures. The code relies on a number of external libraries, including more common ones such as `numpy` and `scipy`, as well as auditory-specific libraries such as `cochlea`, `gammatone`, and our modeling toolbox, `apcmodels`.

# File structure

The basic file structure is shown in the file hierarchy below. Essential code required to generate the subfigures in each paper figure is stored in its own folder. A variety of code that was integral to the neural simulations featured in the paper but does not correspond to one particular figure is located in the `nofigure` subfolder. Finally, a few other scripts and utilities are stored in top-level `.R` and `.py` files. 

```
.  
├── data                     # Behavioral data 
├── figure1                  # Code for Figure 1
├── ...  
├── figure4                  # Code for Figure 5
│   ├── figure4a.py          # Python code to generate run simulations featured in Figure 4
│   ├── figure4a.R           # R code to plot results from figure4.py
│   ├── *.csv                # Results generated by figure4.py
│   └── ...      
├── figure5                  # Code for Figure 5, similar in structure to /figure4
├── figure6                  # Code for Figure 6
├── nofigure                 # Code that is needed but is not directly featured in a manuscript figure
│   ├── absolute_thresholds  # Scripts to estimate absolute thresholds at a range of CFs
│   ├── tuning_curves        # Scripts to estimate tuning curves and Q10 values at a range of CFs
│   └── vector_strength      # Scripts to estimate vector strength at a range of CFs
├── plots                    # .png files, exact matches for figures in manuscript
├── supplemental_figure_1    # Scripts to generate the supplemental figure
├── config.py                # Short script to provide constants shared across all Python files
├── config.R                 # Short script to provide constants shared across all R files
├── functions.py             # Miscellaneous functions used by a few Python scripts
├── LICENSE                  # License file for this repository
└── README.md                # This README file
```

## Data files

Two behavioral data files are included in the repository in the folder `data`. Each is a `.csv` file where each row corresponds to a single run in the adaptive procedure. These data are not raw data, but contain only a minor amount of preprocessing. First, data from Experiment 1 were screened to exclude data from participants whose average thresholds in the task did not exceed our screening task thresholds (6% and 12% in the low- and high-frequency conditions, respectively). Second, data from runs where the procedure did not converge and was terminated early were excluded. The columns in each datafile are documented below. 

- `exp1.csv`
  - `F0`: F0 of run in Hz
  - `masker`: Masker condition of run, either ISO or GEOM
  - `threshold`: Threshold calculated from run, in 10*log10(%)
  - `sd`: Standard deviation of threshold from run
  - `subj`: Anonymized participant identifier
  - `experiment`: Sub-experiment threshold was collected in (either Experiment 1a or Experiment 1b)
- `exp2.csv`
  - `F0`: F0 of run in Hz
  - `interval`: Interval size of run, either 1.5 times or 2.5 times the listener's average F0DL in Experiment 1
  - `threshold`: Threshold calculated from run, in 10*log10(%)
  - `sd`: Standard deviation of threshold from run
  - `subj`: Anonymized participant identifier. Same identifiers were used in Experiment 1 and Experiment 2, so some participants can be identified across experiments. 

# Instructions

To replicate the paper figures, you will need Python and R. Instructions for how to install each and configure your environments are provided below. Once you have successfully installed both R and Python and the requisite packages for each, proceed to `Figures` below and read about the code for each figure there. Output figure images will be saved in the `plots` folder as `.png` files.

## Python

A Python 3 interpreter is required to run the simulation code (Figure 4, Figure 5, Figure 6, supplemental figures). We recommend using `pyenv`, `conda`, or another similar tool to install Python 3.6, as well as the packages (with version numbers) listed below:

- `numpy` -
- `scipy` -
- `pathos` -
- `cochlea` -
- `gammatone` -
- `yo`

Once your Python interpreter is configured successfully, set your working directory to your local copy of this repository. Additionally, edit the `config.py` file to indicate the location of the files. Then, run `.py` files as needed. Note that all the outputs of `.py` files are already pre-included in the repository, so no Python code needs to be run to reproduce the manuscript figures. 

## R

R is required to generate all the behavioral and modeling figures. The paper figures were generated using R 4.0.3, although in theory any fairly recent version of R should suffice. Below a list of required packages (and the versions used to generate the figures) is provided:

- `merTools` - 0.5.2
- `dplyr` - 1.0.2
- `effects` - 4.2-0
- `ggplot2` - 3.3.2
- `lme4` - 1.1-25
- `phia` - 0.2-1
- `tidyr` - 1.1.2

Once your R  is configured successfully, set your working directory to your local copy of this repository. Now, you can run any of the plotting scripts (e.g., `figure1.R`) Some of these scripts depend on the output of the Python scripts. However, every required output has been pre-generated and included in this repository. These outputs are precisely those used to generate the figures in the manuscript. As a result, all the R scripts should correctly generate the paper figures even if you don't have a Python interpreter installed, or you have not yet run the Python scripts.

# Figures

## Figure 1

## Figure 2

## Figure 3

## Figure 4

Figure 4 features simulated frequency difference limens (FDLs) derived using ideal observer analysis for three auditory nerve model. Each subfigure has a corresponding `.py` script (to generate the neural simulations) and a `.R` script (to plot the figure). The `.py` files can take a considerable amount of time and RAM to run, particularly for the sections simulating thresholds for the Verhulst et al. (2018) auditory nerve model.

## Figure 5

Figure 5 features simulated F0 difference limens (FDLs) derived using ideal observer analysis for three auditory nerve model. Each subfigure has a corresponding `.py` script (to generate the neural simulations) and a `.R` script (to plot the figure). The `.py` files can take a considerable amount of time and RAM to run, particularly for the sections simulating thresholds for the Verhulst et al. (2018) auditory nerve model.

## Figure 6

## Supplemental Figure 1

The supplemental figure features a range of simulation results including vector strength and filter tuning plots for all of the tested auditory nerve models and model responses for the Zilany et al. (2014) auditory nerve model for various types of complex tone stimuli. Each subfigure has a `.py` file to generate it. The first two subfigures rely on simulation results from the `nofigure/vector_strength_curves` and `nofigure/tuning_curves`, respectively. 