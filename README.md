# ice-air

A project to analyze data from Immigration and Customs Enforcement's Alien Repatriation and Transfer System (ARTS) obtained via FOIA.

Raw Excel files used in this project can be found on [UWCHR's Google Drive](https://drive.google.com/drive/folders/1DFhlKSI1u9yrPqPmLKW0o2IKUsUhSEIl?usp=sharing).

Input files in `import/input/` have been renamed to remove spaces, converted to CSV, and Gzipped. Input files are symlinked to `import/output/` and then to `input/` of downstream tasks for modification and analysis.

This repo uses [Git LFS](https://git-lfs.github.com/).

This project uses "Principled Data Processing" techniques and tools developed by [@HRDAG](https://github.com/HRDAG); see for example ["The Task Is A Quantum of Workflow."](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/)

Tasks in this project are designed to be executed using the recursive make tool [makr](https://github.com/hrdag/makr).

# ARTS PASSENGER DATA DICTIONARY

Field|Description
-----|-----------
Status|Criminal Status
Sex|Sex
Convictions|Convictions
GangMember|Gang Member
ClassLvl|Class Level
Age|Age
MissionDate|Mission Date
MissionNumber|Mission Number (i.e., Flight Number)
PULOC|Pick up location
DropLoc|Drop off location
StrikeFromList|Was Alien struck from mission 
ReasonStruck|Reason Struck
R-T|Removal or Transfer
Code|Criminality Code
CountryOfCitizenship|Country of Citizenship
Juvenile|Is Alien a Juvenile
MissionWeek|Mission Week
MissionQuarter|Mission Quarter
MissionYear|Mission Year
MissionMonth|Mission Month
Criminality|Criminality
FamilyUnitFlag|Family Unit Flag
UnaccompaniedFlag|Unaccompanied Flag
AlienMasterID|Unique value assigned by ARTS for Alien
MissionID|Unique value assigned by ARTS for mission
air_AirportID|Airport ID (numerical)
air_AirportName|Airport Name
air_City|Airport City
st_StateID|State ID (Numerical)
st_StateAbbr|State Abbreviation
AOR_AORID|Area of Responsibility (Numerical)
AOR_AOR|Area of Responsibility (Abbreviation)
AOR_AORName|Area of Responsibility
air_Country|Airport Country
air2_AirportID|Airport ID (numerical)
air2_AirportName|Airport Name
air2_City|Airport City 
st2_StateID|State ID (Numerical)
st2_StateAbbr|State Abbreviation
aor2_AORID|Area of Responsibility (Numerical)
aor2_AOR|Area of Responsibility (Abbreviation)
aor2_AORName|Area of Responsibility
air2_Country|Airport Country