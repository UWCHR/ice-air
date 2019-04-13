#
# Authors:     PN
# Maintainers: PN
# Copyright:   2019, UWCHR, GPL v2 or later
# ============================================
# ice-air/write/src/Makefile

.PHONY: all clean

all: \
	output/ice-air-data-appendix.html

clean:
	rm -r output/*

output/ice-air-data-appendix.html: \
		src/data-appendix.pmd \
		input/ice-air.csv.gz \
		input/clean_stats.yaml\
		input/dtypes.yaml \
		hand/arts_cols.yaml
	pweave src/data-appendix.pmd -f md2html -o output/ice-air-data-appendix.html


# done.
