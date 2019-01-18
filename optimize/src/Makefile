#
# :author: PN
# :date: 2019-01-17
# :license: GPL 2.0 or greater
#
# ice-air/optimize/src/Makefile
#
#

all: \
	output/dtypes.yaml
	
PHONY: all

output/dtypes.yaml: \
	src/optimize.py \
	input/ARTS_Passenger_Data_FY11.csv.gz
	python $< \
		--input=input/ARTS_Passenger_Data_FY11.csv.gz \
		--output=$@

# End.