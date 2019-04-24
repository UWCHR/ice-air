# ice-air

A project analyzing data from Immigration and Customs Enforcement's Alien Repatriation and Transfer System (ARTS) for the report [Hidden in Plain Sight: ICE Air and the Machinery of Mass Deportation](https://jsis.washington.edu/humanrights/2019/04/23/ice-air/) by the [University of Washington Center for Human Rights](https://jsis.washington.edu/humanrights/).

## Report contents

- [Hidden in Plain Sight: ICE Air and the Machinery of Mass Deportation](https://jsis.washington.edu/humanrights/2019/04/23/ice-air/)
- [Hidden in Plain Sight: King County Collaboration with ICE Air Deportation Flights at Boeing Field](https://jsis.washington.edu/humanrights/2019/04/23/ice-air-king-county/)
- [Hidden in Plain Sight: ICE Air Data Appendix](https://uwchr.github.io/ice-air/)

# Repository description

This repo uses [Git LFS](https://git-lfs.github.com/).

This project uses "Principled Data Processing" techniques and tools developed by [@HRDAG](https://github.com/HRDAG); see for example ["The Task Is A Quantum of Workflow."](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/)

Tasks in this project are designed to be executed using the recursive make tool [makr](https://github.com/hrdag/makr).

## Task structure

- `import/` - Convenience task for importing ICE Air ARTS dataset. Input files in `import/input/` have been previously renamed to remove spaces in filenames, converted to CSV with pipe separator (`|`), and compressed using Gzip. Input files are symlinked to `import/output/` and then to `input/` of downstream tasks for modification and analysis. Original Excel files as released by ICE can be found on [UWCHR's Google Drive](https://drive.google.com/open?id=1GVeLTfCm846YkZKWPlK0HF5eRxxYqPsF). These raw files are excluded from the repository due to their size.
- `optimize/` - Determines optimal Python/Pandas data types for each field in the original dataset and outputs this as a YAML dictionary used and modified in downstream tasks.
- `clean/` - Standardizes selected field values in `clean/hand/clean.yaml`; fixes missing and bad airport data; removes duplicate passenger records. Outputs  full ICE Air ARTS dataset, after cleaning, as a Gzipped CSV file at [`clean/output/ice-air.csv.gz`](https://github.com/UWCHR/ice-air/blob/master/clean/output/ice-air.csv.gz)
- `analyze/` - Contains various exploratory Jupyter notebooks and R Markdown. These notebooks and their outputs are exploratory and do not necessarily reflect the findings of UWCHR's report.
  - `analyze/output/` contains various versions of figures and data subsets; currently none of these are used in any downstream tasks.
- `write/` - Writes out reports to HTML using [Pweave](http://mpastell.com/pweave/). All analysis, figure generation, etc. takes place in `write/src/`.
- `share/` - Contains various hand-written files and resources shared by multiple other tasks.
- `docs/` - Contains HTML documentation published at https://uwchr.github.io/ice-air/

## To-do

- [ ] Clean up and annotate analyis notebooks.