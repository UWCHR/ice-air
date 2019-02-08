#
# :author: PN
# :date: 2019-01-17
# :license: GPL 2.0 or greater
#
# ice-air/clean/src/Makefile
#
#

all: \
	output/ice-air.csv.gz
	
PHONY: all

output/ice-air.csv.gz: \
	src/clean.py \
	hand/clean.yaml \
	hand/missing_airports.csv \
	input/dtypes.yaml \
	input/ARTS_Passenger_Data_FY11.csv.gz \
	input/ARTS_Passenger_Data_FY12.csv.gz \
	input/ARTS_Passenger_Data_FY13.csv.gz \
	input/ARTS_Passenger_Data_FY14.csv.gz \
	input/ARTS_Passenger_Data_FY15.csv.gz \
	input/ARTS_Passenger_Data_FY16.csv.gz \
	input/ARTS_Passenger_Data_FY17.csv.gz \
	input/ARTS_Passenger_Data_FY18.csv.gz \
	input/ARTS_Passenger_Data_FY19.csv.gz
	python $< \
		--fy11=input/ARTS_Passenger_Data_FY11.csv.gz \
		--fy12=input/ARTS_Passenger_Data_FY12.csv.gz \
		--fy13=input/ARTS_Passenger_Data_FY13.csv.gz \
		--fy14=input/ARTS_Passenger_Data_FY14.csv.gz \
		--fy15=input/ARTS_Passenger_Data_FY15.csv.gz \
		--fy16=input/ARTS_Passenger_Data_FY16.csv.gz \
		--fy17=input/ARTS_Passenger_Data_FY17.csv.gz \
		--fy18=input/ARTS_Passenger_Data_FY18.csv.gz \
		--fy19=input/ARTS_Passenger_Data_FY19.csv.gz \
		--clean=hand/clean.yaml \
		--missing_airports=hand/missing_airports.csv \
		--airport_dict=output/airport_dict.yaml \
		--dtypes_in=input/dtypes.yaml \
		--dtypes_out=output/dtypes.yaml \
		--output=$@

# End.