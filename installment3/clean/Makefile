#
# :author: PN
# :date: 2020-12-11
# :license: GPL 2.0 or greater
#
# ice-air/installment3/clean/src/Makefile
#
#

all: \
	output/ice-air-passengers.csv.gz \
	output/ice-air-missions.csv.gz

passengers: \
	output/ice-air-passengers.csv.gz

missions: \
	output/ice-air-missions.csv.gz

clean: \
	rm output/*

PHONY: all

output/ice-air-passengers.csv.gz: \
	src/clean-passengers.py \
	hand/clean.yaml \
	hand/bad_airports.csv \
	hand/airports_to_merge.csv \
	frozen/airport_dict.yaml \
	input/passenger-dtypes.yaml \
	input/status.csv \
	input/ARTS_Passenger-redacted.csv.gz
	python $< \
		--input=input/ARTS_Passenger-redacted.csv.gz \
		--clean=hand/clean.yaml \
		--status=input/status.csv \
		--airports_to_merge=hand/airports_to_merge.csv \
		--bad_airports=hand/bad_airports.csv \
		--bad_statuses=output/bad_statuses.yaml \
		--airport_dict_updated=frozen/airport_dict.yaml \
		--airport_dict=output/airport_dict.yaml \
		--dtypes_in=input/passenger-dtypes.yaml \
		--dtypes_out=output/passenger-dtypes.yaml \
		--clean_stats=output/passenger-clean_stats.yaml \
		--output=$@

output/ice-air-missions.csv.gz: \
	src/clean-missions.py \
	hand/clean.yaml \
	hand/bad_airports.csv \
	hand/airports_to_merge.csv \
	frozen/mission_airports.csv.gz \
	input/mission-dtypes.yaml \
	input/status.csv \
	input/ARTS_Missions-redacted.csv.gz
	python $< \
		--input=input/ARTS_Missions-redacted.csv.gz \
		--clean=hand/clean.yaml \
		--status=input/status.csv \
		--mission_airports=frozen/mission_airports.csv.gz \
		--airports_to_merge=hand/airports_to_merge.csv \
		--bad_airports=hand/bad_airports.csv \
		--bad_statuses=output/bad_statuses.yaml \
		--airport_dict=output/airport_dict.yaml \
		--dtypes_in=input/mission-dtypes.yaml \
		--dtypes_out=output/mission-dtypes.yaml \
		--clean_stats=output/mission-clean_stats.yaml \
		--output=$@

# End.