#
# Authors:     PN
# Maintainers: PN
# Copyright:   2020, UWCHR, GPL v2 or later
# ============================================
# ice-air/installment2/write/src/Makefile

.PHONY: all clean

all: \
	output/wal-kbro-memo.pdf

clean:
	rm -rf output/*

output/wal-kbro-memo.pdf: \
		src/wal-kbro-memo.pmd \
		input/airport_dict.yaml \
		input/ice-air-missions.csv.gz \
		input/mission-dtypes.yaml \
		input/RadarBoxWAL20200116-20200417.csv.gz

	cd src && pweave wal-kbro-memo.pmd -f pandoc2latex wal-kbro-memo.tex
	cd src && pdflatex wal-kbro-memo.tex
	cd src && pdflatex wal-kbro-memo.tex
	mv src/figures/ output/.
	mv src/wal-kbro-memo.tex output/.
	mv src/wal-kbro-memo.out output/.
	mv src/wal-kbro-memo.aux output/.
	mv src/wal-kbro-memo.log output/.
	mv src/wal-kbro-memo.pdf output/.


# done.
