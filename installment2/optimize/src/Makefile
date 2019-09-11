#
# :author: PN
# :date: 2019-01-17
# :license: GPL 2.0 or greater
#
# ice-air/optimize/src/Makefile
#
#

all: \
	output/passenger-dtypes.yaml \
	output/mission-dtypes.yaml
	
PHONY: all

output/passenger-dtypes.yaml: \
	src/optimize.py \
	input/ARTS_Passenger_Data_FY11-redacted.csv.gz
	python $< \
		--input=input/ARTS_Passenger_Data_FY11-redacted.csv.gz \
		--output=$@

output/mission-dtypes.yaml: \
	src/optimize.py \
	input/ARTS_Data_FY11-reviewed.csv.gz
	python $< \
		--input=input/ARTS_Data_FY11-reviewed.csv.gz \
		--output=$@

# End.