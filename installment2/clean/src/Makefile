#
# :author: PN
# :date: 2019-09-24
# :license: GPL 2.0 or greater
#
# ice-air/installment2/clean/src/Makefile
#
#

all: \
	output/ice-air-passengers.csv.gz \
	output/ice-air-missions.csv.gz

PHONY: all

output/ice-air-passengers.csv.gz: \
	src/clean-passengers.py \
	hand/clean.yaml \
	hand/bad_airports.csv \
	hand/airports_to_merge.csv\
	input/passenger-dtypes.yaml \
	input/status.csv \
	input/ARTS_Passenger_Data_FY11-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY12-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY13-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY14-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY15-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY16-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY17-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY18-redacted.csv.gz \
	input/ARTS_Passenger_Data_FY19_Year_To_Date-redacted.csv.gz
	python $< \
		--fy11=input/ARTS_Passenger_Data_FY11-redacted.csv.gz \
		--fy12=input/ARTS_Passenger_Data_FY12-redacted.csv.gz \
		--fy13=input/ARTS_Passenger_Data_FY13-redacted.csv.gz \
		--fy14=input/ARTS_Passenger_Data_FY14-redacted.csv.gz \
		--fy15=input/ARTS_Passenger_Data_FY15-redacted.csv.gz \
		--fy16=input/ARTS_Passenger_Data_FY16-redacted.csv.gz \
		--fy17=input/ARTS_Passenger_Data_FY17-redacted.csv.gz \
		--fy18=input/ARTS_Passenger_Data_FY18-redacted.csv.gz \
		--fy19=input/ARTS_Passenger_Data_FY19_Year_To_Date-redacted.csv.gz \
		--clean=hand/clean.yaml \
		--status=input/status.csv \
		--airports_to_merge=hand/airports_to_merge.csv \
		--bad_airports=hand/bad_airports.csv \
		--bad_statuses=output/bad_statuses.yaml \
		--airport_dict=output/airport_dict.yaml \
		--dtypes_in=input/passenger-dtypes.yaml \
		--dtypes_out=output/passenger-dtypes.yaml \
		--clean_stats=output/passenger-clean_stats.yaml \
		--output=$@

output/ice-air-missions.csv.gz: \
	src/clean-missions.py \
	hand/clean.yaml \
	hand/bad_airports.csv \
	hand/airports_to_merge.csv\
	input/mission-dtypes.yaml \
	input/status.csv \
	input/ARTS_Data_FY11-reviewed.csv.gz \
	input/ARTS_Data_FY12-reviewed.csv.gz \
	input/ARTS_Data_FY13-reviewed.csv.gz \
	input/ARTS_Data_FY14-reviewed.csv.gz \
	input/ARTS_Data_FY15-reviewed.csv.gz \
	input/ARTS_Data_FY16-reviewed.csv.gz \
	input/ARTS_Data_FY17-reviewed.csv.gz \
	input/ARTS_Data_FY18-reviewed.csv.gz \
	input/ARTS_Data_FY19_Year_To_Date-reviewed.csv.gz
	python $< \
		--fy11=input/ARTS_Data_FY11-reviewed.csv.gz \
		--fy12=input/ARTS_Data_FY12-reviewed.csv.gz \
		--fy13=input/ARTS_Data_FY13-reviewed.csv.gz \
		--fy14=input/ARTS_Data_FY14-reviewed.csv.gz \
		--fy15=input/ARTS_Data_FY15-reviewed.csv.gz \
		--fy16=input/ARTS_Data_FY16-reviewed.csv.gz \
		--fy17=input/ARTS_Data_FY17-reviewed.csv.gz \
		--fy18=input/ARTS_Data_FY18-reviewed.csv.gz \
		--fy19=input/ARTS_Data_FY19_Year_To_Date-reviewed.csv.gz \
		--clean=hand/clean.yaml \
		--status=input/status.csv \
		--airports_to_merge=hand/airports_to_merge.csv \
		--bad_airports=hand/bad_airports.csv \
		--bad_statuses=output/bad_statuses.yaml \
		--airport_dict=output/airport_dict.yaml \
		--dtypes_in=input/mission-dtypes.yaml \
		--dtypes_out=output/mission-dtypes.yaml \
		--clean_stats=output/mission-clean_stats.yaml \
		--output=$@

# End.