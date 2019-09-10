library(tidyverse)
library(data.table)
library(lubridate)

setwd('~/git/ice-air/analyze/src/')

path <- '../input/ice-air.csv.gz'
DT = fread(path, stringsAsFactors=TRUE)

DT$MissionDate <- ymd(DT$MissionDate)

q <- quarter(DT$MissionDate, with_year = TRUE, fiscal_start = 10)
fy <- stringr::str_sub(q, 1, 4)
DT$FY <- fy
rm(q, fy)

annual_passengers <- DT[,
                        .(number_of_passengers = length(unique(AlienMasterID))),
                        by = FY]
annual_removals <- DT[`R-T` == 'R',
                      .(number_of_removals = length(unique(AlienMasterID))),
                      by = FY]
annual_transfers <- DT[`R-T` == 'T',
                      .(number_of_transfers = length(unique(AlienMasterID))),
                      by = FY]
annual_removal_missions <- DT[DT$'R-T' == 'R',
                      .(number_of_removal_missions = length(unique(MissionID))),
                      by = FY]
annual_transfer_missions <- DT[DT$'R-T' == 'T',
                       .(number_of_transfer_missions = length(unique(MissionID))),
                       by = FY]

removal_nationality <- DT[DT$'R-T' == 'R',
                          .(number_of_removals = length(unique(AlienMasterID))),
                          by = CountryOfCitizenship]

removal_nat_by_FY <- DT[DT$'R-T' == 'R',
                        .(number_of_removals = length(unique(AlienMasterID))),
                        by = .(FY, CountryOfCitizenship)]

setorder(removal_nat_by_FY, FY, -number_of_removals)

top_5_table = data.frame()

for (year in unique(removal_nat_by_FY$FY)){
  top_5 <- removal_nat_by_FY[FY == year,
                                .SD[1:5]]
  others <- removal_nat_by_FY[FY == year,
                            .SD[-1:-5]]
  other_count = sum(others$number_of_removals)
  
  top_5_plus_other <- rbind(top_5, data.frame(FY=year,
                                              CountryOfCitizenship='ALL OTHERS',
                                              number_of_removals=other_count))
  top_5_table <- rbind(top_5_table, top_5_plus_other)
}

levels(top_5_table$CountryOfCitizenship) <- str_to_title(levels(top_5_table$CountryOfCitizenship))

g <- top_5_table[FY != '2019']  %>%
#  mutate(CountryOfCitizenship = fct_relevel(CountryOfCitizenship, "ALL OTHERS", "HAITI", "DOMINICAN REPUBLIC", "EL SALVADOR", "HONDURAS", "GUATEMALA", "MEXICO")) %>%
  ggplot(aes(FY, number_of_removals, fill = CountryOfCitizenship))
g <- g + geom_col(aes(fill = CountryOfCitizenship))
g <- g + labs(fill = "Country of Citizenship",
         x = "Fiscal Year",
         y = "Total Removals",
         title = "ICE Air Removals by Country of Citizenship",
         subtitle = "(Top 5 per year)",
         caption = "(UWCHR, based on data released by ICE)")
g