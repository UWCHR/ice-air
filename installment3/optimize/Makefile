#
# :author: PN
# :date: 2020-12-11
# :license: GPL 2.0 or greater
#
# ice-air/installment3/optimize/src/Makefile
#
#

all: \
	output/passenger-dtypes.yaml \
	output/mission-dtypes.yaml
	
PHONY: all

output/passenger-dtypes.yaml: \
	src/optimize.py \
	input/ARTS_Passenger-redacted.csv.gz
	python $< \
		--input=input/ARTS_Passenger-redacted.csv.gz \
		--output=$@

output/mission-dtypes.yaml: \
	src/optimize.py \
	input/ARTS_Missions-redacted.csv.gz
	python $< \
		--input=input/ARTS_Missions-redacted.csv.gz \
		--output=$@

# End.