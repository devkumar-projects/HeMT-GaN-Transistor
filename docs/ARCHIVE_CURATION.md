# Archive curation decisions

The source archive contained research material, third-party teaching files,
downloaded images, obsolete drafts, and two groups of Ecorce decks. This
repository intentionally keeps only the material that is directly useful to
understand or test the GaN study.

## Included

| Source item | Repository location | Reason |
|---|---|---|
| `academic.eco/device.dev` | `models/ecorce/lateral-gan-hemt/device.dev` | 2-D AlGaN/GaN device with Source, Gate, Drain and Substrate contacts; directly matches the lateral GaN benchmark discussed in the report. |
| `academic.eco/ramp.sti` | `models/ecorce/lateral-gan-hemt/transfer_gate_0_to_5V.sti` | Stationary gate sweep from 0 V to 5 V at 300 K and `VDS = 1 V`. |
| Final research report PDF | `report/` | Primary scientific documentation and evidence audit. |
| Selected figures from the report | `assets/figures/` | README illustrations for architecture, geometry and exported results. |

## Excluded

| Archived content | Why it was excluded |
|---|---|
| `academic.eco/10krad.sti`, `100krad.sti`, and post-irradiation ramps | Radiation-effect exercises inherited from an academic Ecorce example; unrelated to the VertiGaN research question. |
| `hemt/device.dev` and `hemt/Rampe.sti` | Despite the folder name, inspection shows a 1-D Si/SiO2 MOS-capacitor-style structure rather than a GaN HEMT. |
| Ecorce presentation, diode tutorial and another student's report | Third-party teaching material; useful for private study but not necessary or appropriate to redistribute in this project repository. |
| Old Word report drafts and notes | Superseded by the final PDF. |
| Gantt spreadsheet | Project-management artifact with no value for reproducing the device physics. |
| Downloaded web images and institutional logo | Not required and may carry separate copyright or trademark restrictions. |
| `__MACOSX` metadata | Operating-system clutter. |

## Missing scientific artifacts

The archive did **not** contain the complete Ecorce decks for:

- the mirrored six-terminal VertiGaN device;
- the lateral SiC MOSFET benchmark;
- the vertical SiC JFET benchmark;
- the output, off-state and resistance sweeps shown in the report;
- raw machine-readable result tables and solver logs.

The repository therefore makes no claim that every report figure can be
regenerated from the files currently available. Reconstructing a unified,
version-controlled VertiGaN deck is explicitly listed as future work.
