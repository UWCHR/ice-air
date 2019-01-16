# ice-air

A project to analyze data from Immigration and Customs Enforcement's Alien Repatriation and Transfer System (ARTS) obtained via FOIA.

Raw Excel files used in this project can be found on [UWCHR's Google Drive](https://drive.google.com/drive/folders/1DFhlKSI1u9yrPqPmLKW0o2IKUsUhSEIl?usp=sharing).

Input files in `import/input/` have been renamed to remove spaces, converted to CSV, and Gzipped. Input files are symlinked to `import/output/` and then to `input/` of downstream tasks for modification and analysis.

This repo uses [Git LFS](https://git-lfs.github.com/).

This project uses "Principled Data Processing" techniques and tools developed by [@HRDAG](https://github.com/HRDAG); see for example ["The Task Is A Quantum of Workflow."](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/)