# Lateral AlGaN/GaN HEMT benchmark deck

This is the only Ecorce device/stimulus pair recovered from the internship
archive that directly matches a benchmark discussed in the final report.

## Files

- `device.dev`: 2-D AlGaN/GaN/Si structure, Ecorce format 2.22.
- `transfer_gate_0_to_5V.sti`: stationary gate transfer sweep.
- `model-manifest.json`: metadata extracted by the repository parser.

## Device summary

- Contacts: Source, Gate, Drain, Substrate.
- Materials: AlGaN, GaN and Si.
- Physics: Poisson, electron/hole transport and trapping are enabled.
- Impact ionisation and band-to-band tunnelling are disabled.
- Nominal geometry extent recovered from node coordinates: 1.0 µm × 0.45 µm.

## Scientific scope

This deck is a **qualitative lateral GaN benchmark**, not the mirrored vertical
VertiGaN deck. It can test whether an Ecorce installation can load the archived
material definitions and execute the original gate sweep. It cannot reproduce
the report's VertiGaN output, off-state or resistance plots.
