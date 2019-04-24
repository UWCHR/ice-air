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
- `analyze/` - Contains exploratory Jupyter notebooks and R Markdown.
- - `analyze/output/` contains various versions of figures and data subsets; currently none of these are used in any downstream tasks.
- `write/` - Writes out reports to HTML using [Pweave](http://mpastell.com/pweave/). All analysis, figure generation, etc. takes place in `write/src/`.
- `share/` - Contains various hand-written files and resources shared by multiple other tasks.
- `docs/` - Contains HTML documentation published at https://uwchr.github.io/ice-air/

# ARTS PASSENGER DATA DICTIONARY

The following data dictionary was released by ICE 

Field|Description|(UWCHR notes)
-----|-----------|-------------
Status|Criminal Status|(actually relates to status of deportation proceedings, partially cleaned)
Sex|Sex|(cleaned)
Convictions|Convictions|(not consistent with Criminality in early years of dataset, very messy)
GangMember|Gang Member|
ClassLvl|Class Level|
Age|Age|(cleaned)
MissionDate|Mission Date|
MissionNumber|Mission Number (i.e., Flight Number)|
PULOC|Pick up location|
DropLoc|Drop off location|(cleaned)
StrikeFromList|Was Alien struck from mission |
ReasonStruck|Reason Struck|
R-T|Removal or Transfer|(cleaned)
Code|Criminality Code|
CountryOfCitizenship|Country of Citizenship|(partial clean)
Juvenile|Is Alien a Juvenile|(cleaned)
MissionWeek|Mission Week|
MissionQuarter|Mission Quarter|
MissionYear|Mission Year|
MissionMonth|Mission Month|
Criminality|Criminality|(cleaned, missing many values in early years)
FamilyUnitFlag|Family Unit Flag|(this field is never used)
UnaccompaniedFlag|Unaccompanied Flag|(this field is never used)
AlienMasterID|Unique value assigned by ARTS for Alien|
MissionID|Unique value assigned by ARTS for mission|
air_AirportID|Airport ID (numerical)|
air_AirportName|Airport Name|(cleaned, missing values filled)
air_City|Airport City|(cleaned)
st_StateID|State ID (Numerical)|
st_StateAbbr|State Abbreviation|(cleaned)
AOR_AORID|Area of Responsibility (Numerical)|
AOR_AOR|Area of Responsibility (Abbreviation)|
AOR_AORName|Area of Responsibility|
air_Country|Airport Country|(missing values filled)
air2_AirportID|Airport ID (numerical)|
air2_AirportName|Airport Name|(cleaned, missing values filled)
air2_City|Airport City |(cleaned)
st2_StateID|State ID (Numerical)|
st2_StateAbbr|State Abbreviation|(cleaned)
aor2_AORID|Area of Responsibility (Numerical)|
aor2_AOR|Area of Responsibility (Abbreviation)|
aor2_AORName|Area of Responsibility|
air2_Country|Airport Country|(missing values filled)