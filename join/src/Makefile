#
# :date: 2019-01-16
# :author: PN
# :maintainer: PN
# :copyright: GPL v2 or later
#
# ice-air/join/src/Makefile
#

all: \
		output/iceair.csv.gz

.PHONY: all

output/iceair.csv.gz: \
		src/join.py \
		input/ARTS_Passenger_Data_FY11.csv.gz \
		input/ARTS_Passenger_Data_FY12.csv.gz \
		input/ARTS_Passenger_Data_FY13.csv.gz \
		input/ARTS_Passenger_Data_FY14.csv.gz \
		input/ARTS_Passenger_Data_FY15.csv.gz \
		input/ARTS_Passenger_Data_FY16.csv.gz \
		input/ARTS_Passenger_Data_FY17.csv.gz \
		input/ARTS_Passenger_Data_FY18.csv.gz \
		input/ARTS_Passenger_Data_FY19.csv.gz \
		hand/GlobalAirportDatabase.csv.gz
	python $< \
		--arts_fy11=input/ARTS_Passenger_Data_FY11.csv.gz \
		--arts_fy12=input/ARTS_Passenger_Data_FY12.csv.gz \
		--arts_fy13=input/ARTS_Passenger_Data_FY13.csv.gz \
		--arts_fy14=input/ARTS_Passenger_Data_FY14.csv.gz \
		--arts_fy15=input/ARTS_Passenger_Data_FY15.csv.gz \
		--arts_fy16=input/ARTS_Passenger_Data_FY16.csv.gz \
		--arts_fy17=input/ARTS_Passenger_Data_FY17.csv.gz \
		--arts_fy18=input/ARTS_Passenger_Data_FY18.csv.gz \
		--arts_fy19=input/ARTS_Passenger_Data_FY19.csv.gz \
		--airports=hand/GlobalAirportDatabase.csv.gz \
		--output=$@

# END.