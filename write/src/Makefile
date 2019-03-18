#
# Authors:     PN
# Maintainers: PN
# Copyright:   2018, UWCHR, GPL v2 or later
# ============================================
# JailData/county/pierce/write/src/Makefile

.PHONY: all clean

R_OPTS=--no-save --no-restore --no-init-file --no-site-file

all: \
	output/pierce-report.tex \
	output/pierce-report.pdf

clean:
	rm output/*

output/pierce-report.tex: \
		src/pierce-report.Rnw \
		input/data.yaml \
		input/charge-vars.yaml \
		input/MeanJailTime.png \
		input/felony_misdemeanor.csv \
		input/regression_summary.csv \
		input/race_hold_table.csv
	Rscript $(ROPTS) -e "library(knitr); knit('$<')"
	mv pierce-report.tex output/

output/pierce-report.pdf: \
		output/pierce-report.tex
	pdflatex output/pierce-report.tex
	pdflatex output/pierce-report.tex # Compiling twice to get figure labels to display
	-mv pierce-report.pdf output/UWCHR-Pierce-County-ICE-Detainers.pdf
	-rm pierce-report.*


# done.
