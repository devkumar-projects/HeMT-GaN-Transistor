# Scientific and innovation roadmap

The current result set is exploratory. A credible next phase should progress
through explicit verification gates instead of optimising isolated curves.

## 1. Reconstruct one authoritative simulation deck

Store geometry, materials, contacts, interface charges, traps, mobility,
recombination, impact ionisation, thermal properties, terminal definitions,
mesh rules and every bias sequence under one immutable revision.

## 2. Numerical credibility

- current-conservation error at every bias point;
- three-level mesh convergence;
- continuation-state consistency between transfer, output and off-state sweeps;
- branch-current symmetry for both mirrored cells;
- automated unit and depth-normalisation audit.

## 3. Physics hierarchy

1. equilibrium electrostatics;
2. isothermal low-field drift-diffusion;
3. high-field mobility and velocity saturation;
4. polarisation and Schrödinger-Poisson or quantum correction;
5. interface/bulk traps and incomplete ionisation;
6. impact ionisation and field-dependent leakage;
7. electrothermal coupling;
8. transient switching with an external circuit.

## 4. Design of experiments

Explore drift thickness/doping, p-GaN thickness/activation, channel spacing,
gate length, dielectric thickness, interface charge and contact resistivity.
Use a space-filling or Latin-hypercube design, then local optimisation and
uncertainty propagation. Report Pareto fronts rather than a single optimum.

## 5. Potential innovations to investigate

- differential or independently sensed operation of the mirrored cells;
- fault-tolerant or redundant six-terminal configurations;
- thermal balancing between the two current paths;
- field plates and edge termination around gate/dielectric corners;
- alternative central isolation shapes and materials;
- segmented p-GaN control regions for threshold/resistance trade-offs;
- embedded branch-current sensing for current sharing;
- reduced-order surrogate models for rapid multi-objective optimisation.

## 6. Experimental path

Begin with test structures: TLM contacts, MIS capacitors, p-GaN-gated channel
coupons and vertical diode drift stacks. Calibrate each element before a full
six-terminal demonstrator. Required measurements include DC and pulsed I-V,
dynamic on-resistance, C-V, gate charge, temperature dependence, controlled
breakdown, thermal mapping and post-failure physical analysis.

## 7. Decision gates

- **Gate A - numerical consistency:** one deck, conserved current, converged mesh.
- **Gate B - physical completeness:** calibrated traps, contacts, avalanche and heat.
- **Gate C - process plausibility:** reviewed fabrication flow and test structures.
- **Gate D - experimental proof:** positive threshold, repeatable low resistance and controlled breakdown.
- **Gate E - system relevance:** switching loss and reliability beat an equal-class baseline.
