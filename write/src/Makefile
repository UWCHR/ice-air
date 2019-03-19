#
# Authors:     PN
# Maintainers: PN
# Copyright:   2019, UWCHR, GPL v2 or later
# ============================================
# ice-air/write/src/Makefile

.PHONY: all clean

all: \
	output/ice-air-report.html \
	output/ice-air-report.md

clean:
	rm output/*

output/ice-air-report.md: \
		src/report.pmd \
		input/ice-air.csv.gz \
		input/dtypes.yaml
	pweave src/report.pmd -f markdown -o output/ice-air-report.md

output/ice-air-report.html: \
		src/report.pmd \
		input/ice-air.csv.gz \
		input/dtypes.yaml
	pweave src/report.pmd -f md2html -o output/ice-air-report.html


# done.
