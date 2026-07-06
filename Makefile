.PHONY: inspect test check install-analysis

inspect:
	python3 tools/ecorce_deck.py models/ecorce/lateral-gan-hemt

test:
	python3 -m unittest discover -s tests -v

check: inspect test

install-analysis:
	python3 -m pip install -r requirements-analysis.txt
