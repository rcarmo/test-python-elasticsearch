# local overrides
-include .env
PROFILES=$(wildcard *.pstats)
CALL_DIAGRAMS=$(PROFILES:.pstats=.png)

# Run tests
test:
	python -u test.py

deps:
	pip install -U -r requirements.txt

# Render pstats profiler files into nice PNGs (requires dot)
%.png: %.pstats
	python tools/gprof2dot.py -f pstats $< | dot -Tpng -o $@

profile: $(CALL_DIAGRAMS)

clean:
	rm -rf __pycache__
