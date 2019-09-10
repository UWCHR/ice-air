#
# Authors:     PN
# Maintainers: PN
# Copyright:   2019, UWCHR, GPL v2 or later
# ============================================
# ice-air/write/src/Makefile

.PHONY: all clean

all: \
	output/ice-air-global.html \
	output/ice-air-king-county.html \
	output/ice-air-data-appendix.html \
	output/UWCHR-ICEAir-Chart-National.jpg \
	output/UWCHR-ICEAir-Chart-KingCo.jpg \
	output/RPNInvoices.png

clean:
	rm -r output/*

output/ice-air-global.html: \
		src/ice-air-global.pmd \
		input/ice-air.csv.gz \
		input/clean_stats.yaml\
		input/dtypes.yaml \
		input/status.csv \
		input/UWCHR-ICEAir-Chart-National.jpg
	pweave src/ice-air-global.pmd -f md2html -o output/ice-air-global.html

output/ice-air-king-county.html: \
		src/ice-air-king-county.pmd \
		input/ice-air.csv.gz \
		input/clean_stats.yaml\
		input/dtypes.yaml \
		input/status.csv \
		input/UWCHR-ICEAir-Chart-KingCo.jpg \
		input/RPNInvoices.png
	pweave src/ice-air-king-county.pmd -f md2html -o output/ice-air-king-county.html

output/ice-air-data-appendix.html: \
		src/ice-air-data-appendix.pmd \
		input/ice-air.csv.gz \
		input/clean_stats.yaml\
		input/dtypes.yaml \
		input/status.csv \
		hand/arts_cols.yaml
	pweave src/ice-air-data-appendix.pmd -f md2html -o output/ice-air-data-appendix.html

output/UWCHR-ICEAir-Chart-National.jpg: \
		input/UWCHR-ICEAir-Chart-National.jpg
	cd output && ln -sf ../input/UWCHR-ICEAir-Chart-National.jpg .

output/UWCHR-ICEAir-Chart-KingCo.jpg: \
		input/UWCHR-ICEAir-Chart-KingCo.jpg
	cd output && ln -sf ../input/UWCHR-ICEAir-Chart-KingCo.jpg .

output/RPNInvoices.png: \
		input/RPNInvoices.png
	cd output && ln -sf ../input/RPNInvoices.png .

# done.
