# Ecorce setup and model testing

## Important availability note

Ecorce itself is **not included** in this repository. The supplied internship
material describes Ecorce as an experimental TCAD/finite-volume semiconductor
simulator and identifies a legacy download address, `http://www.ecorce.eu/`.
It also states that some trapping/detrapping functionality was distributed
under a private licence. The legacy public site was not reachable when this
repository was prepared in July 2026.

Obtain a legitimate, compatible installer and any required licence directly
from the software author, the relevant laboratory, or your institution. Do
not copy an institutional binary or private plugin into a public repository.

## Tested deck compatibility

The retained files declare Ecorce format version **2.22**. A different Ecorce
release may migrate the files, reject old keywords, or change material-model
defaults. Keep a copy of the original deck before allowing any migration.

## System packages for the repository tools

These packages do **not** install Ecorce. They support Git, Python validation,
optional plotting and archive handling.

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y git unzip python3 python3-venv python3-pip
```

### Fedora

```bash
sudo dnf install -y git unzip python3 python3-pip
```

### macOS

```bash
xcode-select --install
brew install git python
```

### Windows

Install Git and Python 3.10+ from their official installers, then use
PowerShell or Git Bash.

## Static validation without Ecorce

From the repository root:

```bash
python3 tools/ecorce_deck.py models/ecorce/lateral-gan-hemt
python3 -m unittest discover -s tests -v
```

The inspector verifies:

- deck versions;
- device dimensionality;
- contact names;
- materials;
- enabled physical models;
- geometry entity counts;
- stimulus/contact consistency;
- gate-ramp and solver metadata.

## Running the retained model in Ecorce

Exact menu names depend on the installed release. The historic workflow was:

1. Start Ecorce in a Linux graphical session.
2. Open `models/ecorce/lateral-gan-hemt/device.dev`.
3. Load or select `transfer_gate_0_to_5V.sti` as the stimulus deck.
4. Confirm the material files `AlGaN`, `GaN`, and `Si` exist in the installation.
5. Confirm terminal mapping: `Source`, `Gate`, `Drain`, `Substrate`.
6. Generate/refine the mesh and inspect it before solving.
7. Execute the stationary sweep.
8. Read the solver log before interpreting a curve.

Expected stimulus configuration:

| Quantity | Setting |
|---|---:|
| Temperature | 300 K |
| Source | 0 V |
| Drain | 1 V |
| Substrate | 0 V |
| Gate | 0 V to 5 V |
| Gate step | 0.1 V |
| Maximum mesh nodes | 100,000 |
| Minimum edge length | 0.01 µm |
| Maximum Newton iterations | 40 |

## Minimum checks before accepting a result

- Verify that all contact currents use a documented sign convention.
- Check current conservation at every bias point.
- Repeat with at least three mesh densities.
- Confirm that the result is stable to smaller voltage steps.
- Export solver residuals and iteration counts.
- State the implicit out-of-plane depth used to convert A/length into A.
- Do not infer avalanche breakdown while impact ionisation is disabled.
- Do not call a near-floor current a threshold crossing.

## Exporting and plotting data

Export a CSV with explicit, unit-bearing column names. Example:

```text
gate_voltage_V,drain_current_A_per_cm
0.0,1.2e-14
0.1,1.3e-14
```

Install optional plotting packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-analysis.txt
```

Plot two columns:

```bash
python3 tools/plot_iv.py data/export.csv \
  --x gate_voltage_V \
  --y drain_current_A_per_cm \
  --xlabel 'Gate voltage (V)' \
  --ylabel 'Drain current (A/cm)' \
  --output results/transfer_curve.png
```
