# ice-air

A project to analyze data from Immigration and Customs Enforcement's Alien Repatriation and Transfer System (ARTS) obtained via FOIA.

Raw Excel files used in this project can be found on [UWCHR's Google Drive](https://drive.google.com/drive/folders/1DFhlKSI1u9yrPqPmLKW0o2IKUsUhSEIl?usp=sharing).

Input files in `import/input/` have been renamed to remove spaces in filenames, converted to CSV with pipe separator (`|`), and Gzipped. Input files are symlinked to `import/output/` and then to `input/` of downstream tasks for modification and analysis.

This repo uses [Git LFS](https://git-lfs.github.com/).

This project uses "Principled Data Processing" techniques and tools developed by [@HRDAG](https://github.com/HRDAG); see for example ["The Task Is A Quantum of Workflow."](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/)

Tasks in this project are designed to be executed using the recursive make tool [makr](https://github.com/hrdag/makr).

# TO-DO

- [ ] Clean analysis notebooks for publication
  - Move relevant code into report
- [ ] Write data appendix report

# ARTS PASSENGER DATA DICTIONARY

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