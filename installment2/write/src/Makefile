#
# Authors:     PN
# Maintainers: PN
# Copyright:   2020, UWCHR, GPL v2 or later
# ============================================
# ice-air/installment2/write/src/Makefile

.PHONY: all clean

all: \
	output/memo.pdf

clean:
	rm -r output/*

output/memo.pdf: \
		src/memo.pmd \
		input/airport_dict.yaml \
		input/ice-air-missions.csv.gz \
		input/mission-dtypes.yaml \
		input/RadarBoxWAL20200116-20200417.csv.gz

	cd src && pweave memo.pmd -f pandoc2latex memo.tex
	cd src && pdflatex memo.tex
# 	pdflatex src/memo.tex
# 	mv memo.* ../output/.

# done.
