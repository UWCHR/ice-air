# ice-air

A project to analyze data from Immigration and Customs Enforcement's Alien Repatriation and Transfer System (ARTS) obtained via FOIA.

Raw Excel files used in this project can be found on [UWCHR's Google Drive](https://drive.google.com/drive/folders/1DFhlKSI1u9yrPqPmLKW0o2IKUsUhSEIl?usp=sharing).

Input files in `import/input/` have been renamed to remove spaces, converted to CSV, and Gzipped. Input files are symlinked to `import/output/` and then to `input/` of downstream tasks for modification and analysis.

This repo uses [Git LFS](https://git-lfs.github.com/).

This project uses "Principled Data Processing" techniques and tools developed by [@HRDAG](https://github.com/HRDAG); see for example ["The Task Is A Quantum of Workflow."](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/)

Tasks in this project are designed to be executed using the recursive make tool [makr](https://github.com/hrdag/makr).

# TO-DO

`analyze/note/global.ipynb`
- [x] Expansion over time?
- [ ] Cost of most common travel segment? ($7785/hour/flight)

`analyze/note/nationality.ipynb`
- [x] How many deportation flights leave from the US to COUNTRY?
  - [x] Annually from the US in total
  - [x] Annually from King County 
  - [x] Over the course of the whole data set
  - [x] Monthly this past year (FY2018) out of King County
- [ ] What percentage of the passengers on these flights are convicted criminals? 
  - [ ] Over the course of the entire data set annually, particularly FY2018
  - MEXICO
    - [x] Destination locations for removal flights of Mexican nationals over time.
  - CAMBODIA
    - [x] Halt of repatriations in 2017?
    - [x] Average number of people per flight?
    - [x] Flights that land in Cambodia? Flights out of Phoenix?
  - Disproportionate rate of transfers for specific groups? Meaningful?

`analyze/note/juveniles.ipynb`
- [x] Has the number of minors being repatriated increased over time?
- [x] For what countries? 
- [ ] How many minors are typically on a flight? 
- [ ] Are there flights with only minors?
- [ ] Increase in deportations of minors to Guatemala?
  - [ ] Instances of more than 20 unaccompanied minors in Guatemala in one day


`analyze/note/airport.ipynb`
- [ ] How many juveniles left or flew into Seattle, if any?
- [x] How many passengers were included in dropoffs in Seattle?
- [x] What are the top nationalities of folks flying into/out of Seattle?
- [x] What nationalities have seen an uptick in passengers leaving Seattle?
- [x] What year saw the most passengers flying into/out of Seattle? Another question we could base research on is why might this be?
- [ ] Using ICE's cost estimate on their website, could we potentially find out the cost of a flight, say from Seattle to Phoenix?
  - [ ] Most common flight path from/to KBFI
- [ ] Airport ranks (what rank is KBFI for removals, transfers, etc.)
  - [ ] "KBFI is top airport for [transfers/removals] of [nationality]"
    - for CountryOfCitizenship get rank of KBFI

# ARTS PASSENGER DATA DICTIONARY

Field|Description|(UWCHR notes)
-----|-----------|-------------
Status|Criminal Status|(actually relates to grounds for deportation)
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
Criminality|Criminality|(cleaned, missing many values in 2010 but other years pretty good)
FamilyUnitFlag|Family Unit Flag|
UnaccompaniedFlag|Unaccompanied Flag|
AlienMasterID|Unique value assigned by ARTS for Alien|
MissionID|Unique value assigned by ARTS for mission|
air_AirportID|Airport ID (numerical)|
air_AirportName|Airport Name|(cleaned, missing values filled)
air_City|Airport City|
st_StateID|State ID (Numerical)|
st_StateAbbr|State Abbreviation|
AOR_AORID|Area of Responsibility (Numerical)|
AOR_AOR|Area of Responsibility (Abbreviation)|
AOR_AORName|Area of Responsibility|
air_Country|Airport Country|(missing values filled)
air2_AirportID|Airport ID (numerical)|
air2_AirportName|Airport Name|(cleaned, missing values filled)
air2_City|Airport City |
st2_StateID|State ID (Numerical)|
st2_StateAbbr|State Abbreviation|
aor2_AORID|Area of Responsibility (Numerical)|
aor2_AOR|Area of Responsibility (Abbreviation)|
aor2_AORName|Area of Responsibility|
air2_Country|Airport Country|(missing values filled)