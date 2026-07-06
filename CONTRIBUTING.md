# Contributing

Contributions are welcome when they improve reproducibility or scientific
clarity. Please do not submit proprietary Ecorce binaries, private plugins,
confidential material libraries or data you are not authorised to publish.

A model-related pull request should include:

1. provenance and licence of every deck/material file;
2. Ecorce version and operating system;
3. exact terminal map and units;
4. mesh and solver diagnostics;
5. raw machine-readable data;
6. a script or documented rule for each extracted metric;
7. a statement of what the result supports and what it does not prove.

Run before submitting:

```bash
python3 -m unittest discover -s tests -v
python3 tools/ecorce_deck.py models/ecorce/lateral-gan-hemt
```
