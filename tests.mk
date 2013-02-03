
all:
	-PYTHONPATH=source /usr/local/bin/nosetests --with-coverage \
		--cover-package=mach8 \
		--cover-html --cover-html-dir=coverage --with-xunit \
		--xunit-file=nosetests.xml