#
# Authors:     PN
# Maintainers: PN
# Copyright:   2019, UWCHR, GPL v2 or later
# ============================================
# ice-air/share/hand/src/Makefile
#
# This is just a dummy Makefile to allow us to do recursive Make
# in other task directories.

.PHONY: all clean

all: \
	resources/dtypes.yaml

resources/dtypes.yaml:
	cd resources && ln -sf ../../optimize/output/dtypes.yaml .


# done.